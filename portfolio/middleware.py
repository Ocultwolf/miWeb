from django.conf import settings
from django.utils import translation


class CookieLanguageMiddleware:
    """Activa el idioma elegido con los botones EN/ES (cookie de set_language).

    A diferencia de LocaleMiddleware, no mira la cabecera Accept-Language del navegador: la web
    sale en inglés para todo el mundo salvo que el visitante elija español explícitamente.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.supported = {code for code, _ in settings.LANGUAGES}

    def __call__(self, request):
        lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if lang not in self.supported:
            lang = settings.LANGUAGE_CODE
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        response.headers.setdefault('Content-Language', lang)
        response.headers['Vary'] = ', '.join(filter(None, [response.headers.get('Vary'), 'Cookie']))
        return response
