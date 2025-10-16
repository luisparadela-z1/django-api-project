from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tarea
from .serializers import TareaSerializer

class TareaListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todas las tareas y crear nuevas tareas
    GET /api/tareas/ - Lista todas las tareas
    POST /api/tareas/ - Crea una nueva tarea
    """
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

class TareaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar o eliminar una tarea específica
    GET /api/tareas/{id}/ - Obtiene una tarea
    PUT /api/tareas/{id}/ - Actualiza una tarea
    DELETE /api/tareas/{id}/ - Elimina una tarea
    """
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

@api_view(['GET'])
def tareas_completadas(request):
    """
    Vista para obtener solo las tareas completadas
    GET /api/tareas/completadas/
    """
    tareas = Tarea.objects.filter(completada=True)
    serializer = TareaSerializer(tareas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tareas_pendientes(request):
    """
    Vista para obtener solo las tareas pendientes
    GET /api/tareas/pendientes/
    """
    tareas = Tarea.objects.filter(completada=False)
    serializer = TareaSerializer(tareas, many=True)
    return Response(serializer.data)
