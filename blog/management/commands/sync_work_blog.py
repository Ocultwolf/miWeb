"""
Agente de blog: lee el trabajo del dia (Claude Code, Codex y OpenClaw) y
publica una entrada por cada proyecto/trabajo distinto en el que hubo
actividad real.

Diseno de seguridad (no negociable, no lo relajes sin repasar con Pablo):
- Solo se manda al modelo un digesto acotado (titulos/previews truncados),
  nunca el contenido completo de una sesion.
- El prompt exige explicitamente que el post NUNCA incluya rutas de archivo,
  puertos, nombres de contenedores/servicios, URLs internas, tokens ni
  ningun detalle de infraestructura -- solo una narrativa de alto nivel de
  que se construyo y que se aprendio.
- Si un bucket es solo ruido (troubleshooting de sesion, "hola", "OK",
  pruebas triviales) el modelo debe devolver skip=true y no se publica nada.
- Dedupe por source_key: nunca se duplica un post para el mismo
  proyecto+dia aunque el comando se corra varias veces.

Uso:
    python manage.py sync_work_blog [--date YYYY-MM-DD] [--dry-run]
"""
from __future__ import annotations

import datetime
import json
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from blog.models import Post

HOME = Path.home()
CLAUDE_PROJECTS_DIR = HOME / ".claude" / "projects"
CODEX_STATE_DB = HOME / ".codex" / "state_5.sqlite"
OPENCLAW_LOG = HOME / ".openclaw" / "logs" / "commands.log"
# cron no incluye ~/.local/bin en el PATH
CLAUDE_BIN = shutil.which("claude") or str(HOME / ".local" / "bin" / "claude")

NOISE_PATTERNS = re.compile(
    r"^\s*("
    r"hola\b|ok\b|test\b|responde\b|recuper[ae]|puedes recuperar|"
    r"perdi(mos)? la sesion|se me (cayo|apago|quito)|se peto|"
    r"respondeme|solo (con )?ok"
    r")",
    re.IGNORECASE,
)

EVIDENCE_CHAR_CAP = 320
MAX_EVIDENCE_ITEMS_PER_BUCKET = 12

STYLE_REFERENCE = """Ejemplo de tono ya usado en el blog (para que el post nuevo encaje):

---
Titulo: Reconstruyendo mi portfolio y mi CV desde cero
Esta semana me toco ponerme del otro lado: en vez de construir sistemas \
para otros, construir mi propia carta de presentacion. Reescribi el \
contenido de este portfolio para que los proyectos destacados fueran los \
que de verdad representan como trabajo...
---
"""


SECRET_PATTERNS = re.compile(
    r"<pasted_content[^>]*>.*?(</pasted_content>|$)"
    r"|\b(sk|pk|rk)-[A-Za-z0-9_-]{16,}"
    r"|\b(ghp|gho|github_pat|xox[abp]|AKIA)[A-Za-z0-9_-]{12,}"
    r"|\b[A-Za-z0-9_-]{40,}\b",
    re.DOTALL,
)


def redact(text: str) -> str:
    """Quita claves/tokens y bloques pegados antes de mandar nada al modelo."""
    return SECRET_PATTERNS.sub("[redactado]", text)


def is_noise(text: str) -> bool:
    text = (text or "").strip()
    if len(text) < 25:
        return True
    return bool(NOISE_PATTERNS.match(text))


def project_label(cwd: str) -> str:
    if not cwd:
        return "general"
    name = Path(cwd).name or cwd
    return name


def collect_codex(target_date: datetime.date) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}
    if not CODEX_STATE_DB.exists():
        return buckets
    con = sqlite3.connect(str(CODEX_STATE_DB))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select title, preview, cwd, created_at_ms from threads")
    for row in cur.fetchall():
        ts_ms = row["created_at_ms"] or 0
        day = timezone.localtime(
            datetime.datetime.fromtimestamp(ts_ms / 1000, tz=datetime.timezone.utc)
        ).date()
        if day != target_date:
            continue
        text = (row["preview"] or row["title"] or "").strip()
        if is_noise(text) or "/tmp/" in (row["cwd"] or ""):
            continue
        label = project_label(row["cwd"] or "")
        buckets.setdefault(label, []).append(redact(text)[:EVIDENCE_CHAR_CAP])
    con.close()
    return buckets


BLOG_PROMPT_MARKER = "Sos un asistente que escribe UNA entrada de blog"


