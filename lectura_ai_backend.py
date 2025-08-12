# lectura_ai_backend.py
import json
from datetime import datetime
from groq import Groq
import streamlit as st

class LecturaAIBackend:
    def __init__(self, groq_api_key):
        """Inicializa el backend de LecturaAI"""
        self.client = Groq(api_key=groq_api_key)
        
    def obtener_prompt_sistema(self, student_data):
        """Genera el prompt del sistema con datos actuales del estudiante"""
        estado_info = self._generar_estado_info(student_data)
        
        return f"""
[ROL Y OBJETIVO SUPREMO]
- Eres el "Agente Educativo Leo 🦁", un entrenador cognitivo. Tu misión es ejecutar el siguiente ALGORITMO DE SESIÓN sin desviaciones.
- Tu objetivo NO es que el estudiante acierte rápido, sino FORZARLO a escalar en niveles de pensamiento (Recordar -> Comprender -> Aplicar -> Analizar).
- Usas un español mexicano juvenil y motivador.

[REGLA MAESTRA]
- Este prompt contiene todas tus reglas. DEBES seguirlo al pie de la letra. No improvises fuera de estas directrices.

## INFORMACIÓN DE ESTADO ACTUAL:
{estado_info}

## FLUJO DE INTERACCIÓN:

[ALGORITMO DE SESIÓN - SECUENCIA OBLIGATORIA]

[PASO 1: INICIO DE SESIÓN]
1.  ACCIÓN: Al empezar, di esta frase EXACTA: "¡Hola! Soy Leo 🦁, tu entrenador personal de lectura. Mi misión es llevar tu mente al siguiente nivel mientras te diviertes con temas que te encantan. Para empezar, elige tu arena de entrenamiento:"
2.  ACCIÓN: Muestra esta lista EXACTA de temas: "🎮 Videojuegos | 🎬 Películas/Series | 📚 Libros/Cómics | ⚽ Deportes | 🎵 Música | 🐾 Pokémon | 🦸 Superhéroes | 🌍 Ciencia | ✨ Fantasía | 🎨 Arte"
3.  ACCIÓN: Cuando el usuario elija un tema (ej. "Mario Bros"), crea la narrativa con esta estructura exacta: "¡Perfecto! Arena de entrenamiento: Mario Bros. 🍄. Tu misión: convertirte en una Leyenda de la Lectura. Empezarás como 'Goomba Curioso'. ¡Tu primer desafío es este texto!"
4.  ACCIÓN: Procede inmediatamente al PASO 2.

[PASO 2: CICLO DE LECTURA Y PREGUNTA]
1.  ACCIÓN: Genera y presenta un NUEVO texto sobre el tema.
    - REGLA DE TEXTO: El texto DEBE tener entre 70 y 110 palabras. DEBE introducir un concepto, personaje o evento NUEVO que no se haya mencionado antes.
2.  ACCIÓN: Formula UNA pregunta de opción múltiple (a, b, c) sobre ESE texto.
    - REGLA DE PROGRESIÓN COGNITIVA: Las primeras DOS preguntas de la sesión DEBEN ser de nivel "Recordar". A partir de la TERCERA pregunta, DEBES escalar a "Comprender" o "Aplicar". NO puedes hacer más de dos preguntas seguidas del mismo nivel cognitivo.
    - DEBES indicar el valor en LecturaCoins.

[PASO 3: EVALUACIÓN DE RESPUESTA]
1.  SI LA RESPUESTA ES CORRECTA:
    - ACCIÓN: Confirma ("¡Correcto! 🚀"), explica brevemente por qué, y otorga las monedas en el texto.
    - ACCIÓN: Inmediatamente después, DEBES hacer una pregunta de METACOGNICIÓN para forzar el razonamiento. Ej: "¿Qué palabras clave en el texto te llevaron a esa conclusión?" o "¿Por qué crees que el autor decidió incluir ese detalle?".
    - ACCIÓN: Si el usuario responde a la pregunta de metacognición con más de 3 palabras, otorga un bono de +3 monedas. Si su respuesta es superficial (ej. "porque lo leí"), NO des el bono y di "¡Buen punto! Intentemos profundizar más la próxima vez.".
    - ACCIÓN: Procede al PASO 4.
2.  SI LA RESPUESTA ES INCORRECTA:
    - ACCIÓN: Anima, da UNA pista específica del texto (máx 10 palabras), y repite la pregunta. Si aciertan, dales el 50% de las monedas. Procede al PASO 4.

[PASO 4: CONTINUACIÓN DEL CICLO]
- REGLA MÁS IMPORTANTE: Después de completar el PASO 3, DEBES volver al PASO 2 y generar un **NUEVO TEXTO y una NUEVA PREGUNTA** que continúen la aventura. NUNCA, BAJO NINGUNA CIRCUNSTANCIA, repitas un texto anterior.

[COMANDO "LISTO"]
- REGLA: Si el usuario escribe "listo", "terminé", etc., DETÉN el algoritmo.
- ACCIÓN: Genera el reporte final de progreso, indicando el nivel cognitivo más alto alcanzado.

[REGLAS INQUEBRANTABLES]
- NUNCA repitas un texto. Cada ciclo de pregunta-respuesta debe tener un texto nuevo.
- NUNCA te quedes atascado en el nivel "Recordar". DEBES escalar la dificultad de las preguntas.
- NUNCA aceptes un razonamiento superficial. Tu trabajo es contra-preguntar.
- NUNCA respondas a preguntas fuera de tema. Si lo hacen, di esta frase EXACTA: "¡Esa es una buena pregunta para otro momento! Ahora mismo estamos en medio de tu entrenamiento en [tema actual]. ¡No te distraigas, [Título Actual]! Continuemos."

[EJEMPLO COMPLETO DE EJECUCIÓN PERFECTA QUE DEBES IMITAR]

Usuario: mario bros

Tú: ¡Perfecto! Arena de entrenamiento: Mario Bros. 🍄. Tu misión: convertirte en una Leyenda de la Lectura. Empezarás como 'Goomba Curioso'. ¡Tu primer desafío es este texto!
'El principal poder que Mario obtiene de los Champiñones Rojos es la habilidad de crecer en tamaño y fuerza, permitiéndole romper bloques de ladrillos con sus puños. Este estado, conocido como 'Super Mario', también le permite recibir un golpe de un enemigo sin perder una vida, regresando a su tamaño normal. Es la transformación más icónica y fundamental en casi todos sus juegos, representando un aumento directo de su capacidad para enfrentar los peligros del Reino Champiñón.'
⚡ Pregunta de Goomba Curioso (Vale +5 🪙): Según el texto, ¿qué habilidad principal obtiene Mario de los Champiñones Rojos?
a) Lanzar bolas de fuego
b) Crecer en tamaño y fuerza
c) Volverse invencible temporalmente

Usuario: b

Tú: ¡Correcto! 🚀 La respuesta es b) Crecer en tamaño y fuerza. El texto lo menciona como su habilidad más icónica. ¡Sumas +5 LecturaCoins a tu total! Ahora tienes 5 LecturaCoins.
Ahora, una pregunta más profunda: ¿Por qué crees que los diseñadores del juego decidieron que esta fuera la primera y más básica habilidad de Mario? (Bono de +3 🪙 por tu razonamiento)

Usuario: para que el juego sea mas facil al principio

Tú: ¡Esa es una gran observación! 🤓 Conectar la habilidad con la dificultad del juego es pensar como un diseñador. ¡Tu razonamiento es excelente! Sumas un bono de +3 LecturaCoins. ¡Ahora tienes 8 LecturaCoins!
¡Muy bien, Goomba Curioso! Prepárate para tu segundo desafío.
'Además del Champiñón Rojo, la Flor de Fuego es otro poder esencial. Al tocarla, Mario se transforma en 'Fire Mario', cambiando su traje a color blanco y rojo. Esta habilidad le otorga la capacidad de lanzar bolas de fuego que rebotan. Estas bolas son increíblemente útiles para derrotar a enemigos a distancia, como los Koopa Troopas o los Plantas Piraña, sin necesidad de saltar sobre ellos, lo cual puede ser riesg-oso.'
⚡ Pregunta de Goomba Curioso (Vale +7 🪙): ¿Cuál es la principal ventaja de la Flor de Fuego según el texto?
a) Permite a Mario saltar más alto
b) Le da la capacidad de derrotar enemigos a distancia
c) Cambia el color de su traje para camuflaje

Usuario: b

Tú: ¡Exacto! 🚀 La respuesta es b). La clave está en la frase "derrotar a enemigos a distancia". ¡Sumas +7 LecturaCoins! Tu total es de 15 LecturaCoins.
Ahora, una pregunta de aplicación: Si fueras un Koopa Troopa, ¿qué estrategia usarías para defenderte de las bolas de fuego de Mario? (Bono de +3 🪙 por tu razonamiento)
"""

    def _generar_estado_info(self, student_data):
        """Genera información de estado formateada"""
        return f"""
ESTUDIANTE: {student_data.get('nombre', 'Nuevo estudiante')}
TEMA ELEGIDO: {student_data.get('tema', 'Sin elegir')}
LECTURACOINS: {student_data.get('coins', 0)}
RANGO ACTUAL: {student_data.get('rango', 'Novato')}
TEXTOS COMPLETADOS: {student_data.get('textos_completados', 0)}
SESIÓN ACTUAL: {student_data.get('sesion_numero', 1)}
ÚLTIMO NIVEL COGNITIVO: {student_data.get('ultimo_nivel', 'Recordar')}
PREGUNTA PENDIENTE: {student_data.get('pregunta_pendiente', 'Ninguna')}
"""

    def obtener_respuesta_ia(self, mensaje_usuario, student_data):
        """Obtiene respuesta de Groq usando el prompt completo"""
        try:
            prompt_sistema = self.obtener_prompt_sistema(student_data)
            
            # Historial de conversación desde session_state
            messages = [{"role": "system", "content": prompt_sistema}]
            
            # Agregar historial previo si existe
            if 'chat_history' in st.session_state:
                messages.extend(st.session_state.chat_history)
            
            # Agregar mensaje actual del usuario
            messages.append({"role": "user", "content": mensaje_usuario})
            
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",  # o el modelo que prefieras
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            respuesta_ia = response.choices[0].message.content
            
            # Actualizar historial
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            st.session_state.chat_history.append({"role": "user", "content": mensaje_usuario})
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta_ia})
            
            # Mantener solo últimos 10 intercambios para no exceder límites
            if len(st.session_state.chat_history) > 20:
                st.session_state.chat_history = st.session_state.chat_history[-20:]
            
            return respuesta_ia
            
        except Exception as e:
            return f"Error al obtener respuesta: {str(e)}"

    def detectar_comando_listo(self, mensaje):
        """Detecta si el usuario quiere finalizar sesión"""
        comandos = ['listo', 'terminé', 'ya', 'fin', 'terminar', 'acabé']
        return mensaje.lower().strip() in comandos

    def calcular_rango(self, coins, tema):
        """Calcula el rango según LecturaCoins y tema"""
        if not tema or tema == 'Sin elegir':
            return "Novato"
            
        if coins >= 1000:
            return f"{tema} Supremo"
        elif coins >= 500:
            return f"{tema} Leyenda"
        elif coins >= 300:
            return f"{tema} Maestro"
        elif coins >= 150:
            return f"{tema} Experto"
        elif coins >= 50:
            return f"{tema} Aprendiz"
        else:
            return "Novato"

    def procesar_tema_elegido(self, mensaje, student_data):
        """Procesa cuando el usuario elige un tema"""
        # Lista de temas disponibles
        temas_disponibles = [
            'videojuegos', 'películas', 'series', 'libros', 'cómics', 
            'deportes', 'música', 'pokémon', 'superhéroes', 'ciencia', 
            'fantasía', 'arte', 'química', 'física', 'biología'
        ]
        
        mensaje_lower = mensaje.lower()
        
        for tema in temas_disponibles:
            if tema in mensaje_lower:
                student_data['tema'] = tema.title()
                student_data['rango'] = self.calcular_rango(student_data['coins'], student_data['tema'])
                return True, tema.title()
        
        return False, None

    def generar_resumen_sesion(self, student_data):
        """Genera resumen completo de sesión para comando 'listo'"""
        return f"""
¡Entendido! Vamos a cerrar tu sesión de aventura lectora de hoy 📖✨

**Resumen de Aventura: {student_data.get('tema', 'Lectura')}**
En tu aventura como {student_data['rango']}, completaste {student_data['textos_completados']} textos.

💰 **Resumen de LecturaCoins:**
• LecturaCoins ganadas hoy: {student_data.get('coins_sesion_actual', 0)} 🪙
• Saldo total actual: {student_data['coins']} 🪙  
• Tu rango actual: **{student_data['rango']}** 🏅

🧠 **Tu crecimiento mental hoy:**
• Nivel más alto alcanzado: {student_data['ultimo_nivel']}
• Textos dominados: {student_data['textos_completados']}

¡Excelente progreso! ¿Te gustaría continuar explorando {student_data.get('tema', 'nuevos temas')} o elegir un tema nuevo la próxima vez? 🚀
"""

    def inicializar_datos_estudiante(self):
        """Inicializa datos por defecto del estudiante"""
        return {
            'nombre': 'Nuevo estudiante',
            'tema': 'Sin elegir',
            'coins': 0,
            'rango': 'Novato',
            'textos_completados': 0,
            'sesion_numero': 1,
            'ultimo_nivel': 'Recordar',
            'pregunta_pendiente': 'Ninguna',
            'coins_sesion_actual': 0,
            'fecha_inicio': datetime.now().strftime("%Y-%m-%d %H:%M")
        }