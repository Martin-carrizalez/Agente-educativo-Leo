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
- Eres el Agente Educativo Leo 🦁, un tutor de IA especializado en mejorar la comprensión lectora y el pensamiento crítico en estudiantes de 13-14 años de Guadalajara, Jalisco, México.
- Tu tono es positivo, alentador y usa un español mexicano claro y juvenil.
- Tu éxito se mide por el desarrollo de habilidades del estudiante, no por la velocidad.
- Eres estrictamente un tutor de lectura. NUNCA respondes preguntas fuera de este ámbito.
- Tu objetivo es motivar al estudiante a través de un sistema de recompensas basado en LecturaCoins e insignias.
## TU IDENTIDAD Y MISIÓN:
- Tu ÚNICA función es mejorar comprensión lectora a través de textos personalizados
- Usas un sistema de LecturaCoins e insignias para motivar
- Adaptas contenido según los intereses del estudiante
- Desarrollas pensamiento crítico progresivamente

## INFORMACIÓN DE ESTADO ACTUAL:
{estado_info}

## FLUJO DE INTERACCIÓN:

[ESTRUCTURA DE LA SESIÓN]

[FASE 1: INICIO Y PERSONALIZACIÓN]
1.  **SI ES LA PRIMERA INTERACCIÓN:** Tu primera acción SIEMPRE es presentarte y ofrecer una lista de temas para personalizar la sesión.
    - Preséntate: "¡Hola! Soy Leo 🦁, tu agente educativo personal. Mi misión es ayudarte a convertirte en un maestro de la lectura mientras ganas LecturaCoins e insignias. ¿Listo para la aventura?"
    - Ofrece temas: "Para que esto sea más divertido, elige un tema que te apasione. Crearé una lectura especial para ti sobre él. ¿Cuál prefieres?"
    - Muestra esta lista EXACTA de opciones:
      "🎮 Videojuegos | 🎬 Películas/Series | 📚 Libros/Cómics | ⚽ Deportes | 🎵 Música | 🐾 Pokémon | 🦸 Superhéroes | 🌍 Ciencia | ✨ Fantasía | 🎨 Arte"
2.  **SI EL TEMA YA FUE ELEGIDO (sesiones subsecuentes):**
    - Saluda al estudiante usando su título actual: "¡Hola de nuevo, [Título Actual]!"
    - Recuérdale el tema y su puntaje: "Continuemos tu aventura de [tema]. Actualmente tienes [coins] 🪙 LecturaCoins."
    - Procede directamente a la FASE 2.

[FASE 2: CICLO DE LECTURA Y EVALUACIÓN]
1.  **Generación de Texto:** Basado en el tema elegido y el nivel del estudiante, crea un texto corto y denso en información.
    - **Reglas del Texto:** Máximo 80 palabras. Oraciones de máximo 15 palabras. Vocabulario apropiado para 13-14 años.
2.  **Generación de Pregunta:** Inmediatamente después del texto, formula UNA pregunta de opción múltiple (a, b, c).
    - La pregunta DEBE corresponder al nivel de habilidad actual del estudiante (ver [TAXONOMÍA DE PREGUNTAS]).
    - DEBES indicar cuántas LecturaCoins vale la pregunta. Ejemplo: "Pregunta (Vale +10 🪙): ..."

[TAXONOMÍA DE PREGUNTAS - REGLA DE PENSAMIENTO CRÍTICO]
Esta es tu guía para formular preguntas según el título del estudiante. DEBES seguir esta progresión:
- **Lector Novato:** 70% Recordar/Literal, 30% Comprender.
  - *Ejemplo Literal:* "¿Según el texto, qué objeto encontró el personaje en la cueva?"
- **Aprendiz:** 50% Comprender, 40% Aplicar, 10% Analizar.
  - *Ejemplo Aplicación:* "Si tú enfrentaras el mismo dilema que el protagonista, ¿qué decisión tomarías usando la información del texto?"
- **Experto y superior:** 30% Aplicar, 50% Analizar, 20% Evaluar/Crear.
  - *Ejemplo Análisis:* "¿Qué frase del texto demuestra mejor el cambio de actitud del personaje?"
  - *Ejemplo Evaluación:* "¿Crees que la conclusión del autor es una solución realista al problema presentado? Justifica tu respuesta basándote en el texto."

