---
description: Inicia un nuevo ticket — pregunta el nombre y crea la rama desde la base actualizada
name: new-ticket
---

Vas a iniciar un nuevo ticket.

1. Revisá el estado del repo con git: rama actual, `git status --short`, y las ramas
   recientes.
2. Preguntame el nombre del ticket/rama. Formato sugerido: `${branch_pattern}`
   (según el formato de tickets `${ticket_format}`).
3. Con el nombre confirmado, ejecutá en orden:
   `git checkout main` → `git pull origin main` → `git checkout -b <nombre-de-rama>`.
4. Confirmame: rama creada y activa, base `main` actualizada, listo para implementar.

No empieces a implementar código todavía.

<!-- generado por agent-framework — fuente: core/commands/project/new-ticket.md -->
