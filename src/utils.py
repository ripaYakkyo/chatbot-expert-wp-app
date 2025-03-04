from typing import Dict, Any, Union
import requests
import random
import streamlit as st


def call_chatbot(url: str, params: Dict[str, Any]={}, body: Dict[str, Any]=None, headers: Dict[str, Any]={}) -> Union[str, None]:

    print(f"Calling {url} with params: {params} and body: {body}")
    try:
        response = requests.get(url, params=params, json=body, headers=headers)

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

    candidate_ids = list(set(range(1, 100000)).difference(existing_ids))
    st.session_state["sessionIds"][chatbot_name] = str(random.choice(candidate_ids))
    return None
