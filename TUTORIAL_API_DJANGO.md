# Tutorial Completo: API Django REST Framework - TODO List

## Índice
1. [Configuración Inicial de GitHub](#1-configuración-inicial-de-github)
2. [Creación del Proyecto Django](#2-creación-del-proyecto-django)
3. [Configuración del Entorno Virtual](#3-configuración-del-entorno-virtual)
4. [Instalación de Dependencias](#4-instalación-de-dependencias)
5. [Creación de la App Tareas](#5-creación-de-la-app-tareas)
6. [Implementación del Modelo](#6-implementación-del-modelo)
7. [Creación del Serializador](#7-creación-del-serializador)
8. [Implementación de las Vistas API](#8-implementación-de-las-vistas-api)
9. [Configuración de URLs](#9-configuración-de-urls)
10. [Configuración de Settings](#10-configuración-de-settings)
11. [Migraciones de Base de Datos](#11-migraciones-de-base-de-datos)
12. [Control de Versiones con Git](#12-control-de-versiones-con-git)
13. [Ejecución y Pruebas](#13-ejecución-y-pruebas)

---

## 1. Configuración Inicial de GitHub

### 1.1 Crear Token de Acceso Personal (PAT)

1. **Ir a GitHub.com** y hacer login
2. **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token** → **Generate new token (classic)**
4. **Configurar el token:**
   - **Note**: "Django API Project - Desarrollo Local"
   - **Expiration**: 90 days (o según preferencia)
   - **Scopes**: Seleccionar `repo` (acceso completo a repositorios)
5. **Generate token** y **copiar el token** (se muestra solo una vez)

### 1.2 Crear Repositorio en GitHub

1. **New repository** en GitHub
2. **Repository name**: `django-api-project`
3. **Description**: "API REST con Django para gestión de tareas"
4. **Visibility**: Private (recomendado para proyectos de aprendizaje)
5. **Initialize**: NO marcar ninguna opción (crearemos el proyecto localmente)
6. **Create repository**

### 1.3 Clonar Repositorio (si se creó con README)

```bash
git clone https://github.com/tu-usuario/django-api-project.git
cd django-api-project
```

O si se creó vacío, inicializar Git:

```bash
git init
git remote add origin https://ghp_TU_TOKEN@github.com/tu-usuario/django-api-project.git
```

---

## 2. Creación del Proyecto Django

### 2.1 Crear el Proyecto Principal

```bash
# Activar entorno virtual (si ya existe)
source venv/bin/activate

# Crear proyecto Django
django-admin startproject mi_api .

# Verificar estructura
ls -la
```

**Estructura resultante:**
```
django-api-project/
├── manage.py
├── mi_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── venv/
```

### 2.2 Verificar Instalación

```bash
python manage.py runserver
# Abrir http://127.0.0.1:8000/ en el navegador
# Debería mostrar la página de bienvenida de Django
```

---

## 3. Configuración del Entorno Virtual

### 3.1 Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate
```

### 3.2 Verificar Activación

```bash
# El prompt debería mostrar (venv) al inicio
which python
# Debería apuntar a venv/bin/python
```

---

## 4. Instalación de Dependencias

### 4.1 Crear requirements.txt

```bash
# Crear archivo de dependencias
touch requirements.txt
```

**Contenido de requirements.txt:**
```
Django==5.2.7
djangorestframework==3.15.2
django-cors-headers==4.3.1
```

### 4.2 Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

---

## 5. Creación de la App Tareas

### 5.1 Crear la App

```bash
# Crear app dentro del proyecto
python manage.py startapp tareas

# Verificar estructura
ls -la tareas/
```

**Estructura de la app:**
```
tareas/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
└── migrations/
    └── __init__.py
```

---

## 6. Implementación del Modelo

### 6.1 Crear Modelo Tarea

**Archivo: `tareas/models.py`**

```python
from django.db import models
from django.utils import timezone

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
    
    def __str__(self):
        return self.titulo
```

### 6.2 Explicación del Modelo

- **`titulo`**: Campo de texto corto (máximo 200 caracteres)
- **`descripcion`**: Campo de texto largo, opcional
- **`completada`**: Campo booleano, por defecto False
- **`fecha_creacion`**: Se establece automáticamente al crear
- **`fecha_actualizacion`**: Se actualiza automáticamente al modificar
- **`Meta.ordering`**: Ordena por fecha de creación descendente
- **`__str__`**: Representación legible del objeto

---

## 7. Creación del Serializador

### 7.1 Crear Archivo serializers.py

**Archivo: `tareas/serializers.py`**

```python
from rest_framework import serializers
from .models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'completada', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
```

### 7.2 Explicación del Serializador

- **`ModelSerializer`**: Serializador automático basado en el modelo
- **`fields`**: Campos que se incluyen en la serialización
- **`read_only_fields`**: Campos que no se pueden modificar via API
- **Funcionalidad**: Convierte objetos Python ↔ JSON automáticamente

---

## 8. Implementación de las Vistas API

### 8.1 Vistas con Django REST Framework

**Archivo: `tareas/views.py`**

```python
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
```

### 8.2 Explicación de las Vistas

- **`ListCreateAPIView`**: Maneja GET (listar) y POST (crear)
- **`RetrieveUpdateDestroyAPIView`**: Maneja GET (obtener), PUT (actualizar), DELETE (eliminar)
- **`@api_view`**: Decorador para vistas basadas en funciones
- **`Response`**: Respuesta JSON automática
- **`filter()`**: Filtrado de consultas a la base de datos

---

## 9. Configuración de URLs

### 9.1 URLs de la App

**Archivo: `tareas/urls.py`**

```python
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
```

### 9.2 URLs del Proyecto Principal

**Archivo: `mi_api/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tareas/', include('tareas.urls')),
]
```

### 9.3 Endpoints Resultantes

- `GET /api/tareas/` - Lista todas las tareas
- `POST /api/tareas/` - Crea una nueva tarea
- `GET /api/tareas/{id}/` - Obtiene una tarea específica
- `PUT /api/tareas/{id}/` - Actualiza una tarea
- `DELETE /api/tareas/{id}/` - Elimina una tarea
- `GET /api/tareas/completadas/` - Solo tareas completadas
- `GET /api/tareas/pendientes/` - Solo tareas pendientes

---

## 10. Configuración de Settings

### 10.1 Agregar Apps a INSTALLED_APPS

**Archivo: `mi_api/settings.py`**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'tareas',          # Nuestra app
]
```

### 10.2 Configuración de Django REST Framework (Opcional)

```python
# Al final del archivo settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
```

---

## 11. Migraciones de Base de Datos

### 11.1 Crear Migraciones

```bash
# Crear archivos de migración
python manage.py makemigrations

# Verificar migraciones creadas
ls -la tareas/migrations/
```

### 11.2 Aplicar Migraciones

```bash
# Aplicar migraciones a la base de datos
python manage.py migrate

# Verificar estado de migraciones
python manage.py showmigrations
```

### 11.3 Explicación de Migraciones

- **`makemigrations`**: Crea archivos que describen cambios en modelos
- **`migrate`**: Aplica cambios a la base de datos
- **Archivos generados**: `tareas/migrations/0001_initial.py`
- **Base de datos**: Se crea `db.sqlite3` automáticamente

---

## 12. Control de Versiones con Git

### 12.1 Configuración Inicial

```bash
# Inicializar repositorio (si no existe)
git init

# Agregar repositorio remoto
git remote add origin https://ghp_TU_TOKEN@github.com/tu-usuario/django-api-project.git

# Verificar configuración
git remote -v
```

### 12.2 Primer Commit

```bash
# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Django project setup with REST Framework"

# Subir a GitHub
git push -u origin main
```

### 12.3 Commit de la API

```bash
# Agregar cambios de la API
git add .

# Commit descriptivo
git commit -m "Agregar API de TODO list con Django REST Framework

- Crear modelo Tarea con campos: titulo, descripcion, completada, fechas
- Implementar serializador TareaSerializer
- Crear vistas API: ListCreate, Detail, filtros por completadas/pendientes
- Configurar URLs para endpoints de la API
- Agregar app tareas a INSTALLED_APPS
- Crear y aplicar migraciones de base de datos"

# Subir cambios
git push origin main
```

### 12.4 Buenas Prácticas de Git

- **Commits frecuentes**: Hacer commit después de cada funcionalidad
- **Mensajes descriptivos**: Explicar qué se cambió y por qué
- **Branching**: Usar ramas para nuevas funcionalidades
- **Pull antes de push**: Siempre hacer pull antes de push

---

## 13. Ejecución y Pruebas

### 13.1 Iniciar el Servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor de desarrollo
python manage.py runserver

# El servidor estará disponible en:
# http://127.0.0.1:8000/
```

### 13.2 Probar Endpoints con curl

#### Listar todas las tareas
```bash
curl -X GET http://127.0.0.1:8000/api/tareas/
```

#### Crear una nueva tarea
```bash
curl -X POST http://127.0.0.1:8000/api/tareas/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Aprender Django REST Framework",
    "descripcion": "Completar tutorial de API con Django",
    "completada": false
  }'
```

#### Obtener una tarea específica
```bash
curl -X GET http://127.0.0.1:8000/api/tareas/1/
```

#### Actualizar una tarea
```bash
curl -X PUT http://127.0.0.1:8000/api/tareas/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Aprender Django REST Framework",
    "descripcion": "Completar tutorial de API con Django",
    "completada": true
  }'
```

#### Obtener tareas completadas
```bash
curl -X GET http://127.0.0.1:8000/api/tareas/completadas/
```

#### Obtener tareas pendientes
```bash
curl -X GET http://127.0.0.1:8000/api/tareas/pendientes/
```

#### Eliminar una tarea
```bash
curl -X DELETE http://127.0.0.1:8000/api/tareas/1/
```

### 13.3 Probar con Postman

1. **Instalar Postman** desde https://www.postman.com/
2. **Crear nueva colección**: "Django TODO API"
3. **Configurar requests**:
   - **Method**: GET, POST, PUT, DELETE
   - **URL**: `http://127.0.0.1:8000/api/tareas/`
   - **Headers**: `Content-Type: application/json`
   - **Body**: JSON con datos de la tarea

### 13.4 Interfaz de Administración

```bash
# Crear superusuario
python manage.py createsuperuser

# Acceder a admin
# http://127.0.0.1:8000/admin/
```

**Agregar modelo al admin** (`tareas/admin.py`):
```python
from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'completada', 'fecha_creacion']
    list_filter = ['completada', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
```

---

## 14. Estructura Final del Proyecto

```
django-api-project/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── .gitignore
├── mi_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tareas/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   ├── tests.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
└── venv/
    └── ...
```

---

## 15. Comandos de Resumen

### Comandos de Desarrollo
```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### Comandos de Git
```bash
# Ver estado
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Mensaje descriptivo"

# Subir cambios
git push origin main

# Bajar cambios
git pull origin main
```

---

## 16. Próximos Pasos

### Funcionalidades Adicionales
1. **Autenticación**: JWT, OAuth2
2. **Filtros avanzados**: Búsqueda, ordenamiento
3. **Paginación**: Manejo de grandes cantidades de datos
4. **Validaciones**: Campos requeridos, formatos
5. **Tests**: Pruebas unitarias y de integración
6. **Documentación**: Swagger/OpenAPI
7. **Deploy**: Heroku, AWS, DigitalOcean

### Mejoras de Seguridad
1. **CORS**: Configurar dominios permitidos
2. **Rate Limiting**: Límites de requests
3. **HTTPS**: Certificados SSL
4. **Variables de entorno**: Configuración sensible

---

## 17. Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
# Verificar que el entorno virtual esté activado
which python
# Debería mostrar: /ruta/a/venv/bin/python

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "No module named 'rest_framework'"
```bash
# Instalar Django REST Framework
pip install djangorestframework

# Agregar a INSTALLED_APPS en settings.py
```

### Error: "Table doesn't exist"
```bash
# Aplicar migraciones
python manage.py migrate

# Si persiste, eliminar db.sqlite3 y volver a migrar
rm db.sqlite3
python manage.py migrate
```

### Error de Git: "Authentication failed"
```bash
# Verificar token en la URL
git remote -v

# Actualizar token si es necesario
git remote set-url origin https://ghp_NUEVO_TOKEN@github.com/usuario/repo.git
```

---

## 18. Recursos Adicionales

### Documentación Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Git Documentation](https://git-scm.com/doc)

### Tutoriales Recomendados
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Git Tutorial](https://www.atlassian.com/git/tutorials)

### Herramientas Útiles
- **Postman**: Pruebas de API
- **Django Debug Toolbar**: Debugging
- **Django Extensions**: Comandos adicionales
- **Black**: Formateo de código Python

---

## Conclusión

Este tutorial te ha guiado paso a paso para crear una API REST completa con Django. Has aprendido:

✅ **Configuración de GitHub** con tokens de acceso
✅ **Creación de proyectos Django** desde cero
✅ **Implementación de modelos** y serializadores
✅ **Vistas API** con Django REST Framework
✅ **Configuración de URLs** y routing
✅ **Migraciones de base de datos**
✅ **Control de versiones** con Git
✅ **Pruebas de la API** con diferentes métodos

¡Ahora tienes una base sólida para desarrollar APIs más complejas con Django! 🚀
