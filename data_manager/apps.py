from cassandra.cqlengine.connection import setup
from django.apps import AppConfig


class DataManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_manager'

    def ready(self):
        # Configura la conexión con Cassandra
        setup(
            hosts=['127.0.0.1'],  # Cambia por la IP o dominio de tu servidor Cassandra
            default_keyspace='proyecto_final_db'
        )
