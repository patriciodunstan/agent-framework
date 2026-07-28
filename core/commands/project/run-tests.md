---
description: Ejecuta la suite de tests del proyecto y reporta resultados con cobertura
allowed-tools: ["Bash"]
---

## Estado actual

- Rama activa: !`git branch --show-current`
- Archivos modificados: !`git status --short`

## Tu tarea

### 1. Ejecutar tests con cobertura

```bash
${test_cmd}
```

### 2. Linting

```bash
${lint_cmd}
```

### 3. Reportar resultados

Mostrar al usuario:
- Total de tests: pasados / fallados / saltados
- Cobertura por módulo (target: services ≥80%, utils ≥90%)
- Tests fallados con el error completo
- Errores de linting encontrados

### 4. Si hay tests fallando

Analizar el error y sugerir la corrección.
No aplicar la corrección automáticamente — primero consultar al usuario.

### 5. Si cobertura < 80%

Indicar qué funciones/módulos necesitan más cobertura y sugerir casos de test.

<!-- origen: UDLA_backend_ssh/.claude/commands/run-tests.md (generalizado) -->
