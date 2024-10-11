import requests


# URL del servidor
BASE_URL = 'http://localhost:5000/usuarios'

# Función para obtener todos los usuarios
def obtener_usuarios():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        usuarios = response.json()
        print("Usuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios:", response.text)

# Función para crear un nuevo usuario
def crear_usuario(nuevo_usuario):
    response = requests.post(BASE_URL, json=nuevo_usuario)
    if response.status_code == 201:
        print("Usuario creado:", response.json())
    else:
        print("Error al crear usuario:", response.text)

# Función para obtener un usuario por ID
def obtener_usuario_por_id(usuario_id):
    response = requests.get(f"{BASE_URL}/{usuario_id}")
    if response.status_code == 200:
        usuario = response.json()
        print(f"Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuario:", response.text)

# Función para eliminar un usuario por ID
def eliminar_usuario(usuario_id):
    response = requests.delete(f"{BASE_URL}/{usuario_id}")
    if response.status_code == 204:
        print("Usuario eliminado.")
    else:
        print("Error al eliminar usuario:", response.text)

if __name__ == '__main__':
    # Ejemplo de uso
    obtener_usuarios()  # Obtener todos los usuarios

    # Crear un nuevo usuario
    nuevo_usuario = {"id": 3, "nombre": "Pedro"}
    crear_usuario(nuevo_usuario)

    # Obtener un usuario por ID
    obtener_usuario_por_id(1)

    # Eliminar un usuario por ID
    eliminar_usuario(2)

    # Obtener todos los usuarios nuevamente para ver los cambios
    obtener_usuarios()
