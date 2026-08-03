# ADR-0009: Presupuesto de contexto — divulgación progresiva en lo que se genera

- **Estado**: aceptada
- **Fecha**: 2026-08-03
- **Ámbito**: proyecto

## Contexto

El framework no gasta tokens al ejecutarse (Python cero-deps). El coste real está en lo
que **emite**: los archivos que Claude Code y Copilot cargan en cada proyecto instalado.
Medición del output renderizado antes de esta decisión (stack `python-fastapi`, profile
`work`):

| Bloque | Cuándo se carga | Bytes |
|---|---|---|
| `~/.claude/CLAUDE.md` (header + 9 standards) | cada turno | 9.794 |
| `CLAUDE.md` del proyecto | cada turno | 1.649 |
| `AGENTS.md` | cada turno | 729 |
| stdout del hook `load_context.py` | startup, resume y **compact** | 4.874 |
| `SKILL.md` (los 5 del preset) | al invocar cada skill | 92.401 |

El bloque permanente (~4.260 tokens) se paga en cada llamada a la API de la sesión y se
recarga entera en cada compactación. Tres causas identificadas:

1. **Conocimiento genérico en los standards.** Enumerar OWASP Top 10, explicar el ciclo
   Red-Green-Refactor o tabular "JWT vs sesión vs OAuth2" es material que el modelo ya
   tiene; restarlo no cambia comportamiento y se paga cada turno.
2. **Duplicación de lo que el harness ya inyecta.** El estándar de multi-agente mantenía
   una tabla de agentes disponibles que Claude Code ya provee en el system prompt, con el
   riesgo añadido de divergir de la real.
3. **Volcado sin filtrar.** El hook imprimía **todos** los `.md` de `.claude/context/`
   completos, y los `SKILL.md` eran monolitos de hasta 1.050 líneas que entraban enteros
   aunque se necesitara una sola sección.

## Decisión

**El contenido generado se rige por un presupuesto de contexto**: en un archivo que se
carga siempre solo va lo que el modelo no puede derivar — política, umbrales,
prohibiciones y formatos del proyecto. Todo lo demás se carga bajo demanda.

Aplicado en cuatro mecanismos:

1. **Standards sin material derivable.** Se conserva toda regla accionable y se elimina la
   explicación de por qué es buena práctica. Se sigue emitiendo un fragmento por estándar
   (9 archivos, numeración estable).
2. **Procedencia fuera del output.** Los comentarios `<!-- origen: ... -->` documentan de
   dónde viene cada fragmento y sirven a quien mantiene el framework, pero no al modelo:
   `strip_provenance()` (en `generators/common.py`) los elimina de todo `.md` emitido. Se
   quedan en el repo.
3. **Hook con divulgación progresiva.** `load_context.py` inyecta `MEMORY.md` entero —es la
   memoria que se lee siempre— y del resto de `.claude/context/` solo un índice de una línea
   por archivo (nombre, primer encabezado, número de líneas), para que el modelo lea con
   `Read` el que corresponda al módulo en que trabaje.
4. **Skills como índice + `references/`.** Cada `SKILL.md` conserva orientación (cuándo
   usarlo, conceptos, quick start, resumen) y un índice de `references/*.md` con lo que hay
   en cada uno. El generador ya los copia: `skill_dirs()` recorre con `rglob`, no hizo falta
   cambiarlo.

Decisión asociada: los skills que comparten varios stacks viven una sola vez en
`presets/_shared/skills/` y se resuelven por fallback en `skill_dirs()`; los directorios de
`presets/` con `_` inicial no son stacks elegibles (`loader.available()` los filtra).

### Dos políticas heredadas que se invierten

Al medir el coste real salieron dos reglas del `CLAUDE.md` original que empujaban en contra
de la fiabilidad y del gasto a la vez:

**Delegar en subagentes por defecto** (estándar 5 decía: leer >3 archivos → delegar
siempre). Confundía dos recursos distintos. Un subagente ahorra *ventana de contexto* pero
**aumenta** el gasto: arranca en frío y vuelve a pagar entero el system prompt y las
definiciones de herramientas, que pesan más que el propio `CLAUDE.md`. Y es menos fiable,
porque no ve la conversación y devuelve un resumen con pérdida. El default se invierte:
trabajar en la sesión principal, y delegar solo cuando hay que leer mucho para responder
poco, cuando la alternativa es compactar, o cuando hay paralelismo real.

**Estimar el contexto por número de turnos** (estándar 6 y el command `/manage-context`
clasificaban en VERDE/AMARILLO/ROJO según turnos, y mandaban avisar "Contexto al 60%+").
El número de turnos no determina el porcentaje: la regla obligaba a afirmar como medición
un dato fabricado, contradiciendo el estándar 3 del mismo documento. Se elimina la
heurística: el uso real lo reporta el harness (`/context`) y solo con ese dato se avisa.
Se añade además la distinción que faltaba: para una tarea nueva sin relación con la
anterior, `/clear` es más barato que `/compact` —no resume nada y arranca con el prefijo
limpio—, y `/manage-context` pasa a ocuparse de lo único que importa antes de cualquiera
de las dos: guardar en memoria persistente lo que no sobrevive.

## Consecuencias

- **Medido** (mismo stack y profile, output renderizado): bloque permanente 17.046 → 8.131
  bytes (~4.261 → ~2.032 tokens, −52%); invocar un skill 23.100 → 4.793 tokens (−79%).
- **Regla para contribuir contenido**: antes de agregar texto a `core/standards/`,
  `core/claude-md/` o `core/context-templates/`, verificar que sea política del proyecto y
  no conocimiento general. Si es material de referencia, va a `references/` de un skill.
- **Regla para skills**: un `SKILL.md` nuevo no debería pasar de ~150 líneas; el cuerpo va
  en `references/`, citado desde el índice.
- **No duplicar al harness**: no se tabulan en contenido generado los agentes, comandos ni
  skills disponibles — el harness ya los inyecta y una copia diverge.
- **Asimetría Claude↔Copilot deliberada**: Copilot no tiene hook de sesión ni listado
  automático, así que su `MEMORY.md` sí conserva el índice de contexto y el mapa de dónde
  vive su config. La paridad de ADR-0007 es de capacidades, no de bytes.
- **Corregido de paso**: `load_context.py` fuerza UTF-8 en stdout. En Windows la consola es
  cp1252 y el hook moría con `UnicodeEncodeError` tras emitir 816 de 4.874 bytes — la
  memoria del proyecto llegaba truncada al 17%. `tests/test_hooks.py` lo detectaba y estaba
  en rojo antes de esta decisión.
