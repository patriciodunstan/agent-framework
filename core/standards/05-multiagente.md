## Estándar 5: Estrategia Multi-Agente

### Por qué usar subagentes

Los subagentes **protegen el contexto principal** de la sesión. Cada vez que Claude lee muchos archivos o genera código largo, consume tokens del contexto que no se recuperan. Un `Explore` agent puede leer 50 archivos sin contaminar la sesión principal.

### Cuándo usar cada tipo de agente

| Caso | Agente | Razón |
|------|--------|-------|
| Explorar codebase (>3 archivos) | `Explore` | Aísla lecturas masivas del contexto principal |
| Diseñar arquitectura o plan | `Plan` | Razonamiento profundo sin contaminar el contexto |
| Búsquedas amplias (keywords, patrones) | `Explore` | Más eficiente que múltiples Grep manuales |
| Tareas paralelas independientes | `general-purpose` | Paralelización real; lanzar en background |
| Preguntas sobre Claude Code/API | `claude-code-guide` | Especializado, no usa tokens del contexto principal |

### Reglas de uso de agentes

1. **Delegar exploración siempre** — Si necesito leer más de 3 archivos para entender algo, usar `Explore` en lugar de leer directamente.
2. **Paralelizar cuando sea posible** — Lanzar múltiples agentes en un solo mensaje si las tareas son independientes.
3. **No duplicar trabajo** — Si un agente ya investigó algo, usar su resultado directamente.
4. **Handoff de contexto explícito** — Al delegar, incluir en el prompt: archivos clave, decisiones ya tomadas, restricciones del proyecto.

### Patrón para tareas complejas

```
Tarea compleja (>5 archivos o >30 min estimado):

1. Explore agent  → mapear el codebase relevante
2. Plan agent     → diseñar la solución con el mapa
3. Claude principal → implementar con el plan validado
4. Explore agent  → verificar coherencia de los cambios
```

<!-- origen: ~/.claude/CLAUDE.md §Estrategia Multi-Agente -->
