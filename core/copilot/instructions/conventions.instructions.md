---
description: Convenciones de código para ${stack}
applyTo: '${code_globs}'
---
# Convenciones de código — ${language}

Estas reglas se adjuntan automáticamente cuando trabajás sobre archivos de código de
este stack. Complementan las instrucciones generales del proyecto.

- Naming según el lenguaje (${language}); nombres descriptivos, funciones pequeñas.
- Tipos/anotaciones en las firmas; manejo de errores explícito con el status correcto.
- Sin queries directas en controladores/routers — usar servicios o repositorios.
- Dependencias inyectadas, no hardcodeadas; nada de secrets en el código.
- Queries parametrizadas (nunca concatenar input en SQL).
- Tests para la lógica nueva: services ≥80%, utils ≥90%. Verificar contra la realidad,
  no inferir: cada afirmación con evidencia (resultado real de test), lo no comprobable
  se declara `no verificado: <razón>`.

<!-- generado por agent-framework — fuente: core/standards (forma Copilot path-specific) -->
