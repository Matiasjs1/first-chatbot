import groq as gr
import streamlit as st
st.set_page_config("MI CHAT BOT")

FALLBACK = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'gemma2-9b-it']


def crear_usuario():
    clave_secreta = st.secrets['CLAVE_API']
    return gr.Groq(api_key=clave_secreta)


def obtener_modelos(cliente):
    """Trae los IDs de modelos reales disponibles para esta key desde la API de Groq."""
    try:
        modelos = []
        for m in cliente.models.list():
            mid = m.id
            if any(x in mid.lower() for x in ('whisper', 'tts', 'eleven', 'playai', 'guard')):
                continue
            modelos.append(mid)
        if modelos:
            return modelos
    except Exception:
        pass
    return FALLBACK


def configurar_pagina(modelos):
    st.title("Mi chat IA")
    nombre = st.text_input("¿Cuál es tu nombre? ")
    if st.button("Saludar"):
        st.write(f"Hola {nombre}")
    st.sidebar.title("Configuración modelos")
    modelo_elegido = st.sidebar.selectbox("Modelos", modelos, index=0)
    return modelo_elegido


def configurar_modelo(cliente, modelo, mensaje_entrada):
    return cliente.chat.completions.create(model=modelo, messages=[{"role": "user", "content": mensaje_entrada}], stream=True)


def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})


def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


def area_chat():
    contenedor = st.container(height=400, border=True)
    with contenedor:
        mostrar_historial()


def generar_respuesta(respuesta_ia):
    respuesta_completa = ""
    for frase in respuesta_ia:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


def main():
    usuario_groq = crear_usuario()
    modelos = obtener_modelos(usuario_groq)
    inicializar_estado()
    modelo_actual = configurar_pagina(modelos)
    area_chat()
    mensaje_usuario = st.chat_input("Ingrese su prompt")

    if mensaje_usuario:
        actualizar_historial("user", mensaje_usuario, "💀")
        try:
            respuesta_ia = configurar_modelo(usuario_groq, modelo_actual, mensaje_usuario)
        except Exception:
            st.error(f"No pude usar el modelo '{modelo_actual}'. Probá elegir otro de la lista.")
            st.stop()
        if respuesta_ia:
            with st.chat_message("assistant"):
                respuesta_ia = st.write_stream(generar_respuesta(respuesta_ia))
                actualizar_historial("assistant", respuesta_ia, "🤖")
                st.rerun()


if __name__ == "__main__":
    main()
