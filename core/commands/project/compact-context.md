---
description: Guarda el contexto de la sesión en .claude/context/ antes de compactar — luego indica ejecutar /compact
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

## Contexto actual del repo

- Rama activa: !`git branch --show-current`
- Archivos modificados: !`git status --short`
- Último commit: !`git log --oneline -1`

## Tu tarea

### 1. Revisar qué se aprendió en esta sesión

Identificar información nueva que NO esté ya en `.claude/context/`:
- Nuevos endpoints descubiertos o confirmados
- Comportamientos de servicios que no estaban documentados
- Bugs encontrados y sus causas raíz
- Decisiones de diseño tomadas en esta sesión
- Cambios pendientes de implementar en próximos tickets

### 2. Actualizar los archivos de contexto afectados

Editar solo las secciones relevantes:
- Info de endpoints → `.claude/context/api-endpoints.md`
- Modelos/schemas → `.claude/context/data-models.md`
- Servicios/lógica → `.claude/context/services-layer.md`
- Arquitectura → `.claude/context/architecture.md`
- Reglas generales → `.claude/context/MEMORY.md`

### 3. Informar al usuario

```
✓ CONTEXTO GUARDADO — Listo para compactar

Archivos actualizados:
- [lista de archivos modificados]

Tarea actual: [descripción breve]
Estado: [rama] — [commits pendientes o limpios]

Pendiente: [próximos pasos]

→ Ahora ejecuta /compact para liberar contexto
→ Al volver, Claude tendrá todo el contexto desde los archivos guardados
```

<!-- origen: UDLA_backend_ssh/.claude/commands/compact-context.md (generalizado) -->
