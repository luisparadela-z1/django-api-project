from django.urls import path
from . import views

urlpatterns = [
    # Vista principal para listar y crear tareas
    path('', views.TareaListCreateView.as_view(), name='tarea-list-create'),
    
    # Vista para operaciones específicas de una tarea
    path('<int:pk>/', views.TareaDetailView.as_view(), name='tarea-detail'),
    
    # Vistas especiales para filtrar tareas
    path('completadas/', views.tareas_completadas, name='tareas-completadas'),
    path('pendientes/', views.tareas_pendientes, name='tareas-pendientes'),
]
