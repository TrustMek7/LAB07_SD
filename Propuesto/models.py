from spyne import ComplexModel, Unicode, Integer, Float, Array

class Producto(ComplexModel):
    id = Integer
    nombre = Unicode
    precio = Float


