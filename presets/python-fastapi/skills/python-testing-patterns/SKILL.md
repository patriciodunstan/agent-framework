# python-testing-patterns

Patrones de testing con pytest para proyectos ${stack}.

## Fixtures async

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

## Test de endpoint

```python
@pytest.mark.asyncio
async def test_create_item(client, db_session):
    response = await client.post("/items/", json={"name": "test"})
    assert response.status_code == 201
    assert response.json()["name"] == "test"
```

## Mocking servicios externos

```python
from unittest.mock import AsyncMock, patch

@patch("app.services.external.ExternalService.call", new_callable=AsyncMock)
async def test_with_mock(mock_call, client):
    mock_call.return_value = {"status": "ok"}
    response = await client.get("/endpoint/")
    assert response.status_code == 200
```

## pytest.ini / pyproject.toml

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```
