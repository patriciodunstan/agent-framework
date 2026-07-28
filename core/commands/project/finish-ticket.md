---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git branch:*), Bash(git log:*), Read, Edit, Write
description: Cierra un ticket — actualiza el contexto, hace commit, push y crea PR
---

## Contexto actual

- Rama activa: !`git branch --show-current`
- Archivos modificados: !`git status --short`
- Diff completo: !`git diff HEAD`
- Últimos commits: !`git log --oneline -5`

## Tu tarea

### 1. Analizar qué cambió

Revisar el diff y determinar qué archivos de contexto en `.claude/context/` necesitan actualizarse:

- Cambios en routers/ o endpoints → `.claude/context/api-endpoints.md`
- Cambios en schemas/ o models/ → `.claude/context/data-models.md`
- Cambios en services/ o lógica de negocio → `.claude/context/services-layer.md`
- Cambios en dependencias o estructura → `.claude/context/architecture.md`
- Cambios generales/reglas → `.claude/context/MEMORY.md`

### 2. Actualizar los archivos de contexto afectados

Editar solo las secciones relevantes. No reescribir todo, solo actualizar lo que cambió.

`.claude/context/` es la memoria portable del proyecto — viaja con el repo vía `git clone`.

### 3. Commit con todo incluido

```bash
git add <archivos-del-ticket> .claude/context/
git commit -m "tipo(scope): descripción

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin <rama-actual>
```

### 4. Crear PR

Usar el CLI del host git (`${git_host}`):

```bash
# GitHub:
gh pr create --title "<tipo>: descripción" --body "## Cambios\n- <lista>\n\n## Ticket\n${ticket_format}"

# Azure DevOps:
az repos pr create --title "<tipo>: descripción" --source-branch <rama-actual> --target-branch main
```

Si el CLI no está disponible, mostrar al usuario la URL manual para crear el PR.

### 5. Confirmar al usuario

Mostrar resumen de:
- Archivos de contexto actualizados
- Commit creado (hash)
- URL del PR

<!-- origen: UDLA_backend_ssh/.claude/commands/finish-ticket.md (generalizado) -->
