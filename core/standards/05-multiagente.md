## Estándar 5: Cuándo delegar en subagentes

Un subagente ahorra **ventana de contexto**, no tokens: arranca en frío y vuelve a
pagar entero el system prompt y las definiciones de herramientas. Por defecto se
trabaja en la sesión principal.

Delegar solo cuando hay que leer mucho para responder poco:

- Barrido amplio (muchos archivos o directorios) del que solo interesa la
  conclusión, no el contenido.
- La alternativa realista es llenar el contexto y tener que compactar —compactar
  pierde información y recalienta todo el prefijo.
- Tareas genuinamente independientes que corren en paralelo.

No delegar para leer unos pocos archivos concretos ni para algo que ya está en la
sesión: hacerlo directo es más barato y más fiable.

Al delegar: handoff explícito (archivos clave, decisiones ya tomadas,
restricciones), porque el subagente no ve la conversación. Su informe es un
resumen con pérdida — verificar contra el código lo que sea crítico antes de
actuar. No repetir trabajo que otro agente ya hizo.

El harness ya inyecta la lista de agentes disponibles con su descripción; elegir
de ahí.

<!-- origen: ~/.claude/CLAUDE.md §Estrategia Multi-Agente (invertido el default en ADR-0009: delegar era contraproducente para coste y fiabilidad) -->
