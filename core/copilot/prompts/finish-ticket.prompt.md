---
description: Cierra un ticket — actualiza contexto, hace commit, push y crea el PR
name: finish-ticket
agent: 'agent'
---

Vas a cerrar el ticket actual.

## 1. Analizá qué cambió

Revisá el diff (`git diff HEAD`) y determiná qué documentación de contexto del proyecto
conviene actualizar (por ejemplo `.github/copilot-instructions.md` o `docs/`): endpoints,
modelos, servicios, arquitectura o reglas generales. Editá solo las secciones afectadas.

## 2. Commit

```
git add <archivos-del-ticket> <docs-de-contexto>
git commit -m "tipo(scope): descripción"
git push origin <rama-actual>
```

Usá un trailer `Co-Authored-By` apropiado al agente si tu flujo lo requiere.

## 3. Crear el PR

Con el CLI del host git (`${git_host}`):

- GitHub: `gh pr create --title "<tipo>: descripción" --body "## Cambios ... ## Ticket ${ticket_format}"`
- Azure DevOps: `az repos pr create --title "<tipo>: descripción" --source-branch <rama-actual> --target-branch main`

Si el CLI no está disponible, mostrame la URL para crear el PR a mano.

## 4. Confirmá

Resumen: docs de contexto actualizados, commit (hash) y URL del PR.

<!-- generado por agent-framework — fuente: core/commands/project/finish-ticket.md -->
