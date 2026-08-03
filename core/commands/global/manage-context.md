---
description: Guarda en memoria persistente lo aprendido en la sesión y recomienda si conviene /clear o /compact. Usar antes de cambiar de tarea o cuando el contexto se esté llenando.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Gestión de Contexto y Tokens

El valor de este command es **no perder lo aprendido** al liberar contexto. El
porcentaje de uso real lo reporta el harness (`/context`): no estimarlo a partir
del número de turnos ni presentarlo como medición (Estándar 3).

## Tu tarea

### 1. Guardar lo que no sobrevive

Revisar qué se aprendió en esta sesión que **no** esté ya en los archivos de
memoria del proyecto (`.claude/context/`, o `~/.claude/projects/*/memory/`):

- Decisiones técnicas tomadas y su porqué
- Bugs encontrados y su causa real (verificada, no supuesta)
- Patrones o restricciones descubiertos en el código
- Trabajo pendiente y dónde quedó

Escribirlo en el archivo de memoria que corresponda. Si es una decisión de
arquitectura o convención, va a `docs/adr/` (Estándar 1), no a la memoria.

### 2. Recomendar cómo seguir

- **Lo próximo no tiene relación con lo actual** → recomendar `/clear`. No resume
  nada y arranca con el prefijo limpio: es la opción más barata.
- **Hay que seguir con la misma tarea y falta espacio** → recomendar `/compact`.
  Cuesta un pase de resumen y recalentar el prefijo, y pierde detalle; por eso se
  hace después de guardar (paso 1), no antes.
- **Hay espacio de sobra** → no hacer nada. Compactar sin necesidad gasta.

### 3. Informar

```
Guardado en: [archivo(s)]
Pendiente: [qué queda por hacer]
Recomendación: /clear | /compact | seguir sin liberar
```

<!-- origen: ~/.claude/commands/manage-context.md (ADR-0009: quitada la clasificación VERDE/AMARILLO/ROJO por turnos, que fabricaba un dato no verificable) -->
