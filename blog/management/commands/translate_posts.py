"""Traduce al inglés los posts publicados (campos *_en) con `claude -p`.

    python manage.py translate_posts            # solo los que aún no tienen traducción
    python manage.py translate_posts --force    # rehace todas
    python manage.py translate_posts --pk 48    # uno concreto

El español sigue siendo el original. Los bloques de código no pasan por el modelo (se sustituyen por
marcadores y se restauran), y una traducción solo se guarda si conserva todos los marcadores y el mismo
número de títulos de sección que el original.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from blog.models import Post

CLAUDE_BIN = shutil.which("claude") or str(Path.home() / ".local" / "bin" / "claude")
CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
MARKER = "[[CODE_BLOCK_{}]]"

CONTENT_PROMPT = """Translate the following Spanish technical blog chapter into natural, idiomatic English.

It is written in the first person by a self-taught developer. Keep his voice: direct, conversational but
sober, honest about doubts and mistakes. It must read as if he had written it in English himself, not as
a translation.

Rules:
1. Translate everything faithfully: every fact, number, name, decision and caveat. Add nothing, drop nothing.
2. Keep the exact Markdown structure: the same headings (translated), lists, bold, inline code and tables.
3. Keep every placeholder like {marker} exactly as is, in its place.
4. Use English conventions for numbers and dates: "0,05 %" -> "0.05%", "2.400 $" -> "$2,400",
   "12 millones" -> "12 million", "el 19 de septiembre" -> "on September 19".
5. Keep technical terms in their usual English form (backtest, stop loss, prompt, pipeline...).
6. Return ONLY the translated Markdown, with no preamble and without wrapping it in a code block.
   Start directly with the first translated sentence. Never repeat or quote the Spanish source.

<chapter>
{text}
</chapter>"""

META_PROMPT = """Translate these three short Spanish fields of a technical blog post into natural English.
Keep the meaning exactly; the title should read like a good English article title (sentence case).
Return ONLY a JSON object with the keys "title", "excerpt" and "cover_label".

{payload}"""


def _claude(prompt: str, timeout: int = 900) -> str:
    try:
        proc = subprocess.run(
            [CLAUDE_BIN, "-p", "--output-format", "json", "--model", "sonnet"],
            input=prompt, capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        raise CommandError(f"claude falló: {exc!r}") from exc
    if proc.returncode != 0:
        raise CommandError(f"claude salió con {proc.returncode}: {(proc.stderr or proc.stdout)[:300]}")
    result = json.loads(proc.stdout).get("result", "").strip()
    if not result:
        raise CommandError("claude devolvió una respuesta vacía")
    return result


def translate_content(text: str) -> str:
    blocks: list[str] = []

    def stash(m: re.Match) -> str:
        blocks.append(m.group(0))
        return MARKER.format(len(blocks) - 1)

    protected = CODE_BLOCK.sub(stash, text)
    last_error = None
    for _ in range(3):  # el modelo no es determinista: un reintento suele bastar
        try:
            return _restore_and_check(_claude(CONTENT_PROMPT.format(marker=MARKER.format("N"), text=protected)), blocks, text)
        except CommandError as exc:
            last_error = exc
    raise last_error


def _restore_and_check(out: str, blocks: list[str], text: str) -> str:
    for i, block in enumerate(blocks):
        marker = MARKER.format(i)
        if out.count(marker) != 1:
            raise CommandError(f"la traducción perdió o duplicó el bloque de código {i}")
        out = out.replace(marker, block)
    headings = lambda s: len(re.findall(r"^#{1,6} ", s, re.M))  # noqa: E731
    if headings(out) != headings(text):
        raise CommandError(f"cambió el número de títulos ({headings(text)} -> {headings(out)})")
    check_is_clean_english(out)
    return out


CHATTER = re.compile(r"(?im)^\s*(wait\b|here it is|here is the translation|i (should|must|will) (output|produce|be producing))")
SPANISH_WORDS = re.compile(r"\b(que|para|porque|también|cuando|desde|está|después|aunque|siempre|pero|como|una|los|las)\b", re.I)


def check_is_clean_english(text: str) -> None:
    """Rechaza traducciones con comentarios del propio modelo o con texto que se quedó en español
    (pasó una vez: el modelo copió el primer párrafo en español y luego escribió "Wait, I should
    output the translation only")."""
    if CHATTER.search(text):
        raise CommandError("la traducción contiene comentarios del modelo")
    prose = CODE_BLOCK.sub("", text)
    for para in prose.split("\n\n"):
        n = len(para.split())
        if n >= 12 and len(SPANISH_WORDS.findall(para)) / n > 0.08:
            raise CommandError(f"un párrafo se quedó en español: {para[:60]!r}")
    words = len(prose.split()) or 1
    spanish = len(SPANISH_WORDS.findall(prose))
    if spanish / words > 0.01:
        raise CommandError(f"demasiadas palabras en español en la traducción ({spanish} de {words})")


def translate_meta(post: Post) -> dict:
    payload = json.dumps(
        {"title": post.title, "excerpt": post.excerpt, "cover_label": post.cover_label}, ensure_ascii=False
    )
    raw = _claude(META_PROMPT.format(payload=payload), timeout=300)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(raw)
    if set(data) != {"title", "excerpt", "cover_label"}:
        raise CommandError(f"metadatos incompletos: {data}")
    return data


class Command(BaseCommand):
    help = "Traduce al inglés los posts publicados."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--pk", type=int)

    def handle(self, *args, **opts):
        posts = Post.objects.filter(published=True).order_by("published_at")
        if opts["pk"]:
            posts = posts.filter(pk=opts["pk"])
        elif not opts["force"]:
            posts = posts.filter(content_en="")
        failed = []
        for post in posts:
            self.stdout.write(f"[{post.pk}] {post.title[:60]} ...")
            try:
                meta = translate_meta(post)
                content = translate_content(post.content)
            except (CommandError, json.JSONDecodeError) as exc:
                failed.append(post.pk)
                self.stdout.write(f"   FALLO: {exc}")
                continue
            post.title_en = meta["title"][:160]
            post.excerpt_en = meta["excerpt"][:320]
            post.cover_label_en = meta["cover_label"][:80]
            post.content_en = content
            post.save(update_fields=["title_en", "excerpt_en", "cover_label_en", "content_en"])
            self.stdout.write(f"   ok -> {post.title_en}")
        if failed:
            raise CommandError(f"fallaron: {failed}")
