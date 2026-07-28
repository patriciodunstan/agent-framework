## Estándar 2: La config de Claude Code es local

Toda la carpeta `.claude/` (settings, skills, agents, commands, context) es tooling
local del desarrollador, **no se commitea**. Cada proyecto la ignora vía
`.gitignore` (`.claude/`). Lo que sí es proyecto (decisiones, specs) vive en `docs/`.

<!-- origen: ~/.claude/CLAUDE.md §Estándares de Ingeniería / 2. La config de Claude Code es local -->
