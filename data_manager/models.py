from django.db import models
from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from datetime import datetime

# Modelo Estudiante
class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    email = models.EmailField(default='default@example.com')

    def __str__(self):
        return self.nombre

# Modelo Curso
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo Inscripcion
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.nombre} inscrito en {self.curso.nombre}"

class EstudianteMongo(Document):
    nombre = StringField(max_length=100)
    edad = IntField()
    email = StringField()

    def __str__(self):
        return self.nombre

# Modelo CursoMongo
class CursoMongo(Document):
    nombre = StringField(max_length=100)
    descripcion = StringField()

    def __str__(self):
        return self.nombre

# Modelo InscripcionMongo
class InscripcionMongo(Document):
    estudiante = ReferenceField(EstudianteMongo)
    curso = ReferenceField(CursoMongo)
    fecha_inscripcion = DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.estudiante.nombre} inscrito en {self.curso.nombre}"
    
class EstudianteCassandra(Model):
    __keyspace__ = 'proyecto_final_db'
    id = columns.UUID(primary_key=True)
    nombre = columns.Text()  # Añadir 'nombre' como parte de la clave primaria
    edad = columns.Integer()
    email = columns.Text()

class CursoCassandra(Model):
    __keyspace__ = 'proyecto_final_db'
    id = columns.UUID(primary_key=True)
    nombre = columns.Text()
    descripcion = columns.Text()

class InscripcionCassandra(Model):
    __keyspace__ = 'proyecto_final_db'
    id = columns.UUID(primary_key=True)
    estudiante_id = columns.UUID()
    curso_id = columns.UUID()
    fecha_inscripcion = columns.Date()
