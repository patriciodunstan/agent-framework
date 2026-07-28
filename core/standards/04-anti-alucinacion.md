## Estándar 4: Anti-Alucinación

Las alucinaciones ocurren cuando Claude asume en lugar de verificar. Estas reglas las eliminan:

### Reglas de verificación obligatoria

1. **NUNCA asumir que un archivo existe** — hacer `Glob` o `Read` primero
2. **NUNCA asumir firmas de funciones** — hacer `Grep` en el código real antes de referenciarlas
3. **NUNCA asumir APIs de librerías** — usar el MCP Context7 para docs actualizadas
4. **NUNCA inventar rutas, imports o configuraciones** — verificar siempre con Grep/Read
5. **NUNCA asumir el estado actual del código** — si no lo leí en esta sesión, leerlo antes de hacer cambios

### Cuándo decir "no sé"

Si hay incertidumbre sobre cómo funciona algo → leerlo antes de responder.
Decir **"no encontré X, ¿puedes confirmar?"** es mejor que inventar.

### Verificación antes de proponer un cambio

Antes de proponer cualquier cambio de código, Claude DEBE haber leído:
- El archivo que se va a modificar (completo)
- Los archivos que ese archivo importa (si el cambio afecta interfaces)
- Los tests existentes del módulo (para no romperlos)

<!-- origen: ~/.claude/CLAUDE.md §Anti-Alucinación -->
