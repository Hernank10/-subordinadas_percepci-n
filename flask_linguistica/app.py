from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import secrets
import os
import json
import random
from datetime import timedelta, datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(days=7)  # Duración de la sesión: 7 días

# Configuración
app.config['SESSION_TYPE'] = 'filesystem'
app.config['DEBUG'] = True
app.config['JSON_AS_ASCII'] = False  # Para mantener tildes en JSON
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Cargar flashcards desde JSON
def cargar_flashcards():
    json_path = Path('data/ejercicios_flashcards.json')
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('flashcards', [])
    return []

flashcards_data = cargar_flashcards()

# Datos de teoría
teoria_data = [
    {
        "id": 1,
        "titulo": "Predicados Estativos vs. Dinámicos",
        "icono": "lightbulb",
        "color": "primary",
        "contenido": {
            "estativos": {
                "descripcion": "Describen estados o condiciones sin desarrollo temporal",
                "caracteristicas": [
                    "No tienen duración delimitada",
                    "No progresan en el tiempo",
                    "Son homogéneos"
                ],
                "ejemplos": ["saber", "estar", "parecer", "tener", "conocer", "creer"]
            },
            "dinamicos": {
                "descripcion": "Denotan acciones o eventos con desarrollo temporal",
                "caracteristicas": [
                    "Tienen inicio y fin",
                    "Progresan en el tiempo",
                    "Tienen fases internas"
                ],
                "ejemplos": ["correr", "hablar", "construir", "comer", "escribir", "saltar"]
            }
        }
    },
    {
        "id": 2,
        "titulo": "Verbos de Percepción",
        "icono": "eye",
        "color": "success",
        "contenido": {
            "verbos": ["ver", "oir", "escuchar", "observar", "percibir", "notar"],
            "estructuras": [
                {
                    "tipo": "Infinitivo",
                    "formato": "Verbo percepción + NP + infinitivo",
                    "descripcion": "Solo admite predicados dinámicos (eventos perceptibles)",
                    "ejemplo_correcto": "Vi a María correr",
                    "ejemplo_incorrecto": "*Vi a María saber la verdad",
                    "explicacion": "El infinitivo requiere un evento en desarrollo"
                },
                {
                    "tipo": "Con 'que' + subordinada",
                    "formato": "Verbo percepción + 'que' + oración",
                    "descripcion": "Admite estativos y dinámicos (contenido proposicional)",
                    "ejemplo_correcto": "Vi que María estaba nerviosa",
                    "explicacion": "La subordinada finita permite estados"
                }
            ]
        }
    },
    {
        "id": 3,
        "titulo": "Explicación Aspectual",
        "icono": "puzzle",
        "color": "warning",
        "contenido": {
            "requisitos_infinitivo": [
                "Eventos perceptibles sensorialmente",
                "Desarrollo temporal observable",
                "Dinamicidad (cambio a través del tiempo)"
            ],
            "problemas_estativos": [
                "No tienen desarrollo progresivo",
                "No son eventos delimitados",
                "Representan condiciones, no acciones",
                "No son perceptibles directamente"
            ],
            "cita": "La gramaticalidad no depende de si la percepción es epistémica o no epistémica, sino de la compatibilidad aspectual entre el verbo de percepción y el predicado subordinado."
        }
    }
]

# Ejemplos contrastivos
ejemplos_data = {
    "introduccion": "Los siguientes ejemplos ilustran el contraste entre estructuras gramaticales e incorrectas:",
    "categorias": [
        {
            "titulo": "Estructuras Incorrectas",
            "color": "danger",
            "ejemplos": [
                {"oracion": "*Juan vio estar nerviosa a María", "explicacion": "Uso de 'estar' (estativo) con infinitivo"},
                {"oracion": "*Oí saber la respuesta al estudiante", "explicacion": "Uso de 'saber' (estativo) con infinitivo"},
                {"oracion": "*Observé tener frío a los niños", "explicacion": "Uso de 'tener' (estativo) con infinitivo"},
                {"oracion": "*Percibí estar en la cafetería a Pedro", "explicacion": "Uso de 'estar' (estativo) con infinitivo"},
                {"oracion": "*Noté ser inteligente a María", "explicacion": "Uso de 'ser' (estativo) con infinitivo"}
            ]
        },
        {
            "titulo": "Estructuras Correctas",
            "color": "success",
            "ejemplos": [
                {"oracion": "Juan vio que María estaba nerviosa", "explicacion": "Estructura con 'que' + subordinada"},
                {"oracion": "Oí que el estudiante sabía la respuesta", "explicacion": "Estructura con 'que' + subordinada"},
                {"oracion": "Observé que los niños tenían frío", "explicacion": "Estructura con 'que' + subordinada"},
                {"oracion": "Percibí que Pedro estaba en la cafetería", "explicacion": "Estructura con 'que' + subordinada"},
                {"oracion": "Noté que María era inteligente", "explicacion": "Estructura con 'que' + subordinada"}
            ]
        }
    ],
    "nota": {
        "titulo": "Nota importante",
        "mensaje": "La agramaticalidad de las estructuras con infinitivo se debe a un conflicto aspectual, no a la naturaleza de la percepción. Los estados no pueden ser percibidos directamente como eventos en desarrollo."
    }
}

