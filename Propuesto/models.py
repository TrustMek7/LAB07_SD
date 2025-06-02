from spyne import ComplexModel, Unicode, Integer, Float, Array

class Producto(ComplexModel):
    id = Integer
    nombre = Unicode
    precio = Float

class CarritoItem(ComplexModel):
    producto_id = Integer
    nombre = Unicode
    precio = Float
    cantidad = Integer

class Compra(ComplexModel):
    usuario = Unicode
    total = Float
    productos = Array(CarritoItem)
