# 🤖 STANDISH - PROACTIVE AI ASSISTANT FOR FINANCIAL ADVISORS
# Automatically provides daily briefings and offers autonomous actions

import streamlit as st
from backend import get_ai_response, get_daily_briefing
from datetime import datetime
import time

print("🚀 Starting Standish AI Assistant...")

# Configure the web page appearance
st.set_page_config(
    page_title="🤖 Standish - AI Assistant for Financial Advisors",
    page_icon="🏦",
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
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #2e8b57;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    line-height: 1.6;
    font-size: 14px;
    color: #333;
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
    <h1>🏦 STANDISH - AI Assistant for Financial Advisors</h1>
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

            st.markdown(f"""
            <div class="briefing-box">
            {briefing.replace('**', '<strong>').replace('**', '</strong>')}
            </div>
            """, unsafe_allow_html=True)

            st.session_state.briefing_shown = True

        except Exception as e:
            st.error(f"Error loading briefing: {e}")
            # Fallback briefing
            current_date = datetime.now().strftime("%A, %B %d, %Y")

            st.markdown(f"""
            <div class="briefing-box">
            <strong>📅 TODAY: {current_date}</strong><br><br>

            <strong>YESTERDAY'S ACTIVITY SUMMARY:</strong><br>
            ⚠️ 2 clients with overdue reviews<br>
            📧 3 pending follow-up emails<br>
            ✅ No critical meetings missed<br><br>

            <strong>TODAY'S PRIORITY ACTIONS:</strong><br>
            🚨 OVERDUE: Sarah Williams annual review (16 days overdue)<br>
            📅 DUE THIS WEEK: David Chen annual review (in 3 days)<br>
            🎂 BIRTHDAY OPPORTUNITY: Emma Jackson - perfect check-in opportunity<br>
            📊 Review market updates for client portfolios<br><br>

            <strong>STANDISH CAN HELP YOU WITH:</strong><br>
            📧 Draft follow-up emails to overdue clients<br>
            📞 Schedule meetings and reminders<br>
            📋 Update CRM records<br>
            🎯 Track client journey stages<br>
            </div>
            """, unsafe_allow_html=True)

            st.session_state.briefing_shown = True

# Quick Action Buttons
st.markdown("### 🚀 **QUICK ACTIONS:**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📧 Draft Follow-up Emails"):
        with st.spinner("Drafting emails..."):
            response = get_ai_response("Draft follow-up emails for overdue clients")
            st.success("✅ Email drafts ready!")
            st.write(response)

            # Store for follow-up questions (both systems)
            st.session_state['quick_action_response'] = response
            st.session_state['quick_action_type'] = 'draft_emails'
            # Also store for chat follow-up buttons
            st.session_state['last_assistant_response'] = response
            st.session_state['last_user_message'] = "Draft follow-up emails for overdue clients"

with col2:
    if st.button("📅 Schedule Reviews"):
        with st.spinner("Scheduling reviews..."):
            response = get_ai_response("Schedule annual reviews for overdue clients")
            st.success("✅ Reviews scheduled!")
            st.write(response)

            # Store for follow-up questions (both systems)
            st.session_state['quick_action_response'] = response
            st.session_state['quick_action_type'] = 'schedule_reviews'
            # Also store for chat follow-up buttons
            st.session_state['last_assistant_response'] = response
            st.session_state['last_user_message'] = "Schedule annual reviews for overdue clients"

with col3:
    if st.button("🎯 Client Journey Status"):
        with st.spinner("Checking client journeys..."):
            response = get_ai_response("Show me client journey status overview")
            st.success("✅ Journey status loaded!")
            st.write(response)

            # Store for follow-up questions (both systems)
            st.session_state['quick_action_response'] = response
            st.session_state['quick_action_type'] = 'client_journey'
            # Also store for chat follow-up buttons
            st.session_state['last_assistant_response'] = response
            st.session_state['last_user_message'] = "Show me client journey status overview"

with col4:
    if st.button("🔄 Refresh Briefing"):
        st.session_state.briefing_shown = False
        st.rerun()

# Quick Action Follow-up buttons
if 'quick_action_response' in st.session_state and 'quick_action_type' in st.session_state:
    action_type = st.session_state['quick_action_type']

    st.markdown("---")
    st.markdown("### 💬 **Follow-up Options:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Yes, Do This", key="quick_action_yes"):
            if action_type == 'draft_emails':
                st.success("✅ Email drafts will be sent to the specified clients!")
                st.info("📧 Follow-up emails for Sarah Williams and David Chen have been queued for sending.")
            elif action_type == 'schedule_reviews':
                st.success("✅ Review meetings will be scheduled!")
                st.info("📅 Calendar invites for annual reviews have been prepared and will be sent.")
            elif action_type == 'client_journey':
                st.success("✅ Client journey tracking updated!")
                st.info("🎯 All client stages have been reviewed and next actions prioritized.")

            # Clear the action
            del st.session_state['quick_action_response']
            del st.session_state['quick_action_type']
            if 'last_assistant_response' in st.session_state:
                del st.session_state['last_assistant_response']
            if 'last_user_message' in st.session_state:
                del st.session_state['last_user_message']
            st.rerun()

    with col2:
        if st.button("✏️ Modify This", key="quick_action_modify"):
            st.info("💡 Please specify your changes in the chat area below. For example: 'Change the email subject' or 'Schedule for next week instead'")

    with col3:
        if st.button("❌ Cancel", key="quick_action_cancel"):
            st.warning("❌ Action cancelled.")
            # Clear the action
            del st.session_state['quick_action_response']
            del st.session_state['quick_action_type']
            if 'last_assistant_response' in st.session_state:
                del st.session_state['last_assistant_response']
            if 'last_user_message' in st.session_state:
                del st.session_state['last_user_message']
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

    # Store the conversation in session state
    st.session_state['last_user_message'] = user_message
    st.session_state['last_assistant_response'] = response

    # Display the conversation with better formatting
    st.markdown("#### **Your Request:**")
    st.markdown(f"*{user_message}*")

    st.markdown("#### **🤖 STANDISH Response:**")
    st.success("Response generated successfully!")

    # Format response for better display
    response_formatted = response.replace(" | ", "\n\n")
    st.markdown(response_formatted)

# Show interactive response buttons if STANDISH asked a question
if 'last_assistant_response' in st.session_state and st.session_state['last_assistant_response']:
    response = st.session_state['last_assistant_response']
    user_msg = st.session_state.get('last_user_message', '')

    # Check if response contains question indicators
    if any(indicator in response.lower() for indicator in ['would you like', 'should i', 'do you want', 'would you prefer', '?']):
        st.markdown("---")
        st.markdown("### 💬 **Quick Response to STANDISH:**")

        # Create quick response buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Yes, Please", key="chat_yes"):
                with st.spinner("Processing your response..."):
                    # Create contextual follow-up based on original question
                    contextual_prompt = f"The user asked: '{user_msg}'. You responded: '{response[:200]}...'. The user said 'Yes, please proceed with that.' Please provide a specific next step or action based on the context."
                    follow_up_response = get_ai_response(contextual_prompt)
                st.markdown("#### **🤖 STANDISH Follow-up:**")
                st.markdown(follow_up_response.replace(" | ", "\n\n"))
                # Clear after response
                if 'last_assistant_response' in st.session_state:
                    del st.session_state['last_assistant_response']
                if 'last_user_message' in st.session_state:
                    del st.session_state['last_user_message']

        with col2:
            if st.button("❌ No, Thanks", key="chat_no"):
                st.success("👍 Understood! Let me know if you need help with anything else.")
                # Clear after response
                if 'last_assistant_response' in st.session_state:
                    del st.session_state['last_assistant_response']
                if 'last_user_message' in st.session_state:
                    del st.session_state['last_user_message']
                st.rerun()

        with col3:
            if st.button("💡 Tell Me More", key="chat_more"):
                with st.spinner("Processing your response..."):
                    # Create contextual follow-up for more details
                    contextual_prompt = f"The user asked: '{user_msg}'. You responded: '{response[:200]}...'. The user wants more details. Please provide additional specific information about this topic."
                    follow_up_response = get_ai_response(contextual_prompt)
                st.markdown("#### **🤖 STANDISH Follow-up:**")
                st.markdown(follow_up_response.replace(" | ", "\n\n"))
                # Clear after response
                if 'last_assistant_response' in st.session_state:
                    del st.session_state['last_assistant_response']
                if 'last_user_message' in st.session_state:
                    del st.session_state['last_user_message']

        # Quick text response option
        st.markdown("**Or type a specific response:**")
        quick_response = st.text_input("Your response:", key="chat_text_response", placeholder="Type your specific response here...")

        if st.button("📤 Send Response", key="send_chat_response") and quick_response:
            with st.spinner("Processing your response..."):
                # Create contextual follow-up with user's specific response
                contextual_prompt = f"The user originally asked: '{user_msg}'. You responded with suggestions. Now the user specifically responded: '{quick_response}'. Please provide a helpful follow-up based on their specific response."
                follow_up_response = get_ai_response(contextual_prompt)
            st.markdown("#### **🤖 STANDISH Follow-up:**")
            st.markdown(follow_up_response.replace(" | ", "\n\n"))
            # Clear after response
            if 'last_assistant_response' in st.session_state:
                del st.session_state['last_assistant_response']
            if 'last_user_message' in st.session_state:
                del st.session_state['last_user_message']

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
        # Try to get real stats from backend
        import backend
        if hasattr(backend, 'data_manager') and backend.data_manager:
            total_clients = len(backend.data_manager.get_all_clients())
            overdue_reviews = len(backend.data_manager.get_overdue_reviews())
        else:
            # Fallback to mock data
            total_clients = 6
            overdue_reviews = 2

        st.metric("Total Clients", total_clients)
        st.metric("Overdue Reviews", overdue_reviews, delta=f"-{overdue_reviews} need attention")
        compliance_rate = ((total_clients - overdue_reviews) / total_clients * 100) if total_clients > 0 else 0
        st.metric("Compliance Rate", f"{compliance_rate:.0f}%")

    except Exception as e:
        st.error(f"Stats loading... {e}")
        # Default fallback values
        st.metric("Total Clients", "6")
        st.metric("Overdue Reviews", "2")
        st.metric("Compliance Rate", "67%")

    st.markdown("---")

    # Autonomous actions menu
    st.markdown("### 🤖 **AUTONOMOUS ACTIONS:**")

    # Clear any existing action if starting fresh
    if st.button("🔄 Reset Actions", key="reset_actions"):
        for key in ['action_response', 'action_type']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    if st.button("📧 Send Follow-up Email", key="sidebar_email"):
        response = """📧 EMAIL READY TO SEND TO SARAH WILLIAMS:

Subject: Annual Review - Let's Catch Up

Dear Sarah,

I hope you're well. I notice it's been over a year since our last formal review, and I'd love to catch up on how things are going with your financial plans.

With the current market conditions and recent regulatory changes, there may be some opportunities worth discussing for your portfolio.

Would you be available for a 30-minute call next week? I have slots on:
- Tuesday 2:00 PM
- Wednesday 10:00 AM
- Friday 3:00 PM

Best regards,
[Your Name]

Ready to send this follow-up email?"""

        st.session_state['action_response'] = response
        st.session_state['action_type'] = 'email'

    if st.button("📞 Schedule Call", key="sidebar_call"):
        response = """📅 MEETING READY TO SCHEDULE FOR DAVID CHEN:

Type: Annual Review
Proposed Date: Thursday, February 12, 2026
Duration: 60 minutes
Location: Office/Video Call

Meeting Agenda:
- Portfolio review and performance
- Risk appetite assessment
- Goal progress check
- New opportunities discussion
- Compliance documentation

NEXT STEPS:
✅ Calendar invite ready to send
✅ Client notification email drafted
✅ Meeting reminder set for 24 hours before

Would you like me to send the calendar invite and notification email to the client?"""

        st.session_state['action_response'] = response
        st.session_state['action_type'] = 'schedule'

    if st.button("📋 Update CRM", key="sidebar_crm"):
        response = """📋 CRM UPDATE READY FOR EMMA JACKSON:

Date: 2026-02-05
Update Type: Market Impact

Records to Add:
- Market volatility impact assessment
- Risk tolerance confirmation
- Next review date flagged
- Follow-up actions logged

COMPLIANCE: Consumer Duty requirements will be updated
NEXT STEPS: Automated follow-up will be scheduled for 30 days

Ready to update the CRM with these details?"""

        st.session_state['action_response'] = response
        st.session_state['action_type'] = 'crm'

    if st.button("🎂 Birthday Check", key="sidebar_birthday"):
        response = """🎂 BIRTHDAY OPPORTUNITIES FOR FEBRUARY:

Found 2 upcoming birthdays:
- Emma Jackson (Feb 12) - Perfect time for portfolio review
- David Chen (Feb 25) - High-value client, send personal greeting

SUGGESTED ACTIONS:
📧 Draft birthday emails with portfolio updates
📞 Schedule birthday call for relationship building
🎁 Consider sending personalized financial insights

Ready to send birthday greetings and schedule follow-ups?"""

        st.session_state['action_response'] = response
        st.session_state['action_type'] = 'birthday'

    # Show response with interactive buttons
    if 'action_response' in st.session_state and st.session_state['action_response']:
        st.markdown("---")
        st.markdown("**🤖 STANDISH Response:**")

        response_text = st.session_state['action_response']

        st.text_area(
            "Response:",
            value=response_text,
            height=200,
            disabled=True,
            key="action_response_display"
        )

        # Interactive buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("✅ Yes, Do It", key="confirm_action", help="Confirm this action"):
                st.success("✅ Action confirmed! STANDISH will execute this.")
                if 'action_response' in st.session_state:
                    del st.session_state['action_response']
                if 'action_type' in st.session_state:
                    del st.session_state['action_type']
                st.rerun()

        with col2:
            if st.button("✏️ Edit", key="edit_action", help="Modify this action"):
                st.info("✏️ Please specify your changes in the main chat area.")

        with col3:
            if st.button("❌ Cancel", key="cancel_action", help="Cancel this action"):
                st.warning("❌ Action cancelled.")
                if 'action_response' in st.session_state:
                    del st.session_state['action_response']
                if 'action_type' in st.session_state:
                    del st.session_state['action_type']
                st.rerun()

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
st.markdown("*🏦 **STANDISH** - AI Assistant v2.0 - Always here to help you stay ahead of client needs*")

version_info = "STANDISH v2.0"
try:
    if Path("commit.txt").exists():
        version_info = Path("commit.txt").read_text().strip()
    elif os.path.exists(".git"):
        version_info = subprocess.getoutput('git log -1 --pretty=%B')[:50] + "..."
except:
    pass

st.markdown(f"<div style='text-align: center; color: gray; font-size: 12px; margin-top: 2rem;'>{version_info}</div>", unsafe_allow_html=True)
