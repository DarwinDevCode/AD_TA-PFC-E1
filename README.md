# PFC Aplicaciones Distribuidas, TA-PFC-E1

**Nombre del proyecto:** PENDIENTE DE DEFINIR.

## Descripción del proyecto

PENDIENTE DE DEFINIR.

## Integrantes y roles

| Integrante | Rol propuesto |
| --- | --- |
| SANCHEZ VERA DARWIN JOEL | Arquitecto |
| MUÑOZ VERA MELANIE MICHELLE | Líder de Desarrollo y Responsable de Calidad |
| QUINTERO RICO LUIS DAVID | Responsable de Documentación |

Los roles son propuestas cuya confirmación estaba prevista para el **20 de noviembre de 2026**. La confirmación efectiva está **PENDIENTE DE DEFINIR**. MUÑOZ VERA MELANIE MICHELLE asume **dos roles**: Líder de Desarrollo y Responsable de Calidad.

## Estructura del repositorio

- `/src/`: código fuente y servicios del esqueleto funcional.
- `/docs/`: documento único en LaTeX, secciones y bibliografía.
- `/docs/adr/`: registros de decisiones arquitectónicas.
- `/docs/diagramas/`: diagramas del sistema.
- `/evidencias/`: evidencias del trabajo y de las pruebas.
- `BITACORA.md`: sesiones de trabajo, participantes, decisiones y problemas resueltos.
- `README.md`: información del proyecto y guía de compilación.

## Ejecución del esqueleto

Esta sección la completa MUÑOZ VERA MELANIE MICHELLE cuando existan los servicios.

## Video de presentación

PENDIENTE DE DEFINIR.

## Compilación del documento

- **Compilador:** `pdflatex` con `biber`.
- **Archivo principal:** `docs/main.tex`.
- **Directorio de ejecución:** `docs/`.

Ejecutar los comandos en este orden, desde `docs/`:

```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

**Dependencias:** TeX Live o MiKTeX con `pdflatex`, `biber`, `inputenc` (UTF-8), `fontenc` (T1), `lmodern`, `babel` con español, `csquotes`, `geometry`, `graphicx`, `booktabs`, `tabularx`, `longtable`, `hyperref`, `biblatex` y `biblatex-ieee` (estilo IEEE).

En MiKTeX, las versiones de `biber` y `biblatex` deben ser compatibles.
