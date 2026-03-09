#!/bin/bash

echo "🔄 Resubiendo todo el proyecto a GitHub..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: No se encuentra app.py${NC}"
    echo "Asegúrate de estar en el directorio flask_linguistica"
    exit 1
fi

echo -e "${YELLOW}📁 Directorio actual: $(pwd)${NC}"

# Mostrar estado actual
echo -e "${YELLOW}📊 Estado actual del repositorio:${NC}"
git status

# Preguntar si continuar
read -p "¿Continuar con la subida? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${RED}❌ Operación cancelada${NC}"
    exit 1
fi

# Agregar todos los archivos
echo -e "${YELLOW}📦 Agregando archivos...${NC}"
git add .

# Mostrar qué se agregó
echo -e "${GREEN}✅ Archivos agregados:${NC}"
git status --short

# Hacer commit
echo -e "${YELLOW}💬 Escribe el mensaje del commit:${NC}"
read -p "> " commit_message

if [ -z "$commit_message" ]; then
    commit_message="Actualización automática: Aplicación de lingüística con flashcards"
fi

git commit -m "$commit_message"

# Subir a GitHub
echo -e "${YELLOW}🚀 Subiendo a GitHub...${NC}"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Proyecto subido exitosamente a GitHub${NC}"
    echo -e "${GREEN}📎 Repositorio: https://github.com/Hernank10/-subordinadas_percepci-n${NC}"
    
    # Mostrar últimos commits
    echo -e "${YELLOW}📜 Últimos commits:${NC}"
    git log --oneline -3
else
    echo -e "${RED}❌ Error al subir a GitHub${NC}"
    exit 1
fi
