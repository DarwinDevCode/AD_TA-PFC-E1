import asyncio
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import crear_app
from app.sga_simulado import REGISTROS, app as sga_simulado


BASE = "/api/v1"
CONSULTA = f"{BASE}/estudiantes"
ASIGNATURA = {"asignatura": "ASIG-01"}


@pytest.fixture
def cliente():
    transporte = httpx.ASGITransport(app=sga_simulado)
    with TestClient(crear_app(transporte=transporte)) as session:
        yield session


def comprobar_fecha(cuerpo):
    fecha = datetime.fromisoformat(cuerpo["fechaConsulta"])
    assert fecha.utcoffset() == timedelta(0)


def consultar(cliente, estudiante="EST-001", params=ASIGNATURA):
    return cliente.get(f"{CONSULTA}/{estudiante}/elegibilidad", params=params)


def comprobar_error(respuesta, estado, codigo):
    assert respuesta.status_code == estado
    cuerpo = respuesta.json()
    assert set(cuerpo) == {"codigo", "mensaje", "fechaConsulta"}
    assert cuerpo["codigo"] == codigo
    assert cuerpo["mensaje"]
    comprobar_fecha(cuerpo)


def test_salud_sin_acceso_al_sga():
    async def acceso_inesperado(request):
        pytest.fail("La operación de salud consultó el SGA")

    with TestClient(crear_app(transporte=httpx.MockTransport(acceso_inesperado))) as cliente:
        respuesta = cliente.get(f"{BASE}/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "OK"}


def test_ejemplos_200_del_contrato(cliente):
    path = Path(__file__).resolve().parents[2] / "contrato" / "elegibilidad-v1.yaml"
    with path.open(encoding="utf-8") as archivo:
        contrato = yaml.safe_load(archivo)
    operacion = contrato["paths"]["/estudiantes/{estudianteId}/elegibilidad"]["get"]
    ejemplos = operacion["responses"]["200"]["content"]["application/json"]["examples"]

    for ejemplo in ejemplos.values():
        esperado = ejemplo["value"].copy()
        respuesta = consultar(cliente, esperado["estudianteId"])
        assert respuesta.status_code == 200
        cuerpo = respuesta.json()
        comprobar_fecha(cuerpo)
        del cuerpo["fechaConsulta"]
        del esperado["fechaConsulta"]
        assert cuerpo == esperado


@pytest.mark.parametrize(
    ("estudiante", "estado", "resultados"),
    [
        ("EST-005", "NO_ELEGIBLE", ("CUMPLE", "CUMPLE", "NO_CUMPLE")),
        ("EST-007", "NO_ELEGIBLE", ("NO_CUMPLE", "NO_CUMPLE", "NO_CUMPLE")),
        ("EST-009", "NO_ELEGIBLE", ("NO_CUMPLE", "DATO_FALTANTE", "CUMPLE")),
    ],
)
def test_otros_limites_y_precedencia(cliente, estudiante, estado, resultados):
    respuesta = consultar(cliente, estudiante)
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estadoGeneral"] == estado
    assert tuple(
        cuerpo["requisitos"][key]["resultado"] for key in ("matricula", "nota", "promedio")
    ) == resultados


@pytest.mark.parametrize(
    ("estudiante", "params"),
    [
        ("EST-001", {}),
        ("EST-001", {"asignatura": ""}),
        ("EST-001", {"asignatura": "ASIG_01"}),
        ("EST_001", ASIGNATURA),
    ],
)
def test_parametros_invalidos_no_llegan_al_sga(estudiante, params):
    async def acceso_inesperado(request):
        pytest.fail("La consulta inválida llegó al SGA")

    with TestClient(crear_app(transporte=httpx.MockTransport(acceso_inesperado))) as cliente:
        comprobar_error(consultar(cliente, estudiante, params), 400, "PARAMETRO_INVALIDO")


def test_estudiante_sin_registro(cliente):
    comprobar_error(consultar(cliente, "EST-999"), 404, "ESTUDIANTE_NO_ENCONTRADO")


def test_sga_conexion_rechazada():
    async def rechazar(request):
        raise httpx.ConnectError("Conexión rechazada", request=request)

    with TestClient(crear_app(transporte=httpx.MockTransport(rechazar))) as cliente:
        respuesta = consultar(cliente)
    comprobar_error(respuesta, 503, "SGA_NO_DISPONIBLE")
    assert respuesta.headers["Retry-After"] == "60"


def test_sga_demora_y_recuperacion():
    observado = False
    transporte_sga = httpx.ASGITransport(app=sga_simulado)

    async def responder(request):
        nonlocal observado
        if not observado:
            observado = True
            await asyncio.sleep(5)
        return await transporte_sga.handle_async_request(request)

    with TestClient(crear_app(transporte=httpx.MockTransport(responder))) as cliente:
        comprobar_error(consultar(cliente), 503, "SGA_NO_DISPONIBLE")
        recuperada = consultar(cliente)
    assert recuperada.status_code == 200
    assert recuperada.json()["estadoGeneral"] == "ELEGIBLE"


@pytest.mark.parametrize("payload", [{}, {"codigo": "OTRO_ERROR"}])
def test_falla_de_registro_se_distingue_de_inexistencia(payload):
    status = 404 if payload else 200

    async def responder(request):
        return httpx.Response(status, json=payload)

    with TestClient(crear_app(transporte=httpx.MockTransport(responder))) as cliente:
        comprobar_error(consultar(cliente), 503, "SGA_NO_DISPONIBLE")


def test_solo_lectura_del_sga():
    solicitudes = []
    registros_iniciales = REGISTROS.copy()
    transporte_sga = httpx.ASGITransport(app=sga_simulado)

    async def registrar(request):
        solicitudes.append((request.method, request.url.path, dict(request.url.params)))
        return await transporte_sga.handle_async_request(request)

    with TestClient(crear_app(transporte=httpx.MockTransport(registrar))) as cliente:
        assert consultar(cliente).status_code == 200
        assert consultar(cliente, "EST-999").status_code == 404

    assert solicitudes == [
        ("GET", f"{CONSULTA}/EST-001/registro-academico", ASIGNATURA),
        ("GET", f"{CONSULTA}/EST-999/registro-academico", ASIGNATURA),
    ]
    assert REGISTROS == registros_iniciales
