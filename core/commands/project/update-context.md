---
description: Actualiza .claude/context/ con el estado actual del proyecto — sin hacer commit
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

## Estado actual

- Rama activa: !`git branch --show-current`
- Archivos modificados: !`git status --short`
- Diff actual: !`git diff HEAD`

## Tu tarea

Analiza el diff y los archivos modificados para determinar qué secciones de
`.claude/context/` necesitan actualizarse.

Actualiza solo las secciones afectadas — no reescribas archivos completos.

### Mapeo de cambios → archivos de contexto

| Si cambiaron... | Actualizar |
|----------------|-----------|
| Routers / endpoints | `api-endpoints.md` |
| Schemas / modelos | `data-models.md` |
| Services / lógica de negocio | `services-layer.md` |
| Dependencias, Dockerfile, estructura | `architecture.md` |
| Reglas generales o decisiones | `MEMORY.md` |

Al terminar:
1. Lista los archivos de contexto que actualizaste
2. Confirma sin hacer commit

`.claude/context/` es la memoria portable — no copiar a `~/.claude/` (no es portable entre laptops).

No hagas commit. Solo actualiza los archivos de contexto.

<!-- origen: UDLA_backend_ssh/.claude/commands/update-context.md (generalizado) -->
