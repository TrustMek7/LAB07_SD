
from zeep import Client

wsdl = 'http://127.0.0.1:8000/?wsdl'
client = Client(wsdl=wsdl)

print("Lista de usuarios inicial:")
for user in client.service.getUsers():
    print(f"{user.name} {user.username}")

print("\nAgregando usuario nuevo:")
client.service.addUser({"name": "Pablo", "username": "Ruiz"})

print("\nLista actualizada de usuarios:")
for user in client.service.getUsers():
    print(f"{user.name} {user.username}")
