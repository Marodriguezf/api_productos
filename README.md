# API de Productos — Servicios RESTful CRUD

Backend de una aplicación web que expone servicios API REST para gestionar productos,
construido con **Django REST Framework** y **Django ORM**.

Módulo: Arquitectura de Aplicaciones Web — Unidad 2.

---

## Arquitectura de la solución

El proyecto está organizado en capas con responsabilidades separadas, de modo que la
lógica de negocio no queda mezclada con el transporte HTTP ni con el acceso a datos.

```
api-productos/
├── manage.py                    # Utilidad de línea de comandos
├── requirements.txt             # Dependencias
├── .env.example                 # Plantilla de variables de entorno
├── .gitignore
│
├── config/                      # Configuración del proyecto
│   ├── settings.py              # Ajustes, base de datos, DRF
│   ├── urls.py                  # Enrutamiento raíz + Swagger
│   ├── wsgi.py
│   └── asgi.py
│
├── productos/                   # Aplicación de dominio
│   ├── models.py                # Entidad Producto (ORM)
│   ├── repositories.py          # Acceso a datos
│   ├── services.py              # Reglas de negocio
│   ├── admin.py
│   ├── apps.py
│   ├── domain/
│   │   └── exceptions.py        # Excepciones propias del dominio
│   ├── api/
│   │   ├── serializers.py       # Validación y forma del JSON
│   │   ├── views.py             # Endpoints HTTP
│   │   ├── urls.py              # Rutas del módulo
│   │   └── handlers.py          # Manejo centralizado de errores
│   ├── migrations/              # Migraciones generadas por el ORM
│   └── tests/
│       └── test_producto_api.py # 10 pruebas automatizadas
│
└── pruebas/
    └── Productos-API.postman_collection.json
```

**Flujo de una petición:**

```
Cliente HTTP → urls.py → views.py → serializers.py (validación)
                            ↓
                       services.py (reglas de negocio)
                            ↓
                     repositories.py (ORM)
                            ↓
                       Base de datos
```

Si algo falla en cualquier punto, `handlers.py` intercepta la excepción y devuelve
siempre la misma estructura JSON de error.

---

## Modelo de datos

| Campo            | Tipo          | Descripción                                |
|------------------|---------------|--------------------------------------------|
| `id`             | BigAutoField  | Identificador único (generado por el ORM)  |
| `nombre`         | CharField(150)| Nombre del producto, único                 |
| `descripcion`    | TextField(500)| Descripción breve                          |
| `precio`         | Decimal(12,2) | Precio, no admite valores negativos        |
| `creado_en`      | DateTime      | Fecha de creación (automática)             |
| `actualizado_en` | DateTime      | Fecha de última modificación (automática)  |

La tabla `productos` es creada por el ORM mediante migraciones. No se escribe SQL manual.

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/USUARIO/api-productos.git
cd api-productos

# 2. Crear y activar el entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux

# 5. Crear las tablas
python manage.py makemigrations
python manage.py migrate

# 6. Levantar el servidor
python manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

---

## Base de datos

El proyecto soporta dos modos sin cambiar una sola línea de código:

- **Sin `DATABASE_URL`** → usa SQLite local (`db.sqlite3`).
- **Con `DATABASE_URL`** → usa PostgreSQL en la nube (Supabase, Render, Neon).

Ejemplo para Supabase en el archivo `.env`:

```
DATABASE_URL=postgresql://postgres.xxxx:PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## Endpoints

| Método   | Ruta                    | Descripción                     | Respuesta |
|----------|-------------------------|---------------------------------|-----------|
| `GET`    | `/api/productos`        | Lista todos los productos       | 200       |
| `POST`   | `/api/productos`        | Crea un producto                | 201       |
| `GET`    | `/api/productos/{id}`   | Consulta un producto            | 200 / 404 |
| `PUT`    | `/api/productos/{id}`   | Actualiza un producto completo  | 200 / 404 |
| `PATCH`  | `/api/productos/{id}`   | Actualiza campos puntuales      | 200 / 404 |
| `DELETE` | `/api/productos/{id}`   | Elimina un producto             | 204 / 404 |

Documentación interactiva:

- Swagger UI → `http://127.0.0.1:8000/api/docs/`
- ReDoc → `http://127.0.0.1:8000/api/redoc/`
- Esquema OpenAPI → `http://127.0.0.1:8000/api/schema/`

---

## Ejemplos

**Crear un producto**

```http
POST /api/productos
Content-Type: application/json

{
  "nombre": "Teclado mecánico",
  "descripcion": "Teclado con switches rojos",
  "precio": "250000.00"
}
```

Respuesta `201 Created`:

```json
{
  "exito": true,
  "datos": {
    "id": 1,
    "nombre": "Teclado mecánico",
    "descripcion": "Teclado con switches rojos",
    "precio": "250000.00",
    "creado_en": "2026-08-16T18:09:28-05:00",
    "actualizado_en": "2026-08-16T18:09:28-05:00"
  }
}
```

**Error controlado** — `404 Not Found`:

```json
{
  "exito": false,
  "error": {
    "codigo": "producto_no_encontrado",
    "mensaje": "El producto solicitado no existe.",
    "detalles": {}
  }
}
```

---

## Manejo de errores

| Situación                       | Código | Identificador             |
|---------------------------------|--------|---------------------------|
| Datos inválidos                 | 400    | `error_de_solicitud`      |
| Producto inexistente            | 404    | `producto_no_encontrado`  |
| Nombre de producto repetido     | 409    | `nombre_duplicado`        |
| Error no previsto               | 500    | `error_interno`           |

Todas las respuestas de error comparten la misma estructura, lo que facilita el
manejo desde cualquier cliente.

---

## Pruebas

```bash
python manage.py test
```

Cubren los cuatro métodos (GET, POST, PUT, DELETE) y los casos de error.

Para pruebas manuales, importar en Postman:
`pruebas/Productos-API.postman_collection.json`

---

## Tecnologías

- Django 5.1+ y Django REST Framework
- Django ORM
- drf-spectacular (OpenAPI / Swagger)
- SQLite (local) / PostgreSQL (nube)
