from inventario.modelos import LineaVenta, ResultadoVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario
from inventario.excepciones import InventarioInsuficiente

class ServicioVentas:
    def __init__(self, inventario: ServicioInventario, repositorio: RepositorioProductos) -> None:
        self.inventario = inventario
        self.repositorio = repositorio

    def registrar_venta(self, linea: LineaVenta) -> ResultadoVenta:
        if linea.cantidad <= 0:
            raise ValueError("La cantidad de venta debe ser mayor a 0")

        # Verifica si hay stock usando el servicio de inventario
        if not self.inventario.validar_inventario(linea.codigo, linea.cantidad):
            raise InventarioInsuficiente(f"Existencias insuficientes para el producto {linea.codigo}")

        # Obtiene datos del producto para calcular el total
        stock_actual = self.inventario.consultar_existencia(linea.codigo)
        total = self.inventario.calcular_total(linea.codigo, linea.cantidad)

        # Descuenta unidades de forma efectiva actualizando el repositorio
        nuevo_stock = stock_actual - linea.cantidad
        self.repositorio.actualizar_existencia(linea.codigo, nuevo_stock)

        return ResultadoVenta(total=total, unidades=linea.cantidad)
