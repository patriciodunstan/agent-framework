## Estándar 7: Git

### Commits

Formato: `tipo(scope): descripción`

Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

Ejemplos:
- `feat(auth): add JWT refresh token`
- `fix(api): handle null response from external service`
- `refactor(db): extract repository pattern`

### Branches

- `main` / `master`: Producción
- `develop`: Integración
- Ramas de trabajo (features/fixes): usan el patrón de rama y el formato de ticket
  que declara el `CLAUDE.md` del proyecto (p. ej. `feature/<id>-descripcion`)
- `hotfix/descripcion`: Fixes urgentes a producción

### Reglas

- **NUNCA** hacer commit directo a `main`
- Cada cambio corresponde a un ticket con su propia rama y PR
- No commitear secrets, `.env`, credenciales

<!-- origen: ~/.claude/CLAUDE.md §Git -->
