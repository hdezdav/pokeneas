#!/bin/bash
# ========================================
# Script de instalación de Docker en Ubuntu
# Para AWS EC2 - Proyecto Pokeneas
# ========================================

set -e  # Detener en caso de error

echo "=========================================="
echo "Instalando Docker en Ubuntu..."
echo "=========================================="

# Actualizar sistema
echo "1/7 Actualizando sistema..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Instalar dependencias
echo "2/7 Instalando dependencias..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Agregar GPG key de Docker
echo "3/7 Agregando GPG key de Docker..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Agregar repositorio Docker
echo "4/7 Agregando repositorio Docker..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Actualizar repositorios
echo "5/7 Actualizando repositorios..."
sudo apt-get update -y

# Instalar Docker Engine
echo "6/7 Instalando Docker Engine..."
sudo apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-compose-plugin

# Agregar usuario al grupo docker
echo "7/7 Configurando permisos..."
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# Verificar instalación
echo ""
echo "=========================================="
echo "✅ Docker instalado correctamente!"
echo "=========================================="
docker --version

echo ""
echo "⚠️  IMPORTANTE: Cierra esta sesión SSH y vuelve a conectarte"
echo "    para que los permisos de grupo se apliquen."
echo ""
echo "Después de reconectar, verifica con:"
echo "  docker run hello-world"
echo ""
