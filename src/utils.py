from typing import Dict, Any, Union
from time import sleep
import requests
import random
import streamlit as st

from src.config import HEADERS


def call_chatbot(url: str, params: Dict[str, Any]={}, body: Dict[str, Any]=None) -> Union[str, None]:
    # sleep(1.5)
    # return "test response"

    print(f"Calling {url} with params: {params} and body: {body}")
    try:
        response = requests.get(url, params=params, json=body, headers=HEADERS)

        if response.status_code != 200:
            print(f"Error calling {url}: {response.status_code} - {response.text[:100]}")
            return None

        if "output" not in response.json():
            print(f"Error calling {url}: {response.json()} - NO OUTPUT FOUND")
            return None

        return response.json()["output"]

    except Exception as e:
        print(f"Error calling {url}: {e}")
        return None



def reset_chat(chatbot_name: str) -> None:
    del st.session_state["messages"][chatbot_name]
    st.session_state["messages"][chatbot_name] = []

    existing_ids = set(list(st.session_state["sessionIds"].values())).difference(st.session_state["sessionIds"][chatbot_name])
    invalid_ids = existing_ids.union(st.session_state["alltime_sessionIds"])

    candidate_ids = list(set(range(1, 100000)).difference(invalid_ids))

    st.session_state["sessionIds"][chatbot_name] = str(random.choice(candidate_ids))
    st.session_state["alltime_sessionIds"].add(st.session_state["sessionIds"][chatbot_name])

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
