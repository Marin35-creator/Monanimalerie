from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('assign/<int:animal_id>/<int:equipement_id>/', views.assign_animal_to_equipement, name='assign_animal_to_equipement'),
    path('animal/<int:animal_id>/', views.animal_detail, name='animal_detail'),  # Ajout de cette ligne
    path('action_not_allowed/<int:animal_id>/', views.action_not_allowed, name='action_not_allowed'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



