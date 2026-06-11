from django.db import migrations
from django.utils.text import slugify
from django.utils import timezone


PROJECTS = [
    {
        'title': 'ClonadorProfesional',
        'short_description': 'Clonador web en Python para capturar front, assets y comportamiento visual.',
        'description': 'Proyecto para replicar interfaces reales, descargar recursos y montar una copia funcional en local.',
        'technologies': 'Python, Selenium, Flask, HTML, CSS',
        'link': 'https://github.com/Ocultwolf/ClonadorProfesional',
        'impact': 'Base de trabajo para clonación profesional',
        'featured': True,
        'order': 1,
    },
    {
        'title': 'Gasolineras-Canarias-ModaPrecios',
        'short_description': 'Análisis de la moda de precios de gasolineras en Canarias.',
        'description': 'Proyecto de datos para detectar tendencias de precios y comparativas entre estaciones de servicio.',
        'technologies': 'Python, Data Analysis, Pandas, Visualización',
        'link': 'https://github.com/Ocultwolf/Gasolineras-Canarias-ModaPrecios',
        'impact': 'Proyecto orientado a datos y análisis',
        'featured': True,
        'order': 2,
    },
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
    {
        'title': 'miWeb',
        'short_description': 'Repositorio de portfolio personal para presentar la identidad digital.',
        'description': 'Base web personal para mostrar proyectos, datos de contacto y presencia profesional.',
        'technologies': 'HTML, CSS, Personal Branding',
        'link': 'https://github.com/Ocultwolf/miWeb',
        'impact': 'Portfolio personal base',
        'featured': False,
        'order': 5,
    },
]

POSTS = [
    {
        'title': 'Cómo convertir un clon en un portfolio real',
        'excerpt': 'Primero se clona la estructura, luego se limpia el contenido y por último se convierte en algo propio.',
        'content': 'Un buen portfolio no debería parecer un ejercicio de clase. Tiene que mostrar criterio, proyecto y dirección. La base está en copiar la estructura correcta y luego sustituir todo lo que suene a demo por historia real, proyectos y pruebas de trabajo.',
        'cover_label': 'Proceso',
    },
    {
        'title': 'Responsive de verdad: lo que importa',
        'excerpt': 'Responsive no es encoger cosas: es decidir qué mostrar, cómo y en qué orden.',
        'content': 'El responsive serio no se resuelve solo con media queries. Hay que pensar en jerarquía, espacio, lectura y densidad visual. Si una web no respira en móvil, no está lista.',
        'cover_label': 'Responsive',
    },
    {
        'title': 'Por qué Git y ramas separadas te salvan el curro',
        'excerpt': 'Si vas a tocar una base que ya funciona, trabajar con ramas evita cargarte el proyecto principal.',
        'content': 'Cuando el trabajo crece, los cambios pequeños y trazables son una ventaja brutal. Una rama de trabajo limpia permite experimentar sin destruir lo que ya funcionaba.',
        'cover_label': 'Git',
    },
]


def seed_forward(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Post = apps.get_model('blog', 'Post')
    now = timezone.now()
    for idx, item in enumerate(PROJECTS, start=1):
        Project.objects.get_or_create(
            slug=slugify(item['title']),
            defaults={**item, 'order': item.get('order', idx)},
        )
    for idx, item in enumerate(POSTS, start=1):
        Post.objects.get_or_create(
            slug=slugify(item['title']),
            defaults={
                **item,
                'published_at': now,
                'published': True,
            },
        )


def seed_backward(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    Post = apps.get_model('blog', 'Post')
    Project.objects.filter(slug__in=[slugify(item['title']) for item in PROJECTS]).delete()
    Post.objects.filter(slug__in=[slugify(item['title']) for item in POSTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
        ('blog', '0001_initial'),
    ]

    operations = [migrations.RunPython(seed_forward, seed_backward)]
