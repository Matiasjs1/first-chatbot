# 🤖 Mi Chat IA

Primer **chatbot con IA** construido con **Streamlit** y la API de **Groq**. Chat en tiempo real con respuestas en streaming, selector de modelo y guardado del historial de conversación.

🌐 **Probar:** [first-chatbot-mjs.streamlit.app](https://first-chatbot-mjs.streamlit.app/)

---

## ✅ Funcionalidades

- **Chat por streaming:** las respuestas se escriben en tiempo real.
- **Selector de modelos:** elegí el modelo desde la barra lateral.
- **Historial de conversación** persistente en la sesión.
- **Aviso de bienvenida** con nombre del usuario.
- Interfaz limpia con `st.chat_message` y avatares.

### Modelos disponibles (plan Developer de Groq, 2026)

- `openai/gpt-oss-120b`
- `openai/gpt-oss-20b`
- `qwen/qwen3.6-27b`

> Los anteriores (llama 3.1/3.3) pasaron a Enterprise y gemma/mixtral/llama3 fueron descontinuados, por eso solo se listan los modelos vigentes para una key de plan Developer.

---

## 🏗️ Stack

- **App:** Streamlit (Python).
- **IA:** API de Groq (`groq`), con `chat.completions` en modo `stream`.
- **Secrets:** `st.secrets['CLAVE_API']` con la API key de Groq.

```
first-chatbot/
├── main.py           # App Streamlit
├── requirements.txt
└── .streamlit/config.toml
```

---

## 🚀 Setup local

```bash
pip install -r requirements.txt
```

Configurá la API key de Groq en `.streamlit/secrets.toml`:

```toml
CLAVE_API = "gsk_..."
```

Y ejecutá:

```bash
streamlit run main.py
```
