# Services Layer — ${stack}

## Estructura General

Cada módulo sigue el patrón:
```
router → service → repository/db
```

Los servicios contienen toda la lógica de negocio. Los routers solo validan
inputs/outputs y delegan al servicio.

---

## Servicios Implementados

_(documentar aquí los servicios del proyecto)_

### Ejemplo: ResourceService

Operaciones:
- `create(data) → Resource`
- `list(filters) → List[Resource]`
- `get_by_id(id) → Resource | None`
- `update(id, data) → Resource`
- `delete(id) → None`

---

## Inyección de Dependencias

_(documentar el patrón de DI usado en el stack ${stack})_

---

## Cómo agregar un nuevo servicio

1. Crear `service.py` en el módulo correspondiente
2. Heredar o implementar la interfaz base si existe
3. Registrar en el router con `Depends` o el mecanismo del framework
4. Escribir tests unitarios e de integración

<!-- origen: UDLA_backend_ssh/.claude/context/services-layer.md (generalizado) -->
