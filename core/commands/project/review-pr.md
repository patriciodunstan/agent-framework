---
description: "Revisión del PR antes de subirlo — verifica calidad de código, tipos, manejo de errores y cumplimiento del CLAUDE.md"
argument-hint: "[code|types|errors|tests|all]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Agent"]
---

# Revisión de PR — ${stack}

Revisa los cambios actuales antes de hacer commit/push.

**Aspectos a revisar:** "$ARGUMENTS"

## Contexto del proyecto

- Archivos modificados: !`git diff --name-only HEAD`
- Diff completo: !`git diff HEAD`
- Rama actual: !`git branch --show-current`

## Flujo de revisión

### 1. Reglas críticas del proyecto (SIEMPRE verificar)

- No se hacen queries directas en routers — usar servicios o repositorios
- Todos los endpoints tienen schema de request y response
- No se commitean secrets, .env, credenciales
- No commits directos a main
- Convenciones de naming según el stack (${language})
- Queries parametrizadas (no interpolación directa en SQL)

### 2. Verificaciones de calidad

- Type hints / tipos en todas las funciones
- Manejo de errores explícito con status codes correctos
- Dependencias inyectadas, no hardcodeadas
- Tests para la lógica nueva

### 3. Resumen final

```
## Problemas Críticos (bloquean el PR)
- ...

## Problemas Importantes (deben corregirse)
- ...

## Sugerencias (opcional)
- ...

## OK — Listo para commit
- ...
```

Si no hay problemas críticos, indicar que está listo para `/finish-ticket`.

<!-- origen: UDLA_backend_ssh/.claude/commands/review-pr.md (generalizado) -->
