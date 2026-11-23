# Servicio B: postulaciones

Registra postulaciones (RF-02), consulta la elegibilidad del estudiante al servicio A mediante la interacción I-05 (RF-03) y permite consultar el estado (RF-05). Si elegibilidad o el SGA no responden, la postulación queda en «Validación pendiente» y se revalida cada 60 s (RNF-04).

Contrato de I-05: [`src/contrato/elegibilidad-v1.yaml`](../contrato/elegibilidad-v1.yaml).

## Requisitos

- Python 3.12 o superior.
- Dependencias fijadas en `requirements.txt` (FastAPI 0.165.0, Uvicorn 0.54.0, HTTPX 0.28.1).

## Instalación

Linux o macOS:

```bash
cd src/servicio-b-postulaciones
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Windows (PowerShell):

```powershell
cd src\servicio-b-postulaciones
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Ejecución

```bash
uvicorn app.main:crear_app --factory --port 8080
```

| Variable | Valor por defecto | Uso |
| --- | --- | --- |
| `ELEGIBILIDAD_URL` | `http://localhost:8081/api/v1` | URL base del servicio A |
| `ELEGIBILIDAD_TIEMPO_ESPERA` | `3` | Segundos de espera por respuesta de elegibilidad |
| `REVALIDACION_SEGUNDOS` | `60` | Intervalo de revalidación de postulaciones pendientes |
| `POSTULACIONES_BD` | `postulaciones.db` | Archivo SQLite de la BD de postulaciones |

## Operaciones

| Método y ruta | Respuesta |
| --- | --- |
| `GET /api/v1/salud` | `200 {"estado":"OK"}` |
| `POST /api/v1/postulaciones` con `{"estudianteId":"EST-001","asignatura":"ASIG-01"}` | `201` con la postulación y el resultado de elegibilidad; `409` si ya existe para esa asignatura; `422` si los identificadores no son válidos |
| `GET /api/v1/postulaciones/{id}` | `200` con el último estado registrado; `404` si no existe |
| `GET /api/v1/postulaciones` | `200` con todas las postulaciones |

Estados de la postulación: `estado` es «Enviada» al registrarse (RF-02). `estadoValidacion` es «Validada» cuando elegibilidad respondió 200, «Sin registro académico» cuando respondió 404, y «Validación pendiente» ante 503, tiempo agotado o conexión rechazada.

Ejemplo:

```bash
curl -X POST http://localhost:8080/api/v1/postulaciones \
  -H "Content-Type: application/json" \
  -d '{"estudianteId":"EST-001","asignatura":"ASIG-01"}'
```

## Pruebas

```bash
python -m pytest
```

Las pruebas simulan el servicio A con las respuestas de ejemplo del contrato y cubren los resultados 200, 404 y 503, el tiempo agotado, la conexión rechazada, la revalidación de 20 postulaciones registradas durante una falla, los duplicados y que solo se envían lecturas a elegibilidad.
