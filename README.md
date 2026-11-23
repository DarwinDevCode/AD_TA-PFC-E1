# Sistema de Gestión de Ayudantías de Cátedra (SGAC)

**Actividad:** TA-PFC-E1 — Proyecto Fin de Curso de Aplicaciones Distribuidas.

## Descripción del proyecto

El SGAC es una propuesta para gestionar convocatorias, postulaciones, evaluación, seguimiento y certificación de ayudantes de cátedra en la UTEQ. La arquitectura definida en ADR-001 separa servicios por capacidad de negocio. La integración con el SGA se simula con consultas de solo lectura; no se utiliza acceso a registros institucionales reales.

## Integrantes y roles

| Integrante | Rol |
| --- | --- |
| SANCHEZ VERA DARWIN JOEL | Arquitecto |
| MUÑOZ VERA MELANIE MICHELLE | Líder de Desarrollo y Responsable de Calidad (dos roles) |
| QUINTERO RICO LUIS DAVID | Responsable de Documentación |

**Periodo académico:** PENDIENTE DE DEFINIR. Confirmación institucional de los roles: PENDIENTE DE DEFINIR.

## Estructura del repositorio

- `src/`: contratos, servicios y pruebas del esqueleto funcional.
- `docs/`: documento LaTeX, secciones, bibliografía y PDF compilado.
- `docs/adr/`: decisiones arquitectónicas ADR-001 y ADR-002.
- `docs/diagramas/`: archivos editables de los niveles C4.
- `evidencias/`: levantamiento, sesiones de diseño y capturas.
- `BITACORA.md`: registro de sesiones y decisiones reales del equipo.
- `README.md`: orientación para la ejecución y la documentación.

## Ejecución del esqueleto

**PENDIENTE DE COMPLETAR POR MUÑOZ VERA MELANIE MICHELLE:** comandos verificados para instalar dependencias, iniciar los dos servicios y demostrar su comunicación desde un clon limpio. La guía disponible por ahora se limita al servicio B en `src/servicio-b-postulaciones/README.md`.

## Video de presentación

PENDIENTE DE DEFINIR: enlace público al video de 5 a 7 minutos con participación de los tres integrantes y demostración del esqueleto.

## Compilación del documento

- **Compilador:** `pdflatex` y `biber`.
- **Archivo principal:** `docs/main.tex`.
- **Dependencias:** TeX Live o MiKTeX con `pdflatex`, `biber`, `inputenc` UTF-8, `fontenc` T1, `lmodern`, `babel` español, `csquotes`, `geometry`, `graphicx`, `booktabs`, `tabularx`, `longtable`, `hyperref`, `biblatex` y `biblatex-ieee`.

Desde `docs/` ejecutar, en este orden:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

El resultado es `docs/main.pdf`. En MiKTeX, las versiones de `biber` y `biblatex` deben ser compatibles. Para una entrega reproducible, el proceso debe funcionar en un clon limpio y sin referencias sin resolver (`??`).

## Estado de la documentación para E1

El informe se construye en un solo documento LaTeX, desde `docs/main.tex`. El estado del trabajo debe distinguir los archivos ya integrados en `main` de los borradores preparados en ramas de trabajo.

| Entregable | Archivo o ubicación | Situación |
| --- | --- | --- |
| Base documental | `docs/main.tex`, `docs/preambulo.tex`, `docs/main.pdf` | Estructura inicial integrada; el PDF final debe regenerarse tras fusionar cambios. |
| Levantamiento | [`docs/E1-levantamiento-entrevista`](https://github.com/DarwinDevCode/AD_TA-PFC-E1/tree/docs/E1-levantamiento-entrevista/evidencias/levantamiento) | Guion y acta preparados en una rama. Falta contrastar las respuestas, acreditar conformidad y autorización de publicación. |
| Contexto, objetivos y requisitos funcionales | `docs/secciones/02-contexto-problema.tex`, `03-objetivos.tex`, `05-requisitos-funcionales.tex` | Borradores documentales; los requisitos y cifras sin respaldo institucional requieren validación. |
| Presentación y planificación | `docs/secciones/00-portada.tex`, `01-resumen-ejecutivo.tex`, `13-plan-proyecto.tex` | Elaboración y revisión en curso; faltan algunos datos oficiales y el enlace de GitHub Projects. |
| Aportes y uso de IA | `docs/secciones/15-tabla-aportes.tex`, `16-declaracion-ia.tex` | Deben completarse con los enlaces y las declaraciones reales de todos los integrantes. |
| Requisitos no funcionales y riesgos | `docs/secciones/06-requisitos-no-funcionales.tex`, `12-analisis-riesgos.tex` | Responsabilidad de Desarrollo y Calidad; pendiente de integración definitiva. |

Las cifras técnicas de capacidad, respuesta, disponibilidad y recuperación son metas propuestas, no resultados medidos en la UTEQ ni declaraciones verificadas de la entrevista.

## Comprobaciones para el cierre

Antes de entregar E1, verificar la evidencia del levantamiento con el consentimiento requerido, completar las secciones y referencias, ejecutar el esqueleto desde un clon limpio, actualizar la bitácora con sesiones reales, comprobar el PDF compilado y agregar el enlace al video grupal. El PDF de identificación para el SGA debe tener una sola página.

## Organización y trazabilidad

- [Issues del repositorio](https://github.com/DarwinDevCode/AD_TA-PFC-E1/issues).
- [Decisiones de arquitectura](docs/adr/).
- [Documento LaTeX](docs/main.tex).
- [Trabajo de levantamiento](evidencias/levantamiento/): la conformidad de la entrevista debe acreditarse antes de declararlo validado.
- **Tablero GitHub Projects:** PENDIENTE DE DEFINIR.
