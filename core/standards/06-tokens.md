## Estándar 6: Manejo de Contexto y Tokens

Claude DEBE seguir estas reglas en TODAS las sesiones:

### Reglas de eficiencia de tokens

1. **Paralelizar siempre** — llamadas de herramientas independientes deben ir juntas en un solo bloque, nunca secuenciales si no hay dependencia
2. **No re-leer archivos** — si un archivo ya fue leído en la sesión, no volver a leerlo; usar el contenido ya conocido
3. **Respuestas concisas** — no repetir información ya mostrada, no resumir lo que el usuario acaba de decir
4. **No generar código innecesario** — solo escribir lo que se pidió, sin extras no solicitados
5. **Búsquedas dirigidas** — usar Grep/Glob específicos antes de recurrir a agentes de exploración

### Alertas proactivas de contexto

Claude DEBE advertir al usuario cuando detecte que el contexto está por llenarse:

- Sesión con más de 20 turnos de mensajes → avisar con `⚠️ Contexto al 60%+`
- Sesión con mucho código leído/generado → avisar con `⚠️ Considera /compact-context`
- Antes de tareas largas → sugerir `/compact` si la sesión ya es extensa

### Cuándo compactar

- **Siempre antes** de cambiar a una tarea completamente distinta
- **Siempre antes** de iniciar un ticket nuevo si la sesión lleva más de 15 turnos
- **Nunca esperar** a que Claude Code compacte automáticamente — hacerlo manual es más eficiente
- Usar `/manage-context` para evaluar el estado antes de decidir

### Memoria persistente

Los archivos `.claude/context/` dentro de cada proyecto son la memoria permanente.
Siempre actualizarlos antes de compactar para no perder conocimiento entre sesiones.

<!-- origen: ~/.claude/CLAUDE.md §Manejo de Contexto y Tokens -->
