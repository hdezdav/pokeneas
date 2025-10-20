# ========================================
# GUÍA DE DESPLIEGUE AWS - POKENEAS
# ========================================

## PASO 1: CREAR 4 INSTANCIAS EC2

### 1.1 Ir a AWS Console
https://console.aws.amazon.com/ec2/v2/home

### 1.2 Crear Instancias (repetir 4 veces)

**Configuración:**
- Name: pokeneas-leader (primera), pokeneas-manager-1, pokeneas-manager-2, pokeneas-manager-3
- AMI: Ubuntu Server 22.04 LTS (Free tier eligible)
- Instance type: t2.micro (Free tier)
- Key pair: Crear nueva o usar existente (IMPORTANTE: guardar el .pem)
- Network settings:
  - Auto-assign Public IP: Enable
  - Security Group: Crear nueva "pokeneas-swarm-sg"
    ✅ SSH (22) - My IP
    ✅ HTTP (80) - 0.0.0.0/0
    ✅ Custom TCP (8000) - 0.0.0.0/0
    ✅ Custom TCP (2377) - Security Group ID (mismo grupo)
    ✅ Custom TCP (7946) - Security Group ID (mismo grupo)
    ✅ Custom UDP (7946) - Security Group ID (mismo grupo)
    ✅ Custom UDP (4789) - Security Group ID (mismo grupo)
- Storage: 8 GB (default)

**IMPORTANTE:** Anotar las IPs públicas de cada instancia.

---

## PASO 2: INSTALAR DOCKER EN LAS 4 INSTANCIAS

### 2.1 Conectarse a cada instancia (una por una)

```bash
# En PowerShell (Windows):
ssh -i "ruta\a\tu-key.pem" ubuntu@IP_PUBLICA_INSTANCIA
```

### 2.2 Ejecutar en CADA instancia:

```bash
#!/bin/bash

# Actualizar sistema
sudo apt-get update -y
sudo apt-get upgrade -y

# Instalar Docker
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Agregar GPG key de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Agregar repositorio Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker ubuntu

# Habilitar Docker al inicio
sudo systemctl enable docker
sudo systemctl start docker

# Verificar instalación
docker --version

# Salir y volver a entrar para aplicar permisos
exit
```

Después de ejecutar `exit`, vuelve a conectarte:
```bash
ssh -i "ruta\a\tu-key.pem" ubuntu@IP_PUBLICA_INSTANCIA
```

Verifica que Docker funciona sin sudo:
```bash
docker run hello-world
```

---

## PASO 3: INICIALIZAR DOCKER SWARM

### 3.1 En la INSTANCIA LÍDER (pokeneas-leader)

```bash
# Conectarse a la líder
ssh -i "tu-key.pem" ubuntu@IP_PUBLICA_LIDER

# Obtener IP privada de la instancia
IP_PRIVADA=$(hostname -I | awk '{print $1}')
echo "IP Privada: $IP_PRIVADA"

# Inicializar Swarm
docker swarm init --advertise-addr $IP_PRIVADA

# IMPORTANTE: Copiar el comando que aparece para unirse como MANAGER
# Se verá algo así:
# docker swarm join --token SWMTKN-1-xxxxx IP_PRIVADA_LIDER:2377
```

### 3.2 Obtener token de manager

Si no copiaste el token, obtenerlo de nuevo:
```bash
docker swarm join-token manager
```

---

## PASO 4: UNIR LAS OTRAS 3 INSTANCIAS COMO MANAGERS

### 4.1 En cada una de las 3 instancias restantes

```bash
# Conectarse a cada instancia
ssh -i "tu-key.pem" ubuntu@IP_PUBLICA_MANAGER_X

# Ejecutar el comando que copiaste (similar a este):
docker swarm join --token SWMTKN-1-xxxxxxxxxxxxx IP_PRIVADA_LIDER:2377
```

### 4.2 Verificar desde la LÍDER

```bash
# Listar nodos del cluster
docker node ls

# Deberías ver 4 nodos, todos como "manager" y uno como "Leader"
```

---

## PASO 5: DESPLEGAR EL SERVICIO POKENEAS

