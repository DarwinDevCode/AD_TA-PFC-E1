from pathlib import Path

import httpx
import pytest
import yaml
from fastapi.testclient import TestClient

from app.config import Configuracion
from app.elegibilidad import ClienteElegibilidad
from app.main import crear_app
from app.repositorio import RepositorioPostulaciones

CONTRATO = Path(__file__).resolve().parents[2] / "contrato" / "elegibilidad-v1.yaml"
RUTA_ELEGIBILIDAD = "/estudiantes/{estudianteId}/elegibilidad"


def cargar_contrato() -> dict:
    return yaml.safe_load(CONTRATO.read_text(encoding="utf-8"))


class ElegibilidadSimulada:
    """Responde con los ejemplos del contrato; puede simular indisponibilidad del SGA."""

    def __init__(self, contrato: dict):
        respuestas = contrato["paths"][RUTA_ELEGIBILIDAD]["get"]["responses"]
        self.resultados = {
            ejemplo["value"]["estudianteId"]: ejemplo["value"]
            for ejemplo in respuestas["200"]["content"]["application/json"]["examples"].values()
        }
        self.error_404 = respuestas["404"]["content"]["application/json"]["example"]
        self.error_503 = respuestas["503"]["content"]["application/json"]["example"]
        self.modo = "normal"
        self.solicitudes: list[httpx.Request] = []

    def __call__(self, solicitud: httpx.Request) -> httpx.Response:
        self.solicitudes.append(solicitud)
        if self.modo == "sga_no_disponible":
            return httpx.Response(503, json=self.error_503, headers={"Retry-After": "60"})
        if self.modo == "tiempo_agotado":
            raise httpx.ReadTimeout("tiempo agotado", request=solicitud)
        if self.modo == "conexion_rechazada":
            raise httpx.ConnectError("conexión rechazada", request=solicitud)
        estudiante = solicitud.url.path.split("/")[-2]
        if estudiante in self.resultados:
            return httpx.Response(200, json=self.resultados[estudiante])
        return httpx.Response(404, json=self.error_404)


@pytest.fixture
def contrato() -> dict:
    return cargar_contrato()


@pytest.fixture
def elegibilidad(contrato) -> ElegibilidadSimulada:
    return ElegibilidadSimulada(contrato)


@pytest.fixture
def aplicacion(tmp_path, elegibilidad):
    configuracion = Configuracion(elegibilidad_url="http://localhost:8081/api/v1", ruta_bd=str(tmp_path / "p.db"))
    cliente = ClienteElegibilidad(configuracion.elegibilidad_url, 3, transporte=httpx.MockTransport(elegibilidad))
    repositorio = RepositorioPostulaciones(configuracion.ruta_bd)
    app = crear_app(configuracion, cliente, repositorio, revalidacion_automatica=False)
    with TestClient(app) as cliente_http:
        yield cliente_http, app
    repositorio.cerrar()
    cliente.cerrar()
