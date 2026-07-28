# sql-optimization-patterns

Patrones de optimización SQL para proyectos ${stack}.

## Eager loading con SQLAlchemy

```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload: N+1 safe para colecciones
stmt = select(Order).options(selectinload(Order.items))

# joinedload: para relaciones many-to-one
stmt = select(Order).options(joinedload(Order.user))
```

## Índices

```python
from sqlalchemy import Index

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status = Column(String, index=True)
    created_at = Column(DateTime)

    __table_args__ = (
        Index("ix_orders_user_status", "user_id", "status"),
    )
```

## Paginación eficiente

```python
async def paginate(session: AsyncSession, stmt, page: int, size: int):
    total = await session.scalar(select(func.count()).select_from(stmt.subquery()))
    items = await session.scalars(stmt.offset((page - 1) * size).limit(size))
    return {"items": list(items), "total": total, "page": page, "size": size}
```

## EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 1 AND status = 'pending';
```
