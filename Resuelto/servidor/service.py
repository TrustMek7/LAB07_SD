
from spyne import ServiceBase, rpc, Iterable
from .models import User

user_list = [
    User(name="Rosa", username="Marfil"),
    User(name="Pepito", username="Grillo"),
    User(name="Manuela", username="Río")
]

class UserService(ServiceBase):

    @rpc(_returns=Iterable(User))
    def getUsers(ctx):
        return user_list

    @rpc(User, _returns=str)
    def addUser(ctx, user):
        user_list.append(user)
        return "Usuario añadido correctamente"
