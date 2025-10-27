#!/bin/bash

echo "🚀 Inicializando Malware Detection API..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar Python
echo -e "${BLUE}[1/6]${NC} Verificando versión de Python..."
python --version
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Python no encontrado. Instala Python 3.12.3${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python detectado"
echo ""

# 2. Crear entorno virtual
echo -e "${BLUE}[2/6]${NC} Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${YELLOW}ℹ${NC}  Entorno virtual ya existe"
fi
echo ""

# 3. Activar entorno virtual
echo -e "${BLUE}[3/6]${NC} Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Entorno virtual activado"
echo ""

# 4. Instalar dependencias
echo -e "${BLUE}[4/6]${NC} Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencias instaladas"
echo ""

# 5. Configurar Django
echo -e "${BLUE}[5/6]${NC} Configurando Django..."
python manage.py migrate
python manage.py collectstatic --noinput
echo -e "${GREEN}✓${NC} Django configurado"
echo ""

# 6. Verificar modelo
echo -e "${BLUE}[6/6]${NC} Verificando modelo..."
if [ -f "models/malware_detector_rf.pkl" ]; then
    echo -e "${GREEN}✓${NC} Modelo encontrado"
else
    echo -e "${YELLOW}⚠️  Modelo no encontrado. Ejecuta el notebook Random_Forest.ipynb primero.${NC}"
fi
echo ""

echo -e "${GREEN}🎉 ¡Configuración completada!${NC}"
echo ""
echo -e "${BLUE}Para iniciar el servidor:${NC}"
echo "  python manage.py runserver"
echo ""
echo -e "${BLUE}La API estará disponible en:${NC}"
echo "  http://localhost:8000/api/"
echo ""
