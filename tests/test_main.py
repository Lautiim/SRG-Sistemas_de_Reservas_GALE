import pytest
from src.utils import validar_fecha
from src.gestion_hoteles import buscar_hotel_por_id
from src.gestion_clientes import cliente_existente


# Fixtures con datos simples para probar helpers existentes
@pytest.fixture
def hoteles_sample():
    return [
        {"id": 1, "nombre": "Hotel Sol", "ubicacion": "Ciudad", "habitaciones": []},
        {"id": 2, "nombre": "Luna Park", "ubicacion": "Mar", "habitaciones": []},
    ]


@pytest.fixture
def clientes_sample():
    return [
        {"id": 1, "nombre": "Juan Perez", "dni": "12345678", "telefono": "111"},
        {"id": 2, "nombre": "Ana Gomez", "dni": "87654321", "telefono": "222"},
    ]


def test_cliente_existente_true(clientes_sample):
    assert cliente_existente("12345678", clientes_sample) is True


def test_cliente_existente_false(clientes_sample):
    assert cliente_existente("00000000", clientes_sample) is False


def test_buscar_hotel_por_id_existente(hoteles_sample):
    hotel = buscar_hotel_por_id(1, hoteles_sample)
    assert hotel is not None and hotel["nombre"] == "Hotel Sol"


def test_buscar_hotel_por_id_inexistente(hoteles_sample):
    assert buscar_hotel_por_id(99, hoteles_sample) is None


# La función validar_fecha usa formato AAAA-MM-DD (YYYY-MM-DD)
@pytest.mark.parametrize(
    "fecha",
    [
        "2024-01-01",
        "2024-02-29",  # 2024 es bisiesto
        "2025-12-31",
        "2023-04-30",
    ],
)
def test_validar_fecha_valida(fecha):
    assert validar_fecha(fecha) is True


@pytest.mark.parametrize(
    "fecha",
    [
        "2024-01-32",
        "2023-02-29",  # 2023 no es bisiesto
        "2024-05-00",
        "2024-13-15",
        "abcd",
        "15-05-2024",
    ],
)
def test_validar_fecha_invalida(fecha):
    assert validar_fecha(fecha) is False
