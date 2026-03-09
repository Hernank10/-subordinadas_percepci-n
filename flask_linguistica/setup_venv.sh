#!/bin/bash

echo "🔧 Configurando entorno virtual para Flask..."

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: No se encuentra app.py${NC}"
    echo "Asegúrate de estar en el directorio flask_linguistica"
    exit 1
fi

echo -e "${GREEN}📍 Directorio actual: $(pwd)${NC}"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
else
    echo -e "${GREEN}✅ El entorno virtual ya existe${NC}"
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

# Instalar dependencias
echo -e "${YELLOW}📦 Instalando dependencias desde requirements.txt...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias instaladas correctamente${NC}"
else
    echo -e "${RED}❌ Error al instalar dependencias${NC}"
    exit 1
fi

# Mostrar paquetes instalados
echo -e "${GREEN}📋 Paquetes instalados:${NC}"
pip list | grep Flask

echo ""
echo -e "${GREEN}✅ Configuración completada exitosamente!${NC}"
echo -e "${YELLOW}📝 Para ejecutar la aplicación:${NC}"
echo "   python app.py"
echo ""
echo -e "${GREEN}🌐 La aplicación estará disponible en: http://localhost:5000${NC}"
