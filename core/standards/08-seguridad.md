## Estándar 8: Seguridad

### Principios OWASP Top 10

- Validación de inputs en todos los endpoints
- Sanitización de datos para prevenir XSS, SQL Injection
- Autenticación robusta (JWT, OAuth2)
- Autorización por roles/recursos (RBAC)
- Gestión segura de secrets (environment variables, vault)
- Headers de seguridad (CORS, CSP, HSTS)

### Autenticación/Authorization Patterns

| Patrón | Uso |
|--------|-----|
| JWT + Refresh tokens | APIs stateless, microservicios |
| Session + Redis | APIs tradicionales, monolitos |
| OAuth2 / OIDC | Integración con terceros, SSO |
| API Keys | Servicios internos, webhooks |

### Secret Management

- Nunca commitear secrets en el repo
- Usar `.env` files para desarrollo (en `.gitignore`)
- Usar vault services para producción (Key Vault, Secrets Manager)
- Rotar credentials regularmente

<!-- origen: ~/.claude/CLAUDE.md §Seguridad -->
