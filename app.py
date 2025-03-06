from dotenv import load_dotenv
import random
import streamlit as st

from src.config import IS_DEBUG, EXPERTS, HEADERS
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

st.title("Yakkyofy Experts Interface")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = {name: [] for name in EXPERTS.keys()}

if "sessionIds" not in st.session_state:
    ids = random.sample(range(1, 100000), len(EXPERTS.keys()))
    st.session_state["sessionIds"] = {name: str(_id) for _id, name in zip(ids, EXPERTS.keys())}


# create a tab for each chatbot
tabs = st.tabs(EXPERTS.keys())

for (chatbot_name, chatbot_data), tab in zip(EXPERTS.items(), tabs):

    with tab:

        # add the description of the chatbot
        st.write(chatbot_data["description"])

        # add the link to the workflow
        st.markdown(f"**Url**: [n8n WorkFlow]({chatbot_data['workflow_url']})")


        # add a button to rest sessionId and chat history
        if st.button("Reset chat history", key=f"reset_{chatbot_name}"):
            utils.reset_chat(chatbot_name)

        # Display chat messages from history on app rerun
        for message in st.session_state["messages"][chatbot_name]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What is up?", key=f"chat_input_{chatbot_name}"):

            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)

            # Add user message to chat history
            st.session_state["messages"][chatbot_name].append({"role": "user", "content": prompt})

            # Call chatbot
            response = utils.call_chatbot(
                chatbot_data["webhook"],
                params={"text": prompt, "sessionId": st.session_state["sessionIds"][chatbot_name]},
                headers=HEADERS
            )

            if response is None:
                response = "Sorry, an error occured. Please try again refreshing the app."
            else:
                print(f"Response from chatbot: {response} - sessionId: {st.session_state['sessionIds'][chatbot_name]}")

            # Add assistant response to chat history
            st.session_state["messages"][chatbot_name].append({"role": "assistant", "content": response})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
