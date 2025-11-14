import pytest
from datetime import datetime

# Ajuste de sys.path para imports de src
import os, sys
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)

from src.gestion_clientes import actualizar_cliente
from src.gestion_hoteles import actualizar_hotel
from src.gestion_reservas import actualizar_reserva


@pytest.fixture
def data_sample():
    hoteles = [
        {
            "id": 1,
            "nombre": "Hotel Sol",
            "ubicacion": "Ciudad",
            "habitaciones": [
                {"numero": 101, "capacidad": 2, "precio": 100.0},
                {"numero": 102, "capacidad": 2, "precio": 110.0},
            ],
        },
        {
            "id": 2,
            "nombre": "Hotel Mar",
            "ubicacion": "Playa",
            "habitaciones": [
                {"numero": 201, "capacidad": 3, "precio": 150.0},
            ],
        },
    ]
    clientes = [
        {"id": 1, "nombre": "Juan Perez", "dni": "12345678", "telefono": "111"},
        {"id": 2, "nombre": "Ana Gomez", "dni": "87654321", "telefono": "222"},
    ]
    reservas = [
        {
            "id": 1,
            "id_cliente": 1,
            "id_hotel": 1,
            "numero_habitacion": 101,
            "fecha_inicio": "2024-01-10",
            "fecha_fin": "2024-01-15",
        },
        {
            "id": 2,
            "id_cliente": 2,
            "id_hotel": 1,
            "numero_habitacion": 102,
            "fecha_inicio": "2024-01-12",
            "fecha_fin": "2024-01-14",
        },
    ]
    return hoteles, clientes, reservas


def test_actualizar_cliente_nombre_y_dni(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = actualizar_cliente(
        clientes, 1, hoteles=hoteles, reservas=reservas, nombre="Juan P.", dni="11223344"
    )
    assert ok is True
    assert clientes[0]["nombre"] == "Juan P."
    assert clientes[0]["dni"] == "11223344"


def test_actualizar_cliente_dni_duplicado_falla(data_sample):
    hoteles, clientes, reservas = data_sample
    # intenta poner el DNI del cliente 2 en el cliente 1
    ok = actualizar_cliente(
        clientes, 1, hoteles=hoteles, reservas=reservas, dni=clientes[1]["dni"]
    )
    assert ok is False


def test_actualizar_hotel_nombre(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = actualizar_hotel(hoteles, 1, clientes=clientes, reservas=reservas, nombre="Hotel Sol Deluxe")
    assert ok is True
    assert hoteles[0]["nombre"] == "Hotel Sol Deluxe"


def test_actualizar_reserva_cambiar_fechas_sin_solapamiento(data_sample):
    hoteles, clientes, reservas = data_sample
    ok = actualizar_reserva(
        reservas,
        hoteles,
        clientes,
        1,
        fecha_inicio="2024-01-16",
        fecha_fin="2024-01-18",
    )
    assert ok is True
    r = next(r for r in reservas if r["id"] == 1)
    assert r["fecha_inicio"] == "2024-01-16"
    assert r["fecha_fin"] == "2024-01-18"


def test_actualizar_reserva_solapamiento_falla(data_sample):
    hoteles, clientes, reservas = data_sample
    # intentar mover reserva 1 a un rango que se solapa con reserva 2 (misma hab no, pero probemos misma habitación)
    # primero ponela en la hab 102 que tiene otra reserva del 12 al 14
    ok = actualizar_reserva(
        reservas,
        hoteles,
        clientes,
        1,
        numero_habitacion=102,
        fecha_inicio="2024-01-12",
        fecha_fin="2024-01-13",
    )
    assert ok is False
