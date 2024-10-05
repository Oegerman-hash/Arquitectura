import requests # Importa la biblioteca requests para hacer peticiones HTTP
def obtener_usuarios():
 # Realiza una petición GET al servidor
 response = requests.get('http://localhost:5000/usuarios')
 if response.status_code == 200: # Si la respuesta es exitosa (código 200)
 usuarios = response.json() # Convierte el cuerpo de la respuesta JSON a un
objeto de Python (lista de diccionarios)
 print("Usuarios encontrados:")
 for usuario in usuarios: # Itera sobre la lista de usuarios y muestra sus datos
 print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
 else:
 print("Error al obtener usuarios") # Muestra un mensaje de error si la solicitud
falla
if __name__ == '__main__':
 obtener_usuarios() # Ejecuta la función al iniciar el script
