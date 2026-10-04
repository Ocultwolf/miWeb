from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
] + i18n_patterns(
    # Inglés sin prefijo (/), español bajo /es/. Mismo esquema en Django y en la copia estática
    # de GitHub Pages, donde no hay servidor para cambiar de idioma con cookies.
    path('', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    prefix_default_language=False,
) + static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
