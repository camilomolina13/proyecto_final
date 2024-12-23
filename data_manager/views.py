from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Estudiante, Curso, Inscripcion, EstudianteMongo, CursoMongo, InscripcionMongo, EstudianteCassandra, CursoCassandra, InscripcionCassandra
from django.contrib import messages
from uuid import uuid4
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
# ==================
# CRUD para Estudiante
# ==================

def listar_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'listar_estudiantes.html', {'estudiantes': estudiantes})

def crear_estudiante(request):
    if request.method == 'POST':
        print(request.POST)  # Depuración
        nombre = request.POST['nombre']
        edad = request.POST['edad']
        email = request.POST['email']
        estudiante = Estudiante(nombre=nombre, edad=edad, email=email)
        estudiante.save()
        return redirect('listar_estudiantes')
    return render(request, 'crear_estudiante.html')

def editar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        estudiante.nombre = request.POST['nombre']
        estudiante.edad = request.POST['edad']
        estudiante.email = request.POST['email']
        estudiante.save()
        return redirect('listar_estudiantes')
    return render(request, 'editar_estudiante.html', {'estudiante': estudiante})

def eliminar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    estudiante.delete()
    return redirect('listar_estudiantes')

# ==================
# CRUD para Curso
# ==================

def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'listar_cursos.html', {'cursos': cursos})

def crear_curso(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        Curso.objects.create(nombre=nombre, descripcion=descripcion)
        return redirect('listar_cursos')
    return render(request, 'crear_curso.html')

def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.nombre = request.POST['nombre']
        curso.descripcion = request.POST['descripcion']
        curso.save()
        return redirect('listar_cursos')
    return render(request, 'editar_curso.html', {'curso': curso})

def eliminar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    curso.delete()
    return redirect('listar_cursos')

# ======================
# Listar Inscripciones
# ======================
def listar_inscripciones(request):
    inscripciones = Inscripcion.objects.select_related('estudiante', 'curso').all()
    return render(request, 'listar_inscripciones.html', {'inscripciones': inscripciones})

# ======================
# Crear Inscripción
# ======================
def crear_inscripcion(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        curso_id = request.POST.get('curso_id')
        
        # Crear la inscripción
        Inscripcion.objects.create(
            estudiante_id=estudiante_id, 
            curso_id=curso_id
        )
        return redirect('listar_inscripciones')

    # Pasar estudiantes y cursos disponibles al template
    estudiantes = Estudiante.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'crear_inscripcion.html', {'estudiantes': estudiantes, 'cursos': cursos})

# ======================
# Editar Inscripción
# ======================
def editar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        curso_id = request.POST.get('curso_id')

        # Actualizar la inscripción
        inscripcion.estudiante_id = estudiante_id
        inscripcion.curso_id = curso_id
        inscripcion.save()
        return redirect('listar_inscripciones')

    # Pasar datos actuales y opciones al template
    estudiantes = Estudiante.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'editar_inscripcion.html', {
        'inscripcion': inscripcion,
        'estudiantes': estudiantes,
        'cursos': cursos
    })

# ======================
# Eliminar Inscripción
# ======================
def eliminar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    inscripcion.delete()
    return redirect('listar_inscripciones')

# Exportar de MySQL a MongoDB
def exportar_a_mongo(request):
    try:
        # Exportar estudiantes
        for estudiante in Estudiante.objects.all():
            EstudianteMongo.objects.create(
                nombre=estudiante.nombre,
                edad=estudiante.edad,
                email=estudiante.email
            )

        # Exportar cursos
        for curso in Curso.objects.all():
            CursoMongo.objects.create(
                nombre=curso.nombre,
                descripcion=curso.descripcion
            )

        # Exportar inscripciones
        for inscripcion in Inscripcion.objects.all():
            estudiante_mongo = EstudianteMongo.objects.get(nombre=inscripcion.estudiante.nombre)
            curso_mongo = CursoMongo.objects.get(nombre=inscripcion.curso.nombre)
            InscripcionMongo.objects.create(
                estudiante=estudiante_mongo,
                curso=curso_mongo,
                fecha_inscripcion=inscripcion.fecha_inscripcion
            )

        return JsonResponse({"mensaje": "Exportación a MongoDB exitosa"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_cassandra_connection():
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()
    return session

# Crear las tablas de Cassandra si no existen
def crear_tablas_cassandra(): 
    session = get_cassandra_connection()

    # Crear el keyspace si no existe
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS proyecto_final_db 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)

    # Usar el keyspace
    session.set_keyspace('proyecto_final_db')

    # Crear la tabla de estudiantes con clave primaria compuesta
    session.execute("""
    CREATE TABLE IF NOT EXISTS estudiante_cassandra (
        id UUID,
        nombre TEXT,
        edad INT,
        email TEXT,
        PRIMARY KEY (id, nombre)
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS curso_cassandra (
        id UUID PRIMARY KEY,
        nombre TEXT,
        descripcion TEXT
    );
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS inscripcion_cassandra (
        id UUID PRIMARY KEY,
        estudiante_id UUID,
        curso_id UUID,
        fecha_inscripcion DATE
    );
    """)

    print("Tablas creadas correctamente.")

def exportar_a_cassandra(request):
    try:
        # Limpia los datos existentes
        for estudiante in EstudianteCassandra.objects.all():
            EstudianteCassandra.objects.filter(id=estudiante.id, nombre=estudiante.nombre).delete()

        for curso in CursoCassandra.objects.all():
            CursoCassandra.objects.filter(id=curso.id).delete()

        for inscripcion in InscripcionCassandra.objects.all():
            InscripcionCassandra.objects.filter(id=inscripcion.id).delete()

        # Exporta los estudiantes
        for estudiante in Estudiante.objects.all():
            print(f"Exportando estudiante: {estudiante.nombre}")
            EstudianteCassandra.create(
                id=uuid4(),
                nombre=estudiante.nombre,
                edad=estudiante.edad,
                email=estudiante.email
            )

        # Exporta los cursos
        for curso in Curso.objects.all():
            print(f"Exportando curso: {curso.nombre}")
            CursoCassandra.create(
                id=uuid4(),
                nombre=curso.nombre,
                descripcion=curso.descripcion
            )

        # Exporta las inscripciones
        for inscripcion in Inscripcion.objects.all():
            estudiante = EstudianteCassandra.objects.filter(nombre=inscripcion.estudiante.nombre).first()
            curso = CursoCassandra.objects.filter(nombre=inscripcion.curso.nombre).first()
            if estudiante and curso:
                print(f"Exportando inscripción para: {inscripcion.estudiante.nombre} en el curso {inscripcion.curso.nombre}")
                InscripcionCassandra.create(
                    id=uuid4(),
                    estudiante_id=estudiante.id,
                    curso_id=curso.id,
                    fecha_inscripcion=inscripcion.fecha_inscripcion
                )
            else:
                print(f"Error: Inscripción no encontrada para {inscripcion.estudiante.nombre} en el curso {inscripcion.curso.nombre}")

        # Mensaje de éxito
        messages.success(request, "Exportación a Cassandra completada con éxito.")
        return JsonResponse({"mensaje": "Exportación a Cassandra completada con éxito."})

    except Exception as e:
        # Loguear detalles del error para depuración
        print(f"Error al exportar a Cassandra: {str(e)}")
        messages.error(request, f"Error al exportar a Cassandra: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


def exportar_datos_pantalla(request):
    return render(request, 'exportar_datos.html')



