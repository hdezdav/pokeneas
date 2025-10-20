# 🎮 Pokeneas

Aplicación web Flask que muestra **Pokeneas** - criaturas inspiradas en la cultura paisa de Antioquia, Colombia.

## 📖 ¿Qué es esto?

Pokeneas es una parodia de Pokémon con personajes basados en la gastronomía y cultura antioqueña como:
- **Arepa** - El pokenea más paisa
- **Bandeja** - Maestro de la abundancia  
- **Parcero** - El más social
- Y 7 más...

## ✨ Características

- � **2 rutas principales:**
  - `/api/pokenea` - Retorna JSON con un Pokenea aleatorio
  - `/pokenea` - Vista HTML con imagen y frase filosófica
- 🐳 **Dockerizado** - Listo para desplegar con Docker Swarm
- ☁️ **Imágenes en S3** - Integración con Amazon S3
- 🔄 **CI/CD** - Build automático a DockerHub con GitHub Actions
- 🎨 **Diseño minimalista** - Interfaz moderna con dark mode

## 🚀 Inicio Rápido

### Desarrollo Local

```powershell
# 1. Clonar repositorio
git clone https://github.com/hdezdav/pokeneas.git
cd pokeneas

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env con tus valores (opcional S3)

# 5. Ejecutar
python run.py
```

Visita: http://localhost:8000/pokenea

### Con Docker

```powershell
# Construir y ejecutar
docker-compose up --build

# O directamente
docker build -t pokeneas .
docker run -p 8000:8000 pokeneas
```

## 🎯 Endpoints

| Ruta | Método | Descripción | Respuesta |
|------|--------|-------------|-----------|
| `/api/pokenea` | GET | Pokenea aleatorio en JSON | `{id, nombre, altura, habilidad, container_id}` |
| `/pokenea` | GET | Vista HTML con imagen y frase | HTML |
| `/health` | GET | Health check | `{status: "healthy"}` |

## 📦 Tecnologías

- **Backend:** Flask 3.0
- **Storage:** AWS S3 (boto3)
- **Container:** Docker
- **CI/CD:** GitHub Actions
- **Deploy:** Docker Swarm en AWS EC2

## 👨‍💻 Desarrollo

```powershell
# Ejecutar tests
pytest -v

# Ver cobertura
pytest --cov=app

# Linters
black app/ tests/
flake8 app/ tests/
```

## 📄 Licencia

MIT

---

**Hecho con ❤️ en Medellín, Colombia** 🇨🇴

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
