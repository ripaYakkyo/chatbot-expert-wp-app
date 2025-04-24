from dotenv import load_dotenv
import random
import streamlit as st

from src.config import IS_DEBUG, EXPERTS
from src import auth, utils

load_dotenv(override=True)


# ---------------------------- AUTH CHECKS ----------------------------
if IS_DEBUG:
    # skip password check in debug mode
    print("Running in debug mode, skipping password check.")
    st.session_state["password_correct"] = True

elif not auth.check_password():
    print("Password incorrect, stopping the script.")
    st.stop()  # Do not continue if check_password is not True.


# ---------------------------- APP INTERFACE ----------------------------

st.title("Yakkyofy Experts Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = {name: [] for name in EXPERTS.keys()}

if "sessionIds" not in st.session_state:
    ids = random.sample(range(1, 100000), len(EXPERTS.keys()))
    st.session_state["sessionIds"] = {name: str(_id) for _id, name in zip(ids, EXPERTS.keys())}
    st.session_state["alltime_sessionIds"] = set(st.session_state["sessionIds"].values())


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

        # Display chat messages from history on app rerun
        for message in st.session_state["messages"][chatbot_name]:
            tab.chat_message(message["role"]).markdown(message["content"])

        if user_input := tab.chat_input("What is up?", key=f"chat_input_{chatbot_name}"):

            # Display user message in chat message container
            tab.chat_message("user").markdown(user_input)

            # Add user message to chat history
            st.session_state["messages"][chatbot_name].append({"role": "user", "content": user_input})

            # Call chatbot
            chatbot_message, intermediate_steps = utils.call_chatbot(
                chatbot_data["webhook"],
                params={"text": user_input, "sessionId": st.session_state["sessionIds"][chatbot_name]},
            )

            if chatbot_message is None:
                chatbot_message = "Sorry, an error occured. Please try again refreshing the app."
            else:
                print(f"chatbot_message from chatbot: {chatbot_message} - sessionId: {st.session_state['sessionIds'][chatbot_name]}")

            # Add assistant chatbot_message to chat history
            st.session_state["messages"][chatbot_name].append({"role": "assistant", "content": chatbot_message})
            st.sidebar.write("Intermediate steps:")
            for step in intermediate_steps:
                st.sidebar.write(step.get("action").get("tool"))
            # Display assistant chatbot_message in chat message container
            tab.chat_message("assistant").markdown(chatbot_message)

