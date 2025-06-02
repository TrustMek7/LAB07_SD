
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from .service import UserService

application = Application(
    [UserService],
    tns='spyne.examples.userservice',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('127.0.0.1', 8000, wsgi_app)
    print("Servidor SOAP activo en http://127.0.0.1:8000")
    server.serve_forever()