def collect_claude_code(target_date: datetime.date) -> dict[str, list[str]]:
    """Un bucket por trabajo: cada sesion con nombre (/rename) es su propio
    post aunque varias compartan carpeta; las interactivas sin nombre tambien
    van aparte; las ejecuciones automaticas (sdk-cli) se agrupan por proyecto."""
    buckets: dict[str, list[str]] = {}
    if not CLAUDE_PROJECTS_DIR.exists():
        return buckets
    for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        project = project_dir.name.replace("-home-ocultwolf-", "").replace(
            "-home-ocultwolf", "home"
        ) or "general"
        for jsonl_file in project_dir.glob("*.jsonl"):
            title = None
            entrypoint = None
            texts: list[str] = []
            try:
                with jsonl_file.open() as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if entry.get("type") == "custom-title":
                            title = (entry.get("customTitle") or "").strip() or title
                            continue
                        if entry.get("type") != "user" or entry.get("isMeta"):
                            continue
                        entrypoint = entrypoint or entry.get("entrypoint")
                        ts = entry.get("timestamp")
                        if not ts:
                            continue
                        try:
                            day = timezone.localtime(
                                datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                            ).date()
                        except ValueError:
                            continue
                        if day != target_date:
                            continue
                        msg = entry.get("message", {})
                        content = msg.get("content")
                        if isinstance(content, list):
                            text = " ".join(
                                b.get("text", "")
                                for b in content
                                if isinstance(b, dict) and b.get("type") == "text"
                            )
                        else:
                            text = content or ""
                        text = text.strip()
                        if text.startswith("<") or is_noise(text):
                            continue
                        texts.append(redact(text)[:EVIDENCE_CHAR_CAP])
            except OSError:
                continue
            # Las propias ejecuciones de este agente no son trabajo publicable.
            if not texts or texts[0].startswith(BLOG_PROMPT_MARKER):
                continue
            if title:
                label = f"{title} ({project})"
            elif entrypoint == "cli":
                label = f"{project} {jsonl_file.stem[:8]}"
            else:
                label = project
            buckets.setdefault(label, []).extend(texts)
    return buckets


def collect_openclaw(target_date: datetime.date) -> list[str]:
    if not OPENCLAW_LOG.exists():
        return []
    date_str = target_date.isoformat()
    lines = []
    try:
        with OPENCLAW_LOG.open(errors="ignore") as f:
            for line in f:
                if date_str in line:
                    lines.append(redact(line.strip())[:EVIDENCE_CHAR_CAP])
    except OSError:
        pass
    return lines[:MAX_EVIDENCE_ITEMS_PER_BUCKET]


