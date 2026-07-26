# Diseño: `agent-framework` — configurador portable de agentes de IA

- **Fecha**: 2026-07-26
- **Autor**: Patricio Dunstan
- **Estado**: aprobado (diseño) — pendiente plan de implementación

## Contexto

Existe una configuración de agentes de IA (Claude Code) madura y probada, repartida
en dos niveles:

- **Global** (`~/.claude/`): estándares de ingeniería portables en `CLAUDE.md` +
  commands globales (`manage-context`, `review-changes`, `setup-standards`).
- **Local** (por repo): patrón consistente en los servicios del workspace
  `lambda-scanner` — `ocrPDFCustom` (OCR, Python), `UDLA_backend_ssh` (backend
  FastAPI, el más maduro) y `UDLA_front` (React+Vite). Cada uno tiene `CLAUDE.md`
  (+ `AGENTS.md`), un `.claude/` con `commands/` (los 6: `new-ticket`,
  `finish-ticket`, `run-tests`, `review-pr`, `compact-context`, `update-context`),
  `context/` (`MEMORY.md` + docs de dominio), `skills/`, `agents/`, y `docs/adr/`
  como fuente de verdad de decisiones.

El patrón funciona, pero hoy vive copiado a mano en cada servicio y solo existe en un
computador. Se necesita:

