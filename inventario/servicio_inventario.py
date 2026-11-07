from decimal import Decimal
from inventario.modelos import Producto
from inventario.repositorio import RepositorioProductos
from inventario.excepciones import ProductoNoEncontrado

class ServicioInventario:
    def __init__(self, repositorio: RepositorioProductos) -> None:
        self.repositorio = repositorio

    def agregar_producto(self, codigo: str, nombre: str, precio: Decimal, existencia: int) -> Producto:
        if not codigo or not nombre:
            raise ValueError("El código y el nombre no pueden estar vacíos")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if existencia < 0:
            raise ValueError("La existencia no puede ser negativa")
        
        try:
            self.repositorio.obtener(codigo)
            raise ValueError(f"El producto con código {codigo} ya existe")
        except ProductoNoEncontrado:
            pass

        nuevo_producto = Producto(codigo=codigo, nombre=nombre, precio=precio, existencia=existencia)
        self.repositorio.guardar(nuevo_producto)
        return nuevo_producto

    def consultar_existencia(self, codigo: str) -> int:
        producto = self.repositorio.obtener(codigo)
        return producto.existencia

    def validar_inventario(self, codigo: str, cantidad: int) -> bool:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        producto = self.repositorio.obtener(codigo)
        return producto.existencia >= cantidad

    def calcular_total(self, codigo: str, cantidad: int) -> Decimal:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        producto = self.repositorio.obtener(codigo)
        return producto.precio * cantidad
