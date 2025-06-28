import os 
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  

def ask_ai(prompt): 
    url = "https://api.together.xyz/v1/chat/completions"  
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json" 
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  
        "messages": [{"role": "user", "content": prompt}], 
        "temperature": 0.7,  
        "max_tokens": 800  
    }
    response = requests.post(url, headers=headers, json=data)  
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ API Error: {response.text}"  
    
st.set_page_config(page_title="SmartAnalyst - AI Dataset Explorer", layout="wide")
st.title("📊 SmartCSV - AI-Powered Big Dataset Analyzer")

uploaded_file = st.file_uploader("📁 Upload Your Dataset CSV here 📁", type=["csv"])
if uploaded_file:
    st.success("✅ File uploaded successfully!")
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("🔍 Data Preview 🔍")
        st.dataframe(df)
        
        st.subheader("📊 Data Summary Statistics")
        st.write(df.describe(include='all'))

        st.subheader("⚠️ Missing Values in Dataset")
        st.write(df.isnull().sum())

        st.subheader("💬 Ask AI About Your Data")
        query = st.text_area("Type query for your dataset")
        if st.button("Ask from AI"):
            prompt = f"""
            Analyze the following CSV dataset:

            Sample Rows:
            {df.to_string(index=False)}

            Summary:
            {df.describe(include='all').to_string()}

            Null Info:
            {df.isnull().sum().to_string()}

            Question: {query}
            """
            with st.spinner("AI is thinking..."):
                result = ask_ai(prompt)
                st.subheader("📌 AI Response")
                st.markdown(result)

        st.subheader("🧹 Suggest Data Cleaning Steps")
        if st.button("AI Cleaning Suggestions"):
            prompt = f"""
            Suggest data cleaning operations for this dataset:
            Summary:
            {df.describe(include='all').to_string()}
            Null Info:
            {df.isnull().sum().to_string()}
            """
            with st.spinner("Getting AI suggestions..."):
                suggestions = ask_ai(prompt)
                st.markdown(suggestions)

        # ✅ Corrected download button
        clean_csv = df.dropna(axis=1, thresh=int(0.7 * len(df)))
        st.download_button("⬇️ Download Cleaned CSV", clean_csv.to_csv(index=False), file_name="Cleaned_dataset.csv")

    except Exception as e:
        st.error(f"❌ Error in file reading: {e}")
