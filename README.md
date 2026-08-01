# agent-framework

Configurador portable de agentes de IA (**Claude Code** y **GitHub Copilot**). Extrae el
conocimiento reutilizable a una fuente única neutral y lo **estampa** en cualquier máquina o
proyecto mediante un instalador Python sin dependencias externas. Una sola fuente `core/`,
múltiples agentes de salida.

---

## ¿Qué es?

Un repositorio que actúa como framework/configurador: mantiene en un solo lugar
los estándares de ingeniería, commands, skills y context-templates probados, y los
combina según tres ejes (scope × stack × profile) para generar la configuración
correcta para cada entorno.

La fuente de verdad se dogfoodea: el propio framework tiene su `docs/adr/` con las
decisiones de diseño registradas.

---

## Requisitos

- **Python 3.11+** (usa `tomllib` de la stdlib para leer presets)
- Sin dependencias externas — funciona en cualquier máquina con Python 3.11+
  sin necesidad de `pip install`

---

## El modelo: `core` + scope × stack × profile (+ addons)

Una instalación se define como:

```
core (neutral) + scope × stack × profile (+ addons opcionales)
```

### agente — `--agent {claude,copilot}` (default `claude`)

Selecciona el generador de salida. La fuente `core/` es la misma; cada agente la traduce
a su formato:

| agente | scope `global` | scope `project` |
|--------|----------------|-----------------|
| `claude` | `~/.claude/CLAUDE.md` + commands globales | `.claude/` (commands, agents, skills, context), `CLAUDE.md`, `AGENTS.md`, `docs/adr/` |
| `copilot` | `~/.copilot/copilot-instructions.md` | `.github/copilot-instructions.md`, `AGENTS.md`, `.github/prompts/*.prompt.md` (los 6 commands, invocables con `/`) |

### scope — nivel de salida

| Valor | Destino | Cuándo |
|-------|---------|--------|
| `global` | `~/.claude/` o `~/.copilot/` según agente | Una vez por máquina; reconstruye el entorno base del agente |
| `project` | `.claude/` o `.github/` según agente | Por cada proyecto nuevo que se quiere configurar |

### stack — lenguaje/patrones técnicos

Define comandos de test/lint/build/typecheck, estructura de carpetas y skills
técnicas del preset.

### profile — entorno de trabajo

Ambos entornos usan **GitHub** como host de repos. El profile diferencia por CI,
nube, agente y convención de ticket/rama:

| Campo | `personal` | `work` |
|-------|-----------|--------|
| git host | GitHub | GitHub |
| CI / pipelines | GitHub Actions | Azure DevOps pipelines *(migración a GH Actions pendiente ~2027)* |
| Nube / hosting | AWS | Azure |
| Agente | Claude Code | Claude Code y/o GitHub Copilot (`--agent`) |
| Ticket / rama | GitHub Issues `#123` / `feature/123-desc` | Azure Boards `AB#123` / `feature/AB#123-desc` |

### addons — capas opcionales ortogonales

Se superponen a cualquier stack sin duplicar conocimiento. Se activan con
`--addons`:

| Addon | Qué agrega |
|-------|------------|
| `docker` | Context y skills de contenedorización |
| `k8s` | Context y skills de orquestación Kubernetes |

---

## Uso

```bash
# Restaurar/actualizar tu entorno global personal (backup de máquina)
python install.py --scope global --profile personal

# Estampar un proyecto de trabajo Spring Boot con Docker + Kubernetes
python install.py --scope project --stack java-springboot --profile work \
  --addons docker,k8s --target C:\repos\mi-servicio

# Proyecto personal Python, sobre el directorio actual
python install.py --scope project --stack python-fastapi --profile personal --target .

# Estampar un proyecto de trabajo para GitHub Copilot (VS Code Copilot Chat)
python install.py --scope project --agent copilot --stack python-fastapi --profile work \
  --target C:\repos\mi-servicio
```

El instalador es **idempotente**: no pisa archivos que ya existen; agrega solo lo que
falta y reporta qué creó / qué ya estaba. No hace commit en el proyecto destino.

### GitHub Copilot en VS Code

Con `--agent copilot --scope project`, VS Code Copilot Chat lee `.github/copilot-instructions.md`
automáticamente en cada request, y los `.github/prompts/*.prompt.md` quedan invocables
escribiendo `/` en el chat (`/new-ticket`, `/run-tests`, `/review-pr`, …).

El scope `global` (`--agent copilot --scope global`) escribe
`~/.copilot/copilot-instructions.md`, que **Copilot CLI** lee nativamente. Para que
**VS Code** también lo use, apuntá el setting `chat.instructionsFilesLocations` a ese
archivo (o sincronizá tus instrucciones de usuario con Settings Sync).

---

## Presets disponibles

| Preset | Stack | Madurez | Nota |
|--------|-------|---------|------|
| `python-fastapi` | Python 3.12+ / FastAPI | **real** | Extraído de config madura de producción |
| `react-vite` | TypeScript + React (Vite) | **real** | Extraído de config madura de producción |
| `java-springboot` | Java 21 + Spring Boot | plantilla-base | Sin probar en proyecto real todavía; ver nota nano/BFF |
| `dotnet` | C# / .NET 8 | plantilla-base | Sin probar en proyecto real todavía |
| `aws-lambda` | Python 3.12 (AWS Lambda) | plantilla-base | Sin probar en proyecto real todavía |

> **Nota `java-springboot`**: en el entorno de trabajo se usa el framework interno
> `nano` (sobre Spring Boot, orientado a BFF). El preset cubre Spring Boot genérico y
> deja marcado dónde encajan las convenciones de `nano` para endurecerlo al usarlo en
> un proyecto real.
>
> **Aviso presets plantilla-base**: el instalador emite un aviso explícito al usar
> cualquier preset marcado `plantilla-base`. Revisarlo antes de confiar en él.

---

## Qué se commitea y qué no

- **Claude (`.claude/`)**: es tooling local del desarrollador y **no se commitea**. El
  instalador la agrega automáticamente a `.gitignore` (estándar de ingeniería #2). El
  conocimiento del proyecto (decisiones, specs) vive en `docs/`.
- **Copilot (`.github/`, `AGENTS.md`)**: **sí se commitea** — Copilot lee estos archivos
  desde el repo, así que viajan con `git clone`. El instalador no toca `.gitignore` para
  el agente `copilot`.
