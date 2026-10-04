"""Textos bilingües de los proyectos (inglés por defecto en la web, español como alternativa)."""

from django.db import migrations

PROJECTS = {
    "jarvis-pd": {
        "title": "JARVIS P.D.",
        "title_en": "",
        "short_description": "Sistema multiagente autónomo orquestado con LangGraph, con estado canónico en PostgreSQL y gates de auditoría por fase.",
        "short_description_en": "Autonomous multi-agent system orchestrated with LangGraph, with canonical state in PostgreSQL and audit gates per phase.",
        "description": "Arquitectura backend para un sistema de agentes autónomos: los agentes proponen acciones, servicios deterministas las validan y las materializan, y LangGraph coordina el flujo sin ser nunca la fuente de verdad. Estado, outbox y auditoría comparten transacción. El desarrollo avanza por fases con gates auditados (PASS/FAIL documentado) en vez de por intuición.",
        "description_en": "Backend architecture for an autonomous agent system: agents propose actions, deterministic services validate and materialize them, and LangGraph coordinates the flow without ever being the source of truth. State, outbox and audit share a transaction. Development moves forward in phases with audited gates (documented PASS/FAIL) rather than on gut feeling.",
        "impact": "Sistema de agentes con gobierno técnico auditado por fases",
        "impact_en": "Agent system with phase-audited technical governance"
    },
    "agente-de-bitacora-automatica": {
        "title": "Blog técnico escrito con agentes",
        "title_en": "Agent-assisted technical blog",
        "short_description": "Convierte mis sesiones de trabajo con agentes de IA en capítulos técnicos, con mi voz y sin filtrar secretos.",
        "short_description_en": "Turns my working sessions with AI agents into technical chapters, in my own voice and without leaking secrets.",
        "description": "Un comando nocturno de Django recoge el trabajo del día (Claude Code, Codex y OpenClaw), descarta el ruido y lo guarda como borrador. Los capítulos se construyen a partir de fuentes verificadas (commits, código, logs), pasan por un filtro que los reescribe con mi forma de expresarme y por una auditoría automática que censura claves, tokens, IPs y rutas internas antes de publicar.",
        "description_en": "A nightly Django command collects the day's work (Claude Code, Codex and OpenClaw), drops the noise and saves it as a draft. Chapters are built from verified sources (commits, code, logs), go through a filter that rewrites them in my own voice, and through an automatic audit that redacts keys, tokens, IPs and internal paths before publishing.",
        "impact": "Contenido técnico verificado a partir del trabajo real",
        "impact_en": "Verified technical content from real work"
    },
    "clonadorprofesional": {
        "title": "ClonadorProfesional",
        "title_en": "",
        "short_description": "Clonador web en Python: descarga interfaces reales (HTML, CSS, JS, assets) y las sirve en local con Flask.",
        "short_description_en": "Python web cloner: downloads real interfaces (HTML, CSS, JS, assets) and serves them locally with Flask.",
        "description": "Herramienta de automatización que controla Chrome mediante Selenium, extrae el DOM renderizado con BeautifulSoup y reescribe las rutas de los recursos estáticos para levantar en local una copia funcional de cualquier web. Es la base técnica de este mismo portfolio.",
        "description_en": "Automation tool that drives Chrome through Selenium, extracts the rendered DOM with BeautifulSoup and rewrites static asset paths to stand up a working local copy of any website. It is the technical foundation of this very portfolio.",
        "impact": "Automatización de scraping y reconstrucción de interfaces",
        "impact_en": "Scraping automation and interface reconstruction"
    },
    "gasolineras-canarias-modaprecios": {
        "title": "Gasolineras-Canarias-ModaPrecios",
        "title_en": "",
        "short_description": "Pipeline de datos que descarga los precios oficiales de las gasolineras y genera informes de Excel segmentados por isla.",
        "short_description_en": "Data pipeline that downloads official fuel-station prices and generates Excel reports segmented by island.",
        "description": "Script que descarga el dataset público de precios de carburantes, lo procesa con pandas y genera informes de Excel con formato (tablas, estilos, columnas) separados por Tenerife y Gran Canaria, con reintento automático de conexión.",
        "description_en": "Script that downloads the public fuel-price dataset, processes it with pandas and produces formatted Excel reports (tables, styles, columns) split by Tenerife and Gran Canaria, with automatic connection retries.",
        "impact": "Automatización de informes con datos abiertos",
        "impact_en": "Automated reporting on open data"
    },
    "miweb": {
        "title": "miWeb",
        "title_en": "",
        "short_description": "Repositorio de mi portfolio personal para presentar mi identidad digital.",
        "short_description_en": "My personal portfolio repository, presenting my digital identity.",
        "description": "Base web personal para mostrar proyectos, datos de contacto y presencia profesional.",
        "description_en": "Personal website foundation to showcase projects, contact details and professional presence.",
        "impact": "Portfolio personal",
        "impact_en": "Personal portfolio"
    }
}


def apply(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    for slug, fields in PROJECTS.items():
        Project.objects.filter(slug=slug).update(**fields)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0006_project_title_en")]
    operations = [migrations.RunPython(apply, migrations.RunPython.noop)]
