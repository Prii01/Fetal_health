from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('detect_fetal_health/',views.predict_fetal_health,name='detect_fetal_health'),
    path('view_fetal_health_data/',views.view_fetal_health_data,name='view_fetal_health_data'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
