---
description: Actualiza la documentación de contexto del proyecto con el estado actual — sin hacer commit
name: update-context
agent: 'agent'
---

Analizá el diff (`git diff HEAD`) y los archivos modificados para determinar qué
documentación de contexto del proyecto conviene actualizar (por ejemplo
`.github/copilot-instructions.md` o `docs/`).

Actualizá solo las secciones afectadas — no reescribas archivos completos.

Mapeo orientativo:

| Si cambiaron... | Actualizá |
|-----------------|-----------|
| Controladores / endpoints | la sección de API / endpoints |
| Schemas / modelos | la sección de modelos de datos |
| Servicios / lógica de negocio | la sección de servicios |
| Dependencias, Dockerfile, estructura | la sección de arquitectura |
| Reglas generales o decisiones | las instrucciones del proyecto |

Al terminar: listame los archivos que actualizaste y confirmá. **No hagas commit.**

<!-- generado por agent-framework — fuente: core/commands/project/update-context.md -->
