# API Endpoints — ${stack}

Todos los endpoints del proyecto.

---

## PÚBLICOS (sin autenticación)

### GET /health
- **Auth**: No
- **Response 200**: `{ status: "ok" }`
- **Response 503**: `{ status: "degraded", detail: "..." }`

---

## PROTEGIDOS

_(documentar aquí los endpoints protegidos del proyecto)_

### Ejemplo: GET /api/resource/
- **Auth**: Bearer token
- **Query params**: `limit` (int, default: 100), `offset` (int, default: 0)
- **Response**: `List[Resource]`

---

## Documentación Interactiva

- **Swagger UI**: `GET /docs`
- **OpenAPI JSON**: `GET /openapi.json`

<!-- origen: UDLA_backend_ssh/.claude/context/api-endpoints.md (generalizado) -->
