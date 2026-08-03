## Estándar 7: Git

- Commits: `tipo(scope): descripción` — tipos `feat`, `fix`, `refactor`, `test`,
  `docs`, `chore`. Ej.: `feat(auth): add JWT refresh token`.
- Ramas: `main`/`master` producción, `develop` integración, `hotfix/<desc>`
  urgencias a producción. Las de trabajo siguen el patrón de rama y el formato
  de ticket que declara el `CLAUDE.md` del proyecto.
- **NUNCA** hacer commit directo a `main`.
- Cada cambio corresponde a un ticket con su propia rama y PR.
- No commitear secrets, `.env` ni credenciales.

<!-- origen: ~/.claude/CLAUDE.md §Git -->
