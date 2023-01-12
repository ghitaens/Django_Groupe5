from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.homeemploye_view, name='home_employe'),
    path('ajoutersalle/',views.insert_view,name='ajouter_salle'),
    path('listesalle/',views.view_salle, name="liste_salle"),
    path('reserversalle/',views.search_view,name='reserversalle'),
    path('mesreservations/',views.view_reservation,name='mesreservations'),
    path('form_submit/',views.form_submit,name='form_submit')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)