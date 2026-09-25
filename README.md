# Onboarding Hostelería

Prototipos para validar la incorporación, formación y evaluación de personal de hostelería.

| Versión | Uso | Entrada |
| --- | --- | --- |
| Onboarding1.1 | Responsable: empleados, observaciones y evaluación | `index.html` |
| Onboarding1.2 | Empleado: lecciones, casos, prácticas, dudas y progreso | `empleado/index.html` |

## Probar en tu ordenador

Descarga el repositorio como ZIP, descomprímelo y abre la entrada correspondiente con Chrome, Safari o Firefox. Conserva `index.html`, `app.js` y `styles.css` juntos en su carpeta.

También se puede servir todo el repositorio con `python3 -m http.server 8000` y entrar en `http://localhost:8000/empleado/`.

## GitHub Pages

El flujo existente `.github/workflows/pages.yml` publica desde `main`. Al integrar esta versión en `main`, la vista del empleado se publicará bajo `/onboarding-hosteleria-mvp/empleado/`. La disponibilidad de la web depende de que la ejecución de GitHub Actions finalice correctamente.

Esta carpeta utiliza rutas relativas y no requiere instalar dependencias ni compilar.

## Alcance de Onboarding1.2

- Cinco hitos alineados con el PDF: días 1, 3, 7, 15 y 30.
- Lección, caso con corrección, registro de práctica supervisada y notas.
- Gráficos sencillos de avance a partir de las actividades realizadas.
- Espacios para vídeos propios, aún sin material audiovisual.
- Avance guardado en el navegador mediante `localStorage`.

Las dos vistas son demostraciones independientes. No hay cuentas, permisos por empleado, envío de dudas ni sincronización entre dispositivos o con el responsable. El progreso del repaso no sustituye la evaluación laboral 1–4.

## Adaptación

Consulta [la guía de la vista del empleado](empleado/README.md) y [las comprobaciones realizadas](docs/REVISION_ONBOARDING1.2.md). Los contenidos son ejemplos genéricos que deben adaptarse a los procedimientos reales del establecimiento.
