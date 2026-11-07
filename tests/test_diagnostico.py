import pytest
from inventario.diagnostico import aplicar_descuento # Ajusta el nombre del archivo según corresponda

def test_aplicar_descuento_falla_por_suma():
    """Demuestra que la función falla al aumentar el precio en lugar de reducirlo."""
    precio_inicial = 100.0
    porcentaje = 10.0
    resultado_esperado = 90.0  # El 10% de 100 es 10; 100 - 10 = 90
    
    resultado_real = aplicar_descuento(precio_inicial, porcentaje)
    
    # Esta aserción fallará en el código original porque devolverá 110.0 en lugar de 90.0
    assert resultado_real == resultado_esperado, f"Error: Devolvió {resultado_real} en vez de {resultado_esperado}"
