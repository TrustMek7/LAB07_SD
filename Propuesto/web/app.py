from flask import Flask, render_template, request, redirect, url_for
from zeep import Client

app = Flask(__name__)
client = Client("http://127.0.0.1:8000/?wsdl")

def dict_to_obj(d):
    # Convierte un dict a un objeto con atributos
    class Obj: pass
    o = Obj()
    for k, v in d.items():
        setattr(o, k, v)
    return o

def fix_items(items):
    # Convierte cada item a objeto si es dict
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append(dict_to_obj(item))
        else:
            result.append(item)
    return result

@app.route("/")
def index():
    productos = client.service.getProductos()
    if productos is None:
        productos = []
    return render_template("index.html", productos=productos)

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    precio = float(request.form["precio"])
    client.service.addProducto(nombre, precio)
    return redirect(url_for("index"))

@app.route("/carrito/<usuario>")
def carrito(usuario):
    carrito_items = client.service.getCarrito(usuario)
    if carrito_items is None:
        carrito_items = []
    else:
        carrito_items = fix_items(carrito_items)
    productos = client.service.getProductos()
    if productos is None:
        productos = []
    return render_template("carrito.html", usuario=usuario, carrito=carrito_items, productos=productos)

@app.route("/carrito/<usuario>/add", methods=["POST"])
def add_carrito(usuario):
    producto_id = int(request.form["producto_id"])
    cantidad = int(request.form["cantidad"])
    client.service.crearCarrito(usuario)
    client.service.addAlCarrito(usuario, producto_id, cantidad)
    return redirect(url_for("carrito", usuario=usuario))

@app.route("/comprar/<usuario>")
def comprar(usuario):
    compra = client.service.comprar(usuario)
    if not hasattr(compra, "productos") or compra.productos is None:
        compra.productos = []
    else:
        compra.productos = fix_items(compra.productos)
    productos = client.service.getProductos()
    if productos is None:
        productos = []
    return render_template("compra.html", compra=compra, productos=productos)

@app.route("/historial/<usuario>")
def historial(usuario):
    historial = client.service.getHistorialCompras(usuario)
    if historial is None:
        historial = []
    else:
        for c in historial:
            if not hasattr(c, 'productos') or c.productos is None:
                c.productos = []
            else:
                c.productos = fix_items(c.productos)
    productos = client.service.getProductos()
    if productos is None:
        productos = []
    return render_template("historial.html", usuario=usuario, historial=historial, productos=productos)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
