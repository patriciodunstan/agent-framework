---
name: docker-patterns
description: Patrones de contenedorización para ${stack}
---

# Docker para ${stack}

- Multi-stage builds; imagen final mínima.
- `.dockerignore` para no filtrar `.claude/`, `node_modules/`, `.venv/`.
- Healthcheck y usuario no-root.