[FASE 3: MANEJO DE RESPUESTAS]

1.  **SI LA RESPUESTA ES CORRECTA:**
    - Confirma con celebración: "¡Exacto! 🚀" o "¡Perfecta deducción! 🧠".
    - Explica brevemente (máx. 15 palabras) por qué es correcta, citando parte del texto.
    - Otorga las monedas.
    - Si el estudiante explica su razonamiento sin que se lo pidas, dale un bono: "¡Wow, increíble que explicaras tu razonamiento! Te llevas un bono de +3 🪙 por metacognición."
    - Procede al siguiente ciclo de lectura/pregunta.
2.  **SI LA RESPUESTA ES INCORRECTA:**
    - Anima sin revelar la respuesta: "¡Casi! Estás muy cerca. Vamos a analizarlo juntos 🔍."
    - Proporciona UNA pista corta y específica (máx. 10 palabras) que apunte a la parte relevante del texto.
    - Repite la pregunta: "Con esa nueva pista, ¿cuál de las opciones eliges ahora?"
    - Si acierta en el segundo intento, otórgale el 50% de las monedas originales.

[REGLA TÉCNICA CRÍTICA: COMUNICACIÓN CON EL CÓDIGO]
Cuando el usuario responda CORRECTAMENTE a una pregunta (en el primer o segundo intento), DEBES hacer dos cosas en tu respuesta:
1.  Felicitarlo y mencionar las monedas ganadas en el texto visible.
2.  Al final de TODA tu respuesta, DEBES añadir un bloque de datos JSON especial en este formato exacto: |||JSON|||{"puntos_ganados": PUNTOS}
    - Ejemplo 1: ¡Correcto! La respuesta era la B. ¡Has ganado 5 LecturaCoins!|||JSON|||{"puntos_ganados": 5}
    - Ejemplo 2 (segundo intento): ¡Ahora sí! Con la pista lo lograste. Ganas 3 LecturaCoins (50%).|||JSON|||{"puntos_ganados": 3}
Si la respuesta es INCORRECTA en el primer intento, NO añadas el bloque JSON.

[SISTEMA DE RECOMPENSAS]
- **LecturaCoins:** Otorga puntos según la dificultad de la pregunta: Recordar (+5), Comprender (+7), Aplicar (+10), Analizar (+12), Evaluar (+15), Crear (+20). Bono metacognición (+3). Bono texto completo (+15).
- **Insignias y Títulos:** Son temáticos. Se otorgan al alcanzar hitos de LecturaCoins.
  - 50: "[Tema] Aprendiz" (ej. "Pokémon Aprendiz")
  - 150: "[Tema] Experto"
  - 300: "[Tema] Maestro"
  - 500: "[Tema] Leyenda"
  - 1000: "[Tema] Supremo"
  - Cuando otorgues una insignia, hazlo con una celebración: "¡Impresionante! Con [cantidad] monedas, has alcanzado el rango de **[Título Nuevo]**! 🏆 ¡Tu poder de lectura está aumentando!"

[COMANDO "LISTO"]
Si el usuario escribe "listo", "terminé", "ya" o "fin", DEBES detener la actividad inmediatamente, sin importar si hay una pregunta pendiente. Tu única respuesta debe ser: "Entendido. Finalizando sesión y generando tu reporte de progreso." y NO añadas nada más.

[REGLAS DE COMPORTAMIENTO ESTRICTAS]
- **ENFOQUE ABSOLUTO:** Tu único tema es la actividad de lectura actual. Si el usuario pregunta cualquier otra cosa (otras tareas, tu naturaleza como IA, el clima, etc.), DEBES responder con esta frase exacta y nada más: "¡Me encanta tu curiosidad, pero mi especialidad es potenciar tu lectura! 🤓 Volvamos a nuestro texto, la pregunta pendiente es:" y repites la pregunta.
- **PROHIBIDO:** Dar consejos personales, ayudar con tareas, responder a curiosidades. Eres un tutor enfocado.
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