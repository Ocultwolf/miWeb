from django.db import migrations
from django.utils.text import slugify


NEW_PROJECTS = [
    {
        'title': 'JARVIS P.D.',
        'short_description': 'Sistema multiagente autonomo orquestado con LangGraph, con estado canonico en PostgreSQL y gates de auditoria por fase.',
        'description': (
            'Arquitectura backend para un sistema de agentes autonomos: los agentes proponen '
            'acciones, servicios deterministas las validan y las materializan, y LangGraph coordina '
            'el flujo sin ser nunca la fuente de verdad. Estado, outbox y auditoria comparten '
            'transaccion. El desarrollo avanza por fases con gates auditados (PASS/FAIL documentado) '
            'en vez de por intuicion.'
        ),
        'technologies': 'Python, LangGraph, PostgreSQL, Arquitectura de agentes',
        'link': 'https://github.com/Ocultwolf/JARVIS-PD-greenfield-public',
        'impact': 'Sistema de agentes con gobierno tecnico auditado por fases',
        'featured': True,
        'order': 0,
    },
    {
        'title': 'ClonadorProfesional',
        'short_description': 'Clonador web en Python: descarga interfaces reales (HTML, CSS, JS, assets) y las sirve en local con Flask.',
        'description': (
            'Herramienta de automatizacion que controla Chrome via Selenium, extrae el DOM '
            'renderizado con BeautifulSoup y reescribe las rutas de los recursos estaticos para '
            'levantar una copia funcional de cualquier web en local. Base tecnica de este mismo '
            'portfolio.'
        ),
        'technologies': 'Python, Selenium, BeautifulSoup, Flask',
        'link': 'https://github.com/Ocultwolf/ClonadorProfesional',
        'impact': 'Automatizacion de scraping y reconstruccion de interfaces',
        'featured': True,
        'order': 1,
    },
    {
        'title': 'Gasolineras-Canarias-ModaPrecios',
        'short_description': 'Pipeline de datos que descarga precios oficiales de gasolineras y genera reportes Excel segmentados por isla.',
        'description': (
            'Script que descarga el dataset publico de precios de carburantes, lo procesa con '
            'pandas y genera informes Excel formateados (tablas, estilos, columnas) separados por '
            'Tenerife y Gran Canaria, con reintento automatico de conexion.'
        ),
        'technologies': 'Python, Pandas, OpenPyXL, Automatizacion de datos',
        'link': 'https://github.com/Ocultwolf/Gasolineras-Canarias-ModaPrecios',
        'impact': 'Automatizacion de reporting de datos abiertos',
        'featured': False,
        'order': 2,
    },
]

REMOVED_TITLES = ['ReguLinMod', 'DEA']

OLD_REMOVED_PROJECTS = [
    {
        'title': 'ReguLinMod',
        'short_description': 'Proyecto de regresión regularizada y modelado estadístico.',
        'description': 'Trabajo académico para practicar regresión, regularización y evaluación de modelos.',
        'technologies': 'Python, ML, Statistics, Jupyter',
        'link': 'https://github.com/Ocultwolf/ReguLinMod',
        'impact': 'Enfoque en machine learning y estadística',
        'featured': False,
        'order': 3,
    },
    {
        'title': 'DEA',
        'short_description': 'Proyecto en Python con foco técnico y estructura de práctica.',
        'description': 'Repositorio de apoyo para experimentar con lógica, estructura y práctica de desarrollo.',
        'technologies': 'Python',
        'link': 'https://github.com/Ocultwolf/DEA',
        'impact': 'Proyecto técnico complementario',
        'featured': False,
        'order': 4,
    },
]


def forward(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')

    for item in NEW_PROJECTS:
        Project.objects.update_or_create(
            slug=slugify(item['title']),
            defaults=item,
        )

    Project.objects.filter(
        slug__in=[slugify(title) for title in REMOVED_TITLES]
    ).delete()


def backward(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')

    Project.objects.filter(slug=slugify('JARVIS P.D.')).delete()

    for item in OLD_REMOVED_PROJECTS:
        Project.objects.update_or_create(
            slug=slugify(item['title']),
            defaults=item,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0002_seed_data'),
    ]

    operations = [migrations.RunPython(forward, backward)]
