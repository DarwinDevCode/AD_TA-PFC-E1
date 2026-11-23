from dataclasses import dataclass
from enum import Enum

import httpx


class TipoRespuesta(str, Enum):
    RESULTADO = "RESULTADO"
    SIN_REGISTRO = "SIN_REGISTRO"
    NO_DISPONIBLE = "NO_DISPONIBLE"


@dataclass
class RespuestaElegibilidad:
    tipo: TipoRespuesta
    cuerpo: dict | None = None


class ClienteElegibilidad:
    """Cliente de la interacción I-05 según src/contrato/elegibilidad-v1.yaml."""

    def __init__(self, url_base: str, tiempo_espera: float, transporte: httpx.BaseTransport | None = None):
        self._cliente = httpx.Client(base_url=url_base, timeout=tiempo_espera, transport=transporte)

    def consultar(self, estudiante_id: str, asignatura: str) -> RespuestaElegibilidad:
        try:
            respuesta = self._cliente.get(
                f"/estudiantes/{estudiante_id}/elegibilidad", params={"asignatura": asignatura}
            )
        except httpx.TransportError:
            return RespuestaElegibilidad(TipoRespuesta.NO_DISPONIBLE)

        if respuesta.status_code == 200:
            return RespuestaElegibilidad(TipoRespuesta.RESULTADO, respuesta.json())
        if respuesta.status_code == 404:
            return RespuestaElegibilidad(TipoRespuesta.SIN_REGISTRO, respuesta.json())
        if respuesta.status_code == 400:
            raise ValueError(respuesta.json().get("mensaje", "Solicitud inválida"))
        return RespuestaElegibilidad(TipoRespuesta.NO_DISPONIBLE)

    def cerrar(self) -> None:
        self._cliente.close()
