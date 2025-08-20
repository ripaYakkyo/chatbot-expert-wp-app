from typing import Dict, Any, Union, Optional
from time import sleep
from time import time
import requests
import random
import streamlit as st
from pydantic import BaseModel

from src.config import HEADERS


class BodyChat(BaseModel):
    sessionId: str
    user_query: str
    image: Optional[Union[str, None]] = None
    is_test_chat: Optional[Union[bool, None]] = False
    add_tools_to_chat: Optional[Union[bool, None]] = True
    model: Optional[Union[str, None]] = "ft:gpt-4.1-mini-2025-04-14:yakkyo-spa:tools-and-knowledge:Bx7yOspD"


def call_chatbot(url: str, body_chat: BodyChat) -> Union[str, None]:
    # sleep(1.5)
    # return "test response"

    print(f"Calling {url} with body: {body_chat.model_dump()}")
    try:
        response = requests.post(url, json=body_chat.model_dump(), headers=HEADERS)

        if response.status_code != 200:
            print(f"Error calling {url}: {response.status_code} - {response.text[:100]}")
            return None, None
        res = response.json()
        if "output" not in res:
            print(f"Error calling {url}: {res} - NO OUTPUT FOUND")
            return None, None

        return res["output"], res.get("intermediateSteps", None)

    except Exception as e:
        print(f"Error calling {url}: {e}")
        return None, None



def reset_chat(chatbot_name: str) -> None:
    del st.session_state["messages"][chatbot_name]
    st.session_state["messages"][chatbot_name] = []

    # existing_ids = set(list(st.session_state["sessionIds"].values())).difference(st.session_state["sessionIds"][chatbot_name])
    
    # invalid_ids = existing_ids.union(st.session_state["alltime_sessionIds"])

    # candidate_ids = list(set(range(1, 100000)).difference(invalid_ids))

    st.session_state["sessionIds"][chatbot_name] = str(time()*1000)+ str(chatbot_name)
    # st.session_state["alltime_sessionIds"].add(st.session_state["sessionIds"][chatbot_name])

    return None


# def on_chat_input(chatbot_name: str, chatbot_data: dict) -> None:

#     # retrieve the user_input from the chat_input widget
#     user_input = st.session_state[f"chat_input_{chatbot_name}"]

#     # Display user message in chat message container
#     st.chat_message("user").markdown(user_input)

#     # Add user message to chat history
#     st.session_state["messages"][chatbot_name].append({"role": "user", "content": user_input})

#     # Call chatbot
#     # response = call_chatbot(
#     #     chatbot_data["webhook"],
#     #     params={"text": user_input, "sessionId": st.session_state["sessionIds"][chatbot_name]},
#     #     headers=HEADERS
#     # )
#     sleep(1.5)
#     response = "This is a test response"

#     if response is None:
#         response = "Sorry, an error occured. Please try again refreshing the app."
#     else:
#         print(f"Response from chatbot: {response} - sessionId: {st.session_state['sessionIds'][chatbot_name]}")

#     # Add assistant response to chat history
#     st.session_state["messages"][chatbot_name].append({"role": "assistant", "content": response})

#     # Display assistant response in chat message container
#     st.chat_message("assistant").markdown(response)

#     return None
