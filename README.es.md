# Automatización QA con Playwright + pytest

[![CI](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Playwright](https://img.shields.io/badge/playwright-1.63-2EAD33)
![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)

*Read in [English](README.md).*

Proyecto de portfolio que muestra cómo pruebo una aplicación web de punta a punta: una
**suite de pruebas de UI** para la tienda demo [Sauce Demo](https://www.saucedemo.com)
con **Playwright + pytest** y el patrón **Page Object Model**, una pequeña **suite de API REST**
contra [JSONPlaceholder](https://jsonplaceholder.typicode.com), **documentación de QA**
(plan de pruebas, casos de prueba, reportes de bugs) y **CI en GitHub Actions** que ejecuta
todo en cada push y publica un reporte HTML.

> Es un proyecto personal de portfolio sobre sitios demo públicos, no un trabajo para clientes.

## Qué se prueba

| Área | Tests | Puntos clave |
|------|------:|-------------|
| Login / logout | 9 | login válido, usuario bloqueado, contraseña incorrecta, campos vacíos (parametrizado), cerrar error, logout, acceso directo bloqueado tras logout |
| Inventario | 6 | nombres y precios del catálogo, orden por defecto, orden por nombre y precio en ambos sentidos |
| Carrito | 6 | agregar/quitar desde la grilla y el carrito, contador del ícono, carrito se mantiene al navegar |
| Checkout | 6 | compra completa hasta la confirmación, validación de campos obligatorios (×3), **subtotal + 8 % de impuesto = total**, cancelar |
| Bugs conocidos (`problem_user`) | 4 | imágenes incorrectas, orden roto, "Add to cart" que falla, campo Apellido roto — `xfail(strict=True)` |
| API REST | 12 | GET/POST/PUT/PATCH/DELETE, filtros, rutas anidadas, 404, validación con JSON Schema, tiempo de respuesta |
| **Total** | **43** | |

Cada test automatizado está vinculado a un ID de caso de prueba en [`docs/test-cases.md`](docs/test-cases.md)
(la documentación detallada está en inglés).

## Resultados

Salida copiada de una ejecución real de CI
([run #2](https://github.com/gabrielvalle-491/qa-automation-playwright/actions/runs/37161068047),
Chromium headless en `ubuntu-latest`, 03/10/2026):

```
collected 43 items

tests/api/test_posts.py .........                                        [ 20%]
tests/api/test_users.py ...                                              [ 27%]
tests/ui/test_cart.py ......                                             [ 41%]
tests/ui/test_checkout.py ....                                           [ 51%]
tests/ui/test_inventory.py ....                                          [ 60%]
tests/ui/test_login.py .......                                           [ 76%]
tests/ui/test_problem_user.py xxxx                                       [ 86%]
tests/ui/test_checkout.py .                                              [ 88%]
tests/ui/test_inventory.py ..                                            [ 93%]
tests/ui/test_login.py .                                                 [ 95%]
tests/ui/test_checkout.py .                                              [ 97%]
tests/ui/test_login.py .                                                 [100%]

=========================== short test summary info ============================
XFAIL tests/ui/test_problem_user.py::test_each_product_has_its_own_image[chromium] - BUG-001: every product shows the same placeholder image
XFAIL tests/ui/test_problem_user.py::test_sort_by_price_low_to_high[chromium] - BUG-002: sorting dropdown has no effect for problem_user
XFAIL tests/ui/test_problem_user.py::test_add_every_product_to_cart[chromium] - BUG-003: 'Add to cart' does nothing for some products
XFAIL tests/ui/test_problem_user.py::test_checkout_with_valid_information[chromium] - BUG-004: Last Name field cannot be filled, checkout is blocked
======================== 39 passed, 4 xfailed in 32.96s ========================
```

- **39 pasaron** — todas las verificaciones funcionales con `standard_user` y la API.
- **4 xfailed** — defectos reales de `problem_user`, documentados en [`docs/bug-reports.md`](docs/bug-reports.md).
  Son xfail *estrictos*: si algún día se corrige uno, la suite se pone en rojo y se puede cerrar el reporte.

El reporte HTML (y capturas de pantalla de cualquier fallo) se adjunta a cada ejecución como
artefacto `test-report`: pestaña **Actions** → la ejecución → *Artifacts*.

## Estructura del proyecto

```
qa-automation-playwright/
├── pages/                    # Page Object Model
├── tests/
│   ├── ui/                   # tests de Playwright (saucedemo.com)
│   └── api/                  # tests con requests (jsonplaceholder)
├── utils/data.py             # usuarios demo, catálogo, tasa de impuesto
├── conftest.py               # fixtures de login, marcadores ui/api automáticos
├── docs/                     # plan de pruebas, casos de prueba, reportes de bugs
├── .github/workflows/ci.yml  # lint + tests + reporte HTML
├── pytest.ini
└── requirements.txt
```

## Cómo ejecutarlo

Requisitos: Python 3.11+.

```bash
git clone https://github.com/gabrielvalle-491/qa-automation-playwright.git
cd qa-automation-playwright
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                                   # todo (headless)
pytest -m api                            # solo API
pytest -m ui --headed --slowmo 300       # ver el navegador
pytest -m smoke                          # solo camino crítico
pytest --html=reports/report.html --self-contained-html   # reporte HTML
```

## Decisiones de diseño

- **Page Object Model**: los localizadores están en un solo lugar y los tests se leen como los casos de prueba.
- **Localizadores `data-test`**: estables ante cambios de CSS o diseño.
- **Sin `sleep()`**: solo la espera automática de Playwright (aserciones `expect(...)`), que reintenta hasta que se cumple la condición o vencen 10 s.
- **Tests aislados**: contexto de navegador nuevo por test y login mediante fixtures.
- **Datos parametrizados** para validaciones y ordenamientos.
- **xfail estricto para bugs conocidos**: la suite queda en verde y los bugs siguen visibles.
- **Validación de esquema** de las respuestas de la API con `jsonschema`, no solo códigos de estado.

## Herramientas

Python 3.11 · pytest · Playwright (API sync) · pytest-playwright · pytest-html · requests ·
jsonschema · ruff · GitHub Actions

## Documentación

- [Plan de pruebas](docs/test-plan.md) — alcance, enfoque, entornos, criterios de entrada/salida, riesgos
- [Casos de prueba](docs/test-cases.md) — 47 casos con prioridad y estado de automatización
- [Reportes de bugs](docs/bug-reports.md) — 4 defectos con pasos, esperado vs. obtenido, severidad y evidencia

## Licencia

[MIT](LICENSE) © 2026 Gabriel Valle

---

**Gabriel Valle — QA & Automation · Villa Mercedes, Argentina · Remoto**
