import asyncio
import os
import re
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Literal

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, ValidationError


PATRON_IDENTIFICADOR = re.compile(r"[A-Za-z0-9-]{1,20}")
TIEMPO_ESPERA_SGA = 2.0
INTERVALO_REINTENTO = 60
NOTA_MINIMA = 8.00


class RegistroAcademico(BaseModel):
    model_config = ConfigDict(strict=True, allow_inf_nan=False)

    estudianteId: str
    asignatura: str
    matricula: Literal["REGULAR", "NO_REGULAR"] | None
    nota: float | None
    promedio: float | None
    promedioCarrera: float | None


def fecha_consulta() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def error(codigo_http: int, codigo: str, mensaje: str) -> JSONResponse:
    headers = {"Retry-After": str(INTERVALO_REINTENTO)} if codigo_http == 503 else None
    return JSONResponse(
        status_code=codigo_http,
        content={"codigo": codigo, "mensaje": mensaje, "fechaConsulta": fecha_consulta()},
        headers=headers,
    )


def sga_no_disponible() -> JSONResponse:
    return error(503, "SGA_NO_DISPONIBLE", "El SGA no respondió con un registro válido.")


def resultado(cumple: bool | None) -> str:
    if cumple is None:
        return "DATO_FALTANTE"
    return "CUMPLE" if cumple else "NO_CUMPLE"


def evaluar(registro: RegistroAcademico) -> dict:
    matricula = resultado(None if registro.matricula is None else registro.matricula == "REGULAR")
    nota = resultado(None if registro.nota is None else registro.nota >= NOTA_MINIMA)
    promedio = resultado(
        None
        if registro.promedio is None or registro.promedioCarrera is None
        else registro.promedio > registro.promedioCarrera
    )

    resultados = (matricula, nota, promedio)
    if "NO_CUMPLE" in resultados:
        estado = "NO_ELEGIBLE"
    elif "DATO_FALTANTE" in resultados:
        estado = "INCOMPLETO"
    else:
        estado = "ELEGIBLE"

    return {
        "estudianteId": registro.estudianteId,
        "asignatura": registro.asignatura,
        "fechaConsulta": fecha_consulta(),
        "estadoGeneral": estado,
        "requisitos": {
            "matricula": {"resultado": matricula, "valor": registro.matricula},
            "nota": {"resultado": nota, "valor": registro.nota, "minimo": NOTA_MINIMA},
            "promedio": {
                "resultado": promedio,
                "valor": registro.promedio,
                "promedioCarrera": registro.promedioCarrera,
            },
        },
    }


def crear_app(
    url_sga: str | None = None, transporte: httpx.AsyncBaseTransport | None = None
) -> FastAPI:
    base = url_sga or os.getenv("SGA_URL", "http://localhost:8090/api/v1")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with httpx.AsyncClient(
            base_url=base, timeout=TIEMPO_ESPERA_SGA, transport=transporte, trust_env=False
        ) as cliente:
            app.state.sga = cliente
            yield

    app = FastAPI(title="Elegibilidad SGAC", lifespan=lifespan, openapi_url=None)

    @app.get("/api/v1/salud", operation_id="consultarSalud")
    async def consultar_salud():
        return {"estado": "OK"}

    @app.get(
        "/api/v1/estudiantes/{estudianteId}/elegibilidad",
        operation_id="consultarElegibilidad",
    )
    async def consultar_elegibilidad(
        request: Request, estudianteId: str, asignatura: str | None = None
    ):
        for nombre, valor in (("estudianteId", estudianteId), ("asignatura", asignatura)):
            if valor is None or not PATRON_IDENTIFICADOR.fullmatch(valor):
                return error(400, "PARAMETRO_INVALIDO", f"El parámetro {nombre} es obligatorio y debe ser válido.")

        try:
            async with asyncio.timeout(TIEMPO_ESPERA_SGA):
                respuesta = await request.app.state.sga.get(
                    f"/estudiantes/{estudianteId}/registro-academico", params={"asignatura": asignatura}
                )
        except (httpx.RequestError, TimeoutError):
            return sga_no_disponible()

        if respuesta.status_code == 404:
            try:
                cuerpo = respuesta.json()
            except ValueError:
                return sga_no_disponible()
            if isinstance(cuerpo, dict) and cuerpo.get("codigo") == "ESTUDIANTE_NO_ENCONTRADO":
                return error(404, "ESTUDIANTE_NO_ENCONTRADO", "El SGA no tiene registro del estudiante.")
            return sga_no_disponible()
        if respuesta.status_code != 200:
            return sga_no_disponible()

        try:
            registro = RegistroAcademico.model_validate_json(respuesta.content)
        except ValidationError:
            return sga_no_disponible()
        if registro.estudianteId != estudianteId or registro.asignatura != asignatura:
            return sga_no_disponible()
        return evaluar(registro)

    return app
