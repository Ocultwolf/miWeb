from django.db import migrations
from django.utils.text import slugify


PROJECT = {
    'title': 'Agente de bitácora automática',
    'short_description': 'Un agente que lee mis sesiones de IA del día y publica solo las entradas del blog.',
    'description': (
        'Comando de Django que revisa mis sesiones de trabajo diarias (Claude Code, '
        'Codex y OpenClaw), agrupa el trabajo por proyecto, descarta ruido operativo '
        '(recuperar sesiones, pruebas triviales) y redacta una entrada de blog por '
        'cada pieza de trabajo real -- sin exponer rutas, infraestructura ni datos '
        'internos. Corre solo cada noche vía cron y publica directo, con '
        'deduplicacion para no repetir contenido.'
    ),
    'technologies': 'Python, Django, SQLite, Claude Code CLI',
    'link': 'https://github.com/Ocultwolf/miWeb',
    'impact': 'El blog se escribe solo a partir del trabajo real del dia',
    'featured': True,
    'order': 1,
}

REORDER = {
    'ClonadorProfesional': 2,
    'Gasolineras-Canarias-ModaPrecios': 3,
    'miWeb': 4,
}


def forward(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Project.objects.update_or_create(
        slug=slugify(PROJECT['title']),
        defaults=PROJECT,
    )
    for title, order in REORDER.items():
        Project.objects.filter(slug=slugify(title)).update(order=order)


def backward(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Project.objects.filter(slug=slugify(PROJECT['title'])).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0003_update_projects'),
    ]

    operations = [migrations.RunPython(forward, backward)]