# Ejercicios interactivos
ejercicios_data = [
    {
        "id": 1,
        "tipo": "multiple",
        "dificultad": "fácil",
        "pregunta": "¿Cuál de estas oraciones es gramaticalmente correcta?",
        "opciones": [
            "Oí a Juan saber la respuesta",
            "Observé que Juan sabía la respuesta",
            "Vi estar preocupado a Pedro",
            "Escuché sonar inteligente al profesor"
        ],
        "respuesta_correcta": 1,
        "explicacion": "La opción 2 es correcta porque usa 'que' + subordinada, permitiendo el estativo 'saber'. Las demás usan estructura de infinitivo con predicados estativos.",
        "pista": "Recuerda: los predicados estativos necesitan la estructura con 'que'"
    },
    {
        "id": 2,
        "tipo": "multiple",
        "dificultad": "fácil",
        "pregunta": "Identifica el error en: '*Vimos tener frío a los niños'",
        "opciones": [
            "Uso incorrecto del verbo de percepción",
            "Predicado estativo en estructura de infinitivo",
            "Error de concordancia verbal",
            "Ninguno es incorrecto"
        ],
        "respuesta_correcta": 1,
        "explicacion": "El error es la opción 2: 'tener' es estativo y no puede usarse con la estructura de infinitivo después de verbo de percepción.",
        "pista": "¿Qué tipo de predicado es 'tener'?"
    },
    {
        "id": 3,
        "tipo": "multiple",
        "dificultad": "media",
        "pregunta": "¿Por qué es agramatical '*Juan vio estar nerviosa a María'?",
        "opciones": [
            "Porque 'ver' no puede subordinar infinitivos",
            "Porque 'estar' es un predicado estativo y el infinitivo requiere dinamismo",
            "Porque hay error de concordancia de género",
            "Porque el verbo de percepción está en pasado"
        ],
        "respuesta_correcta": 1,
        "explicacion": "La agramaticalidad se debe al conflicto aspectual: 'estar' es estativo y el infinitivo después de verbo de percepción requiere un predicado dinámico.",
        "pista": "Piensa en la naturaleza aspectual de 'estar'"
    }
]

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teoria')
def teoria():
    return render_template('teoria.html', teoria_data=teoria_data)

@app.route('/ejemplos')
def ejemplos():
    return render_template('ejemplos.html', ejemplos=ejemplos_data)

@app.route('/ejercicios')
def ejercicios():
    if 'ejercicios_completados' not in session:
        session['ejercicios_completados'] = []
    if 'puntaje' not in session:
        session['puntaje'] = 0
    return render_template('ejercicios.html', ejercicios=ejercicios_data)

# Rutas para flashcards
@app.route('/flashcards')
def flashcards():
    """Página principal de flashcards"""
    # Inicializar datos de usuario si no existen
    inicializar_datos_usuario()
    return render_template('flashcards.html', total_flashcards=len(flashcards_data))

