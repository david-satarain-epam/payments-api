# Payment API — Demo

Payments Microservice for demo purposes. 

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/` | Service info |

## Estructura

- `src/` — Source Code
- `governance/` — Risk politics, test map and contracts diff
- `openapi/` — OpenAPI Specifications
- `tests/` — Tests (unit, integration, contract, smoke)

## Ejecutar localmente

```bash
pip install -r requirements.txt
python app.py