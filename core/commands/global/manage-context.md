---
description: Analiza el estado del contexto actual, advierte si está por llenarse y prepara un resumen antes de compactar. Usar antes de /compact o cuando la sesión sea larga.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Gestión de Contexto y Tokens

## Tu tarea

### 1. Evaluar el estado actual del contexto

Estima el nivel de uso del contexto basándote en:
- Cantidad de mensajes intercambiados en la sesión
- Cantidad de archivos leídos y código generado
- Si ya hubo una compactación automática previa

Clasifica el estado en uno de estos niveles:
- **VERDE**: Sesión corta, contexto libre. Continuar normal.
- **AMARILLO**: Sesión mediana (>15 turnos o varios archivos leídos). Considerar /compact pronto.
- **ROJO**: Sesión larga (>25 turnos o mucho código generado). Compactar AHORA antes de seguir.

### 2. Si el estado es AMARILLO o ROJO — preparar antes de compactar

Antes de que el usuario ejecute `/compact`:

a) **Resumir lo importante de la sesión actual** que NO esté ya guardado en los archivos de memoria del proyecto (`.claude/context/` o `~/.claude/projects/*/memory/`):
   - Decisiones técnicas tomadas en esta sesión
   - Bugs encontrados y sus soluciones
   - Patrones descubiertos
   - Cambios pendientes de implementar

b) **Guardar ese resumen** en el archivo de memoria correspondiente del proyecto activo.

c) **Avisar al usuario** con el mensaje:

```
⚠️ CONTEXTO [AMARILLO/ROJO]
- Estado: [descripción breve]
- Recomendación: Ejecuta /compact ahora
- Ya guardé el resumen de esta sesión en [archivo]
- Después de /compact podrás continuar sin perder contexto
```

### 3. Si el estado es VERDE

Informar brevemente:
```
✓ CONTEXTO OK
- Sesión: [corta/mediana]
- Puedes continuar trabajando
- Sugerencia: usa /manage-context periódicamente en sesiones largas
```

### 4. Recomendaciones de eficiencia

Recordar al usuario estas buenas prácticas para esta sesión:
- Usar /compact proactivamente (no esperar a que sea automático)
- Iniciar nueva sesión para tareas completamente distintas
- El contexto se compacta automáticamente cuando se llena — /compact manual es más eficiente
- Los archivos `.claude/context/` son la memoria persistente — siempre actualizarlos antes de compactar

<!-- origen: ~/.claude/commands/manage-context.md -->
