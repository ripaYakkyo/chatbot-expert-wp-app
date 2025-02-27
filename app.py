import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv
import time
from src import auth

load_dotenv(override=True)

# Configurazione della pagina
st.set_page_config(
    page_title="Winning Expert",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Applica CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChat message {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .chat-container {
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        background-color: #f9f9f9;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f0f2f6;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------- AUTH CHECKS ----------------------------
if os.getenv("DEBUG", "").lower() == "true":
    print("Running in debug mode, skipping password check.")
    st.session_state["password_correct"] = True
    st.session_state["user_email"] = os.getenv("DEFAULT_EMAIL")
    # Mostrare una notifica per debug
    st.toast("App in modalità debug", icon="⚠️")

elif not auth.check_password():
    # Versione migliorata della pagina di login
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>Winning Expert</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Il tuo assistente esperto per le decisioni vincenti</p>", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/300x150?text=Winning+Expert+Logo", use_column_width=True)
        st.info("Inserisci la password per accedere all'applicazione")
    st.stop()  # Do not continue if check_password is not True.

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150?text=Logo", use_column_width=True)
    st.markdown("### Menu")
    
    # Informazioni utente
    st.markdown("---")
    st.markdown("### Profilo Utente")
    if "user_email" in st.session_state:
        st.info(f"Logged in as: {st.session_state['user_email']}")
    else:
        st.info("Utente autenticato")
    
    # Tema dell'applicazione
    st.markdown("---")
    theme = st.selectbox("Tema", ["Chiaro", "Scuro", "Sistema"])
    
    # Impostazioni aggiuntive
    st.markdown("---")
    st.markdown("### Impostazioni")
    response_speed = st.slider("Velocità risposte", min_value=1, max_value=5, value=3)
    st.checkbox("Salva conversazioni", value=True)
    
    st.markdown("---")
    if st.button("Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

# Contenuto principale
st.markdown("<h1 class='main-header'>Winning Expert</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Il tuo assistente esperto per le decisioni vincenti</p>", unsafe_allow_html=True)

# Tabs per organizzare il contenuto
tab1, tab2 = st.tabs(["Chat", "Informazioni"])

with tab1:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Messaggio di benvenuto
        welcome_msg = "Ciao! Sono Winning Expert, il tuo assistente personale. Come posso aiutarti oggi?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Cosa desideri sapere?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Simulate typing
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ Sto elaborando la risposta...")
            
            # Actual API request
            sessionId = random.randint(1, 100000)
            get_response = requests.get(
                st.secrets["webhook"], 
                params={"text": prompt, "sessionId": str(sessionId)}, 
                headers={"x-access-password": st.secrets["password_endpoint"]}
            )
            
            try:
                response = get_response.json()
                # Simula lentamente la risposta
                full_response = response["output"]
                
                if response_speed < 5:  # Se non è impostato alla velocità massima
                    for i in range(len(full_response) // 10):
                        time.sleep(0.05)  # Piccolo ritardo
                        displayed_response = full_response[:i*10]
                        message_placeholder.markdown(displayed_response + "▌")
                
                # Mostra risposta completa
                message_placeholder.markdown(full_response)
                # Aggiungi risposta alla cronologia
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                message_placeholder.markdown(f"Mi dispiace, si è verificato un errore: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.header("Informazioni su Winning Expert")
    st.write("""
    Winning Expert è il tuo assistente personale per prendere decisioni informate.
    Utilizza tecnologie all'avanguardia per fornirti le migliori risposte alle tue domande.
    """)
    
    st.subheader("Come utilizzare la chat")
    st.write("""
    1. Inserisci la tua domanda nella barra di input in basso
    2. Attendi la risposta dell'assistente
    3. Continua la conversazione con domande di follow-up
    """)
    
    st.subheader("Funzionalità")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- 💬 Conversazione naturale")
        st.markdown("- 🔍 Risposte dettagliate")
    with col2:
        st.markdown("- 📊 Analisi personalizzate")
        st.markdown("- 📘 Consigli esperti")

# Footer
st.markdown("""
<div class="footer">
    © 2025 Winning Expert | Per supporto: support@winningexpert.com | Versione 1.0.0
</div>
""", unsafe_allow_html=True)