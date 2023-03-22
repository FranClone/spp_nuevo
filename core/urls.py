from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Carga_sv

urlpatterns = [
    path('', Carga_sv.as_view(), name='carga_servidor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
