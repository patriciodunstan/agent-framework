# ADR-0002: Modelo core + scope×stack×profile + addons

- **Estado**: aceptada
- **Fecha**: 2026-07-28
- **Ámbito**: proyecto

## Contexto

El framework debe configurar dos entornos radicalmente distintos (personal: Python/FastAPI,
AWS, GitHub Actions, ticket `#123`; trabajo: Java/Spring Boot, Azure, Azure Pipelines,
ticket `AB#123`) que comparten el 90% de las prácticas y difieren solo en CI, nube y
convención de ticket. Además debe operar en dos niveles de salida (entorno global de
máquina vs. repositorio específico) y soportar capas ortogonales como Docker y Kubernetes
que aplican a cualquier stack.

Codificar estas variaciones en archivos distintos por combinación produciría explosión
combinatoria y drift. Se necesita una estructura que minimice la duplicación y haga
explícitas las diferencias.

## Decisión

Una instalación se define como el producto de tres ejes ortogonales más addons opcionales:

```
core (neutral) + scope × stack × profile (+ addons)
```

- **scope** (`global` | `project`): nivel de salida. `global` arma `~/.claude/` (una vez
  por máquina); `project` estampa un repo concreto. Determina qué archivos se emiten y
  dónde.
- **stack** (`python-fastapi`, `react-vite`, `java-springboot`, `dotnet`, `aws-lambda`):
  lenguaje y patrones técnicos. Vive en `presets/<stack>/preset.toml`. Define comandos de
  test/lint/build/typecheck, estructura de carpetas y skills.
- **profile** (`personal` | `work`): entorno de trabajo. Vive en `profiles/<profile>.toml`.
  Ambos usan GitHub como host; el profile diferencia CI, nube, agente y formato de ticket.
- **addons** (`docker`, `k8s`, ...): capas ortogonales opcionales que se superponen a
  cualquier stack tras la generación base. Se activan con `--addons`. Viven en
  `addons/<addon>/`.

## Consecuencias

- **Permitido**: agregar un nuevo stack creando `presets/<nuevo>/preset.toml` sin tocar
  ningún otro preset ni el generador. Ídem para nuevos profiles y addons.
- **Prohibido**: duplicar en un preset datos que corresponden al profile (CI, nube,
  ticket format) ni viceversa. La prueba: si un dato cambia entre `personal` y `work` pero
  el stack es el mismo, pertenece al profile.
- **Obligatorio**: todo nuevo preset declara el campo `maturity` (`real` | `plantilla-base`).
  El instalador emite aviso si `maturity = plantilla-base`.
- **Violación a marcar en review**: datos de CI/nube/ticket hardcodeados en un preset;
  datos de test/lint/build hardcodeados en un profile; addons con conocimiento específico
  de un stack concreto (los addons deben ser ortogonales).