1. **Respaldarlo** en GitHub personal (resiliencia ante pérdida del equipo).
2. **Reutilizarlo** para crear el mismo ambiente en proyectos futuros.
3. **Adaptarlo** a dos entornos distintos:
   - **Personal**: Claude Code · Python/FastAPI, React, AWS Lambda · GitHub · ticket `#123`.
   - **Trabajo**: Spring Boot (Java), .NET (C#), React+Vite, Python puro · Azure DevOps
     · ticket `AB#123` · GitHub Copilot como agente.

## Objetivo

Un **repositorio único** en GitHub personal que actúe como framework/configurador:
extrae el conocimiento reutilizable a una **fuente única neutral**, y mediante un
instalador **estampa** la configuración adecuada en dos niveles (global de máquina y
local de proyecto), parametrizada por stack tecnológico y por perfil de entorno.

## Decisiones tomadas (brainstorming)

| # | Decisión | Elegido |
|---|----------|---------|
| 1 | Forma del framework | Un repo con presets por stack (no dos repos, no CLI interactivo) |
| 2 | Manejo de múltiples agentes | Núcleo neutral + generadores por agente (una fuente, múltiples salidas) |
| 3 | Alcance v1 | Núcleo + generador Claude Code + los 5 presets (Copilot en v2) |
| 4 | Implementación del instalador | Script Python (`install.py`), cross-plataforma, cero dependencias |
| 5 | Global vs local | Un repo, una fuente de verdad, dos *scopes* de salida (global / project) |
| 6 | Host git en ambos entornos | **GitHub** (personal y trabajo usan GitHub para repos) |
| 7 | Ticket/work-item en trabajo | Azure Boards (`AB#123`), rama `feature/AB#123-desc` |
| 8 | Docker / Kubernetes | Eje **addon** ortogonal (`--addons docker,k8s`), incluido en v1 |

## Modelo conceptual: 3 ejes + addons

Una instalación se define como
**`core` (neutral) + `scope` × `stack` × `profile` (+ `addons` opcionales)**.
Separar estos ejes es lo que evita duplicación y drift.

- **scope** — nivel de salida:
  - `global`: arma `~/.claude/` (backup/restore de máquina; se instala 1 vez por equipo).
  - `project`: estampa un repo (se instala por cada proyecto). El `CLAUDE.md` del
    proyecto queda **delgado** y referencia al global (patrón ya usado en
    `UDLA_backend_ssh`: *"Complementa las instrucciones globales de `~/.claude/CLAUDE.md`"*).
- **stack** — lenguaje/patrones técnicos: `python-fastapi`, `java-springboot`,
  `dotnet`, `react-vite`, `aws-lambda`. Define comandos de test/lint/build/typecheck,
  estructura de carpetas y skills técnicas.
- **profile** — entorno de trabajo: `personal` vs `work`. **Ambos usan GitHub como
  host de repos**; el profile diferencia por CI, nube, infraestructura, agente y
  convención de ticket/rama:

  | Campo | `personal` | `work` |
  |-------|-----------|--------|
  | git host | GitHub | GitHub |
  | CI / pipelines | GitHub Actions | Azure DevOps pipelines *(migración a GH Actions pendiente ~2027)* |
  | Nube / hosting | AWS | Azure (resource groups, agentes) |
  | Agente | Claude | Copilot *(v2)* |
  | Ticket / rama | GitHub Issues `#123` / `feature/123-desc` | Azure Boards `AB#123` / `feature/AB#123-desc` |

- **addons** — capas ortogonales opcionales que se superponen a cualquier stack:
  `docker`, `k8s`. Agregan context/skills de contenedores y orquestación sin duplicar
  ese conocimiento en cada preset. Se activan con `--addons docker,k8s`.

Ejemplo del porqué de la separación: `UDLA_backend_ssh` es
`stack=python-fastapi` + `profile=work` (CI Azure Pipelines, `AB#`); un futuro proyecto
personal en Python sería `stack=python-fastapi` + `profile=personal` (GitHub Actions,
`#`). Comparten el 90%; solo difieren en CI, nube y ticket, que viven en el `profile`.
La migración de pipelines del próximo año = cambiar un campo (`ci:` en `work.yaml`).

## Arquitectura del repositorio

```
agent-framework/
├── core/                       # Conocimiento NEUTRAL — fuente única
│   ├── standards/              # Estándares de ingeniería, troceados en fragmentos:
│   │                           #   adr, config-local, anti-alucinacion,
│   │                           #   verificar-no-inferir, multi-agente, tokens,
│   │                           #   git, seguridad, testing
│   ├── commands/               # Los 6 commands como plantillas con placeholders
│   ├── agents/                 # subagents neutrales (validator-reviewer, pipeline-debugger)
│   ├── context-templates/      # esqueletos: MEMORY.md, architecture.md, api-*.md, ...
│   └── adr/                    # README.md + template.md canónicos
├── presets/                    # Un directorio por STACK (datos, no código)
│   ├── python-fastapi/         # preset.yaml (+ skills/ y commands extra del stack)
│   ├── java-springboot/
│   ├── dotnet/
│   ├── react-vite/
│   └── aws-lambda/
├── profiles/                   # personal.yaml · work.yaml
├── addons/                     # capas ortogonales opcionales
│   ├── docker/                 # context/skills de contenedores
│   └── k8s/                    # context/skills de orquestación
├── generators/
│   └── claude/                 # v1: (core+preset+profile) → salida para Claude Code
│                               # v2 (futuro): generators/copilot/
├── install.py                  # CLI orquestador (Python stdlib, idempotente)
├── tests/                      # pytest: golden-master (stack×profile×scope) + idempotencia
├── docs/
│   ├── adr/                    # Decisiones DEL PROPIO framework (se dogfoodea)
│   └── superpowers/specs/      # Este spec y futuros
└── README.md
```

### `core/` — la fuente única neutral

Contenido **extraído y generalizado** de las configs reales ya maduras (sobre todo
`UDLA_backend_ssh`) y del `CLAUDE.md` global. Se elimina lo específico de UDLA
(Textract, SQL Server, Azure AD, nombres de módulos) y se reemplaza por placeholders
tipo `${language}`, `${test_cmd}`, `${ticket_format}`. **Nada se inventa**: el origen
de cada fragmento se documenta en el plan de implementación.

### `presets/<stack>/preset.yaml` — el corazón

> **Nota de formato**: los ejemplos usan sintaxis YAML por legibilidad, pero el
> formato de serialización concreto es **decisión del plan**, acotada por el objetivo
> de cero dependencias. Candidatos stdlib: TOML (`tomllib`, requiere Python 3.11+) o
> JSON. YAML solo si se acepta PyYAML como única dependencia. El resto del diseño es
> agnóstico al formato elegido.

Cada preset es **datos** que rellenan los placeholders del núcleo:

```yaml
# presets/python-fastapi/preset.yaml
stack: python-fastapi
language: "Python 3.12+"
commands:
  test:      "pytest tests/ -q"
  lint:      "ruff check app/"
  typecheck: "mypy app/"
  build:     null
structure: |
  app/{core,api,services,models,schemas,db}/ ...
skills: [async-python-patterns, fastapi-templates, python-testing-patterns, ...]
precommit: [test, lint]            # orden del protocolo pre-commit
maturity: real                     # real | plantilla-base
```

```yaml
# profiles/work.yaml
profile: work
agents: [claude]                   # v2: [claude, copilot]
git_host: github                   # los repos de trabajo también viven en GitHub
ci: azure-pipelines                # migración a github-actions pendiente (~2027)
cloud: azure                       # resource groups, agentes
ticket_format: "AB#<número>"       # Azure Boards
branch_pattern: "feature/AB#<n>-descripcion"

# profiles/personal.yaml
# profile: personal
# agents: [claude]
# git_host: github
# ci: github-actions
# cloud: aws
# ticket_format: "#<número>"       # GitHub Issues
# branch_pattern: "feature/<n>-descripcion"
```

> **Presets de trabajo, nota de realidad**: el stack Java del entorno de trabajo usa
> un framework interno llamado **"nano"** (sobre Spring Boot, orientado a BFF). Como es
> propietario, el preset `java-springboot` es `plantilla-base`: cubre el Spring Boot
> genérico y deja marcado dónde encajan las convenciones de `nano` para endurecerlo al
> usarlo en un proyecto real.

### `generators/claude/` — traductor a Claude Code

Toma `core + preset + profile` y, según el `scope`, emite:

- **scope `global`** → `~/.claude/CLAUDE.md` (estándares ensamblados desde
  `core/standards`) + commands globales (`manage-context`, `review-changes`,
  `setup-standards`) en `~/.claude/commands/`.
- **scope `project`** → en el `--target`:
  - `CLAUDE.md` **delgado** que referencia al global + contexto del stack.
  - `AGENTS.md` (para interoperar con otros agentes).
  - `.claude/{commands,agents,skills,context}/` + `settings.json`.
  - `docs/adr/{README.md,template.md}`.
  - Entrada `.claude/` en `.gitignore` (según estándar #2).

Si se pasan `--addons`, el generador **superpone** el context/skills de cada addon
sobre la salida del stack (después del stack, para que un addon pueda añadir sin pisar).

En v2 se agrega `generators/copilot/` que consume la **misma** `core` y emite
`.github/copilot-instructions.md` + `AGENTS.md` + prompt files.

## Flujo de datos

```
core/ (neutral) ──┐
presets/<stack> ──┤
profiles/<prof> ──┼─► install.py ─► generators/<agente> ─► árbol de archivos escrito
addons/<addon>* ──┘        │                                  (según --scope y --target)
                           └── resuelve placeholders con string.Template (stdlib);
                               los addons se superponen tras el stack
```

## El instalador (`install.py`)

Uso:

```bash
# Restaurar/actualizar tu entorno global personal (backup de máquina)
python install.py --scope global --profile personal

# Estampar un proyecto de trabajo Spring Boot (nano/BFF) con Docker + Kubernetes
python install.py --scope project --stack java-springboot --profile work \
  --addons docker,k8s --target C:\repos\mi-servicio

# Proyecto personal Python, sobre el directorio actual
python install.py --scope project --stack python-fastapi --profile personal --target .
```

Comportamiento:

- **Idempotente** (igual que el `/setup-standards` actual): no pisa lo que ya existe;
  agrega solo lo que falta y **reporta** qué creó / qué ya estaba / qué queda por
  commitear. No commitea nada en el proyecto destino.
- **Cero dependencias** (objetivo): solo stdlib (`argparse`, `pathlib`,
  `string.Template`, y lector de presets según el formato que elija el plan — ver
  "Nota de formato"). Meta: correr en cualquier máquina con Python 3.11+ sin
  `pip install`. La versión mínima de Python se fija en el plan junto con el formato.
- **Validación de entrada**: combinaciones inválidas (stack/profile/scope inexistente)
  fallan con mensaje claro antes de escribir nada.

## Manejo de errores

- Target inexistente o no escribible → error claro, no se escribe nada parcial.
- `scope global` sin `~/.claude` → se crea; si existe, modo idempotente (no pisa).
- Placeholder sin valor en el preset/profile → **falla la generación** (no se emite un
  archivo con `${...}` sin resolver). Esto también es un test.
- Preset con `maturity: plantilla-base` → el instalador imprime un aviso: *"preset sin
  probar en proyecto real; revísalo antes de confiar en él"*.
- Addon inexistente en `--addons` → error claro listando los addons disponibles, antes
  de escribir nada.

## Testing (estándar "flujo real")

`pytest` sobre `install.py` y los generadores:

1. **Golden-master**: renderiza cada combinación relevante `scope × stack × profile`
   a un directorio temporal y verifica el árbol de archivos esperado y que **no queden
   placeholders `${...}` sin resolver**.
2. **Idempotencia**: correr el instalador dos veces sobre el mismo target → la segunda
   corrida no produce cambios.
3. **Smoke de equivalencia**: para `python-fastapi` + `project`, el `.claude/` generado
   es estructuralmente equivalente al de `UDLA_backend_ssh` (validación contra la
   realidad de origen).
4. **Addons**: instalar `--addons docker,k8s` sobre un stack agrega el context/skills
   de contenedores sin romper la salida base ni la idempotencia.

## Fidelidad de los presets (honestidad, no humo)

- **Reales** (extraídos de configs maduras): `python-fastapi` (de `UDLA_backend_ssh`),
  `react-vite` (de `UDLA_front`).
- **Plantilla base** (marcados `maturity: plantilla-base`, "sin probar en proyecto real
  todavía"): `java-springboot`, `dotnet`, `aws-lambda`. Son puntos de partida honestos
  que se endurecen al usarlos en trabajo.

## Fuera de alcance de v1 (YAGNI)

- Generador Copilot y sus prompt files (v2).
- Pipelines reales de Azure DevOps / GitHub Actions (el framework describe la convención
  de CI vía `profile`, pero no genera YAML de pipeline en v1).
- CLI interactivo con menús (v1 usa flags; interactivo es mejora futura).
- Autoactualización del framework en proyectos ya estampados (v2).

## Criterios de éxito de la v1

1. El repo `agent-framework` existe en GitHub personal, con `core`, 5 presets,
   2 profiles, generador Claude, `install.py` y tests.
2. `install.py --scope global --profile personal` reconstruye un `~/.claude/`
   equivalente al actual en una máquina limpia.
3. `install.py --scope project --stack python-fastapi --profile work` produce una
   config equivalente a la de `UDLA_backend_ssh`.
4. `pytest` pasa (golden-master + idempotencia + smoke) y `ruff check` limpio.
5. El framework se dogfoodea: tiene su propio `docs/adr/` con las decisiones de este
   diseño registradas.

## Fases (alto nivel — el detalle va al plan de implementación)

1. Andamiaje del repo + `install.py` mínimo (resuelve placeholders, escribe árbol).
2. `core/` extraído y generalizado desde las configs reales.
3. Presets reales (`python-fastapi`, `react-vite`) + validación por equivalencia.
4. Generador Claude para ambos scopes (global y project).
5. Presets plantilla-base (`java-springboot` con notas de `nano`/BFF, `dotnet`,
   `aws-lambda`).
6. Addons `docker` y `k8s` (overlay ortogonal) + su aplicación en el generador.
7. Suite de tests (golden-master, idempotencia, smoke, addons) + ruff.
8. README + ADRs propios + primer push a GitHub personal.