@app.route('/dashboard')
def dashboard():
    """Dashboard de usuario con estadísticas y progreso"""
    inicializar_datos_usuario()
    
    # Obtener estadísticas
    stats = obtener_estadisticas_usuario()
    
    # Obtener flashcards por categoría para gráficos
    flashcards_por_categoria = {}
    for flashcard in flashcards_data:
        cat = flashcard.get('categoria', 'sin categoria')
        if cat not in flashcards_por_categoria:
            flashcards_por_categoria[cat] = 0
        flashcards_por_categoria[cat] += 1
    
    # Obtener progreso por categoría
    progreso_categoria = {}
    for cat in flashcards_por_categoria.keys():
        completadas_cat = [f for f in session.get('flashcards_completadas', []) 
                          if any(fc['categoria'] == cat for fc in flashcards_data if fc['id'] == f)]
        progreso_categoria[cat] = len(completadas_cat)
    
    return render_template('dashboard.html', 
                         stats=stats,
                         flashcards_por_categoria=flashcards_por_categoria,
                         progreso_categoria=progreso_categoria)

# Funciones de inicialización y estadísticas
def inicializar_datos_usuario():
    """Inicializar todos los datos del usuario en sesión"""
    session.permanent = True
    
    if 'flashcards_vistas' not in session:
        session['flashcards_vistas'] = []
    
    if 'flashcards_completadas' not in session:
        session['flashcards_completadas'] = []  # IDs de flashcards completadas
    
    if 'flashcards_acertadas' not in session:
        session['flashcards_acertadas'] = 0
    
    if 'flashcards_falladas' not in session:
        session['flashcards_falladas'] = 0
    
    if 'historial_respuestas' not in session:
        session['historial_respuestas'] = []  # Historial de últimas respuestas
    
    if 'racha_actual' not in session:
        session['racha_actual'] = 0  # Racha de respuestas correctas
    
    if 'mejor_racha' not in session:
        session['mejor_racha'] = 0
    
    if 'ultima_actividad' not in session:
        session['ultima_actividad'] = datetime.now().isoformat()
    
    if 'tiempo_total' not in session:
        session['tiempo_total'] = 0  # Tiempo total de estudio en minutos
    
    session.modified = True

def obtener_estadisticas_usuario():
    """Obtener estadísticas completas del usuario"""
    vistas = session.get('flashcards_vistas', [])
    completadas = session.get('flashcards_completadas', [])
    acertadas = session.get('flashcards_acertadas', 0)
    falladas = session.get('flashcards_falladas', 0)
    total_intentos = acertadas + falladas
    
    # Calcular porcentajes
    porcentaje_completado = (len(completadas) / len(flashcards_data)) * 100 if flashcards_data else 0
    porcentaje_aciertos = (acertadas / total_intentos) * 100 if total_intentos > 0 else 0
    
    # Calcular distribución por dificultad
    dificultades = {'fácil': 0, 'media': 0, 'difícil': 0}
    for f_id in completadas:
        flashcard = next((f for f in flashcards_data if f['id'] == f_id), None)
        if flashcard:
            dif = flashcard.get('dificultad', 'media')
            dificultades[dif] = dificultades.get(dif, 0) + 1
    
    # Calcular tiempo estimado de estudio
    tiempo_estudio = session.get('tiempo_total', 0)
    
    return {
        'total_flashcards': len(flashcards_data),
        'vistas': len(vistas),
        'completadas': len(completadas),
        'pendientes': len(flashcards_data) - len(completadas),
        'acertadas': acertadas,
        'falladas': falladas,
        'total_intentos': total_intentos,
        'porcentaje_completado': round(porcentaje_completado, 1),
        'porcentaje_aciertos': round(porcentaje_aciertos, 1),
        'racha_actual': session.get('racha_actual', 0),
        'mejor_racha': session.get('mejor_racha', 0),
        'dificultades': dificultades,
        'tiempo_estudio': tiempo_estudio,
        'ultima_actividad': session.get('ultima_actividad', '')
    }