### 5.1 Crear archivo .env en la LÍDER

```bash
# Conectarse a la líder
ssh -i "tu-key.pem" ubuntu@IP_PUBLICA_LIDER

# Crear archivo .env
nano .env
```

Contenido del .env:
```env
FLASK_ENV=production
SECRET_KEY=super-secret-key-production-2025
S3_BUCKET=
S3_REGION=us-east-1
USE_S3_PRESIGNED=false
```

Guardar: Ctrl+O, Enter, Ctrl+X

### 5.2 Desplegar servicio con 10 réplicas

```bash
# Crear servicio
docker service create \
  --name pokeneas \
  --replicas 10 \
  --publish published=80,target=8000 \
  --env FLASK_ENV=production \
  --env SECRET_KEY=super-secret-key-production-2025 \
  --env S3_BUCKET= \
  --env S3_REGION=us-east-1 \
  --env USE_S3_PRESIGNED=false \
  TU_USUARIO_DOCKERHUB/pokeneas:latest

# Reemplaza TU_USUARIO_DOCKERHUB con tu usuario real
# Ejemplo: hdezdav/pokeneas:latest
```

### 5.3 Verificar despliegue

```bash
# Ver servicios
docker service ls

# Ver réplicas y en qué nodos están
docker service ps pokeneas

# Ver logs
docker service logs pokeneas --tail 50
```

---

## PASO 6: VERIFICACIÓN FINAL

### 6.1 Probar desde cualquier IP pública

```bash
# API JSON
curl http://IP_PUBLICA_CUALQUIER_INSTANCIA/api/pokenea

# Vista HTML
curl http://IP_PUBLICA_CUALQUIER_INSTANCIA/pokenea
```

### 6.2 Verificar balanceo de carga y container_id

Ejecuta varias veces:
```bash
for i in {1..20}; do
  curl http://IP_PUBLICA/api/pokenea | jq -r '.container_id'
done
```

Deberías ver diferentes container_id en cada petición (10 diferentes).

### 6.3 Probar desde navegador

Abre en tu navegador:
```
http://IP_PUBLICA_CUALQUIER_INSTANCIA/pokenea
```

Recarga varias veces y verifica que el container_id cambia.

---

## COMANDOS ÚTILES DE DOCKER SWARM

### Escalar servicio
```bash
docker service scale pokeneas=20
```

### Actualizar servicio
```bash
docker service update --image TU_USUARIO/pokeneas:latest pokeneas
```

### Eliminar servicio
```bash
docker service rm pokeneas
```

### Ver información de nodos
```bash
docker node ls
docker node inspect pokeneas-leader
```

### Drenar un nodo (no recibe más tareas)
```bash
docker node update --availability drain NOMBRE_NODO
```

### Activar nodo
```bash
docker node update --availability active NOMBRE_NODO
```

---

## TROUBLESHOOTING

### Error: No se puede conectar entre nodos
- Verifica que el Security Group permite tráfico entre las instancias
- Puertos necesarios: 2377, 7946, 4789

### Error: Servicio no inicia
```bash
docker service logs pokeneas --tail 100
```

### Ver recursos del cluster
```bash
docker node ls
docker service ps pokeneas
```

### Reiniciar servicio
```bash
docker service update --force pokeneas
```

---

## LIMPIEZA (cuando termines)

```bash
# Eliminar servicio
docker service rm pokeneas

# Dejar el swarm (en cada nodo manager)
docker swarm leave

# En la líder (forzar)
docker swarm leave --force

# Terminar instancias EC2 desde AWS Console
```

---

## CHECKLIST FINAL

- [ ] 4 instancias EC2 creadas
- [ ] Docker instalado en las 4
- [ ] Swarm inicializado en líder
- [ ] 3 managers unidos al cluster
- [ ] Servicio desplegado con 10 réplicas
- [ ] API responde en /api/pokenea
- [ ] Vista HTML responde en /pokenea
- [ ] Container_id varía entre peticiones
- [ ] Funciona desde cualquier IP pública del cluster

---

¡Éxito con tu despliegue! 🚀
