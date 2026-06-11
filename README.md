# miWeb

Portfolio personal de Pablo D V montado con Django y un blog integrado.

## Qué incluye

- Home tipo portfolio con secciones de presentación, servicios, proyectos y contacto
- Blog con listado y detalle de posts
- Panel de admin para editar proyectos y artículos
- Datos semilla con proyectos públicos del GitHub de Ocultwolf

## Arranque rápido

1. Entrar al repo:
   cd /home/openclaw/script_github/miWeb
2. Aplicar migraciones:
   ./.venv/bin/python manage.py migrate
3. Levantar el servidor:
   ./.venv/bin/python manage.py runserver 0.0.0.0:8000

## Rutas

- /  portada del portfolio
- /blog/  listado del blog
- /admin/  panel de administración

## Contenido semilla

El portfolio ya viene con proyectos y posts iniciales para enseñar la base mañana. Después se reemplaza por contenido real, capturas y enlaces definitivos.