# API endpoints para flashcards
@app.route('/api/flashcards/random')
def get_random_flashcard():
    """Obtener una flashcard aleatoria no completada prioritariamente"""
    if not flashcards_data:
        return jsonify({'error': 'No hay flashcards disponibles'}), 404
    
    # Parámetros de filtro
    categoria = request.args.get('categoria')
    dificultad = request.args.get('dificultad')
    tipo = request.args.get('tipo')
    modo = request.args.get('modo', 'normal')  # 'normal', 'revision', 'solo_pendientes'
    
    # Obtener flashcards completadas
    completadas = session.get('flashcards_completadas', [])
    
    # Filtrar flashcards
    flashcards_filtradas = flashcards_data.copy()
    
    if modo == 'solo_pendientes':
        # Solo flashcards no completadas
        flashcards_filtradas = [f for f in flashcards_filtradas if f['id'] not in completadas]
    elif modo == 'revision':
        # Priorizar flashcards falladas o con más errores
        # Por ahora, 50% completadas y 50% nuevas
        if completadas and random.random() < 0.5:
            # Revisar algunas completadas
            flashcards_filtradas = [f for f in flashcards_filtradas if f['id'] in completadas]
    
    if categoria and categoria != 'todas':
        flashcards_filtradas = [f for f in flashcards_filtradas if f.get('categoria') == categoria]
    
    if dificultad and dificultad != 'todas':
        flashcards_filtradas = [f for f in flashcards_filtradas if f.get('dificultad') == dificultad]
    
    if tipo and tipo != 'todos':
        flashcards_filtradas = [f for f in flashcards_filtradas if f.get('tipo') == tipo]
    
    if not flashcards_filtradas:
        # Si no hay con filtros, devolver todas
        flashcards_filtradas = flashcards_data
    
    flashcard = random.choice(flashcards_filtradas)
    
    # Registrar vista
    if flashcard['id'] not in session.get('flashcards_vistas', []):
        session['flashcards_vistas'].append(flashcard['id'])
        session.modified = True
    
    return jsonify(flashcard)

@app.route('/api/flashcards/responder', methods=['POST'])
def responder_flashcard():
    """Registrar respuesta a una flashcard"""
    data = request.json
    flashcard_id = data.get('flashcard_id')
    correcta = data.get('correcta', False)
    tiempo_respuesta = data.get('tiempo_respuesta', 0)  # Tiempo en segundos
    
    # Inicializar datos si es necesario
    inicializar_datos_usuario()
    
    # Actualizar estadísticas
    if correcta:
        session['flashcards_acertadas'] = session.get('flashcards_acertadas', 0) + 1
        session['racha_actual'] = session.get('racha_actual', 0) + 1
        
        # Actualizar mejor racha
        if session['racha_actual'] > session.get('mejor_racha', 0):
            session['mejor_racha'] = session['racha_actual']
        
        # Si no estaba completada, marcarla como completada
        completadas = session.get('flashcards_completadas', [])
        if flashcard_id not in completadas:
            completadas.append(flashcard_id)
            session['flashcards_completadas'] = completadas
    else:
        session['flashcards_falladas'] = session.get('flashcards_falladas', 0) + 1
        session['racha_actual'] = 0  # Reiniciar racha
    
    # Registrar en historial
    historial = session.get('historial_respuestas', [])
    historial.append({
        'id': flashcard_id,
        'correcta': correcta,
        'timestamp': datetime.now().isoformat(),
        'tiempo': tiempo_respuesta
    })
    # Mantener solo últimos 50 registros
    if len(historial) > 50:
        historial = historial[-50:]
    session['historial_respuestas'] = historial
    
    # Actualizar tiempo de estudio (aproximado)
    session['tiempo_total'] = session.get('tiempo_total', 0) + round(tiempo_respuesta / 60, 1)
    session['ultima_actividad'] = datetime.now().isoformat()
    
    session.modified = True
    
    return jsonify({'status': 'success'})

@app.route('/api/flashcards/categorias')
def get_categorias():
    """Obtener todas las categorías disponibles"""
    categorias = list(set(f.get('categoria', 'sin_categoria') for f in flashcards_data))
    return jsonify(sorted(categorias))

@app.route('/api/flashcards/dificultades')
def get_dificultades():
    """Obtener todos los niveles de dificultad"""
    dificultades = list(set(f.get('dificultad', 'media') for f in flashcards_data))
    return jsonify(sorted(dificultades))

@app.route('/api/flashcards/tipos')
def get_tipos():
    """Obtener todos los tipos de flashcards"""
    tipos = list(set(f.get('tipo', 'concepto') for f in flashcards_data))
    return jsonify(sorted(tipos))

@app.route('/api/flashcards/estadisticas')
def get_flashcard_stats():
    """Obtener estadísticas de uso de flashcards"""
    inicializar_datos_usuario()
    stats = obtener_estadisticas_usuario()
    return jsonify(stats)

@app.route('/api/flashcards/buscar')
def buscar_flashcards():
    """Buscar flashcards por término"""
    termino = request.args.get('q', '').lower()
    if not termino or len(termino) < 3:
        return jsonify([])
    
    resultados = [
        f for f in flashcards_data 
        if termino in f.get('frontal', '').lower() 
        or termino in f.get('reverso', '').lower()
        or termino in f.get('ejemplo', '').lower()
    ]
    
    return jsonify(resultados[:10])

