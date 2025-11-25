# Changelog – Cálculo de Nocturnidad TITSA

Todas las modificaciones relevantes del proyecto se documentan aquí para asegurar trazabilidad y reproducibilidad.

---

## [v1.0.0] – 23 Noviembre 2025
### Estado estable recuperado
- **Parser (`parser.py`)**
  - Lectura de PDFs con `pdfplumber`.
  - Extracción de columnas fijas: `Fecha [0]`, `HI [15]`, `HF [16]`.
  - Soporte para múltiples horas en HI/HF:
    - Tramo principal = HI superior + HF inferior.
    - Tramo secundario = HI inferior + HF superior.
  - Herencia de fecha en filas partidas.

- **Cálculo (`nocturnidad.py`)**
  - Tramos oficiales: 22–23:59, 00–00:59, 04–06.
  - Tarifa aplicada:
    - 0.05 €/min hasta 25 abril 2025.
    - 0.062 €/min desde 26 abril 2025.
  - Filtrado de horas inválidas (>23h).

- **Agregador (`aggregator.py`)**
  - Resumen mensual: minutos, importe y días con nocturnidad.
  - Resumen global: totales acumulados.

- **Exportador (`pdf_export.py`)**
  - Informe PDF con:
    - Cabecera (empleado, nombre).
    - Tabla detalle (solo tramos principales).
    - Tabla resumen mensual.
    - Tabla resumen global.
  - Estilos básicos con `reportlab`.

- **Frontend**
  - `index.html`: formulario de subida con campos de empleado y nombre.
  - `result.html`: visualización de detalle, resumen mensual y global.
  - `styles.css`: estilos básicos para tablas y formulario.

- **Infraestructura**
  - `requirements.txt` con dependencias estables:
    - Flask, pdfplumber, reportlab, gunicorn.
  - Despliegue en Render con `gunicorn app:app`.

---

## [v1.0.1] – (Pendiente)
### Próximas mejoras previstas
- Añadir logo TITSA y pie legal al informe PDF.
- Automatizar copia de informes en carpeta de respaldo.
- Documentación breve para conductores (manual de uso básico).