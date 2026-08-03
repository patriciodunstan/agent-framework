---
name: async-python-patterns
description: Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations.
---


# Async Python Patterns

Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

## When to Use This Skill

- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues

## Sync vs Async Decision Guide

Before adopting async, consider whether it's the right choice for your use case.

| Use Case | Recommended Approach |
|----------|---------------------|
| Many concurrent network/DB calls | `asyncio` |
| CPU-bound computation | `multiprocessing` or thread pool |
| Mixed I/O + CPU | Offload CPU work with `asyncio.to_thread()` |
| Simple scripts, few connections | Sync (simpler, easier to debug) |
| Web APIs with high concurrency | Async frameworks (FastAPI, aiohttp) |

**Key Rule:** Stay fully sync or fully async within a call path. Mixing creates hidden blocking and complexity.

## Core Concepts

### 1. Event Loop

The event loop is the heart of asyncio, managing and scheduling asynchronous tasks.

**Key characteristics:**

- Single-threaded cooperative multitasking
- Schedules coroutines for execution
- Handles I/O operations without blocking
- Manages callbacks and futures

### 2. Coroutines

Functions defined with `async def` that can be paused and resumed.

**Syntax:**

```python
async def my_coroutine():
    result = await some_async_operation()
    return result
```

### 3. Tasks

Scheduled coroutines that run concurrently on the event loop.

### 4. Futures

Low-level objects representing eventual results of async operations.

### 5. Async Context Managers

Resources that support `async with` for proper cleanup.

### 6. Async Iterators

Objects that support `async for` for iterating over async data sources.

## Quick Start

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+
asyncio.run(main())
```

## Resources

- **Python asyncio documentation**: https://docs.python.org/3/library/asyncio.html
- **aiohttp**: Async HTTP client/server
- **FastAPI**: Modern async web framework
- **asyncpg**: Async PostgreSQL driver
- **motor**: Async MongoDB driver

## Best Practices Summary

1. **Use asyncio.run()** for entry point (Python 3.7+)
2. **Always await coroutines** to execute them
3. **Limit concurrency with semaphores** - unbounded `gather()` can exhaust resources
4. **Implement proper error handling** with try/except
5. **Use timeouts** to prevent hanging operations
6. **Pool connections** for better performance
7. **Never block the event loop** - use `asyncio.to_thread()` for sync code
8. **Use semaphores** for rate limiting external API calls
9. **Handle task cancellation** properly - always re-raise `CancelledError`
10. **Test async code** with pytest-asyncio
11. **Stay consistent** - fully sync or fully async, avoid mixing

## Reference Files

Load only the file you need for the task at hand:

- `references/patterns.md` — gather, task groups, semaphores, queues, async context managers
- `references/applications.md` — HTTP clients, producer/consumer, rate limiting, testing async code
- `references/performance.md` — blocking calls, event-loop starvation, connection reuse, profiling