@app.route('/api/flashcards/recomendadas')
def get_recomendadas():
    """Obtener flashcards recomendadas (las que más necesita repasar)"""
    completadas = session.get('flashcards_completadas', [])
    falladas = session.get('flashcards_falladas', 0)
    
    # Lógica simple: recomendar las no vistas primero, luego las más difíciles
    no_vistas = [f for f in flashcards_data if f['id'] not in session.get('flashcards_vistas', [])]
    
    if no_vistas:
        recomendadas = random.sample(no_vistas, min(5, len(no_vistas)))
    else:
        # Si ya vio todas, recomendar algunas al azar
        recomendadas = random.sample(flashcards_data, min(5, len(flashcards_data)))
    
    return jsonify(recomendadas)

# Rutas para ejercicios
@app.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    ejercicio_id = data.get('ejercicio_id')
    respuesta_usuario = data.get('respuesta')
    
    ejercicio = next((e for e in ejercicios_data if e['id'] == ejercicio_id), None)
    
    if not ejercicio:
        return jsonify({'error': 'Ejercicio no encontrado'}), 404
    
    if ejercicio['tipo'] == 'multiple':
        try:
            es_correcto = int(respuesta_usuario) == ejercicio['respuesta_correcta']
        except ValueError:
            es_correcto = False
    else:
        respuesta_normalizada = respuesta_usuario.lower().strip()
        respuesta_correcta_normalizada = ejercicio['respuesta_correcta'].lower()
        es_correcto = respuesta_normalizada == respuesta_correcta_normalizada
    
    if 'ejercicios_completados' not in session:
        session['ejercicios_completados'] = []
    
    if ejercicio_id not in session['ejercicios_completados']:
        session['ejercicios_completados'].append(ejercicio_id)
        if es_correcto:
            session['puntaje'] = session.get('puntaje', 0) + 1
    
    session.modified = True
    
    return jsonify({
        'correcto': es_correcto,
        'explicacion': ejercicio['explicacion'],
        'pista': ejercicio.get('pista', ''),
        'respuesta_correcta': ejercicio['respuesta_correcta'] if not es_correcto else None,
        'progreso': {
            'completados': len(session['ejercicios_completados']),
            'total': len(ejercicios_data),
            'puntaje': session.get('puntaje', 0)
        }
    })

@app.route('/get-progress', methods=['GET'])
def get_progress():
    return jsonify({
        'ejercicios_completados': session.get('ejercicios_completados', []),
        'puntaje': session.get('puntaje', 0),
        'total_ejercicios': len(ejercicios_data)
    })

@app.route('/reset-progress', methods=['POST'])
def reset_progress():
    """Reiniciar todo el progreso del usuario"""
    session['ejercicios_completados'] = []
    session['puntaje'] = 0
    session['flashcards_vistas'] = []
    session['flashcards_completadas'] = []
    session['flashcards_acertadas'] = 0
    session['flashcards_falladas'] = 0
    session['racha_actual'] = 0
    session['mejor_racha'] = 0
    session['historial_respuestas'] = []
    session['tiempo_total'] = 0
    session.modified = True
    return jsonify({'status': 'success'})

@app.route('/get-pista/<int:ejercicio_id>', methods=['GET'])
def get_pista(ejercicio_id):
    ejercicio = next((e for e in ejercicios_data if e['id'] == ejercicio_id), None)
    if ejercicio and 'pista' in ejercicio:
        return jsonify({'pista': ejercicio['pista']})
    return jsonify({'pista': 'No hay pista disponible para este ejercicio.'})

# Manejo de errores
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Contexto para todas las plantillas
@app.context_processor
def inject_now():
    return {
        'now': datetime.now(),
        'total_ejercicios': len(ejercicios_data),
        'total_flashcards': len(flashcards_data)
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"📚 Total flashcards cargadas: {len(flashcards_data)}")
    print(f"🎯 Total ejercicios: {len(ejercicios_data)}")
    print(f"🚀 Servidor iniciado en http://localhost:{port}")
    print(f"📊 Dashboard disponible en: http://localhost:{port}/dashboard")
    app.run(host='0.0.0.0', port=port, debug=True)
