"""Exporta la web a HTML estático para GitHub Pages (https://ocultwolf.github.io).

    python manage.py export_site --out ../Ocultwolf.github.io

GitHub Pages no ejecuta Django: aquí se renderiza cada página con el propio Django (inglés en /,
español en /es/) y se escribe como index.html, junto con los archivos estáticos. El contenido del
directorio de salida se reemplaza, salvo .git, para que lo que desaparece de la web también desaparezca
de la copia publicada.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.urls import reverse
from django.utils import translation

from blog.models import Post

KEEP = {".git", "CNAME"}


class Command(BaseCommand):
    help = "Exporta la web a HTML estático para GitHub Pages."

    def add_arguments(self, parser):
        parser.add_argument("--out", required=True)

    def handle(self, *args, **opts):
        out = Path(opts["out"]).resolve()
        if out == Path(settings.BASE_DIR).resolve() or not out.parent.exists():
            raise CommandError(f"directorio de salida no válido: {out}")
        out.mkdir(exist_ok=True)
        for child in out.iterdir():
            if child.name not in KEEP:
                shutil.rmtree(child) if child.is_dir() else child.unlink()

        paths = []
        slugs = list(Post.objects.filter(published=True).values_list("slug", flat=True))
        for lang, _ in settings.LANGUAGES:
            with translation.override(lang):
                paths += [reverse("home"), reverse("blog_index")]
                paths += [reverse("blog_detail", args=[slug]) for slug in slugs]

        client = Client()
        for path in paths:
            resp = client.get(path)
            if resp.status_code != 200:
                raise CommandError(f"{path} devolvió {resp.status_code}")
            target = out / path.lstrip("/") / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resp.content)

        for src in settings.STATICFILES_DIRS:
            shutil.copytree(src, out / "static", dirs_exist_ok=True)
        (out / ".nojekyll").write_text("")  # que GitHub Pages sirva los archivos tal cual
        (out / "404.html").write_text(
            '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/">'
            '<title>Pablo Dominguez Viera</title><a href="/">Pablo Dominguez Viera</a>\n'
        )
        self.stdout.write(f"{len(paths)} páginas exportadas en {out}")
