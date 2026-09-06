# API de Productos — REST y GraphQL

Backend de una aplicación web que expone la gestión de productos a través de **dos
protocolos**: servicios API REST y una API GraphQL. Construido con **Django**,
**Django REST Framework**, **Strawberry GraphQL** y **Django ORM**.

Módulo: Arquitectura de Aplicaciones Web — Unidades 2 y 3.

- **Unidad 2** — Servicios RESTful CRUD sobre base de datos.
- **Unidad 3** — Integración de la librería GraphQL.

Ambas capas comparten el mismo modelo y la misma capa de servicios: las reglas de negocio
se escriben una sola vez y cada protocolo es únicamente una puerta de entrada al dominio.

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
│   ├── api/                     # Capa REST
│   │   ├── serializers.py       # Validación y forma del JSON
│   │   ├── views.py             # Endpoints HTTP
│   │   ├── urls.py              # Rutas del módulo
│   │   └── handlers.py          # Manejo centralizado de errores
│   ├── graphql_api/             # Capa GraphQL
│   │   ├── types.py             # Tipos del esquema
│   │   ├── queries.py           # Consultas de lectura
│   │   ├── mutations.py         # Operaciones de escritura
│   │   └── schema.py            # Ensamblaje del esquema
│   ├── migrations/              # Migraciones generadas por el ORM
│   └── tests/
│       └── test_producto_api.py # 10 pruebas automatizadas
│
└── pruebas/
    └── Productos-API.postman_collection.json
```

**Flujo de una petición:**

```
Cliente REST  → api/urls.py → api/views.py → serializers.py
                                     ↘
                                      services.py  (reglas de negocio)
                                     ↗        ↓
Cliente GraphQL → /graphql/ → queries.py    repositories.py (ORM)
                              mutations.py        ↓
                                              Base de datos
```

Ambos protocolos convergen en `services.py`. Si algo falla en la capa REST,
`handlers.py` intercepta la excepción y devuelve siempre la misma estructura JSON de
error; en GraphQL los fallos se reportan en el arreglo `errors` de la respuesta.

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

## Endpoints REST

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

## API GraphQL

Toda la API GraphQL se expone en **un único endpoint**, a diferencia de REST que necesita
una ruta por recurso y operación:

```
POST http://127.0.0.1:8000/graphql/
```

Abriendo esa misma URL en el navegador se carga **GraphiQL**, una interfaz interactiva
que incluye el explorador del esquema. El esquema no se escribe a mano: Strawberry lo
deriva de las anotaciones de tipo de Python.

### Operaciones disponibles

| Tipo | Operación | Descripción |
|------|-----------|-------------|
| Query | `productos` | Lista todos los productos |
| Query | `producto(id)` | Consulta un producto por identificador |
| Query | `buscarProductos(texto)` | Filtra por coincidencia en el nombre |
| Mutation | `crearProducto(datos)` | Crea un producto |
| Mutation | `actualizarProducto(id, datos)` | Actualiza los campos enviados |
| Mutation | `eliminarProducto(id)` | Elimina un producto |

### Consultas declarativas

El cliente define la forma de la respuesta. Misma consulta, distinto resultado:

```graphql
{
  productos {
    id
    nombre
    descripcion
    precio
  }
}
```

```graphql
{
  productos {
    nombre
  }
}
```

La segunda devuelve únicamente los nombres. En REST, el servidor decide qué campos
entrega y el cliente recibe información que quizá no necesita.

### Mutaciones

```graphql
mutation {
  crearProducto(datos: {
    nombre: "Teclado mecánico"
    descripcion: "Switches rojos"
    precio: "250000.00"
  }) {
    id
    nombre
    precio
  }
}
```

```graphql
mutation {
  actualizarProducto(id: 1, datos: { precio: "310000.00" }) {
    id
    nombre
    precio
  }
}
```

```graphql
mutation {
  eliminarProducto(id: 2) {
    exito
    mensaje
  }
}
```

### Configuración aplicada

1. Instalación de la librería con pip:

   ```bash
   pip install strawberry-graphql-django
   ```

2. Registro de `strawberry_django` en `INSTALLED_APPS` (`config/settings.py`).

3. Creación del paquete `productos/graphql_api/` con los tipos, las consultas, las
   mutaciones y el ensamblaje del esquema.

4. Exposición del endpoint en `config/urls.py`:

   ```python
   path(
       "graphql/",
       csrf_exempt(GraphQLView.as_view(schema=schema, graphql_ide="graphiql")),
       name="graphql",
   ),
   ```

   El parámetro `graphql_ide` habilita GraphiQL. `csrf_exempt` permite probar el endpoint
   desde clientes externos como Postman o Insomnia.

### Por qué Strawberry y no Graphene

| Criterio | Graphene-Django | Strawberry |
|---|---|---|
| Definición de tipos | Clases con campos propios | Anotaciones de tipo nativas de Python |
| Soporte `async` | Limitado | Nativo |
| Mantenimiento | Ritmo lento | Activo |
| Compatibilidad Django 6 | Irregular | Verificada |

---

## Ejemplos REST

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

En REST, todas las respuestas de error comparten la misma estructura:

| Situación                       | Código | Identificador             |
|---------------------------------|--------|---------------------------|
| Datos inválidos                 | 400    | `error_de_solicitud`      |
| Producto inexistente            | 404    | `producto_no_encontrado`  |
| Nombre de producto repetido     | 409    | `nombre_duplicado`        |
| Error no previsto               | 500    | `error_interno`           |

En GraphQL la semántica es distinta: el protocolo responde siempre con HTTP 200 y
reporta los fallos en el arreglo `errors` del cuerpo de la respuesta.

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

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Framework | Django 5.1+ |
| API REST | Django REST Framework |
| API GraphQL | Strawberry GraphQL (`strawberry-graphql-django`) |
| ORM | Django ORM |
| Documentación REST | drf-spectacular (OpenAPI / Swagger) |
| Documentación GraphQL | GraphiQL (esquema autogenerado) |
| Base de datos | SQLite (local) / PostgreSQL (nube) |
