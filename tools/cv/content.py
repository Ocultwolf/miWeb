"""Texto del CV en cada idioma. El diseño vive en build_cv.py; aquí solo el contenido."""

CONTACT = ["+41 77 968 30 12", "pablodominguezviera@gmail.com", "github.com/Ocultwolf"]

CV = {
    "en": {
        "subtitle": ["PYTHON DEVELOPER", "AUTOMATION & BACKEND"],
        "contact_title": "CONTACT",
        "location": "Zurich, Switzerland",
        "skills_title": "SKILLS",
        "skills": [
            "Python (advanced)", "Django", "Automation & Selenium", "REST APIs & scraping",
            "Pandas / NumPy", "scikit-learn", "HTML / CSS / JS", "Git", "SQL",
        ],
        "languages_title": "LANGUAGES",
        "languages": [("Spanish", "Native"), ("English", "Conversational"), ("French", "Basic")],
        "education_title": "EDUCATION",
        "education": [
            ("Machine Learning Bootcamp", "4Geeks Academy"),
            ("Intermediate Java Course", "SEAS Campus"),
            ("ESO (2017-2020)", None),
        ],
        "title": "Python Developer",
        "tagline": "Automation, backend systems & applied data science",
        "availability": "AVAILABLE FOR FREELANCE & CONTRACT WORK — ZURICH / REMOTE",
        "about_title": "ABOUT",
        "about": (
            "Self-taught Python developer building autonomous systems, automation tools and data "
            "pipelines. Focus on backend architecture, scripted automation (Selenium, APIs, scraping) "
            "and applied data science. Comfortable working independently end-to-end, from design to "
            "deployment."
        ),
        "strengths_title": "CORE STRENGTHS",
        "strengths": [
            ("Automation & Scripting", "Selenium, APIs and scraping pipelines that remove repetitive manual work."),
            ("Backend & Data Systems", "Django services and structured data pipelines backed by PostgreSQL."),
            ("Independent Delivery", "Self-directed from architecture to deployment — comfortable owning a project end-to-end."),
        ],
        "projects_title": "FEATURED PROJECTS",
        "projects": [
            ("JARVIS P.D.", "Python, LangGraph, PostgreSQL",
             "Autonomous multi-agent system orchestrated with LangGraph; deterministic services validate "
             "and persist agent proposals against a canonical PostgreSQL state, with each development "
             "phase gated and audited before advancing."),
            ("ClonadorProfesional", "Python, Selenium, BeautifulSoup, Flask",
             "Web automation tool that captures a live site's front-end and rebuilds it locally as a "
             "functioning copy — used as the base for this same portfolio."),
            ("Gasolineras Canarias — Price Trend Pipeline", "Python, Pandas, OpenPyXL",
             "Data pipeline that downloads official fuel-price datasets and generates formatted, "
             "region-segmented Excel reports."),
        ],
        "experience_title": "OTHER EXPERIENCE",
        "experience_intro": "Hands-on work across demanding environments — discipline and reliability built outside a screen too.",
        "experience": [
            ("Junior Electrical Installer", "Tenerife, Canary Islands"),
            ("Gardening & Outdoor Maintenance", "Germany"),
            ("Agricultural Worker", "France"),
            ("Logistics Operator", "Netherlands"),
            ("Kitchen Assistant", "Various restaurants"),
        ],
        "closing": (
            "Currently based in Zurich and open to freelance, contract and remote collaborations — "
            "reach out if there's a project to build."
        ),
    },
    "es": {
        "subtitle": ["DESARROLLADOR PYTHON", "AUTOMATIZACIÓN Y BACKEND"],
        "contact_title": "CONTACTO",
        "location": "Zúrich, Suiza",
        "skills_title": "HABILIDADES",
        "skills": [
            "Python (avanzado)", "Django", "Automatización y Selenium", "APIs REST y scraping",
            "Pandas / NumPy", "scikit-learn", "HTML / CSS / JS", "Git", "SQL",
        ],
        "languages_title": "IDIOMAS",
        "languages": [("Español", "Nativo"), ("Inglés", "Conversacional"), ("Francés", "Básico")],
        "education_title": "FORMACIÓN",
        "education": [
            ("Bootcamp de Machine Learning", "4Geeks Academy"),
            ("Curso de Java intermedio", "SEAS Campus"),
            ("ESO (2017-2020)", None),
        ],
        "title": "Desarrollador Python",
        "tagline": "Automatización, sistemas backend y ciencia de datos aplicada",
        "availability": "DISPONIBLE PARA FREELANCE Y CONTRATOS — ZÚRICH / REMOTO",
        "about_title": "SOBRE MÍ",
        "about": (
            "Desarrollador Python autodidacta que construye sistemas autónomos, herramientas de "
            "automatización y pipelines de datos. Me centro en la arquitectura backend, la "
            "automatización con scripts (Selenium, APIs, scraping) y la ciencia de datos aplicada. "
            "Trabajo con autonomía de principio a fin, del diseño al despliegue."
        ),
        "strengths_title": "PUNTOS FUERTES",
        "strengths": [
            ("Automatización y scripting", "Pipelines con Selenium, APIs y scraping que eliminan trabajo repetitivo."),
            ("Backend y sistemas de datos", "Servicios en Django y pipelines de datos estructurados sobre PostgreSQL."),
            ("Entrega autónoma", "De la arquitectura al despliegue por mi cuenta, haciéndome cargo del proyecto de punta a punta."),
        ],
        "projects_title": "PROYECTOS DESTACADOS",
        "projects": [
            ("JARVIS P.D.", "Python, LangGraph, PostgreSQL",
             "Sistema multiagente autónomo orquestado con LangGraph: servicios deterministas validan y "
             "persisten las propuestas de los agentes en un estado canónico de PostgreSQL, con cada fase "
             "auditada antes de avanzar."),
            ("ClonadorProfesional", "Python, Selenium, BeautifulSoup, Flask",
             "Herramienta de automatización web que captura el front-end de un sitio real y lo reconstruye "
             "en local como una copia funcional; es la base de este mismo portfolio."),
            ("Gasolineras Canarias — Pipeline de precios", "Python, Pandas, OpenPyXL",
             "Pipeline de datos que descarga los precios oficiales de los carburantes y genera informes de "
             "Excel con formato, segmentados por zona."),
        ],
        "experience_title": "OTRA EXPERIENCIA",
        "experience_intro": "Trabajo práctico en entornos exigentes: disciplina y fiabilidad aprendidas también lejos de una pantalla.",
        "experience": [
            ("Instalador electricista junior", "Tenerife, Islas Canarias"),
            ("Jardinería y mantenimiento exterior", "Alemania"),
            ("Trabajador agrícola", "Francia"),
            ("Operario de logística", "Países Bajos"),
            ("Ayudante de cocina", "Varios restaurantes"),
        ],
        "closing": (
            "Actualmente vivo en Zúrich y estoy abierto a colaboraciones freelance, por contrato y en "
            "remoto: escríbeme si tienes un proyecto que construir."
        ),
    },
}
