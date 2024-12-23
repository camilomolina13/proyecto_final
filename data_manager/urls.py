from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_estudiantes, name='listar_estudiantes'),
    path('crear/', views.crear_estudiante, name='crear_estudiante'),
    path('estudiantes/editar/<int:pk>/', views.editar_estudiante, name='editar_estudiante'),
    path('eliminar/<int:pk>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('curso/crear/', views.crear_curso, name='crear_curso'),
    path('curso/editar/<int:pk>/', views.editar_curso, name='editar_curso'),
    path('curso/eliminar/<int:pk>/', views.eliminar_curso, name='eliminar_curso'),
    path('inscripciones/', views.listar_inscripciones, name='listar_inscripciones'),
    path('inscripciones/crear/', views.crear_inscripcion, name='crear_inscripcion'),
    path('inscripciones/editar/<int:pk>/', views.editar_inscripcion, name='editar_inscripcion'),
    path('inscripciones/eliminar/<int:pk>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
    path('exportar_a_mongo/', views.exportar_a_mongo, name='exportar_a_mongo'),
    path('exportar_a_cassandra/', views.exportar_a_cassandra, name='exportar_a_cassandra'),
    path('exportar_datos/', views.exportar_datos_pantalla, name='exportar_datos'),
]
