from dotenv import load_dotenv
import random
import streamlit as st
import base64
import io
from time import time
import json
from src.config import IS_DEBUG, EXPERTS
from src import auth, utils
import streamlit.components.v1 as components

load_dotenv(override=True)

def log_to_console(message: str) -> None:
    js_code = f"""
<script>
    console.log({json.dumps(message)});
</script>
"""
    components.html(js_code)
# ---------------------------- AUTH CHECKS ----------------------------
if IS_DEBUG:
    # skip password check in debug mode
    print("Running in debug mode, skipping password check.")
    st.session_state["password_correct"] = True

elif not auth.check_password():
    print("Password incorrect, stopping the script.")
    st.stop()  # Do not continue if check_password is not True.


# Function to convert uploaded image to base64
def get_image_base64(uploaded_file):
    if uploaded_file is not None:
        # Read file as bytes
        bytes_data = uploaded_file.getvalue()
        
        # Encode to base64
        base64_encoded = base64.b64encode(bytes_data).decode("utf-8")
        return base64_encoded
    return None


# ---------------------------- APP INTERFACE ----------------------------

st.title("Yakkyofy Experts Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = {name: [] for name in EXPERTS.keys()}

if "sessionIds" not in st.session_state:
    st.session_state["sessionIds"] = {name: str(time()*1000) + str(name) for name in EXPERTS.keys()}

# Initialize image state
if "images" not in st.session_state:
    st.session_state["images"] = {name: None for name in EXPERTS.keys()}


# ---------------------------- CHATBOT INTERFACE ----------------------------

tabs = st.tabs(EXPERTS.keys())

for (chatbot_name, chatbot_data), tab in zip(EXPERTS.items(), tabs):

    with tab:

        # add the description of the chatbot
        tab.write(chatbot_data["description"])

        # add the link to the workflow
        tab.markdown(f"**Url**: [n8n WorkFlow]({chatbot_data['workflow_url']})")

        # add a button to rest sessionId and chat history
        if tab.button("Reset chat history", key=f"reset_{chatbot_name}"):
            utils.reset_chat(chatbot_name)
            
        # Create a container for the chat messages
        chat_container = tab.container()
            
        # Add image uploader above the chat area
        uploaded_image = tab.file_uploader("Upload an image (optional)", 
                                          type=["png", "jpg", "jpeg"], 
                                          key=f"image_uploader_{chatbot_name}")
        
        # Display the uploaded image if available
        if uploaded_image is not None:
            tab.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            # Store the base64 encoded image in session state
            st.session_state["images"][chatbot_name] = get_image_base64(uploaded_image)
        
        # Button to clear the uploaded image
        if st.session_state["images"][chatbot_name] is not None:
            if tab.button("Clear image", key=f"clear_image_{chatbot_name}"):
                st.session_state["images"][chatbot_name] = None
                st.rerun()

        # Display chat messages from history on app rerun
        with chat_container:
            for message in st.session_state["messages"][chatbot_name]:
                st.chat_message(message["role"]).markdown(message["content"])

        # Place the chat input at the bottom of the page
        if user_input := tab.chat_input("What is up?", key=f"chat_input_{chatbot_name}"):
            print(f"User input for {chatbot_name}: {user_input}")
            # Display user message in chat message container
            with chat_container:
                st.chat_message("user").markdown(user_input)

            # Add user message to chat history
            st.session_state["messages"][chatbot_name].append({"role": "user", "content": user_input})
            
            # Prepare request params and body
            params = {"text": user_input, "sessionId": st.session_state["sessionIds"][chatbot_name]}
            body = {}
            
            # Add image to body if available
            if st.session_state["images"][chatbot_name] is not None:
                body["image"] = st.session_state["images"][chatbot_name]

            # Call chatbot
            chatbot_message, intermediate_steps = utils.call_chatbot(
                chatbot_data["webhook"],
                params=params,
                body=body if body else None
            )
            log_to_console(f"Calling {chatbot_name} with params: {params} and body: {body}, url: {chatbot_data['webhook']}")
            if chatbot_message is None:
                chatbot_message = "Sorry, an error occurred. Please try again refreshing the app."
            else:
                print(f"chatbot_message from chatbot: {chatbot_message} - sessionId: {st.session_state['sessionIds'][chatbot_name]}")

            # Add assistant chatbot_message to chat history
            st.session_state["messages"][chatbot_name].append({"role": "assistant", "content": chatbot_message})

            # Display assistant chatbot_message in chat message container
            with chat_container:
                st.chat_message("assistant").markdown(chatbot_message)

            if isinstance(intermediate_steps, list):
                st.sidebar.write("Intermediate steps:")
                for step in intermediate_steps:
                    st.sidebar.write(step.get("action").get("tool"))
                    st.sidebar.write("Input: " + str(step.get("action").get("toolInput")))