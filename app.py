import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv
import streamlit as st
from src import auth

load_dotenv(override=True)

# ---------------------------- AUTH CHECKS ----------------------------
if os.getenv("DEBUG", "").lower() == "true":
    print("Running in debug mode, skipping password check.")
    st.session_state["password_correct"] = True
    st.session_state["user_email"] = os.getenv("DEFAULT_EMAIL")
    pass # skip password check in debug mode

elif not auth.check_password():
    print("Password incorrect, stopping the script.")
    st.stop()  # Do not continue if check_password is not True.
    
st.title("Winning Expert")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    sessionId = random.randint(1, 100000)
    get_response = requests.get(st.secrets["webhook"], params={"text": prompt, "sessionId": str(sessionId)}, headers={"x-access-password": st.secrets["password_endpoint"]})
    response = get_response.json()
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})

    # response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["output"])
    # Add assistant response to chat history