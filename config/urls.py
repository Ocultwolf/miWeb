from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
] + static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
