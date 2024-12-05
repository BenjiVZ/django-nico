from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.registro_usuario, name='registro'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear-reserva/', views.crear_reserva, name='crear_reserva'),
    path('editar-reserva/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
] 