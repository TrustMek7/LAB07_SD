from spyne import ServiceBase, rpc, Unicode, Integer, Float, Array
from .models import Producto, CarritoItem, Compra

productos = []
carritos = {}
historial_compras = {}
contador_id = [1]

class TiendaService(ServiceBase):

    @rpc(_returns=Array(Producto))
    def getProductos(ctx):
        print("Llamada a getProductos()")
        print("Productos registrados:")
        for p in productos:
            print(f"ID: {p.id}, Nombre: {p.nombre}, Precio: {p.precio}")
        return productos

    @rpc(Unicode, Float, _returns=Unicode)
    def addProducto(ctx, nombre, precio):
        prod = Producto(id=contador_id[0], nombre=nombre, precio=precio)
        productos.append(prod)
        print(f"Producto agregado: ID={prod.id}, Nombre={prod.nombre}, Precio={prod.precio}")
        contador_id[0] += 1
        return "Producto agregado"

    @rpc(Unicode, _returns=Unicode)
    def crearCarrito(ctx, usuario):
        if usuario not in carritos:
            carritos[usuario] = []
            print(f"Carrito creado para usuario: {usuario}")
        return "Carrito creado"

    @rpc(Unicode, Integer, Integer, _returns=Unicode)
    def addAlCarrito(ctx, usuario, producto_id, cantidad):
        if usuario not in carritos:
            print(f"Intento de agregar al carrito inexistente para usuario: {usuario}")
            return "Carrito no existe"
        prod = next((p for p in productos if p.id == producto_id), None)
        if prod is None:
            print(f"Producto no encontrado: ID={producto_id}")
            return "Producto no existe"
        
        item = CarritoItem(
            producto_id=int(producto_id),
            cantidad=int(cantidad),
            nombre=str(prod.nombre),
            precio=float(prod.precio)
        )
        print(f"Creando CarritoItem: id={item.producto_id}, nombre={item.nombre}, precio={item.precio}, cantidad={item.cantidad}")
        carritos[usuario].append(item)
        print(f"Agregado al carrito de {usuario}: Producto ID={producto_id}, Nombre={prod.nombre}, Precio={prod.precio}, Cantidad={cantidad}")
        return "Producto añadido al carrito"

    @rpc(Unicode, _returns=Array(CarritoItem))
    def getCarrito(ctx, usuario):
        print(f"Llamada a getCarrito() para usuario: {usuario}")
        items = carritos.get(usuario, [])
        print(f"Carrito para {usuario}:")
        result = []
        for item in items:
            # Reconstruye siempre como CarritoItem limpio
            result.append(CarritoItem(
                producto_id=int(getattr(item, 'producto_id', 0)),
                nombre=str(getattr(item, 'nombre', '')),
                precio=float(getattr(item, 'precio', 0)),
                cantidad=int(getattr(item, 'cantidad', 0))
            ))
            print(f"  ID: {getattr(item, 'producto_id', None)}, Nombre: {getattr(item, 'nombre', None)}, Precio: {getattr(item, 'precio', None)}, Cantidad: {getattr(item, 'cantidad', None)}")
        return result

    @rpc(Unicode, _returns=Compra)
    def comprar(ctx, usuario):
        items = carritos.get(usuario, [])
        if not items:
            print(f"Intento de compra con carrito vacío para usuario: {usuario}")
            return Compra(usuario=usuario, total=0.0, productos=[])
        total = 0.0
        clean_items = []
        for item in items:
            total += float(getattr(item, 'precio', 0)) * int(getattr(item, 'cantidad', 0))
            # Reconstruye como CarritoItem limpio
            clean_items.append(CarritoItem(
                producto_id=int(getattr(item, 'producto_id', 0)),
                nombre=str(getattr(item, 'nombre', '')),
                precio=float(getattr(item, 'precio', 0)),
                cantidad=int(getattr(item, 'cantidad', 0))
            ))
        print("Resumen de compra a enviar:")
        for item in clean_items:
            print(f"ID: {item.producto_id}, Nombre: {item.nombre}, Precio: {item.precio}, Cantidad: {item.cantidad}")
        compra = Compra(usuario=usuario, total=total, productos=clean_items)
        historial_compras.setdefault(usuario, []).append(compra)
        carritos[usuario] = []
        print(f"Compra realizada por {usuario}: Total={total}, Items={[(item.producto_id, item.nombre, item.cantidad, item.precio) for item in clean_items]}")
        return compra

    @rpc(Unicode, _returns=Array(Compra))
    def getHistorialCompras(ctx, usuario):
        print(f"Llamada a getHistorialCompras() para usuario: {usuario}")
        historial = historial_compras.get(usuario, [])
        # Reconstruye cada compra y sus productos
        result = []
        for compra in historial:
            clean_items = []
            for item in getattr(compra, 'productos', []):
                clean_items.append(CarritoItem(
                    producto_id=int(getattr(item, 'producto_id', 0)),
                    nombre=str(getattr(item, 'nombre', '')),
                    precio=float(getattr(item, 'precio', 0)),
                    cantidad=int(getattr(item, 'cantidad', 0))
                ))
            result.append(Compra(
                usuario=str(getattr(compra, 'usuario', '')),
                total=float(getattr(compra, 'total', 0)),
                productos=clean_items
            ))
        return result
