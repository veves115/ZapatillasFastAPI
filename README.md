# ZapatillasFastAPI

API REST para gestionar un catalogo de zapatillas.

## Requisitos

- Python 3.11+
- MySQL 8.0+

## Instalacion Local

```bash
# Clonar repositorio
git clone <url-repo>
cd ZapatillasFastAPI

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de MySQL

# Ejecutar en desarrollo
uvicorn src.main:app --reload
```

## Despliegue en Produccion (Debian/Ubuntu)

### 1. Preparar el servidor

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip nginx mysql-server -y
```

### 2. Configurar MySQL

```bash
sudo mysql_secure_installation

sudo mysql -u root -p
```

```sql
CREATE DATABASE zapatillas;
CREATE USER 'zapatillas_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON zapatillas.* TO 'zapatillas_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Configurar la aplicacion

```bash
cd /var/www
sudo git clone <url-repo> zapatillas
cd zapatillas

sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Configurar .env
sudo nano .env
```

### 4. Crear servicio systemd

```bash
sudo nano /etc/systemd/system/zapatillas.service
```

```ini
[Unit]
Description=Zapatillas FastAPI
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/zapatillas
Environment="PATH=/var/www/zapatillas/venv/bin"
ExecStart=/var/www/zapatillas/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 127.0.0.1:8000 src.main:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start zapatillas
sudo systemctl enable zapatillas
```

### 5. Configurar NGINX

```bash
sudo nano /etc/nginx/sites-available/zapatillas
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/zapatillas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL con Certbot (opcional)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /zapatillas | Lista todas |
| POST | /zapatillas | Crear nueva |
| GET | /zapatillas/{id} | Obtener por ID |
| PATCH | /zapatillas/{id} | Actualizar |
| DELETE | /zapatillas/{id} | Eliminar |
| GET | /docs | Swagger UI |
| GET | /redoc | ReDoc |

## Estructura

```
.
├── src/
│   ├── main.py              # Aplicacion FastAPI
│   ├── models/              # Modelos SQLModel
│   ├── data/                # Repositorio y DB
│   ├── routers/             # Endpoints API
│   ├── templates/           # Plantillas Jinja2
│   └── static/              # Archivos estaticos
├── requirements.txt
├── .env
└── README.md
```
