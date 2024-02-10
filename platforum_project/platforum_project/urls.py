from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('account/', include('account.urls')),
    path('forum/', include('forum.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sav/', include('sav.urls')),
]

if settings.ENV != "PROD":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
