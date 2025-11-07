import pytest
from main import validar_cliente, validar_hotel, validar_fecha, clientes, hoteles
def test_validar_cliente_existente():
    assert validar_cliente("Juan Perez") == 1

def test_validar_cliente_inexistente():
    assert validar_cliente("Juan sin tierra") == 0

def test_validar_hotel_existente():
    assert validar_hotel("Hotel Sol") == 1

def test_validar_hotel_inexistente():
    assert validar_hotel("Howard Johnsons") == 0


@pytest.mark.parametrize("fecha", [
    "01/01/2024", "29/02/2024", "31/12/2025", "30/04/2023"
])

def test_validar_fecha_valida():
    assert validar_fecha(fecha) == True

@pytest.mark.parametrize("fecha", [
    "32/01/2024", "29/02/2023", "00/05/2024", "15/13/2024", "abcd", "15-05-2024"
])
def test_validar_fecha_invalida(fecha):
    assert validar_fecha(fecha) == False