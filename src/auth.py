import streamlit as st
import hmac
import time

def check_password():
    """
    Funzione migliorata per la verifica della password con una migliore esperienza utente.
    """
    def password_entered():
        """Callback eseguito quando viene inserita la password."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            # Simula un breve caricamento per feedback visivo
            progress_text = "Autenticazione in corso..."
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            st.success("Autenticazione riuscita!")
            time.sleep(0.5)
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False
            st.session_state["login_attempts"] = st.session_state.get("login_attempts", 0) + 1

    # Controllo se l'utente è già autenticato
    if st.session_state.get("password_correct", False):
        return True

    # Controlla se ci sono troppi tentativi falliti
    if st.session_state.get("login_attempts", 0) >= 5:
        st.error("⚠️ Troppi tentativi falliti. Riprova più tardi.")
        time.sleep(5)  # Aggiungi un ritardo per sicurezza
        st.session_state["login_attempts"] = 0
        return False

    # UI migliorata per il login
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-header">', unsafe_allow_html=True)
    st.markdown('### Accesso richiesto</div>', unsafe_allow_html=True)
    
    # Campo password con istruzioni
    st.text_input(
        "Inserisci la password per accedere", 
        type="password", 
        on_change=password_entered, 
        key="password",
        help="Contatta l'amministratore se hai dimenticato la password"
    )
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        attempts_left = 5 - st.session_state.get("login_attempts", 0)
        st.error(f"❌ Password non corretta. Tentativi rimasti: {attempts_left}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return False