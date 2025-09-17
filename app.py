# 🤖 AI Chatbot Frontend - Part 1: Simple Chat UI
#
# NOTE FOR ENTIRE EXERCISE:
# This frontend file (app.py) will NOT change throughout the 7-part tutorial.
# You will only work on different backend.py logic files for each part.
# When your initial backend.py is ready, uncomment lines 15-16 below to connect to your AI backend.

import streamlit as st
from backend import get_ai_response

print("🚀 Starting chatbot...")

# Configure the web page appearance
st.set_page_config(page_title="My First GPT Chat App", page_icon="🤖")
st.title("🤖 My First GPT Chat App")

# Create text input area for user messages
user_message = st.text_area("Your message:", height=100)

# Handle send button click
if st.button("📤 Send") and user_message:
     
    with st.spinner("Connecting to OpenAI..."):
        response = get_ai_response(user_message)
    

    # Display the conversation
    st.markdown("**You:**")
    st.write(user_message)

    
    st.markdown("**AI:**")
    st.write(response)
    
    
    
    
    
    
# --- Show Latest Commit Message ---
# This snippet displays the last commit message at the bottom-right of the Streamlit app.
# It first checks if a 'commit.txt' file exists (useful for deployments),
# otherwise it falls back to reading the latest commit from git.
# If neither is available, it shows a default message.
# No need to deep dive – just a simple way to know what version of code is running.


import subprocess, os
from pathlib import Path
 
st.markdown(f"<div style='position:fixed; bottom:20px; right:20px; color:gray; font-size:15px; opacity:0.8;'>{(Path(__file__).parent / 'commit.txt').read_text().strip() if (Path(__file__).parent / 'commit.txt').exists() else subprocess.getoutput('git log -1 --pretty=%B') if os.path.exists(Path(__file__).parent / '.git') else 'No commit info'}</div>", unsafe_allow_html=True)
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-4.1",
  input=[
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "ou are a helpful assistant that answers customer FAQs about Metadata IQ.\nAlways provide clear, concise, and accurate information about the product.\nUse the official product documentation and FAQs provided in your knowledge base as the source of truth.\nIf you are unsure of an answer or if the question is outside the product’s scope, politely state that and suggest contacting support at support@digital-nirvana.com.\nKeep answers simple and easy to understand.\nAvoid making assumptions or providing information not related to Metadata IQ."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is metadatiq"
        }
      ]
    },
    {
      "id": "msg_0464d0a6bd3271550068ca5087d11081a0bf3a403bf47f40ee",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata IQ is an on-premises, AI-powered tool developed by Digital Nirvana. It automates the generation, enrichment, and management of metadata for video and audio content. By integrating with Avid® MediaCentral | Production Management, Metadata IQ helps users easily tag, index, and organize their media assets, making content discovery, editing, and production workflows more efficient.\n\nIf you have more specific questions about its features or usage, feel free to ask!"
        }
      ]
    }
  ],
  text={
    "format": {
      "type": "text"
    }
  },
  reasoning={},
  tools=[],
  temperature=1,
  max_output_tokens=2048,
  top_p=1,
  store=True,
  include=["web_search_call.action.sources"]
)