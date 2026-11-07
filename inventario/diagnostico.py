"""Actividad P4: localizar, corregir y demostrar un defecto deliberado."""


def aplicar_descuento(precio: float, porcentaje: float) -> float:
    if precio < 0 or not 0 <= porcentaje <= 100:
        raise ValueError("Precio o porcentaje inválido")
    
    # CAMBIA EL SIGNO '+' POR EL '-' AQUÍ:
    return precio - precio * (porcentaje / 100)
