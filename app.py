# 🤖 PROACTIVE AI ASSISTANT FOR FINANCIAL ADVISORS
# Automatically provides daily briefings and offers autonomous actions

import streamlit as st
from backend import get_ai_response, get_daily_briefing
from datetime import datetime
import time

print("🚀 Starting Proactive AI Assistant...")

# Configure the web page appearance
st.set_page_config(
    page_title="🤖 Proactive AI Assistant - Financial Advisor",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4e79, #2e8b57);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}
.briefing-box {
    background: #f0f8ff;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #2e8b57;
    margin-bottom: 1rem;
}
.action-button {
    background: #2e8b57;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 5px;
    margin: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 Proactive AI Assistant for Financial Advisors</h1>
    <p>Your intelligent assistant managing client relationships proactively • Ready to take autonomous actions</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for proactive briefing
if 'briefing_shown' not in st.session_state:
    st.session_state.briefing_shown = False
    st.session_state.auto_briefing = True

# Auto-show daily briefing on page load
if not st.session_state.briefing_shown and st.session_state.auto_briefing:
    st.markdown("### 🌅 **GOOD MORNING! HERE'S YOUR DAILY BRIEFING:**")

    with st.spinner("📊 Generating your daily briefing..."):
        try:
            briefing = get_daily_briefing()

            # Format briefing with better styling
            briefing_formatted = briefing.replace(" | ", "\n\n")

            st.markdown(f"""
            <div class="briefing-box">
            {briefing_formatted.replace('**', '<strong>').replace('**', '</strong>')}
            </div>
            """, unsafe_allow_html=True)

            st.session_state.briefing_shown = True

        except Exception as e:
            st.error(f"Error loading briefing: {e}")
            st.info("💡 Try typing 'Good morning' to get your daily briefing!")

# Quick Action Buttons
st.markdown("### 🚀 **QUICK ACTIONS:**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📧 Draft Follow-up Emails"):
        with st.spinner("Drafting emails..."):
            response = get_ai_response("Draft follow-up emails for overdue clients")
            st.success("✅ Email drafts ready!")
            st.write(response)

with col2:
    if st.button("📅 Schedule Reviews"):
        with st.spinner("Scheduling reviews..."):
            response = get_ai_response("Schedule annual reviews for overdue clients")
            st.success("✅ Reviews scheduled!")
            st.write(response)

with col3:
    if st.button("🎯 Client Journey Status"):
        with st.spinner("Checking client journeys..."):
            response = get_ai_response("Show me client journey status overview")
            st.success("✅ Journey status loaded!")
            st.write(response)

with col4:
    if st.button("🔄 Refresh Briefing"):
        st.session_state.briefing_shown = False
        st.rerun()

# Separator
st.markdown("---")

# Chat Interface
st.markdown("### 💬 **CHAT WITH YOUR ASSISTANT:**")
st.markdown("*Ask me anything or request autonomous actions like: 'Send birthday email to Emma' or 'Update CRM for David Chen'*")

# Create text input area for user messages
user_message = st.text_area("Your message:", height=100, placeholder="Type your request here... (e.g., 'Send follow-up email to Sarah Williams' or 'What are my urgent tasks today?')")

# Handle send button click
if st.button("📤 Send Message") and user_message:
    with st.spinner("🤖 Processing your request..."):
        response = get_ai_response(user_message)

    # Display the conversation with better formatting
    st.markdown("#### **Your Request:**")
    st.markdown(f"*{user_message}*")

    st.markdown("#### **🤖 Assistant Response:**")
    st.success("Response generated successfully!")

    # Format response for better display
    response_formatted = response.replace(" | ", "\n\n")
    st.markdown(response_formatted)

# Sidebar with additional proactive features
with st.sidebar:
    st.markdown("## 🎯 **PROACTIVE DASHBOARD**")

    # Current time
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"**📅 Today:** {current_date}")
    st.markdown(f"**🕒 Time:** {current_time}")

    st.markdown("---")

    # Quick stats
    st.markdown("### 📊 **QUICK STATS:**")
    try:
        from backend import data_manager, USE_REAL_DATA
        if USE_REAL_DATA:
            total_clients = len(data_manager.get_all_clients())
            overdue_reviews = len(data_manager.get_overdue_reviews())
        else:
            total_clients = 6
            overdue_reviews = 2

        st.metric("Total Clients", total_clients)
        st.metric("Overdue Reviews", overdue_reviews, delta=f"-{overdue_reviews} need attention")
        compliance_rate = ((total_clients - overdue_reviews) / total_clients * 100) if total_clients > 0 else 0
        st.metric("Compliance Rate", f"{compliance_rate:.0f}%")

    except Exception as e:
        st.error(f"Stats unavailable: {e}")

    st.markdown("---")

    # Autonomous actions menu
    st.markdown("### 🤖 **AUTONOMOUS ACTIONS:**")

    if st.button("📧 Send Follow-up Email", key="sidebar_email"):
        st.session_state['auto_action'] = 'email'

    if st.button("📞 Schedule Call", key="sidebar_call"):
        st.session_state['auto_action'] = 'schedule'

    if st.button("📋 Update CRM", key="sidebar_crm"):
        st.session_state['auto_action'] = 'crm'

    if st.button("🎂 Birthday Check", key="sidebar_birthday"):
        st.session_state['auto_action'] = 'birthday'

    # Handle sidebar actions
    if 'auto_action' in st.session_state:
        action = st.session_state['auto_action']
        if action == 'email':
            with st.spinner("Drafting email..."):
                response = get_ai_response("Draft follow-up email for the most overdue client")
                st.write(response)
        elif action == 'schedule':
            with st.spinner("Scheduling..."):
                response = get_ai_response("Schedule meeting for highest priority client")
                st.write(response)
        elif action == 'crm':
            with st.spinner("Updating CRM..."):
                response = get_ai_response("Update CRM records with recent market impacts")
                st.write(response)
        elif action == 'birthday':
            with st.spinner("Checking birthdays..."):
                response = get_ai_response("Check for birthday opportunities this month")
                st.write(response)
        del st.session_state['auto_action']

    st.markdown("---")

    # Help section
    st.markdown("### 💡 **NEED HELP?**")
    st.markdown("Try these commands:")
    st.code("""
• "Good morning"
• "Send email to John"
• "Schedule Sarah's review"
• "Client journey status"
• "What's urgent today?"
    """)

# Footer with system info
import subprocess, os
from pathlib import Path

st.markdown("---")
st.markdown("*🤖 Proactive AI Assistant v2.0 - Always here to help you stay ahead of client needs*")

# Version info at bottom
version_info = "Proactive Assistant v2.0"
try:
    if Path("commit.txt").exists():
        version_info = Path("commit.txt").read_text().strip()
    elif os.path.exists(".git"):
        version_info = subprocess.getoutput('git log -1 --pretty=%B')[:50] + "..."
except:
    pass

st.markdown(f"<div style='text-align: center; color: gray; font-size: 12px; margin-top: 2rem;'>{version_info}</div>", unsafe_allow_html=True)
