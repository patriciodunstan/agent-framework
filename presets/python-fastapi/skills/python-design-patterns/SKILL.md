# python-design-patterns

Patrones de diseño aplicados a proyectos Python como ${stack}.

## Repository pattern

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: int) -> T | None: ...
    @abstractmethod
    async def list(self) -> list[T]: ...
    @abstractmethod
    async def create(self, data: dict) -> T: ...
    @abstractmethod
    async def delete(self, id: int) -> bool: ...
```

## Service layer

```python
class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def get_or_404(self, user_id: int):
        user = await self._repo.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
```

## Factory

```python
def make_service(session: AsyncSession) -> UserService:
    repo = SQLAlchemyUserRepository(session)
    return UserService(repo)
```
