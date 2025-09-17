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