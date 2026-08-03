## Estándar 6: Contexto y tokens

- Paralelizar: las llamadas de herramientas independientes van juntas en un solo
  bloque, nunca secuenciales si no hay dependencia.
- No re-leer archivos ya leídos en la sesión.
- Respuestas concisas: no repetir lo ya mostrado ni resumirle al usuario lo que
  acaba de decir.
- No generar código que no se pidió.
- Búsquedas dirigidas (`Grep`/`Glob`) antes de recurrir a agentes de exploración.
- Leer solo el tramo de archivo que hace falta cuando ya se sabe cuál es.

### Cambiar de tarea o liberar contexto

- **Tarea nueva sin relación con la anterior → `/clear`.** Es lo más barato: no
  resume nada y arranca con el prefijo limpio.
- **Misma tarea sin espacio → `/compact-context` y luego `/compact`.** Compactar
  cuesta un pase de resumen más recalentar todo el prefijo, y pierde detalle: no
  hacerlo "por las dudas".
- **No inferir cuánto contexto queda por el número de turnos.** El uso real lo
  reporta el harness (`/context`); avisar solo con ese dato, nunca con una
  estimación presentada como medición (Estándar 3). `/manage-context` prepara el
  traspaso antes de limpiar o compactar.

Memoria permanente entre sesiones: `.claude/context/`. Actualizarla antes de
compactar o limpiar — es lo único que sobrevive.

<!-- origen: ~/.claude/CLAUDE.md §Manejo de Contexto y Tokens (ADR-0009: quitada la heurística de turnos, que obligaba a afirmar un porcentaje no verificable; añadida la distinción /clear vs /compact) -->
