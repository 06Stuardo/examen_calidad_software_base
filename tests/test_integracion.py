"""Actividad P3: escribir 3 pruebas que integren dos o más componentes.

Flujos requeridos:
1. Alta de producto -> consulta de inventario.
2. Alta -> venta -> descuento de existencias -> total.
3. Alta -> intento de venta insuficiente -> rechazo sin modificar stock.
"""

# TODO P3: implementar 3 pruebas de integración con aserciones.
import pytest
from decimal import Decimal
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario
from inventario.servicio_ventas import ServicioVentas
from inventario.modelos import LineaVenta
from inventario.excepciones import InventarioInsuficiente

# ==============================================================================
# ESCENARIO 1: Integración Completa - Flujo Feliz de Venta
# ==============================================================================
def test_integracion_venta_exitosa_descuenta_stock():
    """Verifica que una venta exitosa calcule el total y actualice el repositorio."""
    # 1. Arrange: Inicializar componentes reales conectados
    repo = RepositorioProductos()
    inventario = ServicioInventario(repo)
    ventas = ServicioVentas(inventario, repo)
    
    inventario.agregar_producto(codigo="PROD-OK", nombre="Martillo", precio=Decimal("15.00"), existencia=10)
    linea = LineaVenta(codigo="PROD-OK", cantidad=3)

    # 2. Act: Registrar la venta
    resultado = ventas.registrar_venta(linea)

    # 3. Assert: Comprobación funcional completa
    assert resultado.total == Decimal("45.00")
    # CAMBIA ESTA LÍNEA AQUÍ:
    assert resultado.unidades == 3  
    assert inventario.consultar_existencia("PROD-OK") == 7


# ==============================================================================
# ESCENARIO 2: Integración Negativa - Bloqueo e Invariabilidad por Falta de Stock
# ==============================================================================
def test_integracion_venta_insuficiente_lanza_excepcion_y_no_modifica_stock():
    """Verifica que si no hay existencias, se lance excepción y el stock no varíe."""
    repo = RepositorioProductos()
    inventario = ServicioInventario(repo)
    ventas = ServicioVentas(inventario, repo)
    
    inventario.agregar_producto(codigo="PROD-ERR", nombre="Tornillo", precio=Decimal("1.50"), existencia=5)
    linea_excesiva = LineaVenta(codigo="PROD-ERR", cantidad=6)

    # Act & Assert: Debe lanzar la excepción y no tocar el inventario
    with pytest.raises(InventarioInsuficiente):
        ventas.registrar_venta(linea_excesiva)
        
    assert inventario.consultar_existencia("PROD-ERR") == 5, "El stock debió mantenerse intacto en 5 ante el fallo"


# ==============================================================================
# ESCENARIO 3: Integración Límite - Venta de Todo el Inventario Disponible
# ==============================================================================
def test_integracion_venta_limite_exacto_deja_inventario_en_cero():
    """Valida la integridad del flujo vendiendo el stock máximo exacto del almacén."""
    repo = RepositorioProductos()
    inventario = ServicioInventario(repo)
    ventas = ServicioVentas(inventario, repo)
    
    inventario.agregar_producto(codigo="PROD-LIM", nombre="Clavos", precio=Decimal("0.50"), existencia=20)
    linea_limite = LineaVenta(codigo="PROD-LIM", cantidad=20)

    # Act
    resultado = ventas.registrar_venta(linea_limite)

    # Assert
    assert resultado.total == Decimal("10.00")
    assert inventario.consultar_existencia("PROD-LIM") == 0, "El inventario debió quedar exactamente en cero sin errores"
