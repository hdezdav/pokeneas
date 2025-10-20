# Pokeneas - Aplicación Flask con S3

Aplicación Flask profesional que muestra Pokeneas (Pokémon antioqueños) con imágenes almacenadas en Amazon S3.

## Características

- 🏗️ Arquitectura modular con Application Factory y Blueprints
- 🎨 Interfaz moderna y minimalista
- 🐳 Containerización con Docker
- 🧪 Suite de pruebas con pytest
- 🔄 CI/CD con GitHub Actions
- ☁️ Integración con AWS S3 (URLs públicas y presignadas)

## Estructura del Proyecto

```
pokeneas/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuración por entornos
│   ├── blueprints/
│   │   ├── __init__.py
│   │   └── pokeneas.py       # Rutas principales
│   ├── services/
│   │   ├── __init__.py
│   │   └── pokeneas_service.py  # Lógica de negocio
│   └── storage/
│       ├── __init__.py
│       └── s3.py             # Cliente S3
├── templates/
│   ├── base.html
│   └── pokenea.html
├── static/
│   └── css/
│       └── base.css
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   └── test_s3.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Pokeneas Disponibles

La aplicación incluye 10 Pokeneas únicos:

1. **Arepa** - El pokenea más paisa
2. **Bandeja** - Maestro de la abundancia
3. **Parcero** - El más social
4. **Guaro** - Espíritu festivo
5. **Silletero** - Guardián de las flores
6. **Empanada** - Crujiente y versátil
7. **Mondongo** - Sabio ancestral
8. **Mazamorra** - Dulce tradición
9. **Paisita** - Espíritu emprendedor
10. **Fríjoles** - Esencia antioqueña

## Endpoints

### API REST

**GET /api/pokenea**

Retorna un Pokenea aleatorio en formato JSON.

```json
{
  "id": 1,
  "nombre": "Arepa",
  "altura": "0.3m",
  "habilidad": "Doble Sabor",
  "container_id": "a3f2b1c4d5e6"
}
```

### Vista Web

**GET /pokenea**

Renderiza una página HTML con:
- Imagen del Pokenea
- Frase filosófica
- Container ID

## Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura las variables:

```bash
# Flask
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui

# AWS S3
S3_BUCKET=tu-bucket-name
S3_REGION=us-east-1
USE_S3_PRESIGNED=false
S3_PUBLIC_BASE_URL=https://tu-bucket.s3.us-east-1.amazonaws.com

# Credenciales AWS (solo si USE_S3_PRESIGNED=true)
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_SESSION_TOKEN=tu-session-token  # Opcional

# Configuración de URLs presignadas
PRESIGNED_URL_EXPIRATION=3600
```

### Modos de operación S3

#### Modo Público (USE_S3_PRESIGNED=false)

Las imágenes deben estar públicamente accesibles en S3. La URL se construye como:
```
https://{bucket}.s3.{region}.amazonaws.com/{key}
```

#### Modo Presignado (USE_S3_PRESIGNED=true)

Genera URLs temporales firmadas. Requiere credenciales AWS válidas.

## Instalación y Ejecución

### Desarrollo Local (sin Docker)

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Ejecutar aplicación
flask run --host=0.0.0.0 --port=8000
```

### Con Docker

```bash
# Construir imagen
docker build -t pokeneas:latest .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env pokeneas:latest

# O usar docker-compose
docker-compose up --build
```

### Verificar Container ID

Ejecuta múltiples instancias para ver diferentes container IDs:

```bash
docker-compose up --scale web=3
```

## Pruebas

```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Ejecutar todas las pruebas
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Ejecutar linters
black app/ tests/
flake8 app/ tests/
isort app/ tests/
```

## CI/CD con GitHub Actions

El proyecto incluye un workflow que:

1. ✅ Ejecuta linters (black, flake8, isort)
2. ✅ Ejecuta suite de pruebas
3. 🐳 Construye imagen Docker multi-plataforma
4. 📦 Publica en Docker Hub (en push a main o tags)

### Configurar Secrets en GitHub

```
DOCKERHUB_USERNAME=tu-usuario
DOCKERHUB_TOKEN=tu-token-de-acceso
```

## Uso de la Aplicación

### Obtener Pokenea Aleatorio (JSON)

```bash
curl http://localhost:8000/api/pokenea
```

### Ver Pokenea en el Navegador

Visita: http://localhost:8000/pokenea

## Configuración de S3

### 1. Crear Bucket

```bash
aws s3 mb s3://tu-bucket-pokeneas --region us-east-1
```

### 2. Subir Imágenes

```bash
aws s3 cp pokeneas/arepa-001.jpg s3://tu-bucket-pokeneas/pokeneas/arepa-001.jpg
```

### 3. Configurar Acceso Público (Opcional)

Si usas `USE_S3_PRESIGNED=false`, desactiva el bloqueo de acceso público:

1. Ve a AWS Console → S3 → Tu Bucket
2. Permisos → Bloqueo de acceso público
3. Desactiva "Bloquear todo el acceso público"
4. Aplica una política de bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::tu-bucket-pokeneas/*"
    }
  ]
}
```

## Estructura de Keys de Imágenes

Las imágenes deben seguir esta convención:

```
pokeneas/arepa-001.jpg
pokeneas/bandeja-002.jpg
pokeneas/parcero-003.jpg
...
```

## Seguridad

- ❌ **NO** subas credenciales al repositorio
- ✅ Usa variables de entorno
- ✅ Añade `.env` al `.gitignore`
- ✅ Usa `.env.example` como plantilla
- ✅ Rota credenciales regularmente
- ✅ Usa IAM roles cuando sea posible

## Troubleshooting

### Error: "Unable to locate credentials"

- Verifica que `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY` estén configuradas
- Asegúrate de que el archivo `.env` se esté cargando correctamente

### Error: "Access Denied" en S3

- Verifica permisos del bucket
- Confirma que la política permite `s3:GetObject`
- Si usas presigned URLs, verifica que las credenciales sean válidas

### Imagen no se muestra

- Verifica que la key de la imagen exista en S3
- Confirma que `S3_BUCKET` y `S3_REGION` sean correctos
- Revisa logs del contenedor: `docker logs <container_id>`

## Licencia

MIT

## Autor

Tu Nombre - Proyecto Pokeneas 2025
