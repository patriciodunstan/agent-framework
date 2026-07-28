# ADR-0003: Instalador Python cero-deps + TOML/tomllib + Python 3.11+

- **Estado**: aceptada
- **Fecha**: 2026-07-28
- **Ámbito**: proyecto

## Contexto

El instalador (`install.py`) debe correr en cualquier máquina del desarrollador —
incluidos entornos nuevos o restringidos— sin necesidad de `pip install`. El objetivo
es que restaurar el entorno de agente sea tan simple como clonar el repo y ejecutar
un script Python.

El formato de los presets y profiles requiere un parser. Las opciones evaluadas:

| Formato | Parser | Dependencia externa |
|---------|--------|---------------------|
| JSON | `json` (stdlib) | Ninguna, disponible siempre |
| TOML | `tomllib` (stdlib desde 3.11) | Ninguna en Python 3.11+ |
| YAML | `PyYAML` | Sí — rompe el objetivo cero-deps |

TOML es más legible que JSON para archivos de configuración editados a mano (los presets
se editan, no se generan), y `tomllib` está en la stdlib desde Python 3.11.

Python 3.11 salió en octubre 2022 y es la versión mínima compatible con soporte activo
al momento del diseño. Fijar el mínimo en 3.11 es razonable para máquinas de desarrollo.

## Decisión

1. El instalador usa **exclusivamente la stdlib de Python**: `argparse`, `pathlib`,
   `string.Template`, `tomllib`, `shutil`. Cero dependencias externas.
2. El formato de serialización de presets, profiles y addons es **TOML** (`.toml`),
   leído con `tomllib`.
3. La versión mínima de Python requerida es **3.11** (necesaria para `tomllib`).
4. El runtime de tests (`pytest`, `ruff`) son dependencias de **desarrollo** declaradas
   en `pyproject.toml` bajo `[tool.pytest.ini_options]` y `[dependency-groups]`, no
   dependencias de ejecución del instalador.

## Consecuencias

- **Permitido**: usar cualquier módulo de la stdlib de Python 3.11+ en el framework.
- **Prohibido**: importar en `framework/` o `install.py` cualquier paquete no incluido
  en la stdlib de Python 3.11 (e.g., `pydantic`, `click`, `toml` — este último es
  distinto de `tomllib`).
- **Obligatorio**: documentar Python 3.11+ como requisito mínimo en el README.
- **Violación a marcar en review**: cualquier `import` en `framework/` o `install.py`
  de un paquete que no sea stdlib; bajar el `requires-python` en `pyproject.toml` por
  debajo de `>=3.11`.
