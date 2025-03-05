import streamlit as st
from dotenv import load_dotenv
import os, random

load_dotenv(override=True)

IS_DEBUG = os.getenv("DEBUG", "").lower() == "true"

HEADERS = {
    "x-access-password": st.secrets["password_endpoint"]
}

EXPERTS = {
    "Master": {
        "webhook": st.secrets.get("MASTER_ENDPOINT"),
        "description": """\
            This is the master chatbot, it can answer any question and he's connected with all the other experts.
        """
    },
    "Amazon Expert": {
        "webhook": st.secrets.get("AMAZON_ENDPOINT"),
        "description": """\
            This is the expert of Amazoon.
            It can find best sellers by category, scrape details of a single product or search for products by keyword.
            It is also connected with the Trends Expert to query interesting topics.
        """
    },
    "Shopify Expert": {
        "webhook": st.secrets.get("SHOPIFY_ENDPOINT"),
        "description": """\
            This is the Shopify expert.
            It can:
            1) get newest shopify products
            2) search shopify shops by their domain (via regex), 
            3) get products of a shopify shop
            4) get shop by category or country
        It is also connected with the Trends Expert to query interesting topics.
        """
    },
    "AliExpress Expert": {
        "webhook": st.secrets.get("ALIEXPRESS_ENDPOINT"),
        "description": """\
            This is the AliExpress expert.
            It can search among winning products using text (via embeddings), or by category.
            It is also connected with the Trends Expert to query interesting topics.
        """
    },
    "GoogleTrend Expert": {
        "webhook": st.secrets.get("GTREND_ENDPOINT"),
        "description": """\
            This is the GoogleTrend expert.
            It can get the latest trends from GoogleTrend.
        """
    },
    # "1688 Expert": {
    #     "webhook": st.secrets.get("1688_ENDPOINT"),
    #     "description": "This is the master chatbot, it can answer any question."
    # },
}