import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# Matrícula, nota, promedio del estudiante y promedio de la carrera.
REGISTROS = {
    "EST-001": ("REGULAR", 9.25, 8.70, 8.20),
    "EST-002": ("REGULAR", 8.00, 8.01, 8.00),
    "EST-003": ("REGULAR", 7.99, 8.70, 8.20),
    "EST-004": ("REGULAR", 9.25, 8.20, 8.20),
    "EST-005": ("REGULAR", 9.25, 8.19, 8.20),
    "EST-006": ("NO_REGULAR", 9.25, 8.70, 8.20),
    "EST-007": ("NO_REGULAR", 7.99, 8.20, 8.20),
    "EST-008": ("REGULAR", None, 8.70, 8.20),
    "EST-009": ("NO_REGULAR", None, 8.70, 8.20),
}
ASIGNATURA = "ASIG-01"
logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="SGA simulado", openapi_url=None)


@app.middleware("http")
async def registrar_solicitud(request: Request, call_next):
    logger.info("SGA simulado: %s %s", request.method, request.url.path)
    return await call_next(request)


@app.get(
    "/api/v1/estudiantes/{estudianteId}/registro-academico",
    operation_id="consultarRegistroAcademico",
)
async def consultar_registro(estudianteId: str, asignatura: str):
    if estudianteId not in REGISTROS:
        return JSONResponse(
            status_code=404,
            content={
                "codigo": "ESTUDIANTE_NO_ENCONTRADO",
                "mensaje": "No existe registro académico del estudiante.",
            },
        )

    matricula, nota, promedio, promedio_carrera = REGISTROS[estudianteId]
    return {
        "estudianteId": estudianteId,
        "asignatura": asignatura,
        "matricula": matricula,
        "nota": nota if asignatura == ASIGNATURA else None,
        "promedio": promedio,
        "promedioCarrera": promedio_carrera,
    }
