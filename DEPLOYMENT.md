# Despliegue en Render - Zapatillas API

## Enlace de la aplicación desplegada

**URL**: [https://zapatillas-api.onrender.com]

## Cambios realizados para el despliegue

### 1. Dockerfile

Se configuró el Dockerfile para ejecutar la aplicación con Uvicorn, usando la variable de entorno `PORT` que Render asigna dinámicamente:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN rm -f .env

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

**Notas importantes:**
- Se usa `python:3.11-slim` para reducir el tamaño de la imagen
- Se elimina el archivo `.env` para evitar conflictos con las variables de entorno de Render
- Se usa `${PORT:-8000}` para usar el puerto asignado por Render o 8000 por defecto

### 2. Configuración de Base de Datos (src/data/db.py)

La conexión a la base de datos lee las credenciales desde variables de entorno:

```python
db_user: str = os.getenv("DB_USER", "pablo")
db_password: str = os.getenv("DB_PASSWORD", "1234")
db_host: str = os.getenv("DB_HOST", "zapatillas-db")
db_port: str = os.getenv("DB_PORT", "5432")
db_name: str = os.getenv("DB_NAME", "zapatillas-db")

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
```

### 3. requirements.txt

Dependencias necesarias para el despliegue:

```
fastapi
uvicorn
sqlmodel
psycopg2-binary
jinja2
python-multipart
python-dotenv
```
## Proceso de despliegue manual (Projects)

### Paso 1: Crear la Base de Datos PostgreSQL

1. Iniciar sesión en [render.com](https://render.com)
2. Ir a **New** → **PostgreSQL**
3. Configurar:
   - **Name**: `zapatillas-db`
   - **Database**: `zapatillas_db`
   - **User**: `zapatillas_user`
   - **Region**: Elegir la más cercana
   - **Plan**: **Free**
4. Click en **Create Database**
5. Esperar a que se cree y copiar los datos de conexión desde la pestaña **Info**:
   - Hostname
   - Port
   - Database
   - Username
   - Password

### Paso 2: Crear el Web Service

1. Ir a **New** → **Web Service**
2. Conectar el repositorio de GitHub/GitLab
3. Configurar:
   - **Name**: `zapatillas-api`
   - **Region**: La misma que la base de datos
   - **Branch**: `main`
   - **Runtime**: **Docker**
   - **Plan**: **Free**

4. Añadir las **Environment Variables**:

   | Variable | Valor |
   |----------|-------|
   | `DB_USER` | (Username de la base de datos) |
   | `DB_PASSWORD` | (Password de la base de datos) |
   | `DB_HOST` | (Hostname de la base de datos) |
   | `DB_PORT` | `5432` |
   | `DB_NAME` | (Database name) |


