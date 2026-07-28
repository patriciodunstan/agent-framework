# fastapi-templates

Plantillas y patrones para APIs con FastAPI en proyectos ${stack}.

## Estructura de un router

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.example import ExampleCreate, ExampleRead
from app.services.example import ExampleService

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/", response_model=list[ExampleRead])
async def list_items(service: ExampleService = Depends()):
    return await service.list()

@router.post("/", response_model=ExampleRead, status_code=201)
async def create_item(body: ExampleCreate, service: ExampleService = Depends()):
    return await service.create(body)
```

## Dependency injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
```

## Error handling

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Resource not found")
raise HTTPException(status_code=422, detail="Validation error")
```
