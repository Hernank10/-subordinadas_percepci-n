#!/bin/bash

echo "📤 Subiendo cambios del Dashboard a GitHub..."
echo "=============================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Función para mostrar progreso
show_progress() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Ir al directorio de la aplicación
cd /workspaces/-subordinadas_percepci-n/flask_linguistica

# Verificar cambios
show_progress "Verificando cambios..."
git status

# Preguntar si continuar
read -p "¿Continuar con la subida? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${RED}❌ Operación cancelada${NC}"
    exit 1
fi

# Agregar archivos principales
show_progress "Agregando archivos modificados..."

# Archivos de la aplicación
git add app.py
git add templates/dashboard.html
git add templates/flashcards.html
git add templates/base.html
git add data/ejercicios_flashcards.json

# Scripts de utilidad
git add *.sh 2>/dev/null

# README principal
cd /workspaces/-subordinadas_percepci-n
git add README.md 2>/dev/null

cd /workspaces/-subordinadas_percepci-n/flask_linguistica

# Mostrar qué se agregó
echo -e "${GREEN}✅ Archivos agregados:${NC}"
git status --short

# Hacer commit
show_progress "Haciendo commit..."
git commit -m "feat: Implementar dashboard de usuario y sistema de progreso para flashcards

- Nuevo dashboard con estadísticas en tiempo real
- Sistema de seguimiento de progreso para 100 flashcards
- Registro de respuestas (aciertos/fallos) con tiempos
- Rachas de estudio y sistema de logros (5 niveles)
- Filtros mejorados y modo de estudio (pendientes/revisión)
- Gráficos de progreso por categoría y dificultad
- Interfaz mejorada con Bootstrap 5
- Scripts de utilidad para gestión del entorno"

# Verificar si el commit fue exitoso
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Commit creado exitosamente${NC}"
else
    echo -e "${YELLOW}⚠️ No hay cambios para commitear o hubo un error${NC}"
fi

# Subir a GitHub
show_progress "Subiendo a GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Cambios subidos exitosamente a GitHub${NC}"
    echo -e "${GREEN}📎 Repositorio: https://github.com/Hernank10/-subordinadas_percepci-n${NC}"
    
    # Mostrar últimos commits
    echo ""
    echo -e "${YELLOW}📜 Últimos commits:${NC}"
    git log --oneline -3
else
    echo -e "${RED}❌ Error al subir a GitHub${NC}"
    echo "Intentando con pull primero..."
    
    git pull origin main --rebase
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Cambios subidos exitosamente (después de pull)${NC}"
    else
        echo -e "${RED}❌ Error persistente. Revisa manualmente.${NC}"
    fi
fi

# Mostrar resumen
echo ""
echo -e "${GREEN}📊 Resumen de archivos modificados:${NC}"
git log --name-only -1

echo ""
echo -e "${GREEN}✅ Proceso completado${NC}"
echo -e "${GREEN}🌐 Ver en GitHub: https://github.com/Hernank10/-subordinadas_percepci-n${NC}"
