#!/bin/bash

echo "🔧 Reparando entorno virtual..."

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: No se encuentra app.py${NC}"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

# Activar entorno virtual
echo -e "${YELLOW}🚀 Activando entorno virtual...${NC}"
source venv/bin/activate

# Verificar activación
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Entorno virtual activado${NC}"
else
    echo -e "${RED}❌ Error al activar entorno virtual${NC}"
    exit 1
fi

# Actualizar pip
echo -e "${YELLOW}📦 Actualizando pip...${NC}"
pip install --upgrade pip

# Instalar Flask
echo -e "${YELLOW}📦 Instalando Flask...${NC}"
pip install flask

# Instalar dependencias desde requirements.txt
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 Instalando dependencias desde requirements.txt...${NC}"
    pip install -r requirements.txt
fi

# Verificar instalación
echo -e "${GREEN}📋 Paquetes instalados:${NC}"
pip list | grep -E "Flask|Jinja2|Werkzeug"

echo ""
echo -e "${GREEN}✅ Reparación completada${NC}"
echo -e "${YELLOW}📝 Para ejecutar la aplicación:${NC}"
echo "   python app.py"
echo ""
echo -e "${GREEN}🌐 Dashboard: http://localhost:5000/dashboard${NC}"
