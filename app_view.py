import streamlit as st
from controllers.chat_controllers import ChatController

def main():
    # Configuración de la página de Streamlit
    st.set_page_config(
        page_title="GOBS Expert Bot",
        layout="centered"
    )

    # Inicializar el Controlador en la sesión para preservar el estado de la app
    if "controller" not in st.session_state:
        st.session_state.controller = ChatController()

    # Inicializar el historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Encabezado de la interfaz gráfica
    st.title("GOBS Expert Assistant")
    st.subheader("Global Operation Business System & Operational Excellence")
    st.caption("Consulta procedimientos, KPIs, 5S, Six Sigma (DMAIC), ALCOA+ y estándares de manufactura.")
    st.markdown("---")

    # --- COMPONENTE: LISTA DESPLEGABLE DE PREGUNTAS PARA LA DEMO ---
    example_questions = [
        "--- Selecciona una pregunta guiada para la presentación ---",
        "¿Qué es GOBS y cuáles son sus 4 pilares fundamentales?",
        "¿Cuáles son las 8 Mudas que busca eliminar el sistema SPS?",
        "¿Qué pasa si una estación obtiene un puntaje del 80% en la auditoría de 5S?",
        "Explica las 5 fases del ciclo DMAIC en Six Sigma.",
        "¿Cuáles son los principios de integridad de datos exigidos por ALCOA+?",
        "Explica la diferencia entre los indicadores LEADING y LAGGING.",
        "¿Qué protocolo de seguridad es obligatorio antes de intervenir una máquina?",
        "¿Cuál es el menú de hoy en el comedor principal de la planta? (Prueba Anti-Alucinación)"
    ]

    selected_example = st.selectbox("💡 Consultas rápidas cargadas del manual:", example_questions)
    
    # Variable central para capturar la petición activa (MVC Flow)
    active_input = None

    # Si se selecciona una pregunta válida, renderizamos un botón de ejecución inmediata
    if selected_example != "--- Selecciona una pregunta guiada para la presentación ---":
        if st.button("Ejecutar pregunta seleccionada"):
            # Limpiamos la etiqueta de la pregunta trampa antes de enviarla al backend
            active_input = selected_example.replace(" (Prueba Anti-Alucinación)", "")

    # Caja de entrada de texto tradicional por si el profesor quiere preguntar algo libre
    user_query = st.chat_input("O escribe una pregunta personalizada sobre operaciones aquí...")
    if user_query:
        active_input = user_query

    # --- RENDERIZADO DEL HISTORIAL DE CHAT ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- PROCESAMIENTO DE LA PREGUNTA ACTIVA ---
    if active_input:
        # 1. Añadir e imprimir el mensaje del usuario en pantalla
        with st.chat_message("user"):
            st.markdown(active_input)
        st.session_state.messages.append({"role": "user", "content": active_input})

        # 2. Flujo del Controlador: Solicitar respuesta al motor de datos (Modelo RAG)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Buscando en la base de conocimiento GOBS..."):
                answer = st.session_state.controller.process_user_message(active_input)
            
            # 3. Desplegar la respuesta final provista por Gemini
            response_placeholder.markdown(answer)
            
        # Guardar respuesta en el historial de sesión
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # Recarga limpia para actualizar la UI y evitar bucles repetitivos del botón
        st.rerun()

if __name__ == "__main__":
    main()