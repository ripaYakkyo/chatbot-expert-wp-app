import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv(override=True)

IS_DEBUG = os.getenv("DEBUG", "").lower() == "true"

HEADERS = {
    "x-access-password": st.secrets["password_endpoint"]
}

EXPERTS = {
    "Master": {
        "webhook": st.secrets.get("MASTER_ENDPOINT"),
        "workflow_url": st.secrets.get("WORKFLOW_MASTER"),
        "description": """\
            This is the master chatbot, it can answer any question and he's connected with all the other experts.
        """
    },
    "Amazon Expert": {
        "webhook": st.secrets.get("AMAZON_ENDPOINT"),
        "workflow_url": st.secrets.get("WORKFLOW_AMAZON"),
        "description": """\
            This is the expert of Amazoon.
            It can find best sellers by category, scrape details of a single product or search for products by keyword.
            It is also connected with the Trends Expert to query interesting topics.
        """
    },
    "Shopify Expert": {
        "webhook": st.secrets.get("SHOPIFY_ENDPOINT"),
        "workflow_url": st.secrets.get("WORKFLOW_SHOPIFY"),
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
        "workflow_url": st.secrets.get("WORKFLOW_ALIEXPRESS"),
        "description": """\
            This is the AliExpress expert.
            It can search among winning products using text (via embeddings), or by category.
            It can also search on the whole AliExpress via image search.
            It can query product details providing the productId.
            It is also connected with the Trends Expert to query interesting topics.
        """
    },
    "TRENDS Expert": {
        "webhook": st.secrets.get("GTREND_ENDPOINT"),
        "workflow_url": st.secrets.get("WORKFLOW_TRENDS"),
        "description": """\
            This is the TRENDS expert.
            It can get the latest trends from GoogleTrends.
        """
    },
    "1688 Expert": {
        "webhook": st.secrets.get("ENDPOINT_1688"),
        "workflow_url": st.secrets.get("WORKFLOW_1688"),
        "description": """\
            This is the 1688 expert.
            It can search for winning products from 1688 by category or by title;
            it can also perform image-search (with an url provided) on the whole 1688 platform.
            It is also connected with the Trends Expert to query interesting topics.
        """
    },
    "Ads Expert": {
        "webhook": st.secrets.get("ADS_ENDPOINT"),
        "workflow_url": st.secrets.get("WORKFLOW_ADS"),
        "description": """\
            This is the Ads expert.
            It can get the latest ads from Meta (Facebook, Instagram etc..) and TikTok.
        """
    },
    "Shein Expert": {
        "webhook": st.secrets.get("SHEIN_ENDPOINT"),
        "workflow_url": st.secrets.get("WORKFLOW_SHEIN"),
        "description": """\
            This is the Shein expert.
            It can get the best sellers of shein and the top products by category
        """
    }
}