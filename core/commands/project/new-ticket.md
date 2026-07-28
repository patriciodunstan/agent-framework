---
allowed-tools: Bash(git checkout:*), Bash(git pull:*), Bash(git branch:*), Bash(git status:*)
description: Inicia un nuevo ticket — pregunta el nombre, crea la rama desde la base actualizada
---

## Contexto actual

- Rama actual: !`git branch --show-current`
- Estado del repo: !`git status --short`
- Últimas ramas: !`git branch --sort=-committerdate | head -10`

## Tu tarea

1. Pregunta al usuario el nombre del ticket/rama con este formato sugerido:
   - `${branch_pattern}` (adaptar al formato de tickets `${ticket_format}`)

2. Una vez que el usuario entregue el nombre, ejecuta en orden:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b <nombre-de-rama>
   ```

3. Confirma al usuario:
   - Rama creada y activa
   - Base: main actualizado
   - Listo para implementar los cambios del ticket

No hagas nada más. No empieces a implementar código.

<!-- origen: UDLA_backend_ssh/.claude/commands/new-ticket.md (generalizado) -->
