
#Realizamos la importación de nuestra función de conexión
from bd import obtener_conexion

#Controlador: insertar_juego
def insertar_juego(nombre, descripcion, precio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO juegos(nombre, descripcion, precio) VALUES (%s, %s, %s)",
                       (nombre, descripcion, precio))
    conexion.commit()
    conexion.close()

#Controlador: obtener_juego
def obtener_juegos():
    conexion = obtener_conexion()
    juegos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos")
        juegos = cursor.fetchall()
    conexion.close()
    return juegos
 
# Controlador: obtener juego por ID
def obtener_juego_por_id(id):
    """Obtiene los datos de un juego a partir de su ID."""

    juego = None
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos WHERE id = %s", (id,))
        juego = cursor.fetchone()

    conexion.close()
    return juego

# Controlador: obtener juego por ID
def obtener_juego_por_id(id):
    """Obtiene los datos de un juego a partir de su ID."""

    juego = None
    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio FROM juegos WHERE id = %s", (id,))
        juego = cursor.fetchone()

    conexion.close()
    return juego

# Controlador: actualizar juego
def actualizar_juego(nombre, descripcion, precio, id):
    """Actualiza los datos de un juego dado su ID."""

    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE juegos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
            (nombre, descripcion, precio, id)
        )

    conexion.commit()
    conexion.close()

# Controlador: eliminar juego
def eliminar_juego(id):
    """Elimina un juego a partir de su ID."""

    conexion = obtener_conexion()

    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))

    conexion.commit()
    conexion.close()
