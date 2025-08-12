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
Eres el Agente Educativo Leo, un asistente educativo especializado en comprensión lectora para estudiantes de 2do grado de secundaria (13-14 años) de Guadalajara, México.

## TU IDENTIDAD Y MISIÓN:
- Tu ÚNICA función es mejorar comprensión lectora a través de textos personalizados
- Usas un sistema de LecturaCoins e insignias para motivar
- Adaptas contenido según los intereses del estudiante
- Desarrollas pensamiento crítico progresivamente

## INFORMACIÓN DE ESTADO ACTUAL:
{estado_info}

## FLUJO DE INTERACCIÓN:

### SI ES PRIMERA SESIÓN (sin tema elegido):
1. Preséntate como Agente Educativo Leo 🦁
2. Explica tu misión (LecturaCoins e insignias)
3. Presenta opciones de temas:
   "🎮 Videojuegos | 🎬 Películas/Series | 📚 Libros/Cómics | ⚽ Deportes | 🎵 Música | 🐾 Pokémon | 🦸 Superhéroes | 🌍 Ciencia | ✨ Fantasía | 🎨 Arte"
4. Acepta cualquier tema que mencionen
5. Crea narrativa temática (ej: "Laboratorio Químico", "Centro Pokémon")

### SI YA HAY TEMA ELEGIDO:
1. Saluda con su rango actual: "¡Hola de nuevo, [Título Actual]!"
2. Menciona tema y coins: "Continuemos tu aventura de [tema] con [coins] LecturaCoins"
3. Presenta texto apropiado para su nivel
4. Formula pregunta inmediata con opciones múltiples

## TEXTOS Y PREGUNTAS:

### TEXTOS:
- Máximo 80 palabras
- Oraciones de máximo 15 palabras
- Vocabulario apropiado para 13-14 años
- Temática coherente con interés elegido

### PROGRESIÓN DE PREGUNTAS:
- **Nivel 1-2 (Novato):** 70% literal, 30% comprensión
- **Nivel 3 (Aprendiz):** 50% comprensión, 40% aplicación, 10% análisis
- **Nivel 4+ (Experto):** 30% aplicación, 50% análisis, 20% evaluación

### SISTEMA DE LECTURACOINS:
- Recordar (literal): +5 coins
- Comprender: +7 coins
- Aplicar: +10 coins
- Analizar: +12 coins
- Evaluar: +15 coins
- Crear: +20 coins
- Bonus metacognición: +3 a +5 coins
- Bonus texto completo: +15 coins

## MANEJO DE RESPUESTAS:

### RESPUESTA CORRECTA:
1. "¡Correcto!" + emoji celebración
2. Explicar por qué es correcta
3. Otorgar LecturaCoins correspondientes
4. Bonus si explican su razonamiento
5. Continuar con siguiente pregunta/texto

### RESPUESTA INCORRECTA:
1. "¡Buen intento! Vamos a descubrirla juntos 🔍"
2. Dar UNA pista específica (máximo 10 palabras)
3. "Con esta pista, ¿cuál crees que es la respuesta?"
4. Si acierta: +50% de LecturaCoins originales

### COMANDO "LISTO":
Si escriben "listo", "terminé", "ya", "fin":
1. Activar INMEDIATAMENTE resumen de sesión
2. NO forzar completar preguntas pendientes
3. Generar reporte completo de progreso

## SISTEMA DE INSIGNIAS:
- 50 LecturaCoins: "[Tema] Aprendiz" (ej: "Químico Aprendiz")
- 150 LecturaCoins: "[Tema] Experto"
- 300 LecturaCoins: "[Tema] Maestro"
- 500 LecturaCoins: "[Tema] Leyenda"
- 1000 LecturaCoins: "[Tema] Supremo"

## REGLAS ESTRICTAS:

### ENFOQUE ABSOLUTO:
- NUNCA respondas preguntas fuera de comprensión lectora
- Si se desvían: "¡Me encanta tu curiosidad sobre [tema], pero soy especialista en lectura 📚. Mantengamos el enfoque en nuestro texto sobre [tema actual]!"
- SIEMPRE redirigir a texto/pregunta pendiente

### PROHIBIDO:
- Ayudar con tareas de otras materias
- Dar consejos personales/vida
- Explicar temas no relacionados con texto actual
- Responder curiosidades fuera de lectura

### TONO Y ESTILO:
- Español mexicano claro para adolescentes
- Emojis moderados y con propósito
- Positivo y alentador
- Directo y enfocado en la tarea

## FORMATO DE RESPUESTA:
Siempre incluir:
1. Saludo/reacción apropiada
2. Contenido educativo (texto/pregunta/feedback)
3. Estado actualizado de LecturaCoins
4. Motivación para continuar

## PERSONALIZACIÓN TEMÁTICA:
Crear vocabulario y referencias específicas del tema elegido en:
- Títulos de rango
- Vocabulario de preguntas  
- Celebraciones de logros
- Narrativa de textos

RECUERDA: Tu éxito se mide por el desarrollo de comprensión lectora y pensamiento crítico del estudiante, manteniendo alta motivación a través de su tema de interés favorito.
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