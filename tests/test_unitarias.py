import pytest
from inventario.diagnostico import aplicar_descuento # Ajusta el nombre del archivo de origen según corresponda

# ==============================================================================
# PRUEBA 1: Caso Positivo (Cálculo normal del descuento)
# ==============================================================================
def test_aplicar_descuento_normal():
    """Verifica que un descuento estándar reduzca correctamente el precio."""
    precio_inicial = 100.0
    porcentaje = 10.0
    resultado_esperado = 90.0  # 100 - 10 = 90
    
    assert aplicar_descuento(precio_inicial, porcentaje) == resultado_esperado


# ==============================================================================
# PRUEBA 2: Valor Límite Inferior (0% de descuento)
# ==============================================================================
def test_aplicar_descuento_cero_porciento():
    """Verifica que un descuento del 0% mantenga el precio original intacto."""
    precio_inicial = 50.0
    porcentaje = 0.0
    resultado_esperado = 50.0
    
    assert aplicar_descuento(precio_inicial, porcentaje) == resultado_esperado


# ==============================================================================
# PRUEBA 3: Valor Límite Superior (100% de descuento)
# ==============================================================================
def test_aplicar_descuento_cien_porciento():
    """Verifica que un descuento del 100% deje el precio final en cero."""
    precio_inicial = 250.0
    porcentaje = 100.0
    resultado_esperado = 0.0
    
    assert aplicar_descuento(precio_inicial, porcentaje) == resultado_esperado


# ==============================================================================
# PRUEBA 4: Caso Negativo / Excepción (Porcentaje inválido)
# ==============================================================================
def test_aplicar_descuento_porcentaje_invalido_lanza_excepcion():
    """Verifica que un porcentaje fuera de rango (ej. 150%) lance un ValueError."""
    precio_inicial = 100.0
    porcentaje_invalido = 150.0
    
    # Valida que pytest capture correctamente el error esperado según el contrato
    with pytest.raises(ValueError, match="Precio o porcentaje inválido"):
        aplicar_descuento(precio_inicial, porcentaje_invalido)
