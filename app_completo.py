# app.py - Aplicación principal de Streamlit
import streamlit as st
import json
from datetime import datetime
from lectura_ai_backend import LecturaAIBackend
import os
from PIL import Image


# Configuración de página
st.set_page_config(
    page_title="Agente Educativo Leo 🦁",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejor apariencia
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.stAlert {
    margin-top: 1rem;
}

.student-stats {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

.coin-display {
    font-size: 1.2em;
    font-weight: bold;
    color: #ff6b35;
}

.rank-display {
    font-size: 1.1em;
    font-weight: bold;
    color: #4a90e2;
}

.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 0.5rem;
    margin: 1rem 0;
}

.user-message {
    background-color: #e3f2fd;
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    text-align: right;
}

.ai-message {
    background-color: #f1f8e9;
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

def inicializar_session_state():
    """Inicializa variables de sesión"""
    if 'backend' not in st.session_state:
        # Aquí debes poner tu API key de Groq
        groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if not groq_api_key:
            st.error("⚠️ API Key de Groq no encontrada. Por favor configúrala en secrets.toml o variables de entorno.")
            st.stop()
        st.session_state.backend = LecturaAIBackend(groq_api_key)
    
    if 'student_data' not in st.session_state:
        st.session_state.student_data = st.session_state.backend.inicializar_datos_estudiante()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'messages_display' not in st.session_state:
        st.session_state.messages_display = []
    
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False

def mostrar_sidebar():
    """Configura y muestra el sidebar con información del estudiante"""
    with st.sidebar:
        st.title("👩‍🏫 Agente Educativo Leo 🦁")
        st.markdown("---")
        
        # Información del estudiante
        st.markdown("### 👤 Perfil del Estudiante")
        
        # Input para nombre del estudiante
        nuevo_nombre = st.text_input(
            "Nombre:", 
            value=st.session_state.student_data.get('nombre', 'Nuevo estudiante'),
            key="student_name_input"
        )
        
        if nuevo_nombre != st.session_state.student_data.get('nombre'):
            st.session_state.student_data['nombre'] = nuevo_nombre
        
        # Estadísticas actuales
        st.markdown("### 📊 Estadísticas")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🪙 LecturaCoins", st.session_state.student_data['coins'])
        with col2:
            st.metric("📖 Textos", st.session_state.student_data['textos_completados'])
        
        # Tema y rango
        if st.session_state.student_data['tema'] != 'Sin elegir':
            st.info(f"🎯 **Tema:** {st.session_state.student_data['tema']}")
            st.success(f"🏅 **Rango:** {st.session_state.student_data['rango']}")
        else:
            st.warning("🎯 **Tema:** No seleccionado")
        
        st.markdown("---")
        
        # Progreso hacia siguiente rango
        coins = st.session_state.student_data['coins']
        tema = st.session_state.student_data['tema']
        
        if tema != 'Sin elegir':
            progreso_siguiente = calcular_progreso_siguiente_rango(coins)
            if progreso_siguiente:
                st.markdown("### 🎯 Próximo Objetivo")
                st.progress(progreso_siguiente['progreso'])
                st.caption(f"{progreso_siguiente['faltante']} coins para {progreso_siguiente['siguiente_rango']}")
        
        # Botones de control
        st.markdown("---")
        st.markdown("### ⚙️ Controles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Nueva Sesión", use_container_width=True):
                reiniciar_sesion()
        
        with col2:
            if st.button("💾 Guardar Progreso", use_container_width=True):
                guardar_progreso()
        
        # Información de sesión
        st.markdown("---")
        st.caption(f"Sesión #{st.session_state.student_data['sesion_numero']}")
        st.caption(f"Iniciada: {st.session_state.student_data.get('fecha_inicio', 'Hoy')}")

def calcular_progreso_siguiente_rango(coins):
    """Calcula progreso hacia el siguiente rango"""
    rangos = [50, 150, 300, 500, 1000]
    
    for rango_coins in rangos:
        if coins < rango_coins:
            progreso = coins / rango_coins
            faltante = rango_coins - coins
            
            # Determinar nombre del rango
            if rango_coins == 50:
                rango_nombre = "Aprendiz"
            elif rango_coins == 150:
                rango_nombre = "Experto"
            elif rango_coins == 300:
                rango_nombre = "Maestro"
            elif rango_coins == 500:
                rango_nombre = "Leyenda"
            else:
                rango_nombre = "Supremo"
            
            return {
                'progreso': progreso,
                'faltante': faltante,
                'siguiente_rango': rango_nombre
            }
    
    return None

def mostrar_chat():
    """Muestra el historial de chat"""
    chat_container = st.container()
    
    with chat_container:
        st.markdown("### 💬 Conversación con Agente Educativo Leo")
        
        # Contenedor scrolleable para mensajes
        messages_container = st.container()
        
        with messages_container:
            for message in st.session_state.messages_display:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>Tú:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <strong>📚 Agente Educativo Leo 🦁:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)

def procesar_mensaje(mensaje_usuario):
    """Procesa el mensaje del usuario y obtiene respuesta de la IA"""
    
    # Agregar mensaje del usuario al display
    st.session_state.messages_display.append({
        'role': 'user',
        'content': mensaje_usuario
    })
    
    # Verificar comando "listo"
    if st.session_state.backend.detectar_comando_listo(mensaje_usuario):
        resumen = st.session_state.backend.generar_resumen_sesion(st.session_state.student_data)
        st.session_state.messages_display.append({
            'role': 'assistant',
            'content': resumen
        })
        return
    
    # Verificar selección de tema (solo si no hay tema elegido)
    if st.session_state.student_data['tema'] == 'Sin elegir':
        tema_detectado, tema = st.session_state.backend.procesar_tema_elegido(
            mensaje_usuario, st.session_state.student_data
        )
        if tema_detectado:
            st.success(f"🎯 ¡Tema seleccionado: {tema}!")
    
    # Obtener respuesta de la IA
    respuesta_ia = st.session_state.backend.obtener_respuesta_ia(
        mensaje_usuario, st.session_state.student_data
    )
    
    # Agregar respuesta de la IA al display
    st.session_state.messages_display.append({
        'role': 'assistant',
        'content': respuesta_ia
    })
    
    # Actualizar rango si es necesario
    st.session_state.student_data['rango'] = st.session_state.backend.calcular_rango(
        st.session_state.student_data['coins'], 
        st.session_state.student_data['tema']
    )
    
def mostrar_logo():
    try:
        logo = Image.open("images/logo.jpg")
        st.image(logo, width=200)
    except FileNotFoundError:
        st.markdown("# 🤖")

def reiniciar_sesion():
    """Reinicia la sesión actual"""
    st.session_state.student_data = st.session_state.backend.inicializar_datos_estudiante()
    st.session_state.chat_history = []
    st.session_state.messages_display = []
    st.session_state.session_started = False
    st.success("🔄 ¡Sesión reiniciada correctamente!")
    st.rerun()

def guardar_progreso():
    """Guarda el progreso del estudiante"""
    try:
        # En un entorno real, aquí guardarías en base de datos
        # Por ahora, simulamos guardado exitoso
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.student_data['ultimo_guardado'] = timestamp
        st.success(f"💾 Progreso guardado: {timestamp}")
    except Exception as e:
        st.error(f"❌ Error al guardar: {str(e)}")

def main():
    """Función principal de la aplicación"""
    inicializar_session_state()
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        col_logo, col_titulo = st.columns([1, 3])

    with col_logo:
        mostrar_logo()

    with col_titulo:
        st.title("Agente Educativo Leo 🦁")
        st.markdown("*Tu asistente personal de comprensión lectora*")
        
        # Mostrar mensaje de bienvenida si es primera vez
        if not st.session_state.session_started:
            st.info("""
            ¡Bienvenido al Agente Educativo Leo! 🦁
            
            Soy tu asistente especializado en comprensión lectora. Te ayudo a:
            - 📖 Mejorar tu comprensión de textos
            - 🪙 Ganar LecturaCoins por tus logros
            - 🏅 Subir de rango y conseguir insignias
            - 🎯 Aprender sobre temas que te interesan
            
            ¿Estás listo para comenzar tu aventura de lectura?
            """)
            
            if st.button("🚀 ¡Comenzar Aventura!", use_container_width=True):
                st.session_state.session_started = True
                # Mensaje inicial automático
                mensaje_inicial = "Hola, soy nuevo aquí"
                procesar_mensaje(mensaje_inicial)
                st.rerun()
        
        else:
            # Mostrar chat
            mostrar_chat()
            
            # Input para nuevo mensaje
            with st.form("mensaje_form", clear_on_submit=True):
                col_input, col_button = st.columns([4, 1])
                
                with col_input:
                    mensaje_usuario = st.text_input(
                        "Escribe tu mensaje:", 
                        placeholder="Escribe aquí tu respuesta o 'listo' para terminar...",
                        key="user_input"
                    )
                
                with col_button:
                    submit_button = st.form_submit_button("📤 Enviar", use_container_width=True)
                
                if submit_button and mensaje_usuario.strip():
                    procesar_mensaje(mensaje_usuario)
                    st.rerun()
    
    with col2:
        # Sidebar se muestra automáticamente
        pass
    
    # Sidebar
    mostrar_sidebar()

if __name__ == "__main__":
    main()