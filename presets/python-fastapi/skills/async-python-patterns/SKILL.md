# async-python-patterns

Patrones async/await para Python en proyectos ${stack}.

## Async context managers

```python
async with aiofiles.open("file.txt") as f:
    content = await f.read()
```

## Gather concurrente

```python
import asyncio

results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
    fetch_profile(user_id),
)
```

## AsyncSession con SQLAlchemy

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_by_id(session: AsyncSession, id: int):
    result = await session.execute(select(Model).where(Model.id == id))
    return result.scalar_one_or_none()
```

## Timeouts

```python
import asyncio

try:
    result = await asyncio.wait_for(long_operation(), timeout=5.0)
except asyncio.TimeoutError:
    raise HTTPException(status_code=504, detail="Operation timed out")
```
