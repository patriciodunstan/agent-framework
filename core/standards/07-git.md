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
- `${branch_pattern}`: Features y fixes (adaptar al ticket_format `${ticket_format}`)
- `hotfix/descripcion`: Fixes urgentes a producción

### Reglas

- **NUNCA** hacer commit directo a `main`
- Cada cambio corresponde a un ticket con su propia rama y PR
- No commitear secrets, `.env`, credenciales

<!-- origen: ~/.claude/CLAUDE.md §Git -->
