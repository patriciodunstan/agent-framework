## Estándar 8: Seguridad

- Validar y sanitizar el input de todos los endpoints (XSS, SQL injection).
- Autenticación robusta y autorización por rol/recurso (RBAC), explícitas.
- Headers de seguridad configurados: CORS, CSP, HSTS.
- Secrets: nunca en el repo. `.env` en desarrollo (ignorado por git), vault
  gestionado en producción (Key Vault, Secrets Manager). Rotar credenciales.

La elección del patrón de autenticación (JWT + refresh, sesión + Redis,
OAuth2/OIDC, API keys) se registra como ADR.

<!-- origen: ~/.claude/CLAUDE.md §Seguridad -->
