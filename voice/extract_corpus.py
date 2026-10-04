"""Extrae los mensajes que Pablo escribio o dicto de verdad, para construir su perfil de voz.

Fuentes:
- Sesiones de Claude Code (~/.claude/projects/*/*.jsonl): solo mensajes de usuario
  tecleados a mano (entrypoint "cli", contenido en texto plano).
- Sesiones de Codex (~/.codex/sessions/**/*.jsonl): eventos user_message.
- Historial de Neon (agent-lab/neon/server/conversation_history*.json): lo que Pablo
  dijo en voz alta, ya transcrito por el STT.

Se descarta lo que no es su voz: prompts automaticos de Saturno/blog, comandos,
mensajes de prueba, texto pegado y lo que Neon reenvia por el puente (voseo y
"Pablo" en tercera persona).

Salida: voice/data/corpus.jsonl con {"source", "date", "text"} por mensaje.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HOME = Path.home()
OUT = Path(__file__).resolve().parent / "data" / "corpus.jsonl"

CLAUDE_DIR = HOME / ".claude" / "projects"
CODEX_DIR = HOME / ".codex" / "sessions"
NEON_HISTORY = sorted((HOME / "agent-lab" / "neon" / "server").glob("conversation_history*.json"))

AUTOMATED = re.compile(
    r"^\s*(Objetivo de largo plazo|Objetivo general|Tarea:|Sos un asistente|You are|"
    r"<command-|<local-command|<system-reminder|<task-notification|Caveat:|\[Request interrupted|"
    r"This session is being continued|Base directory for this skill)",
    re.IGNORECASE,
)
# Lo que Neon reenvia por el puente esta en voseo y habla de Pablo en tercera persona.
RELAYED = re.compile(
    r"\bPablo (pregunta|quiere|siente|dice|pide)\b|\b(decime|confirmame|agarr[aá]|levant[aá]|"
    r"repas[aá]|investigalas|fijate|mir[aá] vos|ten[eé]s|pod[eé]s|quer[eé]s)\b",
    re.IGNORECASE,
)
TEST_PING = re.compile(r"^\s*test\b.*respond", re.IGNORECASE)
PASTED = re.compile(r"<pasted_content[^>]*>.*?(</pasted_content[^>]*>|$)", re.DOTALL)
SECRETS = re.compile(r"\b(sk|pk|rk)-[A-Za-z0-9_-]{16,}|\b[A-Za-z0-9_-]{40,}\b")
# Logs, trazas y salidas de terminal pegadas sin etiqueta.
LOGLIKE = re.compile(r"^(\s*(Traceback|File \"|\$ |>>> |\d{4}-\d{2}-\d{2}[T ]\d|INFO|ERROR|DEBUG|WARNING)|.*\|.*\|)")


def clean(text: str) -> str:
    text = PASTED.sub("", text)
    lines = [ln for ln in text.splitlines() if not LOGLIKE.match(ln)]
    text = "\n".join(lines).strip()
    return SECRETS.sub("[redactado]", text)


def looks_generated(text: str) -> bool:
    """Prompts redactados por otra IA y pegados: estructura markdown que Pablo no escribe a mano."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    structured = sum(bool(re.match(r"(#{1,4} |[-*•] |\d+[.)] |[A-ZÁÉÍÓÚ ]{6,}:)", ln)) for ln in lines)
    if structured >= 2 or "→" in text or re.search(r"^(VOS|NEON)\b", text, re.M):
        return True
    return text.lstrip().startswith(("Error", "Corré", "Ejecutá", "Perfecto. ", "Leé "))


def accent_rate(text: str) -> float:
    words = re.findall(r"\w+", text)
    return sum(bool(re.search("[áéíóúñ¿¡]", w)) for w in words) / max(len(words), 1)


def keep(text: str) -> bool:
    if len(text) < 12 or len(text.split()) < 4:
        return False
    if looks_generated(text):
        return False
    if AUTOMATED.match(text) or TEST_PING.match(text) or RELAYED.search(text):
        return False
    # Mensajes que son casi todo codigo o rutas no dicen nada de como habla.
    letters = sum(ch.isalpha() or ch.isspace() for ch in text)
    return letters / len(text) > 0.85


def from_claude():
    for f in CLAUDE_DIR.glob("*/*.jsonl"):
        for line in f.open(errors="ignore"):
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            if o.get("type") != "user" or o.get("isMeta") or o.get("entrypoint") != "cli":
                continue
            content = o.get("message", {}).get("content")
            if isinstance(content, str):
                yield "claude", (o.get("timestamp") or "")[:10], content


def from_codex():
    for f in CODEX_DIR.rglob("*.jsonl"):
        for line in f.open(errors="ignore"):
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            p = o.get("payload") or {}
            if o.get("type") == "event_msg" and p.get("type") == "user_message":
                yield "codex", (o.get("timestamp") or "")[:10], p.get("message") or ""


def from_neon():
    for f in NEON_HISTORY:
        try:
            turns = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        for t in turns:
            if t.get("role") == "user" and isinstance(t.get("content"), str):
                yield "neon_voz", "", t["content"]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    seen, rows = set(), []
    for source, date, raw in (*from_claude(), *from_codex(), *from_neon()):
        text = clean(raw)
        key = re.sub(r"\W+", " ", text.lower()).strip()
        # Pablo teclea sin tildes: un texto tecleado lleno de tildes es de otra IA, pegado.
        # (El STT de Neon si pone tildes, por eso no se aplica a la voz.)
        typed_by_other = source != "neon_voz" and accent_rate(text) > 0.035
        if not keep(text) or typed_by_other or key in seen:
            continue
        seen.add(key)
        rows.append({"source": source, "date": date, "text": text})
    with OUT.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    by_source = {}
    for r in rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    words = sum(len(r["text"].split()) for r in rows)
    print(f"{len(rows)} mensajes, {words} palabras -> {OUT}  {by_source}")


if __name__ == "__main__":
    main()
