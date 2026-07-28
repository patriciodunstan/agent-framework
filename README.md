# agent-framework

Configurador portable de agentes de IA (Claude Code). Extrae el conocimiento
reutilizable a una fuente única neutral y lo **estampa** en cualquier máquina o
proyecto mediante un instalador Python sin dependencias externas.

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

### scope — nivel de salida

| Valor | Destino | Cuándo |
|-------|---------|--------|
| `global` | `~/.claude/` | Una vez por máquina; reconstruye el entorno base del agente |
| `project` | `<directorio>/.claude/` | Por cada proyecto nuevo que se quiere configurar |

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
| Agente | Claude Code | Claude Code *(Copilot en v2)* |
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
```

El instalador es **idempotente**: no pisa archivos que ya existen; agrega solo lo que
falta y reporta qué creó / qué ya estaba. No hace commit en el proyecto destino.

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

## `.claude/` se ignora en git

La carpeta `.claude/` generada en cada proyecto es tooling local del desarrollador
y **no se commitea**. El instalador la agrega automáticamente a `.gitignore` (estándar
de ingeniería #2 del framework). El conocimiento del proyecto (decisiones, specs) vive
en `docs/`.
