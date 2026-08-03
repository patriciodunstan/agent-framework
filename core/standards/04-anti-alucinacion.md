## Estándar 4: Anti-alucinación

Nunca asumir; verificar contra el código real antes de afirmar o editar:

- Existencia de archivos y rutas → `Glob` / `Read`.
- Firmas de funciones, imports, configuración → `Grep`.
- APIs de librerías → MCP Context7 (docs actualizadas), nunca de memoria.
- Estado del código: si no se leyó en esta sesión, leerlo antes de cambiarlo.

Antes de proponer un cambio, haber leído: el archivo a modificar completo, los
que ese archivo importa si el cambio afecta interfaces, y los tests existentes
del módulo.

Ante incertidumbre, "no encontré X, ¿lo confirmas?" es preferible a inventar.

<!-- origen: ~/.claude/CLAUDE.md §Anti-Alucinación -->
