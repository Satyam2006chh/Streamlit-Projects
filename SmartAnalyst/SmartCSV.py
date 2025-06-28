import os 
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("Your_api_key")


def ask_ai(prompt): 
    url = "https://api.together.xyz/v1/chat/completions"  
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}","Content-Type": "application/json" 
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  
        "messages": [{"role": "user", "content": prompt}], 
        "temperature": 0.7,  
        "max_tokens": 800  
    }
    response = requests.post(url, headers=headers, json=data)  
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']  # Extract AI reply
    else:
        return f"❌ API Error: {response.text}"  
    