def merge_buckets(*sources: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for source in sources:
        for label, items in source.items():
            merged.setdefault(label, []).extend(items)
    for label, items in merged.items():
        # Muestreo repartido para cubrir todo el dia, no solo el principio.
        if len(items) > MAX_EVIDENCE_ITEMS_PER_BUCKET:
            step = len(items) / MAX_EVIDENCE_ITEMS_PER_BUCKET
            items = [items[int(i * step)] for i in range(MAX_EVIDENCE_ITEMS_PER_BUCKET)]
        merged[label] = items
    return merged


def build_prompt(project: str, evidence: list[str], openclaw_lines: list[str]) -> str:
    evidence_block = "\n".join(f"- {e}" for e in evidence)
    extra = ""
    if openclaw_lines:
        extra = "\n\nActividad de OpenClaw ese dia:\n" + "\n".join(
            f"- {l}" for l in openclaw_lines
        )
    return f"""Sos un asistente que escribe UNA entrada de blog personal para Pablo \
Dominguez (Ocultwolf), un desarrollador Python autodidacta que documenta su \
trabajo real de programacion.

{STYLE_REFERENCE}

Reglas ESTRICTAS (rompelas y el post no sirve):
1. NUNCA menciones rutas de archivo, puertos, nombres de contenedores/servicios, \
URLs internas, IPs, nombres de variables de entorno, ni ningun detalle tecnico \
de infraestructura. Habla del QUE y el POR QUE a alto nivel, nunca del COMO \
interno exacto.
2. Primera persona, como si Pablo lo escribiera el mismo. Tono directo, \
tecnico pero legible, sin exagerar logros.
3. De 1 a 5 parrafos cortos segun cuanto trabajo haya: un avance pequeno \
pero real merece un post corto y claro, no se descarta por ser pequeno. \
Nada de listas con vinetas dentro del contenido.
4. El nombre del trabajo es solo una etiqueta: si la evidencia muestra \
otra cosa, escribe sobre lo que la evidencia muestra.
5. Si la evidencia de abajo es solo ruido operativo (arreglar un login, \
recuperar una sesion perdida, probar que el agente responde, mensajes de \
prueba sin sustancia, o solo preguntar como va algo sin \
trabajo nuevo) NO inventes un post: respondé unicamente \
{{"skip": true, "reason": "motivo en una frase"}}.
6. Si hay contenido real, respondé SOLO este JSON (sin markdown, sin \
texto extra):
{{"skip": false, "title": "...", "excerpt": "resumen de una frase, max 200 caracteres", \
"content": "el post completo, parrafos separados por doble salto de linea", \
"cover_label": "una o dos palabras de categoria"}}

Trabajo concreto (escribe SOLO sobre este trabajo, deja claro que se hizo y su alcance): {project}

Evidencia del dia (fragmentos de sesiones de trabajo, resumidos):
{evidence_block}{extra}
"""


def call_claude(prompt: str) -> dict | None:
    try:
        proc = subprocess.run(
            [CLAUDE_BIN, "-p", prompt, "--output-format", "json", "--model", "sonnet", "--effort", "low"],
            capture_output=True,
            text=True,
            timeout=180,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"  claude fallo: {exc!r}")
        return None
    if proc.returncode != 0:
        print(f"  claude salio con {proc.returncode}: {(proc.stderr or proc.stdout)[:300]}")
        return None
    try:
        wrapper = json.loads(proc.stdout)
        result_text = wrapper.get("result", "")
        result_text = result_text.strip()
        if result_text.startswith("```"):
            result_text = re.sub(r"^```(json)?|```$", "", result_text.strip(), flags=re.MULTILINE).strip()
        return json.loads(result_text)
    except (json.JSONDecodeError, AttributeError):
        return None


class Command(BaseCommand):
    help = "Genera entradas de blog a partir del trabajo real del dia (Claude Code, Codex, OpenClaw)."

    def add_arguments(self, parser):
        parser.add_argument("--date", type=str, default=None, help="YYYY-MM-DD, por defecto ayer (dia completo)")
        parser.add_argument("--dry-run", action="store_true", help="No escribe en la base de datos")

    def handle(self, *args, **options):
        if options["date"]:
            target_date = datetime.date.fromisoformat(options["date"])
        else:
            # El cron corre de noche: se procesa el dia anterior, que ya esta completo.
            target_date = timezone.localdate() - datetime.timedelta(days=1)

        codex_buckets = collect_codex(target_date)
        claude_buckets = collect_claude_code(target_date)
        openclaw_lines = collect_openclaw(target_date)
        buckets = merge_buckets(codex_buckets, claude_buckets)

        if not buckets:
            self.stdout.write(f"Sin actividad relevante para {target_date}.")
            return

        created = 0
        for project, evidence in buckets.items():
            if not evidence:
                continue
            source_key = f"auto:{slugify(project)}:{target_date.isoformat()}"
            if Post.objects.filter(source_key=source_key).exists():
                continue

            prompt = build_prompt(project, evidence, openclaw_lines)
            result = call_claude(prompt)
            if not result or result.get("skip"):
                # El modelo no es determinista: un segundo intento evita perder
                # trabajo real por un descarte al azar.
                result = call_claude(prompt)
            if not result:
                self.stdout.write(f"[{project}] fallo la llamada a claude, se reintentara otro dia.")
                continue
            if result.get("skip"):
                reason = (result.get("reason") or "sin motivo").strip()[:200]
                self.stdout.write(f"[{project}] omitido (2 intentos): {reason}")
                continue

            title = (result.get("title") or "").strip()
            content = (result.get("content") or "").strip()
            excerpt = (result.get("excerpt") or "").strip()[:260]
            cover_label = (result.get("cover_label") or "").strip()[:80]
            if not title or not content:
                continue

            if options["dry_run"]:
                self.stdout.write(f"[DRY RUN] {project}: {title}")
                continue

            slug = slugify(title)
            base_slug = slug
            n = 2
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            published_at = timezone.make_aware(
                datetime.datetime.combine(target_date, datetime.time(hour=20))
            )
            Post.objects.create(
                title=title,
                slug=slug,
                excerpt=excerpt or title,
                content=content,
                cover_label=cover_label,
                published_at=published_at,
                # El blog ya no publica entradas tipo diario: quedan como borrador y
                # sirven de material para los capitulos tecnicos.
                published=False,
                source_key=source_key,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"[{project}] creado: {title}"))

        self.stdout.write(f"Listo. Posts creados: {created}")
