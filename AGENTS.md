# miWeb

Portfolio personal de Pablo (Django) con blog integrado. Ruta real:
`/home/ocultwolf/miWeb` -- el propio `README.md` dice una ruta vieja
(`/home/openclaw/script_github/miWeb`), no confiar en esa línea.

## Qué es

Django clásico: `config/settings.py` como settings module, app `blog/`
para el blog, `portfolio/` para el resto del sitio. Publica también una
versión estática en GitHub Pages (`~/Ocultwolf.github.io`).

## Cómo se arranca y se prueba

```bash
cd /home/ocultwolf/miWeb
.venv_host/bin/python manage.py migrate
.venv_host/bin/python manage.py runserver 0.0.0.0:8000
```

## Automatización nocturna (cron, 23:30 diario)

```
manage.py sync_work_blog          # digesto de trabajo del día -> post del blog, vía claude -p
tools/publish_site.sh             # traduce posts nuevos, audita info sensible, exporta a Pages
```

`sync_work_blog.py` solo manda al modelo un digesto acotado (títulos/
previews truncados) y espera `skip=true` cuando no hay nada real que
publicar -- no inventar contenido si el día no tuvo trabajo real.
`voice/voz.py` (filtro de estilo de voz, usado por Neon) sigue la misma
convención de guía de estilo.

## Reglas / trampas

- No commitear `db.sqlite3` ni sus backups (`db.sqlite3.bak-*`).
- `publish_site.sh` bloquea la publicación si su auditoría encuentra
  información sensible -- si un post no se publica, mirar
  `logs/publish.log` antes de forzarlo.
- `--effort low` en las llamadas `claude -p` de `sync_work_blog.py` y
  `voice/voz.py` (fijado 2026-10-06) -- son resúmenes/filtros de estilo,
  no tareas que necesiten razonamiento profundo.
