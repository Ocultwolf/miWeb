"""Filtro de voz: reescribe un texto para que suene como si lo hubiera escrito Pablo.

Usa perfil_voz.md (rasgos de su forma de expresarse) y ejemplos.md (mensajes reales suyos,
corregidos) como guía de estilo para `claude -p`, igual que sync_work_blog. Garantías:
- No toca el contenido técnico: los bloques de código se sustituyen por marcadores antes de llamar
  al modelo y se restauran después, y se comprueba que no se pierda ninguno.
- La ortografía y la puntuación salen corregidas aunque los ejemplos vengan de su forma de teclear.

Uso:
    python3 voice/voz.py borrador.md > final.md
    echo "texto" | python3 voice/voz.py -
    python3 voice/voz.py --post 35            # muestra el post 35 de la BD pasado por el filtro
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLAUDE_BIN = shutil.which("claude") or str(Path.home() / ".local" / "bin" / "claude")
CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
PLACEHOLDER = "[[BLOQUE_CODIGO_{}]]"

PROMPT = """Eres el editor personal de Pablo. Tu único trabajo es reescribir el TEXTO de abajo para que \
suene exactamente como lo escribiría él, siguiendo su perfil de voz y sus ejemplos reales.

<perfil_voz>
{perfil}
</perfil_voz>

<ejemplos_reales>
{ejemplos}
</ejemplos_reales>

Esto NO es una corrección de estilo: reescribe cada frase desde cero como la diría él. Alguien que \
conozca a Pablo tiene que reconocerlo al leerlo. Convierte la narración impersonal o de resumen en su \
forma de razonar: qué esperaba, qué vio, qué le sorprendió o no le cuadraba, cómo le dio la vuelta, \
explicado con un caso concreto cuando el texto lo permita. Prefiere frases directas y verbos coloquiales \
del oficio a frases abstractas ("dediqué tiempo a", "abre la puerta a", "puse a prueba").

Reglas obligatorias:
1. Conserva TODO el contenido técnico: hechos, cifras, nombres de herramientas, decisiones, causas y \
resultados. No añadas hechos, anécdotas, opiniones ni experiencias que no estén en el texto original; \
puedes reformular, reordenar dentro de un párrafo y unir o partir frases, pero no inventar.
2. Mantén la estructura del documento: mismos títulos (puedes mejorar su redacción), mismo orden de \
secciones, misma sintaxis Markdown. Los marcadores {marcador} van intactos y en su sitio.
3. Ortografía, tildes, puntuación y signos ¿¡ impecables según la RAE. Español de España, tuteo, nunca voseo.
4. Usa sus muletillas con la moderación que marca el perfil: el objetivo es que suene a él escribiendo \
con calma, no a una imitación exagerada.
5. Elimina cualquier rastro de texto de IA de la lista "Lo que NUNCA hace".
6. Devuelve SOLO el texto reescrito, sin comentarios, sin preámbulo y sin envolverlo en bloques de código.

<texto>
{texto}
</texto>"""


def _protect_code(text: str) -> tuple[str, list[str]]:
    blocks: list[str] = []

    def stash(m: re.Match) -> str:
        blocks.append(m.group(0))
        return PLACEHOLDER.format(len(blocks) - 1)

    return CODE_BLOCK.sub(stash, text), blocks


def _restore_code(text: str, blocks: list[str]) -> str:
    for i, block in enumerate(blocks):
        marker = PLACEHOLDER.format(i)
        if marker not in text:
            raise ValueError(f"el modelo perdió el bloque de código {i}")
        text = text.replace(marker, block)
    return text


def aplicar_voz(texto: str, model: str = "sonnet", timeout: int = 600) -> str:
    """Devuelve `texto` reescrito con la voz de Pablo. Lanza RuntimeError si el modelo falla."""
    protegido, bloques = _protect_code(texto)
    prompt = PROMPT.format(
        perfil=(HERE / "perfil_voz.md").read_text(),
        ejemplos=(HERE / "ejemplos.md").read_text(),
        marcador=PLACEHOLDER.format("N"),
        texto=protegido,
    )
    try:
        proc = subprocess.run(
            [CLAUDE_BIN, "-p", "--output-format", "json", "--model", model, "--effort", "low"],
            input=prompt, capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        raise RuntimeError(f"claude falló: {exc!r}") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"claude salió con {proc.returncode}: {(proc.stderr or proc.stdout)[:300]}")
    salida = json.loads(proc.stdout).get("result", "").strip()
    if not salida:
        raise RuntimeError("claude devolvió una respuesta vacía")
    return _restore_code(salida, bloques)


def _post_content(pk: int) -> str:
    sys.path.insert(0, str(HERE.parent))
    import os

    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    from blog.models import Post

    post = Post.objects.get(pk=pk)
    return f"# {post.title}\n\n{post.content}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("archivo", nargs="?", help="archivo de texto/Markdown, o - para stdin")
    parser.add_argument("--post", type=int, help="id de un post del blog a pasar por el filtro (no lo guarda)")
    parser.add_argument("--model", default="sonnet")
    args = parser.parse_args()

    if args.post is not None:
        texto = _post_content(args.post)
    elif args.archivo == "-":
        texto = sys.stdin.read()
    elif args.archivo:
        texto = Path(args.archivo).read_text()
    else:
        parser.error("indica un archivo, - o --post ID")
    print(aplicar_voz(texto, model=args.model))


if __name__ == "__main__":
    main()
