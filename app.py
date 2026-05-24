import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="SOMIX — Tu cuerpo, tu amigo",
    page_icon="🫂",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');

:root {
  --purple: #9B59D6;
  --green: #4BC99A;
  --teal: #1B6B5A;
}

@media (prefers-color-scheme: dark) {
  html, body, .stApp { background-color: #0d2620 !important; }
  [data-testid="stSidebar"] { background: linear-gradient(180deg, #0a1f1a 0%, #0d2620 100%) !important; border-right: 1px solid rgba(75,201,154,0.15) !important; }
  [data-testid="stSidebar"] * { color: #c8f0e4 !important; }
  .welcome-card { background: rgba(255,255,255,0.04) !important; border-color: rgba(75,201,154,0.2) !important; }
  .welcome-card-title { color: #6ddbb0 !important; }
  .welcome-card-desc { color: #5a9e80 !important; }
  .edad-container { background: rgba(255,255,255,0.04) !important; border-color: rgba(75,201,154,0.2) !important; }
  .main-subtitle { color: #5a9e80 !important; }
  [data-testid="stChatMessage"] .stChatMessageContent { background: rgba(255,255,255,0.05) !important; border-color: rgba(75,201,154,0.12) !important; color: #e0f5ee !important; }
  [data-testid="stNumberInput"] input { background: rgba(255,255,255,0.07) !important; border-color: rgba(75,201,154,0.3) !important; color: #e0f5ee !important; }
}

@media (prefers-color-scheme: light) {
  html, body, .stApp { background-color: #f0faf6 !important; }
  [data-testid="stSidebar"] { background: linear-gradient(180deg, #e8f8f2 0%, #ddf4eb 100%) !important; border-right: 1px solid rgba(27,107,90,0.15) !important; }
  [data-testid="stSidebar"] * { color: #1B4A3A !important; }
  .welcome-card { background: rgba(255,255,255,0.8) !important; border-color: rgba(75,201,154,0.3) !important; box-shadow: 0 2px 12px rgba(27,107,90,0.08) !important; }
  .welcome-card-title { color: #1B6B5A !important; }
  .welcome-card-desc { color: #4a8a70 !important; }
  .edad-container { background: white !important; border-color: rgba(75,201,154,0.3) !important; box-shadow: 0 4px 24px rgba(27,107,90,0.1) !important; }
  .main-subtitle { color: #4a8a70 !important; }
  [data-testid="stChatMessage"] .stChatMessageContent { background: white !important; border-color: rgba(75,201,154,0.2) !important; color: #1a3a2a !important; }
  [data-testid="stNumberInput"] input { background: white !important; border-color: rgba(75,201,154,0.4) !important; color: #1a3a2a !important; }
}

* { box-sizing: border-box; }
html, body, .stApp { font-family: 'Nunito Sans', sans-serif !important; }

.stButton > button {
  background: linear-gradient(135deg, #9B59D6, #4BC99A) !important;
  color: white !important; border: none !important; border-radius: 14px !important;
  padding: 11px 20px !important; font-family: 'Nunito', sans-serif !important;
  font-weight: 700 !important; font-size: 14px !important; width: 100% !important;
  transition: all 0.25s !important; margin-bottom: 8px !important;
  box-shadow: 0 4px 15px rgba(155,89,214,0.3) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(155,89,214,0.45) !important; }

.main-title {
  font-family: 'Nunito', sans-serif; font-size: 56px; font-weight: 800;
  background: linear-gradient(135deg, #9B59D6, #4BC99A);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; letter-spacing: -1px; line-height: 1; margin-bottom: 10px;
}
.main-subtitle { font-size: 16px; margin-bottom: 30px; }

.welcome-card { border-radius: 18px; padding: 22px; margin-bottom: 14px; border: 1px solid; transition: all 0.25s; }
.welcome-card:hover { transform: translateY(-3px); }
.welcome-card-icon { font-size: 26px; margin-bottom: 10px; }
.welcome-card-title { font-family: 'Nunito', sans-serif; font-weight: 700; font-size: 15px; margin-bottom: 5px; }
.welcome-card-desc { font-size: 13px; line-height: 1.5; }

.edad-container { max-width: 420px; margin: 30px auto; border-radius: 24px; padding: 40px; text-align: center; border: 1px solid; }
.edad-title { font-family: 'Nunito', sans-serif; font-size: 26px; font-weight: 800; color: #9B59D6; margin-bottom: 10px; }
.edad-desc { font-size: 14px; margin-bottom: 24px; line-height: 1.6; }

.sidebar-divider { height: 1px; background: rgba(75,201,154,0.15); margin: 14px 0; }
.sidebar-section-title { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; font-weight: 700; }

[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 6px 0 !important; }
[data-testid="stChatMessage"] .stChatMessageContent { border-radius: 18px !important; padding: 14px 18px !important; font-size: 15px !important; line-height: 1.6 !important; }
[data-testid="stChatInput"] textarea { border-radius: 16px !important; font-family: 'Nunito Sans', sans-serif !important; font-size: 15px !important; }
[data-testid="stNumberInput"] input { text-align: center !important; font-size: 28px !important; font-weight: 700 !important; border-radius: 14px !important; }

#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: linear-gradient(135deg, #9B59D6, #4BC99A) !important;
    border-radius: 0 12px 12px 0 !important;
    color: white !important;
    width: 28px !important;
    height: 52px !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    box-shadow: 3px 3px 10px rgba(155,89,214,0.35) !important;
    transition: all 0.2s !important;
    top: 50% !important;
    position: fixed !important;
    left: 0 !important;
    z-index: 999 !important;
}

[data-testid="collapsedControl"]:hover {
    width: 34px !important;
    box-shadow: 4px 4px 16px rgba(75,201,154,0.45) !important;
}
</style>
""", unsafe_allow_html=True)

if "chats" not in st.session_state:
    st.session_state.chats = {}
if "chat_actual" not in st.session_state:
    st.session_state.chat_actual = None
if "edad" not in st.session_state:
    st.session_state.edad = None

def nuevo_chat():
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.chats[chat_id] = {"titulo": "Nueva conversación", "mensajes": []}
    st.session_state.chat_actual = chat_id
    return chat_id

def get_system_prompt(edad):
    if edad <= 14:
        perfil = "Usa lenguaje muy sencillo y amigable. Explica solo temas básicos: pubertad, higiene, emociones. Evita contenido explícito. Sé cálido y paciente."
    elif edad <= 17:
        perfil = "Habla directo y empático. Puedes hablar de consentimiento, relaciones saludables, ITS y métodos anticonceptivos básicos."
    else:
        perfil = "Usa terminología médica correcta. Aborda educación sexual integral, derechos reproductivos, bienestar emocional y diversidad sexual."
    return f"""Eres SOMIX, asistente de educación sexual para jóvenes mexicanos. El usuario tiene {edad} años.
{perfil}
Nunca juzgues. No pidas datos personales. Si detectas abuso o crisis emocional proporciona: Línea de la Vida 800 911 2000, SAPTEL 55 5259-8121. No reemplazas atención médica. Responde en español mexicano cálido."""

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Nunito',sans-serif; font-size:26px; font-weight:800; background:linear-gradient(135deg,#9B59D6,#4BC99A); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:2px;">🫂 SOMIX</div>
    <div style="font-size:11px; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:20px; font-weight:600; color:#4a8a70;">Tu cuerpo, tu amigo 💚</div>
    """, unsafe_allow_html=True)

    if st.button("✨ Nueva conversación"):
        nuevo_chat()
        st.rerun()

    if st.session_state.chats:
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">💬 Conversaciones</div>', unsafe_allow_html=True)
        for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
            is_active = chat_id == st.session_state.chat_actual
            titulo = chat_data["titulo"]
            titulo_short = titulo[:32] + "..." if len(titulo) > 32 else titulo
            prefix = "▶ " if is_active else "   "
            if st.button(f"{prefix}{titulo_short}", key=f"chat_{chat_id}"):
                st.session_state.chat_actual = chat_id
                st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px; line-height:1.8; color:#4a8a70;">
    🤖 Esta IA utiliza tecnología automatizada. Sus respuestas pueden tener errores. Verifique los datos con fuentes oficiales<br>
    🇲🇽 Hecho con amor en México<br><br>
    <strong>¿Crisis?</strong> Línea de la Vida:<br>
    <strong>800 911 2000</strong> (gratis 24h)
    </div>
    """, unsafe_allow_html=True)

if st.session_state.edad is None:
    st.markdown("""
    <div style="text-align:center; padding:30px 0 10px;">
        <div class="main-title">SOMIX</div>
        <div class="main-subtitle">Tu espacio seguro de educación sexual y bienestar emocional 💜</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="edad-container">
            <div style="font-size:56px; margin-bottom:12px;">🫂</div>
            <div class="edad-title">¡Hola! Soy SOMIX 👋</div>
            <div class="edad-desc">Estoy aquí para orientarte sobre salud sexual y bienestar emocional.<br><br>
            Para darte la mejor información, <strong style="color:#4BC99A;">¿cuántos años tienes?</strong></div>
        </div>
        """, unsafe_allow_html=True)
        edad = st.number_input("", min_value=12, max_value=21, value=16, step=1, label_visibility="collapsed")
        if st.button("Comenzar →"):
            st.session_state.edad = edad
            nuevo_chat()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="welcome-card"><div class="welcome-card-icon">🔴</div><div class="welcome-card-title">Atención</div><div class="welcome-card-desc">Para personas menores de 18 años, el uso de SOMIX debe realizarse con supervisión de padre, madre o tutor.</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="welcome-card"><div class="welcome-card-icon">💜</div><div class="welcome-card-title">Sin juicios</div><div class="welcome-card-desc">Todas las preguntas son válidas. Aquí te escuchamos con respeto.</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="welcome-card"><div class="welcome-card-icon">🔒</div><div class="welcome-card-title">Aviso de privacidad</div><div class="welcome-card-desc">El agente nunca reemplaza a un profesional de la salud. Para mayor orientación consulte a un profesional.</div></div>', unsafe_allow_html=True)

else:
    if st.session_state.chat_actual is None or st.session_state.chat_actual not in st.session_state.chats:
        nuevo_chat()
        st.rerun()

    chat = st.session_state.chats[st.session_state.chat_actual]
    mensajes = chat["mensajes"]

    if not mensajes:
        st.markdown("""
        <div style="text-align:center; padding:30px 0 10px;">
            <div style="font-size:56px; margin-bottom:12px;">🫂</div>
            <div style="font-family:'Nunito',sans-serif; font-size:32px; font-weight:800; background:linear-gradient(135deg,#9B59D6,#4BC99A); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">¿En qué puedo ayudarte? 💚</div>
            <div style="font-size:14px; color:#4a8a70; margin-top:8px;">Pregunta lo que quieras, estoy aquí sin juzgarte.</div>
        </div>
        """, unsafe_allow_html=True)
        sugs = ["¿Qué es el consentimiento?", "¿Cómo sé si mi relación es sana?", "¿Qué métodos anticonceptivos existen?", "¿Qué es la pubertad?"]
        cols = st.columns(2)
        for i, sug in enumerate(sugs):
            with cols[i % 2]:
                if st.button(f"💬 {sug}", key=f"sug_{i}"):
                    mensajes.append({"role": "user", "content": sug})
                    chat["titulo"] = sug
                    with st.spinner("SOMIX está escribiendo..."):
                        model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=get_system_prompt(st.session_state.edad))
                        response = model.start_chat(history=[]).send_message(sug)
                        reply = response.text
                    mensajes.append({"role": "assistant", "content": reply})
                    st.rerun()

    for mensaje in mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if prompt := st.chat_input("Escribe tu pregunta aquí... 💬"):
        mensajes.append({"role": "user", "content": prompt})
        if len(mensajes) == 1:
            chat["titulo"] = prompt[:40] + "..." if len(prompt) > 40 else prompt
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("SOMIX está escribiendo..."):
                history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in mensajes[:-1]]
                model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=get_system_prompt(st.session_state.edad))
                response = model.start_chat(history=history).send_message(prompt)
                reply = response.text
                st.markdown(reply)
        mensajes.append({"role": "assistant", "content": reply})
        st.rerun()