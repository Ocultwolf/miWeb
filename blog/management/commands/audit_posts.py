"""Revisa los posts en busca de información sensible (ver blog/sensitive.py).

    python manage.py audit_posts            # solo informa, de los publicados
    python manage.py audit_posts --all      # incluye borradores
    python manage.py audit_posts --fix      # censura lo encontrado y guarda

Sale con código 1 si queda algo sin censurar, para poder usarlo como freno antes de publicar.
"""

from django.core.management.base import BaseCommand

from blog.models import Post
from blog.sensitive import find_sensitive, redact

FIELDS = ("title", "excerpt", "content")


class Command(BaseCommand):
    help = "Busca y opcionalmente censura información sensible en los posts."

    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", help="incluir borradores")
        parser.add_argument("--fix", action="store_true", help="censurar y guardar")

    def handle(self, *args, **opts):
        posts = Post.objects.all() if opts["all"] else Post.objects.filter(published=True)
        pending = 0
        for post in posts.order_by("pk"):
            hits = [h for f in FIELDS for h in find_sensitive(getattr(post, f))]
            if not hits:
                continue
            kinds = sorted({k for k, _ in hits})
            if opts["fix"]:
                for f in FIELDS:
                    setattr(post, f, redact(getattr(post, f)))
                post.save(update_fields=list(FIELDS))
                self.stdout.write(f"[{post.pk}] {post.slug}: censurado ({', '.join(kinds)})")
            else:
                pending += 1
                self.stdout.write(f"[{post.pk}] {post.slug}: {len(hits)} hallazgo(s) ({', '.join(kinds)})")
        if pending:
            raise SystemExit(1)
        self.stdout.write("Sin información sensible pendiente.")
