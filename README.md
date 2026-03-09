# 🎓 Proyecto de Lingüística: Verbos de Percepción y Predicados Estativos

[![Flask](https://img.shields.io/badge/Flask-2.3.3-blue.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)

## 📋 Descripción del Proyecto

Este repositorio contiene una aplicación web educativa desarrollada con Flask que explora las restricciones sintácticas entre verbos de percepción y predicados estativos en español. La aplicación ofrece una experiencia interactiva para aprender sobre aspectualidad y su manifestación en la gramática española.

## 🏗️ Estructura del Repositorio

-subordinadas_percepci-n/
├── flask_linguistica/ # Aplicación principal
│ ├── app.py # Servidor Flask
│ ├── requirements.txt # Dependencias
│ ├── data/ # Datos de la aplicación
│ │ └── ejercicios_flashcards.json # 100 flashcards
│ ├── static/ # Archivos estáticos
│ │ └── css/
│ │ └── style.css # Estilos personalizados
│ └── templates/ # Plantillas HTML
│ ├── base.html
│ ├── index.html
│ ├── teoria.html
│ ├── ejemplos.html
│ ├── ejercicios.html
│ ├── flashcards.html
│ ├── 404.html
│ └── 500.html
└── README.md # Este archivo

text

## 🚀 Características Principales

### 📚 Contenido Educativo
- **Teoría fundamental** sobre predicados estativos vs. dinámicos
- **Ejemplos contrastivos** de estructuras gramaticales
- **Explicaciones detalladas** basadas en investigación lingüística

### 🎮 Componentes Interactivos
- **3 ejercicios prácticos** con retroalimentación inmediata
- **100 flashcards** organizadas por categorías:
  - Tipos: concepto, ejemplo, gramatical
  - Categorías: definiciones, identificación, estructuras, aspectual
  - Dificultades: fácil, media, difícil

### 🎨 Interfaz de Usuario
- Diseño responsive con Bootstrap 5
- Navegación intuitiva
- Seguimiento visual del progreso
- Filtros y búsqueda de flashcards

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Flask | 2.3.3 | Framework web backend |
| Python | 3.8+ | Lenguaje de programación |
| Bootstrap | 5.3 | Framework CSS frontend |
| JavaScript | ES6 | Interactividad del cliente |
| Jinja2 | 3.1.2 | Motor de plantillas |
| JSON | - | Almacenamiento de datos |

## 📦 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Hernank10/-subordinadas_percepci-n.git
   cd -subordinadas_percepci-n/flask_linguistica
Crear entorno virtual

bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
Instalar dependencias

bash
pip install -r requirements.txt
Ejecutar la aplicación

bash
python app.py
Abrir en el navegador

text
http://localhost:5000
🎯 Uso de la Aplicación
Secciones Disponibles
Inicio (/): Página principal con acceso a todas las secciones

Teoría (/teoria): Explicaciones teóricas fundamentales

Ejemplos (/ejemplos): Casos contrastivos de uso

Ejercicios (/ejercicios): Práctica interactiva

Flashcards (/flashcards): 100 tarjetas de estudio

Sistema de Flashcards
Las flashcards ofrecen:

Filtrado por categoría, dificultad y tipo

Búsqueda por palabras clave

Volteo interactivo de tarjetas

Seguimiento de progreso personal

Aleatoriedad inteligente

📊 Contenido Educativo
Predicados Estativos
saber, estar, parecer, tener, conocer, creer

Describen estados sin desarrollo temporal

Requieren estructura con "que" después de verbos de percepción

Predicados Dinámicos
correr, hablar, construir, comer, escribir, saltar

Denotan acciones con desarrollo temporal

Admiten estructura de infinitivo

🤝 Contribución
Las contribuciones son bienvenidas. Para contribuir:

Fork el repositorio

Crear una rama para tu función (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abrir un Pull Request

📝 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

👨‍🏫 Autor
Hernank10

GitHub: @Hernank10

Proyecto: Verbos de Percepción y Predicados Estativos

🙏 Agradecimientos
Basado en investigaciones de lingüística hispánica

Inspirado en necesidades educativas de estudiantes de español

Diseño enfocado en usabilidad y experiencia de aprendizaje

📬 Contacto
Para preguntas, sugerencias o reportar problemas:

Abrir un issue

Contactar vía GitHub

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐
