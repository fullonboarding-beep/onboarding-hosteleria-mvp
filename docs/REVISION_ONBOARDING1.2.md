# Revisión de Onboarding1.2

Fecha: 25 de septiembre de 2026.

## Comprobaciones realizadas

- Sintaxis JavaScript con `node --check`.
- Prueba de interacción en DOM simulado (jsdom): apertura de los cinco módulos, respuesta incorrecta y correcta, marcado de práctica, guardado de dudas, cálculo del progreso, recuperación de datos en una nueva carga y reinicio.
- Comprobación de que las notas se mantienen como texto literal.
- Recuperación ante JSON inválido y aviso ante fallo de almacenamiento.
- Rutas relativas compatibles con la carpeta `empleado/`.
- Los archivos de la vista del responsable conservan su contenido.

## Pendiente antes de un piloto real

- Revisión visual en un móvil real y comprobación de vídeo cuando exista material.
- Confirmación de los contenidos y prácticas por el responsable del establecimiento.
- Usuarios, permisos y almacenamiento compartido si se quiere sincronizar empleado y responsable.

No se pudo completar la revisión visual automatizada: la descarga del navegador de prueba falló. La prueba de DOM verifica comportamiento, no dimensiones, renderizado ni usabilidad móvil.
