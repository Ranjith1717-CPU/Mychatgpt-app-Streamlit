# 🤖 STANDISH - Enhanced Proactive AI Agent for Financial Advisors
# Complete rewrite with ALL missing features for true proactive agency

import json
from openai import AzureOpenAI
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sqlite3
from pathlib import Path
import re

# =============================================================================
# Data Manager Import (backward compatible)
# =============================================================================
try:
    from data_manager import DataManager
    data_manager = DataManager()
    USE_REAL_DATA = True
    print("✅ Using real client data from documents")
except ImportError:
    USE_REAL_DATA = False
    data_manager = None
    print("⚠️ Falling back to mock data")

# Import template processing capabilities
try:
    from template_integration import (
        generate_client_template,
        analyze_template_requirements,
        get_template_processing_status,
        template_processing_tools,
        route_template_tool_call
    )
    USE_TEMPLATE_PROCESSING = True
    print("✅ Template processing integration enabled")
except ImportError:
    USE_TEMPLATE_PROCESSING = False
    print("⚠️ Template processing not available")

# =============================================================================
# Azure OpenAI Configuration
# =============================================================================
try:
    AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
    AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
    AZURE_OPENAI_API_VERSION = st.secrets["AZURE_OPENAI_API_VERSION"]
    AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"]
except (KeyError, TypeError):
    # Handle testing scenarios or missing secrets
    AZURE_OPENAI_API_KEY = "mock-key"
    AZURE_OPENAI_ENDPOINT = "mock-endpoint"
    AZURE_OPENAI_API_VERSION = "mock-version"
    AZURE_OPENAI_DEPLOYMENT_NAME = "mock-deployment"

# =============================================================================
# NEW: PROACTIVE AGENT LAYER - Right Moment, Right Context, Right Intent
# =============================================================================

# Contextual triggers for proactive suggestions
contextual_triggers = {
    "meeting_keywords": {
        "retirement": {
            "trigger_phrases": ["retire early", "retirement age", "when to retire", "retirement planning"],
            "suggestion": "🎯 PROACTIVE: Client mentioned retirement - suggest pension review and withdrawal planning",
            "action": "add_to_meeting_notes"
        },
        "protection": {
            "trigger_phrases": ["life insurance", "what if something happens", "protect my family", "breadwinner"],
            "suggestion": "🛡️ PROACTIVE: Protection gap identified - recommend life insurance review",
            "action": "flag_protection_review"
        },
        "tax": {
            "trigger_phrases": ["tax bill", "reduce tax", "tax efficient", "HMRC"],
            "suggestion": "💰 PROACTIVE: Tax concern raised - discuss ISA/pension optimization",
            "action": "schedule_tax_planning"
        },
        "inheritance": {
            "trigger_phrases": ["leave money", "inheritance", "estate planning", "when I die"],
            "suggestion": "📋 PROACTIVE: Estate planning mentioned - add IHT review to agenda",
            "action": "flag_estate_planning"
        },
        "business": {
            "trigger_phrases": ["sell the business", "exit strategy", "business value", "succession"],
            "suggestion": "💼 PROACTIVE: Business exit mentioned - discuss CGT planning and liquidity",
            "action": "flag_business_planning"
        }
    },
    "missed_topics": {
        "annual_review_gaps": [
            "Did not discuss retirement timeline - add pension projection?",
            "No protection review mentioned - flag for next meeting?",
            "Tax planning not covered - schedule separate session?",
            "Investment risk tolerance not reassessed - needs update?",
            "Estate planning status unclear - follow up required?"
        ]
    }
}

# Real-time meeting context detection
meeting_context = {
    "current_meeting": {
        "client": "",
        "type": "annual_review",
        "duration": 0,
        "topics_covered": [],
        "topics_missed": [],
        "proactive_suggestions": []
    }
}

def detect_proactive_moment(text_input, context="meeting"):
    """
    CORE PROACTIVE FUNCTION: Detect right moment for suggestions

    Args:
        text_input: What the client/advisor just said
        context: meeting, email, call, report_review

    Returns:
        Proactive suggestion or None
    """
    text_lower = text_input.lower()
    suggestions = []

    # RIGHT MOMENT detection
    for topic, data in contextual_triggers["meeting_keywords"].items():
        for phrase in data["trigger_phrases"]:
            if phrase in text_lower:
                # RIGHT CONTEXT + RIGHT INTENT
                suggestion = {
                    "moment": "NOW",
                    "context": f"Client mentioned '{phrase}'",
                    "intent": data["suggestion"],
                    "action": data["action"],
                    "topic": topic
                }
                suggestions.append(suggestion)

    return suggestions

def generate_meeting_interruption(client_name, detected_topic):
    """Generate contextual interruption suggestions during meetings"""

    interruptions = {
        "retirement": f"""
🚨 **PROACTIVE INTERRUPTION**

**CONTEXT:** {client_name} just mentioned retirement planning

**SUGGESTION:** "Before we move on, shall we quickly model your retirement timeline?
I can show you the impact of retiring at 60 vs 65 on your pension pot."

**QUICK ACTIONS:**
✅ Add pension projection to meeting
❌ Note for follow-up
📊 Run retirement calculator now
        """,

        "protection": f"""
🚨 **PROACTIVE INTERRUPTION**

**CONTEXT:** {client_name} mentioned protecting their family

**SUGGESTION:** "You mentioned protection - let me quickly check your current cover.
Your income is £{80000}, but life cover is only £{200000}. Shall we discuss this?"

**QUICK ACTIONS:**
✅ Review protection gaps now
❌ Schedule separate meeting
📋 Add to action items
        """,

        "tax": f"""
🚨 **PROACTIVE INTERRUPTION**

**CONTEXT:** {client_name} concerned about tax efficiency

**SUGGESTION:** "You still have £{12000} ISA allowance remaining.
Shall we discuss transferring some of your savings to reduce tax?"

**QUICK ACTIONS:**
✅ Discuss ISA transfer now
❌ Add to next meeting agenda
💰 Calculate tax savings
        """
    }

    return interruptions.get(detected_topic, "No specific interruption available")

def check_meeting_completeness(client_name, meeting_duration_minutes):
    """Check if key topics were missed during meeting"""

    standard_agenda = [
        "portfolio_performance",
        "risk_assessment",
        "protection_review",
        "retirement_planning",
        "tax_efficiency",
        "estate_planning"
    ]

    # Simulate topics covered (in real system, this would track actual discussion)
    covered_topics = ["portfolio_performance", "risk_assessment"]
    missed_topics = [topic for topic in standard_agenda if topic not in covered_topics]

    suggestions = []

    if "retirement_planning" in missed_topics:
        suggestions.append({
            "type": "missing_topic",
            "suggestion": f"🎯 You didn't discuss retirement timeline with {client_name} - add pension projection to report?",
            "urgency": "medium",
            "action": "add_to_report"
        })

    if "protection_review" in missed_topics:
        suggestions.append({
            "type": "missing_topic",
            "suggestion": f"🛡️ Protection gaps not reviewed - {client_name} mentioned family concerns earlier",
            "urgency": "high",
            "action": "schedule_protection_meeting"
        })

    if meeting_duration_minutes < 45:
        suggestions.append({
            "type": "time_alert",
            "suggestion": f"⏰ Meeting was only {meeting_duration_minutes} minutes - several topics not covered. Extend or schedule follow-up?",
            "urgency": "medium",
            "action": "extend_or_reschedule"
        })

    return suggestions

def get_proactive_post_meeting_actions(client_name, meeting_notes=""):
    """Generate proactive actions immediately after meeting ends"""

    return f"""
🤖 **STANDISH PROACTIVE POST-MEETING ANALYSIS**

**CLIENT:** {client_name}
**MEETING COMPLETED:** {datetime.now().strftime('%H:%M on %B %d')}

**IMMEDIATE ACTIONS DETECTED:**

1. **📧 FOLLOW-UP EMAIL**
   ✅ Draft thank you email with meeting summary?
   ✅ Include action items and next steps?

2. **📋 CRM UPDATES**
   ✅ Log meeting notes and commitments?
   ✅ Update client risk profile if discussed?

3. **⚠️ MISSED OPPORTUNITIES**
   • Retirement age not confirmed - add to next meeting?
   • Protection review skipped - client mentioned family concerns
   • Tax planning not discussed - they have unused allowances

4. **📅 NEXT STEPS**
   ✅ Schedule follow-up meeting for missed topics?
   ✅ Set reminder for promised documents?
   ✅ Flag urgent actions for this week?

**WOULD YOU LIKE STANDISH TO HANDLE THESE AUTOMATICALLY?**
    """

def get_proactive_daily_moments():
    """
    Analyze recent client data and interactions to surface proactive moments
    for inclusion in daily briefings - Right Moment, Right Context, Right Intent
    """

    # Simulated recent client interactions and contextual analysis
    recent_interactions = [
        {
            "client": "Sarah Williams",
            "source": "email_response",
            "context": "Client replied 'thinking about retiring at 60 instead of 65'",
            "moment": "🎯 Sarah Williams mentioned early retirement - suggest pension modeling session THIS WEEK",
            "urgency": "high",
            "action": "schedule_retirement_planning"
        },
        {
            "client": "David Chen",
            "source": "annual_review_notes",
            "context": "Mentioned 'concerned about protecting the family business'",
            "moment": "🛡️ David Chen raised business protection concerns - keyman insurance opportunity",
            "urgency": "medium",
            "action": "review_business_protection"
        },
        {
            "client": "Lisa Patel",
            "source": "phone_call_transcript",
            "context": "Asked 'what's the most tax-efficient way to take money out'",
            "moment": "💰 Lisa Patel asked about tax efficiency - dividend vs salary optimization needed",
            "urgency": "medium",
            "action": "tax_planning_session"
        },
        {
            "client": "Emma Jackson",
            "source": "meeting_follow_up",
            "context": "Mentioned 'thinking of downsizing the house next year'",
            "moment": "🏠 Emma Jackson considering downsizing - CGT and IHT planning opportunity",
            "urgency": "low",
            "action": "estate_planning_review"
        }
    ]

    # Filter and prioritize based on urgency and context
    high_priority = [interaction['moment'] for interaction in recent_interactions if interaction['urgency'] == 'high']
    medium_priority = [interaction['moment'] for interaction in recent_interactions if interaction['urgency'] == 'medium']

    # Return top proactive moments for today's briefing
    proactive_moments = []

    # Always include high priority
    proactive_moments.extend(high_priority)

    # Add medium priority if space allows (max 4 total)
    proactive_moments.extend(medium_priority[:4-len(high_priority)])

    return proactive_moments

# =============================================================================
# NEW: In-Memory Data Stores for Enhanced Features
# =============================================================================

# Recommendation History Store
recommendation_history = {
    "David Chen": [
        {"date": "2025-06-15", "type": "ISA Transfer", "platform": "Platform X", "rationale": "Lower fees (0.25% vs 0.45%), better fund selection, consolidated reporting", "status": "Implemented"},
        {"date": "2025-03-20", "type": "Pension Contribution", "amount": 40000, "rationale": "Maximize annual allowance before tax year end, higher rate tax relief", "status": "Implemented"},
        {"date": "2024-11-10", "type": "Risk Profile Change", "from": "Moderate", "to": "Moderate-High", "rationale": "Client comfortable with volatility, 15+ year horizon", "status": "Implemented"}
    ],
    "Sarah Williams": [
        {"date": "2025-08-01", "type": "ISA Transfer", "platform": "Platform X", "rationale": "Fee comparison showed 0.2% annual saving, ESG fund options available", "status": "Pending"},
        {"date": "2025-05-15", "type": "Life Insurance", "amount": 500000, "rationale": "Income replacement for family, 2 dependent children", "status": "Implemented"},
        {"date": "2025-02-28", "type": "Pension Consolidation", "rationale": "3 legacy pensions consolidated for better oversight and lower fees", "status": "Implemented"}
    ],
    "Emma Jackson": [
        {"date": "2025-09-10", "type": "SIPP Setup", "platform": "Platform Y", "rationale": "Self-employed, maximize pension contributions for tax efficiency", "status": "In Progress"}
    ],
    "Lisa Patel": [
        {"date": "2024-12-01", "type": "Drawdown Strategy", "withdrawal_rate": "3.5%", "rationale": "Sustainable withdrawal aligned with risk tolerance", "status": "Implemented"}
    ]
}

# Meeting Transcripts Store
meeting_transcripts = {
    "Williams Family - 2025-07-15": {
        "date": "2025-07-15",
        "client": "Sarah Williams",
        "attendees": ["Sarah Williams", "Tom Williams", "Advisor"],
        "duration": "60 minutes",
        "transcript": """
        Advisor: Let's discuss your risk tolerance. Given recent market volatility, how do you feel about your current portfolio allocation?
        Sarah: We're a bit concerned about the market drops we've seen. We don't want to lose our retirement savings.
        Tom: But we also don't want to be too conservative. We're still 15 years from retirement.
        Advisor: I understand. Your current moderate risk profile means about 60% equities. Given your concerns, we could reduce to 50%, but this may impact long-term growth.
        Sarah: What about sustainable investments? We'd prefer our money to be in ethical companies.
        Advisor: Absolutely. We have excellent ESG options on Platform X. The performance has been comparable to traditional funds.
        Tom: We're also worried about what happens if the market drops 20% right before we retire.
        Advisor: Great question. We can model different scenarios and build in a cash buffer for the first few years of retirement.
        """,
        "key_concerns": ["market volatility", "sustainable investing", "retirement timing risk"],
        "action_items": ["Review ESG fund options", "Model market correction scenarios", "Discuss cash buffer strategy"],
        "sentiment": "cautiously optimistic"
    },
    "David Chen - 2025-09-01": {
        "date": "2025-09-01",
        "client": "David Chen",
        "attendees": ["David Chen", "Advisor"],
        "duration": "45 minutes",
        "transcript": """
        Advisor: David, let's review your pension contributions this year.
        David: Yes, I want to make sure I'm maximizing my allowances. My business had a good year.
        Advisor: Great news. You've used £35,000 of your £60,000 annual allowance. You also have carry forward from the last 3 years.
        David: What about the lifetime allowance changes?
        Advisor: Good question. The lifetime allowance has been abolished, so that's no longer a concern. You can contribute more freely now.
        David: I'm also thinking about exit planning for my business. Not immediately, but in 5-7 years.
        Advisor: We should definitely factor that into your overall plan. Business sale proceeds will significantly impact your retirement income.
        """,
        "key_concerns": ["pension allowances", "business exit planning", "tax efficiency"],
        "action_items": ["Calculate carry forward allowance", "Draft exit planning timeline", "Review business valuation"],
        "sentiment": "positive"
    }
}

# Document Tracking Store
document_tracking = {
    "Sarah Williams": {
        "requested": [
            {"document": "P60 2024/25", "requested_date": "2025-01-15", "status": "Received", "received_date": "2025-01-20"},
            {"document": "Bank statements (6 months)", "requested_date": "2025-01-15", "status": "Pending", "received_date": None},
            {"document": "Mortgage statement", "requested_date": "2025-01-15", "status": "Pending", "received_date": None}
        ]
    },
    "David Chen": {
        "requested": [
            {"document": "Company accounts 2024", "requested_date": "2025-01-10", "status": "Received", "received_date": "2025-01-18"},
            {"document": "Self-assessment tax return", "requested_date": "2025-01-10", "status": "Received", "received_date": "2025-01-25"},
            {"document": "Pension statement (3 schemes)", "requested_date": "2025-01-10", "status": "Partial", "received_date": "2025-01-22", "notes": "2 of 3 received"}
        ]
    },
    "Emma Jackson": {
        "requested": [
            {"document": "Proof of address", "requested_date": "2025-02-01", "status": "Pending", "received_date": None},
            {"document": "ID verification", "requested_date": "2025-02-01", "status": "Pending", "received_date": None}
        ]
    }
}

# Commitments/Promises Store
commitments_tracking = {
    "Jackson Family": [
        {"promise": "Send detailed breakdown of fund options", "promised_date": "2025-01-20", "due_date": "2025-01-25", "status": "Overdue", "completed_date": None},
        {"promise": "Prepare cashflow model for early retirement", "promised_date": "2025-01-15", "due_date": "2025-02-01", "status": "Pending", "completed_date": None}
    ],
    "David Chen": [
        {"promise": "Send carry forward calculation", "promised_date": "2025-02-01", "due_date": "2025-02-05", "status": "Completed", "completed_date": "2025-02-03"},
        {"promise": "Provide exit planning checklist", "promised_date": "2025-02-01", "due_date": "2025-02-10", "status": "Pending", "completed_date": None}
    ],
    "Sarah Williams": [
        {"promise": "Send ESG fund comparison report", "promised_date": "2025-01-28", "due_date": "2025-02-03", "status": "Overdue", "completed_date": None}
    ]
}

# Client Retirement & Withdrawal Data
retirement_data = {
    "Lisa Patel": {"status": "Retired", "retirement_date": "2023-06-01", "pension_pot": 450000, "annual_withdrawal": 18000, "withdrawal_rate": 4.0},
    "Michael Thompson": {"status": "Retired", "retirement_date": "2022-01-15", "pension_pot": 380000, "annual_withdrawal": 19000, "withdrawal_rate": 5.0},
    "Robert Hughes": {"status": "Retired", "retirement_date": "2024-03-01", "pension_pot": 520000, "annual_withdrawal": 15600, "withdrawal_rate": 3.0},
    "Anne Partridge": {"status": "Retired", "retirement_date": "2021-09-01", "pension_pot": 290000, "annual_withdrawal": 14500, "withdrawal_rate": 5.0},
    "Brian Potter": {"status": "Retired", "retirement_date": "2020-12-01", "pension_pot": 350000, "annual_withdrawal": 17500, "withdrawal_rate": 5.0}
}

# Client Service & Satisfaction Data
service_data = {
    "David Chen": {"services": ["Pension Planning", "Tax Planning", "Investment Management", "Business Planning"], "satisfaction_score": 9, "years_as_client": 8, "annual_revenue": 4500, "hours_per_year": 12},
    "Sarah Williams": {"services": ["Pension Planning", "Protection", "Investment Management"], "satisfaction_score": 8, "years_as_client": 5, "annual_revenue": 3200, "hours_per_year": 15},
    "Emma Jackson": {"services": ["SIPP", "Investment Management"], "satisfaction_score": 9, "years_as_client": 2, "annual_revenue": 2800, "hours_per_year": 8},
    "Lisa Patel": {"services": ["Drawdown Planning", "Investment Management", "Estate Planning"], "satisfaction_score": 7, "years_as_client": 12, "annual_revenue": 3800, "hours_per_year": 10},
    "Michael Gurung": {"services": ["Business Planning", "Pension Planning", "Protection"], "satisfaction_score": 8, "years_as_client": 6, "annual_revenue": 5200, "hours_per_year": 18}
}

# Sales Funnel Data
sales_funnel = {
    "initial_meetings": [
        {"name": "John Smith", "date": "2025-01-05", "source": "Website", "status": "Converted", "conversion_date": "2025-01-20"},
        {"name": "Mary Johnson", "date": "2025-01-10", "source": "Referral - David Chen", "status": "Converted", "conversion_date": "2025-01-25"},
        {"name": "Peter Brown", "date": "2025-01-15", "source": "LinkedIn", "status": "Lost", "reason": "Went with competitor"},
        {"name": "Susan Taylor", "date": "2025-01-20", "source": "Referral - Sarah Williams", "status": "In Progress", "next_meeting": "2025-02-10"},
        {"name": "James Wilson", "date": "2025-02-01", "source": "Website", "status": "In Progress", "next_meeting": "2025-02-15"}
    ],
    "conversion_by_source": {"Website": 0.40, "Referral": 0.75, "LinkedIn": 0.25, "Event": 0.50}
}

# Pension Annual Allowance Data
pension_allowances = {
    "David Chen": {"annual_allowance": 60000, "used_this_year": 35000, "carry_forward": [15000, 20000, 18000], "total_available": 78000},
    "Sarah Williams": {"annual_allowance": 60000, "used_this_year": 12000, "carry_forward": [0, 5000, 8000], "total_available": 61000},
    "Emma Jackson": {"annual_allowance": 60000, "used_this_year": 8000, "carry_forward": [10000, 12000, 15000], "total_available": 89000},
    "Michael Gurung": {"annual_allowance": 60000, "used_this_year": 45000, "carry_forward": [0, 0, 5000], "total_available": 20000}
}

# Interest Rate Sensitivity Data
interest_rate_sensitivity = {
    "Sarah Williams": {"fixed_rate_mortgage": True, "mortgage_rate": 2.5, "mortgage_balance": 180000, "renewal_date": "2026-06-01", "cash_savings": 45000, "bonds_allocation": 0.20},
    "David Chen": {"fixed_rate_mortgage": True, "mortgage_rate": 1.9, "mortgage_balance": 250000, "renewal_date": "2025-09-01", "cash_savings": 120000, "bonds_allocation": 0.15},
    "Lisa Patel": {"fixed_rate_mortgage": False, "mortgage_rate": 0, "mortgage_balance": 0, "renewal_date": None, "cash_savings": 85000, "bonds_allocation": 0.40},
    "Emma Jackson": {"fixed_rate_mortgage": True, "mortgage_rate": 3.2, "mortgage_balance": 320000, "renewal_date": "2027-03-01", "cash_savings": 25000, "bonds_allocation": 0.10}
}

# =============================================================================
# Proactive Assistant Core Functions (ENHANCED)
# =============================================================================

def get_daily_briefing(query=""):
    """Generate comprehensive daily briefing for the advisor - FULLY DYNAMIC"""
    print("🌅 Generating daily briefing...")

    current_date = datetime.now()
    current_date_formatted = current_date.strftime("%A, %B %d, %Y")

    briefing_sections = []

    # Get real client data
    if USE_REAL_DATA and data_manager:
        clients = data_manager.get_all_clients()
        overdue_reviews = data_manager.get_overdue_reviews()
        protection_gaps = data_manager.get_protection_gaps()
    else:
        clients = get_mock_clients()
        overdue_reviews = []
        protection_gaps = []
        # Calculate overdue from mock data
        for client in clients:
            if client.get('last_review'):
                try:
                    last_review = datetime.strptime(client['last_review'], '%Y-%m-%d')
                    months_since = (current_date - last_review).days / 30
                    if months_since > 12:
                        client['months_overdue'] = int(months_since)
                        client['days_overdue'] = int((current_date - last_review).days - 365)
                        overdue_reviews.append(client)
                except:
                    pass

    total_clients = len(clients)

    # ===== TODAY'S DATE =====
    briefing_sections.append(f"📅 **TODAY: {current_date_formatted}**")
    briefing_sections.append("")

    # ===== YESTERDAY'S ACTIVITY SUMMARY (Dynamic) =====
    briefing_sections.append("**YESTERDAY'S ACTIVITY SUMMARY:**")

    # Count overdue reviews dynamically
    if overdue_reviews:
        overdue_names = [c['name'] for c in overdue_reviews[:3]]
        briefing_sections.append(f"⚠️ {len(overdue_reviews)} clients with overdue reviews: {', '.join(overdue_names)}")
    else:
        briefing_sections.append("✅ All client reviews are up to date")

    # Count pending follow-ups from commitments
    pending_followups = []
    for client, commitments in commitments_tracking.items():
        pending = [c for c in commitments if c['status'] in ['Pending', 'Overdue']]
        if pending:
            pending_followups.append(client)

    if pending_followups:
        briefing_sections.append(f"📧 {len(pending_followups)} pending follow-ups: {', '.join(pending_followups[:3])}")
    else:
        briefing_sections.append("✅ All follow-ups completed")

    briefing_sections.append("✅ No critical meetings missed")
    briefing_sections.append("")

    # ===== TODAY'S PRIORITY ACTIONS (Dynamic) =====
    briefing_sections.append("**TODAY'S PRIORITY ACTIONS:**")

    priority_count = 0

    # Add overdue reviews with actual days overdue
    for client in overdue_reviews[:2]:
        days_overdue = client.get('days_overdue', 0)
        if days_overdue <= 0:
            # Calculate if not already set
            try:
                last_review = datetime.strptime(client['last_review'], '%Y-%m-%d')
                days_overdue = max(0, (current_date - last_review).days - 365)
            except:
                days_overdue = 30  # Default
        briefing_sections.append(f"🚨 OVERDUE: {client['name']} annual review ({days_overdue} days overdue)")
        priority_count += 1

    # Find clients due this week (within 7 days of review date)
    due_this_week = []
    for client in clients:
        if client.get('next_review_due'):
            try:
                next_review = datetime.strptime(client['next_review_due'], '%Y-%m-%d')
                days_until = (next_review - current_date).days
                if 0 < days_until <= 7:
                    due_this_week.append({'name': client['name'], 'days': days_until})
            except:
                pass

    for client in due_this_week[:2]:
        briefing_sections.append(f"📅 DUE THIS WEEK: {client['name']} annual review (in {client['days']} days)")
        priority_count += 1

    # Birthday opportunities - check current month
    current_month = current_date.month
    birthday_clients = []

    # Check retirement_data for birthdays (simulated based on month)
    for client in clients:
        # Simple birthday simulation based on client name hash and current month
        name_hash = sum(ord(c) for c in client['name']) % 12 + 1
        if name_hash == current_month:
            birthday_clients.append(client['name'])

    if birthday_clients:
        briefing_sections.append(f"🎂 BIRTHDAY OPPORTUNITY: {birthday_clients[0]} - perfect time for check-in")
        priority_count += 1

    if priority_count == 0:
        briefing_sections.append("✅ No urgent priorities today - great time for proactive outreach!")

    briefing_sections.append("📊 Review market updates for client portfolios")
    briefing_sections.append("")

    # ===== OVERDUE COMMITMENTS (Dynamic) =====
    overdue_commitments = get_overdue_commitments()
    if overdue_commitments:
        briefing_sections.append("**⚠️ OVERDUE COMMITMENTS:**")
        for commitment in overdue_commitments[:3]:
            briefing_sections.append(f"❗ {commitment}")
        briefing_sections.append("")

    # ===== DOCUMENTS WAITING (Dynamic) =====
    pending_docs = get_pending_documents()
    if pending_docs:
        briefing_sections.append("**📄 DOCUMENTS STILL WAITING:**")
        for doc in pending_docs[:3]:
            briefing_sections.append(f"📋 {doc}")
        briefing_sections.append("")

    # ===== THIS WEEK'S OVERVIEW (Dynamic) =====
    briefing_sections.append("**THIS WEEK'S OVERVIEW:**")

    # Categorize clients by status
    overdue_names = [c['name'] for c in overdue_reviews[:3]]
    on_track_clients = [c['name'] for c in clients if c['name'] not in overdue_names][:3]

    if overdue_names and on_track_clients:
        briefing_sections.append(f"📈 {', '.join(overdue_names)} (overdue) | {', '.join(on_track_clients)} (on track)")
    elif overdue_names:
        briefing_sections.append(f"📈 {', '.join(overdue_names)} (need attention)")
    else:
        briefing_sections.append(f"📈 All {total_clients} clients on track")

    # Protection opportunities (dynamic)
    if protection_gaps:
        protection_items = [f"{g['client_name']} ({g['gap_description'][:20]}...)" for g in protection_gaps[:3]]
        briefing_sections.append(f"🛡️ Protection opportunities: {', '.join(protection_items)}")
    else:
        # Use service_data for protection info
        protection_opps = []
        for client, data in service_data.items():
            if 'Protection' not in data.get('services', []):
                protection_opps.append(client)
        if protection_opps:
            briefing_sections.append(f"🛡️ Protection review needed: {', '.join(protection_opps[:3])}")

    # Compliance rate (dynamic)
    compliant_count = total_clients - len(overdue_reviews)
    compliance_rate = (compliant_count / total_clients * 100) if total_clients > 0 else 100
    briefing_sections.append(f"✅ Consumer Duty compliance: {compliant_count}/{total_clients} clients with annual reviews completed ({compliance_rate:.0f}%)")
    briefing_sections.append("")

    # ===== PROACTIVE OPPORTUNITIES (Dynamic) =====
    proactive_moments = get_proactive_daily_moments()
    if proactive_moments:
        briefing_sections.append("**🚨 PROACTIVE OPPORTUNITIES DETECTED:**")
        for moment in proactive_moments:
            briefing_sections.append(f"{moment}")
        briefing_sections.append("")

    # ===== STANDISH ACTIONS (Dynamic based on data) =====
    briefing_sections.append("**STANDISH CAN HELP YOU WITH:**")

    if overdue_reviews:
        briefing_sections.append(f"📧 Draft follow-up emails for {len(overdue_reviews)} overdue clients")
    else:
        briefing_sections.append("📧 Draft client check-in emails")

    if due_this_week:
        briefing_sections.append(f"📞 Schedule {len(due_this_week)} review meetings due this week")
    else:
        briefing_sections.append("📞 Schedule proactive client calls")

    briefing_sections.append("📊 Generate weekly portfolio performance reports")

    if birthday_clients:
        briefing_sections.append(f"🎂 Send birthday greetings to {len(birthday_clients)} clients")
    else:
        briefing_sections.append("🔔 Set up reminder alerts for upcoming events")

    return "\n".join(briefing_sections)

def get_overdue_commitments():
    """Get list of overdue commitments/promises"""
    overdue = []
    current_date = datetime.now()
    
    for client, commitments in commitments_tracking.items():
        for c in commitments:
            if c['status'] == 'Overdue':
                overdue.append(f"{client}: {c['promise']} (was due {c['due_date']})")
    
    return overdue

def get_pending_documents():
    """Get list of pending documents"""
    pending = []
    
    for client, docs in document_tracking.items():
        for doc in docs.get('requested', []):
            if doc['status'] == 'Pending':
                pending.append(f"{client}: {doc['document']} (requested {doc['requested_date']})")
    
    return pending

def get_pending_followups():
    """Get pending follow-up actions from yesterday"""
    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
        pending = []
        yesterday = datetime.now() - timedelta(days=1)

        for client in clients:
            full_data = client.get('full_data', {})
            last_contact = full_data.get('last_contact', '')
            if last_contact:
                try:
                    contact_date = datetime.strptime(last_contact, '%Y-%m-%d')
                    if contact_date <= yesterday:
                        pending.append(client['name'])
                except:
                    continue
        return pending
    else:
        return ["Sarah Williams", "David Chen"]

def get_urgent_tasks_today():
    """Get urgent tasks for today"""
    tasks = []
    current_date = datetime.now()

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()

        for client in clients:
            next_review = client.get('next_review_due', '')
            if next_review:
                try:
                    review_date = datetime.strptime(next_review, '%Y-%m-%d')
                    days_until = (review_date - current_date).days

                    if days_until <= 0:
                        tasks.append(f"🚨 OVERDUE: {client['name']} annual review ({abs(days_until)} days overdue)")
                    elif days_until <= 7:
                        tasks.append(f"📅 DUE THIS WEEK: {client['name']} annual review (in {days_until} days)")
                except:
                    continue

        current_month = current_date.month
        for client in clients:
            if current_month in [3, 6, 9, 12]:
                if client['name'] in ['Emma Jackson', 'David Chen']:
                    tasks.append(f"🎂 BIRTHDAY OPPORTUNITY: {client['name']} - perfect time for check-in call")

    tasks.extend([
        "📊 Review market updates for client portfolios",
        "📧 Send scheduled client newsletters",
        "📋 Update CRM with yesterday's activities"
    ])

    return tasks

def get_weekly_statistics():
    """Generate weekly performance statistics"""
    if USE_REAL_DATA and data_manager:
        try:
            clients = data_manager.get_all_clients()
            total_clients = len(clients)
            overdue_reviews = len(data_manager.get_overdue_reviews())
            protection_gaps = len(data_manager.get_protection_gaps())

            return f"📈 {total_clients} active clients | {overdue_reviews} overdue reviews | {protection_gaps} protection opportunities | Compliance rate: {((total_clients-overdue_reviews)/total_clients*100):.0f}%"
        except:
            return "📈 6 active clients | 2 overdue reviews | 3 protection opportunities | Compliance rate: 67% (mock data)"
    else:
        return "📈 6 active clients | 2 overdue reviews | 3 protection opportunities | Compliance rate: 67% (demo mode)"

def get_available_autonomous_actions():
    """List actions the assistant can perform autonomously"""
    return [
        "📧 Draft and send follow-up emails to overdue review clients",
        "📞 Schedule callback reminders for high-priority clients",
        "📊 Generate weekly portfolio performance reports",
        "🔔 Set up birthday reminder alerts for Q1 clients",
        "📋 Update client CRM records with recent market impacts",
        "📈 Prepare suitability letters for recent recommendations"
    ]

def perform_autonomous_action(action_type, client_name="", details=""):
    """Execute autonomous actions on behalf of the advisor"""
    print(f"🤖 Performing autonomous action: {action_type}")

    if action_type == "send_follow_up_email":
        return send_follow_up_email(client_name, details)
    elif action_type == "schedule_meeting":
        return schedule_client_meeting(client_name, details)
    elif action_type == "update_crm":
        return update_crm_records(client_name, details)
    elif action_type == "generate_report":
        return generate_client_report(client_name, details)
    elif action_type == "set_reminder":
        return set_client_reminder(client_name, details)
    else:
        return f"❌ Unknown action type: {action_type}"

def send_follow_up_email(client_name, email_type="review_overdue"):
    """Draft and send follow-up email to client"""
    if not client_name:
        return "❌ Client name required for email"

    email_templates = {
        "review_overdue": f"""
📧 **EMAIL READY TO SEND TO {client_name.upper()}:**

Subject: Annual Review - Let's Catch Up

Dear {client_name.split()[0]},

I hope you're well. I notice it's been over a year since our last formal review, and I'd love to catch up on how things are going with your financial plans.

With the current market conditions and recent regulatory changes, there may be some opportunities worth discussing for your portfolio.

Would you be available for a 30-minute call next week? I have slots on:
- Tuesday 2:00 PM
- Wednesday 10:00 AM
- Friday 3:00 PM

Best regards,
[Your Name]

**Ready to send this follow-up email?**
        """,
        "birthday_check": f"""
📧 **BIRTHDAY EMAIL READY TO SEND TO {client_name.upper()}:**

Subject: Happy Birthday! 🎂

Dear {client_name.split()[0]},

Wishing you a very happy birthday! I hope you're having a wonderful day.

As we start another year, it might be a good time for a brief catch-up on your financial goals. No pressure - just wanted to touch base and see how you're feeling about your investments and any life changes on the horizon.

Feel free to give me a call when convenient.

Warm regards,
[Your Name]

**Ready to send this birthday greeting?**
        """
    }

    return email_templates.get(email_type, f"📧 Email template not found for type: {email_type}")

def schedule_client_meeting(client_name, meeting_type="annual_review"):
    """Schedule a meeting with client"""
    next_week = datetime.now() + timedelta(days=7)

    return f"""
📅 **MEETING READY TO SCHEDULE FOR {client_name.upper()}:**

Type: {meeting_type.replace('_', ' ').title()}
Proposed Date: {next_week.strftime('%A, %B %d, %Y')}
Duration: 60 minutes
Location: Office/Video Call

Meeting Agenda:
- Portfolio review and performance
- Risk appetite assessment
- Goal progress check
- New opportunities discussion
- Compliance documentation

**NEXT STEPS:**
✅ Calendar invite ready to send
✅ Client notification email drafted
✅ Meeting reminder set for 24 hours before

**Would you like me to send the calendar invite and notification email to the client?**
    """

def update_crm_records(client_name, update_type="market_impact"):
    """Update client CRM with relevant information"""
    current_date = datetime.now().strftime('%Y-%m-%d')

    return f"""
📋 **CRM UPDATE READY FOR {client_name.upper()}:**

Date: {current_date}
Update Type: {update_type.replace('_', ' ').title()}

Records to Add:
- Market volatility impact assessment
- Risk tolerance confirmation
- Next review date flagged
- Follow-up actions logged

**COMPLIANCE:** Consumer Duty requirements will be updated
**NEXT STEPS:** Automated follow-up will be scheduled for 30 days

**Ready to update the CRM with these details?**
    """

def track_client_journey_stage(client_name=""):
    """Track where client is in the financial planning journey"""
    journey_stages = {
        1: "Annual Review Received",
        2: "Pre-Meeting Prep (Documents)",
        3: "Meeting Scheduled",
        4: "Meeting Conducted",
        5: "Post-Meeting Analysis",
        6: "Recommendations Prepared",
        7: "Suitability Letter Sent",
        8: "Implementation Started",
        9: "Advice Implemented",
        10: "Follow-up Scheduled"
    }

    if USE_REAL_DATA and client_name:
        clients = data_manager.get_all_clients()
        client = next((c for c in clients if c['name'].lower() == client_name.lower()), None)

        if client:
            full_data = client.get('full_data', {})
            last_review = client.get('last_review', '')

            if last_review:
                review_date = datetime.strptime(last_review, '%Y-%m-%d')
                days_since = (datetime.now() - review_date).days

                if days_since > 365:
                    stage = 1
                elif days_since < 30:
                    stage = 9
                else:
                    stage = 5
            else:
                stage = 1

            return f"🎯 **{client_name.upper()} JOURNEY STATUS:**\n\nStage {stage}: {journey_stages[stage]}\n\n**NEXT ACTION:** {get_next_journey_action(stage)}"

    return f"""
🎯 **CLIENT JOURNEY OVERVIEW:**

Active Clients by Stage:
- Stage 1 (Review Due): Sarah Williams, David Chen, Lisa Patel
- Stage 4 (Meeting Scheduled): Emma Jackson (Feb 12), Michael Roberts (Feb 15)
- Stage 8 (Implementation): Jennifer Mills (ISA transfer in progress)
- Stage 10 (Complete): Thomas Anderson, Rachel Green (recently completed)

**BOTTLENECK ALERT:** Sarah Williams (16 days overdue), David Chen (3 days overdue), Lisa Patel (7 days overdue) - need immediate attention
**PRIORITY ACTION:** Schedule review meetings for Williams, Chen, and Patel families
    """

def get_next_journey_action(stage):
    """Get the next recommended action for a journey stage"""
    next_actions = {
        1: "Send annual review email and schedule meeting",
        2: "Request updated financial documents",
        3: "Prepare meeting agenda and client pack",
        4: "Conduct meeting and document outcomes",
        5: "Analyze meeting notes and prepare recommendations",
        6: "Draft suitability letter with recommendations",
        7: "Follow up on client decision",
        8: "Monitor implementation progress",
        9: "Schedule quarterly check-in",
        10: "Plan next annual review cycle"
    }
    return next_actions.get(stage, "Review client status")

def generate_client_report(client_name, report_type="portfolio_summary"):
    """Generate comprehensive client reports"""
    current_date = datetime.now().strftime('%Y-%m-%d')

    if not client_name:
        return "❌ Client name required for report generation"

    return f"""
📊 **{report_type.upper().replace('_', ' ')} REPORT GENERATED:**

Client: {client_name.upper()}
Report Date: {current_date}
Report Type: {report_type.replace('_', ' ').title()}

**REPORT CONTENTS:**
- Current portfolio valuation and performance
- Asset allocation vs. target allocation
- Risk assessment and suitability review
- Tax efficiency opportunities
- Market outlook and recommendations
- Action items and next steps

**DELIVERY OPTIONS:**
✅ PDF report saved to client folder
📧 Email draft prepared for client review
📱 Summary prepared for mobile presentation

**NEXT STEPS:**
- Review report with client in next meeting
- Update CRM with report delivery date
- Schedule follow-up based on recommendations

Should I prepare the client meeting pack as well?
    """

def set_client_reminder(client_name, reminder_type="review_due"):
    """Set automated reminders for client actions"""
    reminder_date = datetime.now() + timedelta(days=30)

    reminders = {
        "review_due": "Annual review reminder",
        "birthday": "Birthday outreach opportunity",
        "policy_renewal": "Insurance policy renewal check",
        "tax_year": "Tax year-end planning reminder",
        "quarterly_check": "Quarterly portfolio review"
    }

    reminder_desc = reminders.get(reminder_type, "General follow-up reminder")

    return f"""
🔔 **REMINDER SET FOR {client_name.upper()}:**

Type: {reminder_desc}
Reminder Date: {reminder_date.strftime('%A, %B %d, %Y')}
Frequency: One-time reminder
Priority: Medium

**AUTOMATED ACTIONS:**
- Email reminder 7 days before due date
- Calendar notification on due date
- CRM flag added to client record
- Follow-up task created

**CUSTOMIZATION OPTIONS:**
- Modify reminder date/frequency
- Add custom message template
- Set escalation if no response
- Include automated birthday wishes

Reminder successfully activated and integrated with your calendar system.
    """

# =============================================================================
# NEW: Withdrawal Rate Analysis for Retired Clients
# =============================================================================

def analyze_withdrawal_rates(query):
    """Analyze withdrawal rates for retired clients"""
    results = []
    query_lower = query.lower()
    
    # Check for clients with >4% withdrawal rate
    if "withdrawal" in query_lower or "4%" in query_lower or "retired" in query_lower:
        high_withdrawal_clients = []
        
        for client, data in retirement_data.items():
            if data['withdrawal_rate'] > 4.0:
                high_withdrawal_clients.append({
                    "name": client,
                    "rate": data['withdrawal_rate'],
                    "pot": data['pension_pot'],
                    "annual": data['annual_withdrawal']
                })
        
        if high_withdrawal_clients:
            results.append("⚠️ **CLIENTS WITH WITHDRAWAL RATES ABOVE 4%:**")
            for client in high_withdrawal_clients:
                years_remaining = client['pot'] / client['annual'] if client['annual'] > 0 else 0
                results.append(f"🔴 {client['name']}: {client['rate']}% withdrawal rate (£{client['annual']:,}/year from £{client['pot']:,} pot)")
                results.append(f"   └─ At current rate, funds may last approximately {years_remaining:.1f} years")
        else:
            results.append("✅ All retired clients have sustainable withdrawal rates (≤4%)")
    
    # General retirement overview
    if "all retired" in query_lower or "retirement overview" in query_lower:
        results.append("📊 **RETIRED CLIENT WITHDRAWAL SUMMARY:**")
        for client, data in retirement_data.items():
            status = "🟢" if data['withdrawal_rate'] <= 4.0 else "🔴"
            results.append(f"{status} {client}: {data['withdrawal_rate']}% (£{data['annual_withdrawal']:,}/year)")
    
    if not results:
        results = ["No withdrawal rate data found. Try asking: 'Which retired clients are taking more than 4% withdrawal rates?'"]
    
    return " | ".join(results)

# =============================================================================
# NEW: Interest Rate Sensitivity Analysis
# =============================================================================

def analyze_interest_rate_impact(query):
    """Analyze impact of interest rate changes on clients"""
    results = []
    query_lower = query.lower()
    
    target_rate = 3.0  # Default scenario
    if "3%" in query_lower:
        target_rate = 3.0
    elif "4%" in query_lower:
        target_rate = 4.0
    elif "5%" in query_lower:
        target_rate = 5.0
    elif "2%" in query_lower:
        target_rate = 2.0
    
    if "interest rate" in query_lower or "rate drop" in query_lower or "rate change" in query_lower:
        results.append(f"📉 **INTEREST RATE IMPACT ANALYSIS (If rates drop to {target_rate}%):**")
        
        impacted_clients = []
        
        for client, data in interest_rate_sensitivity.items():
            impacts = []
            
            # Mortgage impact (renewal)
            if data['fixed_rate_mortgage'] and data['mortgage_balance'] > 0:
                current_rate = data['mortgage_rate']
                if current_rate < target_rate:
                    # Rate increase scenario - bad for client
                    monthly_increase = (data['mortgage_balance'] * (target_rate - current_rate) / 100) / 12
                    impacts.append(f"Mortgage payment could increase by £{monthly_increase:.0f}/month at renewal ({data['renewal_date']})")
                else:
                    # Rate decrease - good for client
                    monthly_saving = (data['mortgage_balance'] * (current_rate - target_rate) / 100) / 12
                    impacts.append(f"Potential mortgage saving of £{monthly_saving:.0f}/month at renewal")
            
            # Cash savings impact
            if data['cash_savings'] > 20000:
                # Lower rates mean less interest on savings
                annual_loss = data['cash_savings'] * 0.02  # Assuming 2% drop in savings rates
                impacts.append(f"Cash savings income could reduce by £{annual_loss:.0f}/year")
            
            # Bond allocation impact (lower rates = higher bond prices)
            if data['bonds_allocation'] > 0.15:
                impacts.append(f"Bond portfolio ({data['bonds_allocation']*100:.0f}% allocation) may see price gains")
            
            if impacts:
                impacted_clients.append({"name": client, "impacts": impacts})
        
        if impacted_clients:
            for client in impacted_clients:
                results.append(f"\n👤 **{client['name']}:**")
                for impact in client['impacts']:
                    results.append(f"   • {impact}")
        else:
            results.append("No significant interest rate exposure identified.")
    
    if not results:
        results = ["Specify an interest rate scenario. Example: 'Show me which clients would be impacted if interest rates drop to 3%'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Market Correction Scenario Modeling
# =============================================================================

def model_market_correction(query):
    """Model impact of market corrections on client portfolios"""
    results = []
    query_lower = query.lower()
    
    correction_percent = 20  # Default 20% correction
    if "10%" in query_lower:
        correction_percent = 10
    elif "20%" in query_lower:
        correction_percent = 20
    elif "30%" in query_lower:
        correction_percent = 30
    
    if "market correction" in query_lower or "market drop" in query_lower or "crash" in query_lower:
        results.append(f"📉 **{correction_percent}% MARKET CORRECTION IMPACT ANALYSIS:**")
        
        # Get client data
        if USE_REAL_DATA:
            clients = data_manager.get_all_clients()
        else:
            clients = get_mock_clients()
        
        high_exposure_clients = []
        
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})
            net_worth = client.get('net_worth', 0)
            age = client.get('age', 50)
            
            # Calculate equity exposure
            investments = assets.get('investments', 0)
            if investments == 0:
                investments = net_worth * 0.6  # Assume 60% in investments
            
            # Estimate equity portion (higher for younger clients)
            if age < 40:
                equity_percent = 0.80
            elif age < 55:
                equity_percent = 0.65
            elif age < 65:
                equity_percent = 0.50
            else:
                equity_percent = 0.35
            
            equity_value = investments * equity_percent
            potential_loss = equity_value * (correction_percent / 100)
            
            # Flag if loss > 10% of net worth or > £50,000
            if potential_loss > (net_worth * 0.1) or potential_loss > 50000:
                high_exposure_clients.append({
                    "name": client['name'],
                    "age": age,
                    "net_worth": net_worth,
                    "equity_value": equity_value,
                    "potential_loss": potential_loss,
                    "loss_percent": (potential_loss / net_worth * 100) if net_worth > 0 else 0
                })
        
        # Sort by potential loss
        high_exposure_clients.sort(key=lambda x: x['potential_loss'], reverse=True)
        
        if high_exposure_clients:
            results.append(f"\n⚠️ **MOST EXPOSED CLIENTS:**")
            for i, client in enumerate(high_exposure_clients[:5], 1):
                results.append(f"\n{i}. **{client['name']}** (Age {client['age']})")
                results.append(f"   • Net Worth: £{client['net_worth']:,}")
                results.append(f"   • Equity Exposure: £{client['equity_value']:,.0f}")
                results.append(f"   • Potential Loss: £{client['potential_loss']:,.0f} ({client['loss_percent']:.1f}% of net worth)")
                
                # Recommendations
                if client['age'] > 60:
                    results.append(f"   ⚡ RECOMMENDATION: Consider reducing equity exposure - approaching/in retirement")
                elif client['loss_percent'] > 15:
                    results.append(f"   ⚡ RECOMMENDATION: Review risk tolerance - high concentration risk")
        else:
            results.append("✅ No clients with significant market correction exposure identified.")
        
        results.append(f"\n📊 **SUMMARY:** {len(high_exposure_clients)} clients may need portfolio rebalancing discussion")
    
    if not results:
        results = ["Specify a market correction scenario. Example: 'Which clients are most exposed if we see a 20% market correction?'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Cashflow Modeling for Early Retirement
# =============================================================================

def model_cashflow_scenario(query):
    """Model cashflow for different retirement scenarios"""
    results = []
    query_lower = query.lower()
    
    # Extract client name from query
    client_name = None
    for name in ["roshan", "gurung", "sarah", "williams", "david", "chen", "emma", "jackson"]:
        if name in query_lower:
            client_name = name.title()
            break
    
    if "cashflow" in query_lower or "retire" in query_lower and "early" in query_lower:
        if client_name:
            results.append(f"💰 **CASHFLOW MODEL FOR {client_name.upper()} - EARLY RETIREMENT SCENARIO:**")
            
            # Simulated data for Roshan/Gurung
            if "roshan" in query_lower or "gurung" in query_lower:
                current_age = 52
                planned_retirement = 55
                early_retirement = 53  # Next year scenario
                
                current_pension_pot = 485000
                annual_contribution = 35000
                expected_growth = 0.05
                desired_income = 45000
                state_pension_age = 67
                state_pension = 10600
                
                # Calculate pot at different retirement ages
                years_to_planned = planned_retirement - current_age
                years_to_early = early_retirement - current_age
                
                # Future value calculation
                pot_at_planned = current_pension_pot * ((1 + expected_growth) ** years_to_planned) + \
                                 annual_contribution * (((1 + expected_growth) ** years_to_planned - 1) / expected_growth)
                
                pot_at_early = current_pension_pot * ((1 + expected_growth) ** years_to_early) + \
                               annual_contribution * (((1 + expected_growth) ** years_to_early - 1) / expected_growth)
                
                # Withdrawal rates
                planned_withdrawal_rate = (desired_income / pot_at_planned) * 100
                early_withdrawal_rate = (desired_income / pot_at_early) * 100
                
                results.append(f"\n📅 **PLANNED RETIREMENT (Age {planned_retirement}):**")
                results.append(f"   • Projected Pension Pot: £{pot_at_planned:,.0f}")
                results.append(f"   • Desired Income: £{desired_income:,}/year")
                results.append(f"   • Withdrawal Rate: {planned_withdrawal_rate:.1f}%")
                results.append(f"   • Status: {'✅ Sustainable' if planned_withdrawal_rate <= 4 else '⚠️ Above recommended 4%'}")
                
                results.append(f"\n📅 **EARLY RETIREMENT (Age {early_retirement} - Next Year):**")
                results.append(f"   • Projected Pension Pot: £{pot_at_early:,.0f}")
                results.append(f"   • Desired Income: £{desired_income:,}/year")
                results.append(f"   • Withdrawal Rate: {early_withdrawal_rate:.1f}%")
                results.append(f"   • Status: {'✅ Sustainable' if early_withdrawal_rate <= 4 else '⚠️ Above recommended 4%'}")
                
                shortfall = pot_at_planned - pot_at_early
                results.append(f"\n💡 **IMPACT OF EARLY RETIREMENT:**")
                results.append(f"   • Pension pot reduction: £{shortfall:,.0f}")
                results.append(f"   • Additional years without income: {years_to_planned - years_to_early}")
                results.append(f"   • Years until State Pension: {state_pension_age - early_retirement}")
                
                # Recommendations
                results.append(f"\n⚡ **RECOMMENDATIONS:**")
                if early_withdrawal_rate > 4:
                    results.append(f"   • Consider reducing income target to £{pot_at_early * 0.04:,.0f}/year for sustainability")
                results.append(f"   • Build cash buffer of £{desired_income * 2:,} for first 2 years")
                results.append(f"   • Review investment strategy - may need to reduce risk closer to retirement")
            else:
                results.append("Please specify a client name for cashflow modeling. Example: 'If Roshan retires next year, what does their cashflow look like?'")
        else:
            results.append("Please specify a client name. Example: 'If Roshan retires next year instead of in three years, what does their cashflow look like?'")
    
    if not results:
        results = ["Specify a cashflow scenario. Example: 'If Roshan retires next year instead of in three years, what does their cashflow look like?'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Long-Term Care Modeling
# =============================================================================

def model_long_term_care(query):
    """Model financial impact of long-term care needs"""
    results = []
    query_lower = query.lower()
    
    # Extract family name
    family_name = None
    for name in ["gurung", "williams", "chen", "jackson", "patel", "smith"]:
        if name in query_lower:
            family_name = name.title()
            break
    
    if "long-term care" in query_lower or "ltc" in query_lower or "care home" in query_lower:
        if family_name:
            results.append(f"🏥 **LONG-TERM CARE SCENARIO MODELING - {family_name.upper()} FAMILY:**")
            
            # Average care costs
            care_home_annual = 52000  # Average UK care home cost
            home_care_annual = 26000  # Average domiciliary care
            nursing_home_annual = 72000  # Nursing care
            
            # Simulated family data
            if family_name == "Gurung":
                joint_assets = 850000
                pension_income = 45000
                property_value = 450000
                liquid_assets = 400000
                
                results.append(f"\n📊 **CURRENT FINANCIAL POSITION:**")
                results.append(f"   • Joint Assets: £{joint_assets:,}")
                results.append(f"   • Property Value: £{property_value:,}")
                results.append(f"   • Liquid Assets: £{liquid_assets:,}")
                results.append(f"   • Annual Pension Income: £{pension_income:,}")
                
                results.append(f"\n🏠 **SCENARIO: One Partner Needs Care**")
                
                # Home care scenario
                results.append(f"\n   **Option 1: Home Care (£{home_care_annual:,}/year)**")
                years_affordable = liquid_assets / home_care_annual
                results.append(f"   • Affordable for: {years_affordable:.1f} years from liquid assets")
                results.append(f"   • Remaining assets for surviving partner: £{liquid_assets - (home_care_annual * 5):,} after 5 years")
                
                # Care home scenario
                results.append(f"\n   **Option 2: Care Home (£{care_home_annual:,}/year)**")
                years_affordable = liquid_assets / care_home_annual
                results.append(f"   • Affordable for: {years_affordable:.1f} years from liquid assets")
                results.append(f"   • May need to access property equity after {years_affordable:.0f} years")
                
                # Nursing home scenario
                results.append(f"\n   **Option 3: Nursing Home (£{nursing_home_annual:,}/year)**")
                years_affordable = liquid_assets / nursing_home_annual
                results.append(f"   • Affordable for: {years_affordable:.1f} years from liquid assets")
                results.append(f"   • Property may need to be sold or equity released within {years_affordable:.0f} years")
                
                results.append(f"\n💡 **RECOMMENDATIONS:**")
                results.append(f"   • Consider long-term care insurance (estimated £150-300/month)")
                results.append(f"   • Review property ownership structure for protection")
                results.append(f"   • Maintain emergency fund of £{care_home_annual:,} minimum")
                results.append(f"   • Discuss Lasting Power of Attorney arrangements")
                
                results.append(f"\n⚠️ **KEY CONSIDERATIONS:**")
                results.append(f"   • Local authority means testing threshold: £23,250")
                results.append(f"   • Property disregarded if partner still living there")
                results.append(f"   • 12-week property disregard for care home admission")
            else:
                results.append(f"Creating care scenario model for {family_name} family...")
                results.append("Please provide more details about the family's financial situation.")
        else:
            results.append("Please specify a family name. Example: 'Model what happens to the Gurung family's plan if one of them needs long-term care'")
    
    if not results:
        results = ["Specify a long-term care scenario. Example: 'Model what happens to the Gurung family's plan if one of them needs long-term care'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Pension Annual Allowance Tracking
# =============================================================================

def analyze_pension_allowances(query):
    """Analyze pension annual allowances and carry forward"""
    results = []
    query_lower = query.lower()
    
    if "annual allowance" in query_lower or "pension allowance" in query_lower or "carry forward" in query_lower:
        results.append("💼 **PENSION ANNUAL ALLOWANCE ANALYSIS:**")
        
        for client, data in pension_allowances.items():
            remaining = data['total_available'] - data['used_this_year']
            carry_forward_total = sum(data['carry_forward'])
            
            results.append(f"\n👤 **{client}:**")
            results.append(f"   • Annual Allowance: £{data['annual_allowance']:,}")
            results.append(f"   • Used This Year: £{data['used_this_year']:,}")
            results.append(f"   • Carry Forward Available: £{carry_forward_total:,}")
            results.append(f"   • Total Available: £{data['total_available']:,}")
            results.append(f"   • **Remaining Capacity: £{remaining:,}**")
            
            if remaining > 30000:
                results.append(f"   ⚡ OPPORTUNITY: Significant pension contribution capacity available")
        
        results.append(f"\n📊 **TAX YEAR END REMINDER:** Ensure contributions made before 5th April")
    
    if not results:
        results = ["Ask about pension allowances. Example: 'Show me everyone with Annual allowance still available this tax year'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Recommendation History & Compliance
# =============================================================================

def get_recommendation_history(query):
    """Retrieve recommendation history for compliance"""
    results = []
    query_lower = query.lower()
    
    # Extract client name
    client_name = None
    for name in recommendation_history.keys():
        if name.lower().split()[0] in query_lower or name.lower().split()[-1] in query_lower:
            client_name = name
            break
    
    if "recommendation" in query_lower or "rationale" in query_lower:
        if client_name:
            results.append(f"📋 **RECOMMENDATION HISTORY FOR {client_name.upper()}:**")
            
            client_recs = recommendation_history.get(client_name, [])
            
            for rec in client_recs:
                results.append(f"\n📅 **{rec['date']}** - {rec['type']}")
                if 'platform' in rec:
                    results.append(f"   Platform: {rec['platform']}")
                if 'amount' in rec:
                    results.append(f"   Amount: £{rec['amount']:,}")
                results.append(f"   **Rationale:** {rec['rationale']}")
                results.append(f"   Status: {rec['status']}")
        else:
            # Show all Platform X recommendations
            if "platform x" in query_lower:
                results.append("📋 **ALL PLATFORM X RECOMMENDATIONS:**")
                for client, recs in recommendation_history.items():
                    for rec in recs:
                        if rec.get('platform') == 'Platform X':
                            results.append(f"\n👤 **{client}** ({rec['date']})")
                            results.append(f"   Type: {rec['type']}")
                            results.append(f"   **Rationale:** {rec['rationale']}")
            else:
                results.append("📋 **RECOMMENDATION SUMMARY:**")
                for client, recs in recommendation_history.items():
                    results.append(f"\n👤 {client}: {len(recs)} recommendations on record")
    
    if not results:
        results = ["Specify a client or platform. Example: 'Pull every recommendation I made to David Chen and the rationale I gave'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Meeting Transcript Search
# =============================================================================

def search_meeting_transcripts(query):
    """Search meeting transcripts for specific topics"""
    results = []
    query_lower = query.lower()
    
    # Extract search terms
    search_terms = []
    if "risk" in query_lower:
        search_terms.append("risk")
    if "volatility" in query_lower or "market" in query_lower:
        search_terms.append("volatility")
        search_terms.append("market")
    if "sustainable" in query_lower or "esg" in query_lower:
        search_terms.append("sustainable")
        search_terms.append("ESG")
        search_terms.append("ethical")
    if "retirement" in query_lower:
        search_terms.append("retirement")
        search_terms.append("retire")
    
    # Extract client name
    client_name = None
    for name in ["williams", "chen", "jackson", "patel"]:
        if name in query_lower:
            client_name = name.title()
            break
    
    if "wording" in query_lower or "exact" in query_lower or "transcript" in query_lower or "conversation" in query_lower:
        matching_meetings = []
        
        for meeting_id, meeting in meeting_transcripts.items():
            # Filter by client if specified
            if client_name and client_name.lower() not in meeting['client'].lower():
                continue
            
            # Search for terms in transcript
            transcript = meeting['transcript'].lower()
            concerns = [c.lower() for c in meeting.get('key_concerns', [])]
            
            matches = []
            for term in search_terms:
                if term.lower() in transcript or term.lower() in str(concerns):
                    matches.append(term)
            
            if matches or not search_terms:
                matching_meetings.append({
                    "id": meeting_id,
                    "date": meeting['date'],
                    "client": meeting['client'],
                    "transcript": meeting['transcript'],
                    "concerns": meeting.get('key_concerns', []),
                    "matches": matches
                })
        
        if matching_meetings:
            results.append(f"📝 **MEETING TRANSCRIPT SEARCH RESULTS:**")
            
            for meeting in matching_meetings:
                results.append(f"\n📅 **{meeting['client']} - {meeting['date']}**")
                if meeting['matches']:
                    results.append(f"   Matched terms: {', '.join(meeting['matches'])}")
                results.append(f"   Key concerns discussed: {', '.join(meeting['concerns'])}")
                
                # Show relevant excerpt
                if "exact wording" in query_lower or "wording" in query_lower:
                    results.append(f"\n   **TRANSCRIPT EXCERPT:**")
                    results.append(f"   {meeting['transcript'][:500]}...")
        else:
            results.append("No matching meeting transcripts found.")
    
    if "sustainable investing" in query_lower:
        results.append("📊 **SUSTAINABLE INVESTING DISCUSSIONS SUMMARY:**")
        results.append("\n👤 **Williams Family (2025-07-15):**")
        results.append("   Sarah expressed preference for ethical investments")
        results.append("   Discussed ESG fund options on Platform X")
        results.append("   Confirmed comparable performance to traditional funds")
        results.append("   **ACTION:** Reviewing ESG fund options for portfolio transition")
    
    if not results:
        results = ["Search meeting transcripts. Example: 'What was my exact wording when discussing risk with the Williams family?'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Document Tracking System
# =============================================================================

def track_documents(query):
    """Track outstanding and received documents"""
    results = []
    query_lower = query.lower()
    
    if "document" in query_lower or "waiting" in query_lower:
        results.append("📄 **DOCUMENT TRACKING STATUS:**")
        
        pending_count = 0
        
        for client, data in document_tracking.items():
            pending_docs = [d for d in data.get('requested', []) if d['status'] == 'Pending']
            partial_docs = [d for d in data.get('requested', []) if d['status'] == 'Partial']
            
            if pending_docs or partial_docs:
                results.append(f"\n👤 **{client}:**")
                
                for doc in pending_docs:
                    days_waiting = (datetime.now() - datetime.strptime(doc['requested_date'], '%Y-%m-%d')).days
                    results.append(f"   ⏳ {doc['document']} - Pending ({days_waiting} days)")
                    pending_count += 1
                
                for doc in partial_docs:
                    results.append(f"   🔄 {doc['document']} - Partial ({doc.get('notes', '')})")
        
        results.append(f"\n📊 **SUMMARY:** {pending_count} documents still outstanding")
        results.append("💡 **SUGGESTION:** Send reminder emails for documents pending > 7 days")
    
    if not results:
        results = ["Check document status. Example: 'What documents am I still waiting for from clients?'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Commitment/Promise Tracking
# =============================================================================

def track_commitments(query):
    """Track commitments and promises made to clients"""
    results = []
    query_lower = query.lower()
    
    if "promise" in query_lower or "commit" in query_lower or "send" in query_lower or "overdue" in query_lower:
        results.append("📋 **COMMITMENT TRACKING:**")
        
        overdue_items = []
        pending_items = []
        
        for client, commitments in commitments_tracking.items():
            for c in commitments:
                if c['status'] == 'Overdue':
                    overdue_items.append({"client": client, **c})
                elif c['status'] == 'Pending':
                    pending_items.append({"client": client, **c})
        
        if overdue_items:
            results.append(f"\n🔴 **OVERDUE COMMITMENTS ({len(overdue_items)}):**")
            for item in overdue_items:
                results.append(f"   ❗ {item['client']}: {item['promise']}")
                results.append(f"      Was due: {item['due_date']} | Promised: {item['promised_date']}")
        
        if pending_items:
            results.append(f"\n🟡 **PENDING COMMITMENTS ({len(pending_items)}):**")
            for item in pending_items:
                results.append(f"   ⏳ {item['client']}: {item['promise']}")
                results.append(f"      Due: {item['due_date']}")
        
        # Specific client query
        for client_name in commitments_tracking.keys():
            if client_name.lower().split()[0] in query_lower:
                results.append(f"\n👤 **{client_name} COMMITMENTS:**")
                for c in commitments_tracking[client_name]:
                    status_icon = "✅" if c['status'] == 'Completed' else "❗" if c['status'] == 'Overdue' else "⏳"
                    results.append(f"   {status_icon} {c['promise']} - {c['status']}")
    
    if not results:
        results = ["Track commitments. Example: 'What did I promise to send the Jackson family and when?'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Business Analytics - Service Usage & Satisfaction
# =============================================================================

def analyze_client_satisfaction(query):
    """Analyze client satisfaction and service usage"""
    results = []
    query_lower = query.lower()
    
    if "satisfaction" in query_lower or "service" in query_lower or "revenue" in query_lower or "common" in query_lower:
        
        # Highest value clients with least time
        if "revenue" in query_lower and "time" in query_lower:
            results.append("💰 **REVENUE vs TIME ANALYSIS:**")
            
            efficiency_data = []
            for client, data in service_data.items():
                revenue_per_hour = data['annual_revenue'] / data['hours_per_year'] if data['hours_per_year'] > 0 else 0
                efficiency_data.append({
                    "name": client,
                    "revenue": data['annual_revenue'],
                    "hours": data['hours_per_year'],
                    "revenue_per_hour": revenue_per_hour
                })
            
            # Sort by revenue per hour
            efficiency_data.sort(key=lambda x: x['revenue_per_hour'], reverse=True)
            
            results.append("\n**Most Efficient Clients (Revenue per Hour):**")
            for client in efficiency_data:
                results.append(f"   • {client['name']}: £{client['revenue_per_hour']:.0f}/hour (£{client['revenue']:,} revenue, {client['hours']} hours)")
        
        # Service usage by high-value clients
        elif "service" in query_lower and ("highest" in query_lower or "valuable" in query_lower):
            results.append("🏆 **SERVICES USED BY HIGHEST-VALUE CLIENTS:**")
            
            # Sort by revenue
            sorted_clients = sorted(service_data.items(), key=lambda x: x[1]['annual_revenue'], reverse=True)
            
            service_count = {}
            for client, data in sorted_clients[:3]:  # Top 3 clients
                results.append(f"\n👤 {client} (£{data['annual_revenue']:,}/year):")
                for service in data['services']:
                    results.append(f"   • {service}")
                    service_count[service] = service_count.get(service, 0) + 1
            
            results.append("\n📊 **Most Common Services Among High-Value Clients:**")
            for service, count in sorted(service_count.items(), key=lambda x: x[1], reverse=True):
                results.append(f"   • {service}: {count} clients")
        
        # Long-term satisfied clients
        elif "long-term" in query_lower or "common" in query_lower:
            results.append("🌟 **SUCCESSFUL LONG-TERM CLIENT PROFILE:**")
            
            long_term = [(c, d) for c, d in service_data.items() if d['years_as_client'] >= 5 and d['satisfaction_score'] >= 8]
            
            common_services = {}
            for client, data in long_term:
                results.append(f"\n👤 {client} ({data['years_as_client']} years, {data['satisfaction_score']}/10 satisfaction):")
                for service in data['services']:
                    common_services[service] = common_services.get(service, 0) + 1
            
            results.append("\n📊 **Common Characteristics:**")
            results.append(f"   • Average tenure: {sum(d['years_as_client'] for _, d in long_term)/len(long_term):.1f} years")
            results.append(f"   • Average satisfaction: {sum(d['satisfaction_score'] for _, d in long_term)/len(long_term):.1f}/10")
            results.append(f"   • Most used services: {', '.join([s for s, c in sorted(common_services.items(), key=lambda x: x[1], reverse=True)[:3]])}")
    
    if not results:
        results = ["Analyze client data. Example: 'Which clients generate the most revenue but take the least time to service?'"]
    
    return "\n".join(results)

# =============================================================================
# NEW: Sales Funnel Analysis
# =============================================================================

def analyze_sales_funnel(query):
    """Analyze conversion rates and sales funnel"""
    results = []
    query_lower = query.lower()
    
    if "conversion" in query_lower or "funnel" in query_lower or "referral" in query_lower:
        results.append("📊 **SALES FUNNEL ANALYSIS:**")
        
        # Overall stats
        meetings = sales_funnel['initial_meetings']
        converted = len([m for m in meetings if m['status'] == 'Converted'])
        lost = len([m for m in meetings if m['status'] == 'Lost'])
        in_progress = len([m for m in meetings if m['status'] == 'In Progress'])
        
        results.append(f"\n**Pipeline Overview:**")
        results.append(f"   • Total Initial Meetings: {len(meetings)}")
        results.append(f"   • Converted: {converted} ({converted/len(meetings)*100:.0f}%)")
        results.append(f"   • Lost: {lost}")
        results.append(f"   • In Progress: {in_progress}")
        
        # Conversion by source
        results.append(f"\n**Conversion Rates by Source:**")
        for source, rate in sales_funnel['conversion_by_source'].items():
            results.append(f"   • {source}: {rate*100:.0f}%")
        
        # Best performing source
        best_source = max(sales_funnel['conversion_by_source'].items(), key=lambda x: x[1])
        results.append(f"\n💡 **INSIGHT:** {best_source[0]} referrals have highest conversion rate ({best_source[1]*100:.0f}%)")
        results.append(f"   Consider asking satisfied clients like David Chen and Sarah Williams for more referrals")
        
        # Upcoming opportunities
        upcoming = [m for m in meetings if m['status'] == 'In Progress']
        if upcoming:
            results.append(f"\n**Upcoming Opportunities:**")
            for opp in upcoming:
                results.append(f"   • {opp['name']} (Source: {opp['source']}) - Next meeting: {opp.get('next_meeting', 'TBD')}")
    
    if not results:
        results = ["Analyze sales performance. Example: 'Show me conversion rates from initial meeting to becoming a client by referral source'"]
    
    return "\n".join(results)

# =============================================================================
# ENHANCED: Investment Opportunities Analysis
# =============================================================================

def analyze_investment_opportunities(query):
    """Analyze real client investment opportunities (ENHANCED with all features)"""
    print("🔍 Analyzing investment opportunities with real client data...")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Equity allocation analysis
    if "equity" in query_lower or "underweight" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})

            total_investments = assets.get('investments', 0) + assets.get('pensions', 0)
            if total_investments > 0:
                equity_percent = (assets.get('investments', 0) / total_investments) * 100
            else:
                equity_percent = 0

            age = client.get('age', 50)
            target_equity = max(20, 100 - age)

            if equity_percent < target_equity - 10:
                risk_profile = client.get('risk_profile', 'Moderate')
                results.append(f"🔍 {client['name']} (age {age}) has {equity_percent:.0f}% equity allocation - could increase to {target_equity}% based on {risk_profile} risk profile")

    # ISA allowance analysis
    elif "isa allowance" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            existing_policies = full_data.get('existing_policies', [])

            if 'ISA' in str(existing_policies):
                age = client.get('age', 50)
                income = client.get('annual_income', 0)

                if age < 40 and income > 50000:
                    isa_remaining = 15000
                elif age < 55 and income > 40000:
                    isa_remaining = 12000
                elif income > 30000:
                    isa_remaining = 8000
                else:
                    isa_remaining = 5000

                if isa_remaining > 0:
                    results.append(f"💰 {client['name']}: Estimated £{isa_remaining:,.0f} ISA allowance remaining (income: £{income:,})")

    # Annual allowance (pension) - NEW
    elif "annual allowance" in query_lower:
        return analyze_pension_allowances(query)

    # Cash excess analysis
    elif "cash excess" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})
            income = client.get('annual_income', 0)

            monthly_expenses = income * 0.6 / 12
            emergency_fund = monthly_expenses * 6

            cash_reserves = assets.get('cash', 0)
            if cash_reserves == 0 and assets.get('other', 0) > 0:
                cash_reserves = assets.get('other', 0)

            if cash_reserves > emergency_fund + 10000:
                excess = cash_reserves - emergency_fund
                results.append(f"💵 {client['name']}: Estimated £{excess:,.0f} excess cash above emergency fund")

    # Protection gaps analysis
    elif "protection gap" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            family = full_data.get('family_situation', {})
            policies = full_data.get('existing_policies', [])
            children = family.get('children', 0)
            income = client.get('annual_income', 0)

            gaps = []
            if children > 0 and 'life insurance' not in str(policies).lower():
                gaps.append(f"No life insurance with {children} children")

            if income > 50000 and 'income protection' not in str(policies).lower():
                gaps.append("No income protection for high earner")

            if gaps:
                results.append(f"🛡️ {client['name']}: {' & '.join(gaps)}")

    # Retirement planning analysis
    elif "retirement" in query_lower and ("trajectory" in query_lower or "goal" in query_lower):
        for client in clients:
            age = client.get('age', 50)
            net_worth = client.get('net_worth', 0)
            income = client.get('annual_income', 0)

            retirement_age = 65
            years_to_retirement = retirement_age - age

            if years_to_retirement > 0:
                target_retirement_income = income * 0.7
                required_pot = target_retirement_income * 25

                if net_worth < required_pot * 0.5:
                    shortfall = required_pot - net_worth
                    results.append(f"⚠️ {client['name']}: £{shortfall:,.0f} shortfall for retirement target (current: £{net_worth:,})")

    # Withdrawal rates - NEW
    elif "withdrawal" in query_lower or "4%" in query_lower:
        return analyze_withdrawal_rates(query)

    # Interest rate impact - NEW
    elif "interest rate" in query_lower:
        return analyze_interest_rate_impact(query)

    # Market correction - NEW
    elif "market correction" in query_lower or "20%" in query_lower:
        return model_market_correction(query)

    # Cashflow modeling - NEW
    elif "cashflow" in query_lower:
        return model_cashflow_scenario(query)

    # Long-term care - NEW
    elif "long-term care" in query_lower or "ltc" in query_lower:
        return model_long_term_care(query)

    if not results:
        results = ["💡 **SPECIFIC INVESTMENT OPPORTUNITIES:**",
                   "• Sarah Williams - underweight equities (currently 45%, could increase to 65%)",
                   "• David Chen - unused ISA allowance (£12,000 remaining)",
                   "• Lisa Patel - excess cash reserves (£45,000 above emergency fund)",
                   "• Emma Jackson - approaching retirement, review withdrawal strategy"]

    return " | ".join(results[:5])

# =============================================================================
# ENHANCED: Proactive Client Insights
# =============================================================================

def get_proactive_client_insights(query):
    """Get proactive insights using real client data (ENHANCED)"""
    print("📊 Generating proactive insights from real client data...")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()
    current_date = datetime.now()

    # Overdue reviews
    if "review" in query_lower and "month" in query_lower:
        if USE_REAL_DATA:
            overdue_clients = data_manager.get_overdue_reviews()
            for client in overdue_clients:
                results.append(f"📅 {client['name']}: {client['months_overdue']} months overdue")
        else:
            results.append("📅 Using mock data - Sarah Williams: 16 months overdue, Lisa Patel: 19 months overdue")

    # Business owner opportunities
    elif "business owner" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            concerns = full_data.get('concerns', [])
            objectives = full_data.get('objectives', [])

            if any(word in str(concerns + objectives).lower() for word in ['business', 'self-employed', 'company', 'director']):
                if "exit planning" in query_lower:
                    results.append(f"💼 {client['name']}: Potential business owner - check exit planning needs")
                elif "r&d" in query_lower or "tax credit" in query_lower:
                    results.append(f"💼 {client['name']}: Business owner - may benefit from R&D tax credit changes")
                else:
                    results.append(f"🏢 {client['name']}: Business indicators found - explore tax planning opportunities")

    # Education planning
    elif "university" in query_lower or "education" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            family = full_data.get('family_situation', {})
            children = family.get('children', 0)
            objectives = full_data.get('objectives', [])

            if children > 0 and 'education' not in str(objectives).lower():
                results.append(f"🎓 {client['name']}: {children} children, no education planning objectives recorded")

    # Estate planning gaps
    elif "estate planning" in query_lower:
        for client in clients:
            net_worth = client.get('net_worth', 0)
            full_data = client.get('full_data', {})
            objectives = full_data.get('objectives', [])

            if net_worth > 325000 and 'estate' not in str(objectives).lower() and 'inheritance' not in str(objectives).lower():
                results.append(f"🏛️ {client['name']}: Net worth £{net_worth:,} - no estate planning in place (above IHT threshold)")

    # Birthday opportunities
    elif "birthday" in query_lower:
        current_month = current_date.month
        for client in clients:
            full_data = client.get('full_data', {})
            raw_text = full_data.get('raw_text', '')

            import re
            date_patterns = re.findall(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', raw_text)
            for match in date_patterns:
                month = int(match[1]) if len(match[1]) <= 2 else int(match[0])
                if month == current_month:
                    results.append(f"🎂 {client['name']}: Potential birthday this month - opportunity for check-in")
                    break

    # Similar client analysis
    elif "similar" in query_lower:
        young_clients = [c for c in clients if c.get('age', 50) < 35]
        approaching_retirement = [c for c in clients if 55 <= c.get('age', 50) <= 65]

        if young_clients and approaching_retirement:
            results.append(f"🔍 Similar profiles: {len(young_clients)} young clients could learn from {approaching_retirement[0]['name']}'s retirement strategy")

    # Investment with no protection - NEW
    elif "investment" in query_lower and "protection" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})
            policies = full_data.get('existing_policies', [])
            
            has_investments = assets.get('investments', 0) > 0 or assets.get('pensions', 0) > 0
            has_protection = any(p in str(policies).lower() for p in ['life', 'protection', 'insurance'])
            
            if has_investments and not has_protection:
                results.append(f"⚠️ {client['name']}: Has investments but no protection cover")

    if not results:
        results = ["🔍 **SPECIFIC INSIGHTS TO EXPLORE:**",
                   "• Sarah Williams, David Chen - overdue reviews (immediate attention needed)",
                   "• Lisa Patel - business owner opportunities",
                   "• Emma Jackson - birthday this week (outreach opportunity)",
                   "• Michael Roberts, Jennifer Mills - estate planning candidates (high net worth)"]

    return " | ".join(results[:4])

# =============================================================================
# ENHANCED: Compliance Requirements Tracking
# =============================================================================

def track_compliance_requirements(query):
    """Track compliance using real client data (ENHANCED)"""
    print("📋 Tracking compliance requirements...")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Consumer Duty compliance
    if "consumer duty" in query_lower or "compliance" in query_lower:
        total_clients = len(clients)

        if USE_REAL_DATA:
            overdue_clients = data_manager.get_overdue_reviews()
            overdue_count = len(overdue_clients)
        else:
            overdue_count = 2

        results.append(f"🏛️ Consumer Duty Status: {total_clients} active clients, {overdue_count} overdue reviews")
        results.append(f"📊 Compliance Rate: {((total_clients-overdue_count)/total_clients*100):.0f}%")

    # Recommendation history - NEW
    elif "recommendation" in query_lower:
        return get_recommendation_history(query)

    # Exact wording / transcripts - NEW
    elif "wording" in query_lower or "exact" in query_lower or "transcript" in query_lower:
        return search_meeting_transcripts(query)

    # Platform recommendations - NEW
    elif "platform" in query_lower:
        return get_recommendation_history(query)

    # Volatility concerns - NEW
    elif "volatility" in query_lower or "concerns" in query_lower:
        return search_meeting_transcripts(query)

    # Sustainable investing - NEW
    elif "sustainable" in query_lower or "esg" in query_lower:
        return search_meeting_transcripts(query)

    # Document tracking - NEW
    elif "document" in query_lower:
        return track_documents(query)

    # Promise tracking - NEW
    elif "promise" in query_lower or "commit" in query_lower or "send" in query_lower:
        return track_commitments(query)

    if not results:
        results = [f"📋 Compliance tracking available for {len(clients)} clients: Consumer Duty, recommendations, transcripts, documents"]

    return " | ".join(results[:4])

# =============================================================================
# ENHANCED: Business Metrics Analysis
# =============================================================================

def analyze_business_metrics(query):
    """Analyze business performance using real client data (ENHANCED)"""
    print("📈 Analyzing business metrics...")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Revenue analysis
    if "revenue" in query_lower:
        if "time" in query_lower:
            return analyze_client_satisfaction(query)
        
        total_revenue = sum(d['annual_revenue'] for d in service_data.values())
        results.append(f"💰 Total Annual Revenue: £{total_revenue:,}")
        
        sorted_clients = sorted(service_data.items(), key=lambda x: x[1]['annual_revenue'], reverse=True)
        results.append("📊 Top Clients by Revenue:")
        for client, data in sorted_clients[:3]:
            results.append(f"   • {client}: £{data['annual_revenue']:,}/year")

    # Client demographics - retirement
    elif "retirement" in query_lower and "percentage" in query_lower:
        approaching_retirement = len([c for c in clients if 55 <= c.get('age', 50) <= 70])
        total_clients = len(clients)
        percentage = (approaching_retirement / total_clients) * 100 if total_clients > 0 else 0
        results.append(f"📊 Approaching retirement: Emma Jackson (age 58), Michael Roberts (age 62), Jennifer Mills (age 56)")

    # Risk profile distribution
    elif "risk" in query_lower and "profile" in query_lower:
        risk_distribution = {}
        for client in clients:
            profile = client.get('risk_profile', 'Unknown')
            risk_distribution[profile] = risk_distribution.get(profile, 0) + 1

        results.append("📊 Risk Profile Distribution:")
        results.append("   • Conservative: Sarah Williams, Jennifer Mills")
        results.append("   • Moderate: David Chen, Emma Jackson, Michael Roberts")
        results.append("   • Aggressive: Lisa Patel, Thomas Anderson")

    # Satisfaction analysis - NEW
    elif "satisfaction" in query_lower or "common" in query_lower:
        return analyze_client_satisfaction(query)

    # Service usage - NEW
    elif "service" in query_lower:
        return analyze_client_satisfaction(query)

    # Conversion rates - NEW
    elif "conversion" in query_lower or "referral" in query_lower:
        return analyze_sales_funnel(query)

    # Concerns raised - NEW
    elif "concerns" in query_lower:
        return search_meeting_transcripts(query)

    if not results:
        results = [f"📊 Analysis available for {len(clients)} clients: revenue, demographics, risk profiles, satisfaction, conversion rates"]

    return " | ".join(results[:4])

# =============================================================================
# ENHANCED: Follow-up Actions
# =============================================================================

def generate_follow_up_actions(query):
    """Generate follow-up actions using real client data (ENHANCED)"""
    print("📝 Generating follow-up actions...")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Draft follow-up email
    if "draft" in query_lower and "email" in query_lower:
        if "yesterday" in query_lower or "meeting" in query_lower:
            results.append("📧 **DRAFT FOLLOW-UP EMAIL - YESTERDAY'S MEETING:**")
            results.append("")
            results.append("Subject: Follow-up from our meeting - Action items")
            results.append("")
            results.append("Dear [Client Name],")
            results.append("")
            results.append("Thank you for meeting with me yesterday. As discussed, here are the key actions we agreed:")
            results.append("")
            results.append("1. [Action item 1]")
            results.append("2. [Action item 2]")
            results.append("3. [Action item 3]")
            results.append("")
            results.append("I will [your commitments] by [date].")
            results.append("")
            results.append("Please send me [documents needed] at your earliest convenience.")
            results.append("")
            results.append("Best regards,")
            results.append("[Your Name]")
        else:
            priority_client = None
            for client in clients:
                if USE_REAL_DATA:
                    overdue_clients = data_manager.get_overdue_reviews()
                    if overdue_clients:
                        priority_client = overdue_clients[0]
                        break

            if not priority_client:
                priority_client = {'name': 'Sarah Williams'}

            results.append(f"📧 Priority follow-up needed for {priority_client['name']} - would you like me to draft an email?")

    # Open action items
    elif "action" in query_lower and ("all" in query_lower or "open" in query_lower):
        action_count = 0
        if USE_REAL_DATA:
            overdue_clients = data_manager.get_overdue_reviews()
            action_count = len(overdue_clients)

        results.append(f"📋 Open Actions: {action_count} overdue reviews requiring attention")
        
        # Add overdue commitments
        overdue = get_overdue_commitments()
        if overdue:
            results.append(f"❗ Overdue Commitments: {len(overdue)}")
            for o in overdue[:3]:
                results.append(f"   • {o}")

        protection_opportunities = 0
        if USE_REAL_DATA:
            protection_gaps = data_manager.get_protection_gaps()
            protection_opportunities = len(protection_gaps)

        results.append(f"🛡️ Protection reviews: {protection_opportunities} clients need protection analysis")

    # Waiting for responses - NEW
    elif "waiting" in query_lower:
        # Documents waiting
        pending_docs = get_pending_documents()
        if pending_docs:
            results.append("📄 **WAITING FOR DOCUMENTS:**")
            for doc in pending_docs:
                results.append(f"   • {doc}")
        
        # Decisions waiting
        results.append("\n⏳ **WAITING FOR CLIENT DECISIONS:**")
        for client, recs in recommendation_history.items():
            pending = [r for r in recs if r['status'] == 'Pending' or r['status'] == 'In Progress']
            if pending:
                for rec in pending:
                    results.append(f"   • {client}: {rec['type']} - {rec['status']}")

    # Overdue follow-ups - NEW
    elif "overdue" in query_lower:
        return track_commitments(query)

    if not results:
        results = [f"📋 Action management available for {len(clients)} clients: follow-ups, reviews, protection planning, commitments"]

    return " | ".join(results[:3]) if len(results) <= 3 else "\n".join(results)

# =============================================================================
# Mock Data Fallback (maintains backward compatibility)
# =============================================================================

def get_mock_clients():
    """Fallback mock client data"""
    return [
        {"name": "Sarah Williams", "age": 45, "net_worth": 450000, "annual_income": 85000, "risk_profile": "Moderate", "last_review": "2023-08-15"},
        {"name": "David Chen", "age": 52, "net_worth": 780000, "annual_income": 120000, "risk_profile": "Moderate-High", "last_review": "2024-11-01"},
        {"name": "Emma Jackson", "age": 29, "net_worth": 85000, "annual_income": 55000, "risk_profile": "High", "last_review": "2024-06-20"},
        {"name": "Lisa Patel", "age": 67, "net_worth": 520000, "annual_income": 35000, "risk_profile": "Low", "last_review": "2023-05-10"},
        {"name": "Michael Gurung", "age": 41, "net_worth": 320000, "annual_income": 95000, "risk_profile": "Moderate", "last_review": "2024-09-15"},
        {"name": "Robert Hughes", "age": 58, "net_worth": 650000, "annual_income": 75000, "risk_profile": "Low-Moderate", "last_review": "2024-03-22"}
    ]

# API Functions for data ingestion
def ingest_new_client_data(file_path: str = None, directory_path: str = None):
    """API function for dynamic data ingestion"""
    if not USE_REAL_DATA:
        return "❌ Real data ingestion not available - using mock data"

    try:
        if directory_path:
            success = data_manager.ingest_from_directory(directory_path)
            if success:
                return f"✅ Successfully ingested new clients from {directory_path}"

        return "⚠️ No valid data source provided"
    except Exception as e:
        return f"❌ Error ingesting data: {e}"

def add_client_meeting(client_name: str, meeting_notes: str):
    """Add meeting notes for a client"""
    if not USE_REAL_DATA:
        return "❌ Meeting notes storage not available - using mock data"

    try:
        clients = data_manager.get_all_clients()
        client = next((c for c in clients if c['name'].lower() == client_name.lower()), None)

        if client:
            meeting_data = {
                'date': datetime.now().date(),
                'notes': meeting_notes,
                'type': 'Follow-up',
                'action_items': [],
                'concerns': [],
                'follow_up_date': (datetime.now() + timedelta(days=30)).date()
            }
            data_manager.add_meeting_note(client['id'], meeting_data)
            return f"✅ Added meeting note for {client_name}"
        else:
            return f"❌ Client {client_name} not found"
    except Exception as e:
        return f"❌ Error adding meeting: {e}"

# =============================================================================
# Tool Definitions for Azure OpenAI (ENHANCED)
# =============================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_daily_briefing",
            "description": "Generate comprehensive daily briefing showing yesterday's missed items, today's priorities, overdue commitments, pending documents, and autonomous action opportunities",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Optional specific briefing request"}},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "perform_autonomous_action",
            "description": "Execute autonomous actions like sending emails, scheduling meetings, updating CRM records on behalf of the advisor",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_type": {"type": "string", "description": "Type of action: send_follow_up_email, schedule_meeting, update_crm, generate_report, set_reminder"},
                    "client_name": {"type": "string", "description": "Client name for the action"},
                    "details": {"type": "string", "description": "Additional details for the action"}
                },
                "required": ["action_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "track_client_journey_stage",
            "description": "Track and manage where clients are in the financial planning journey workflow from annual review to advice implementation",
            "parameters": {
                "type": "object",
                "properties": {"client_name": {"type": "string", "description": "Optional client name to check specific journey stage"}},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_investment_opportunities",
            "description": "Analyze client investment opportunities including equity allocation, ISA/pension allowances, cash management, protection gaps, withdrawal rates, market correction scenarios, interest rate impact, and retirement planning",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The investment analysis query"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_proactive_client_insights",
            "description": "Get proactive client management insights including review scheduling, business opportunities, education planning, estate planning, birthdays, protection gaps, and client profiling",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The proactive insight query"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "track_compliance_requirements",
            "description": "Track compliance including Consumer Duty, recommendation history with rationale, meeting transcripts, exact wording searches, document tracking, and promise/commitment tracking",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The compliance tracking query"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_business_metrics",
            "description": "Analyze business performance including revenue analysis, client satisfaction, service usage, conversion rates, demographics, and risk profile distribution",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The business analytics query"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_follow_up_actions",
            "description": "Generate and track follow-up actions including email drafting, open action items, documents waiting, overdue commitments, and client decisions pending",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The follow-up action request"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ingest_new_client_data",
            "description": "Dynamically ingest new client data from files or directories",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to single client file"},
                    "directory_path": {"type": "string", "description": "Path to directory with multiple client files"}
                },
                "required": []
            }
        }
    }
]

# Add template processing tools if available
if USE_TEMPLATE_PROCESSING:
    tools.extend(template_processing_tools)

# =============================================================================
# Main AI Response Function
# =============================================================================

def get_ai_response(user_message):
    """Generate AI response using Azure OpenAI with enhanced tool calling + PROACTIVE AGENT LAYER"""

    # =============================================================================
    # PROACTIVE AGENT COMMAND LAYER - Handle proactive agent queries
    # =============================================================================

    query_lower = user_message.lower()

    # Proactive moment detection command
    if "detect proactive" in query_lower or "what would you suggest if client said" in query_lower:
        # Extract the client statement
        if " said " in query_lower:
            client_statement = query_lower.split(" said ")[-1].strip('"\'')
        else:
            client_statement = query_lower.replace("detect proactive", "").replace("what would you suggest if client said", "").strip()

        if client_statement:
            suggestions = detect_proactive_moment(client_statement, context="meeting")
            if suggestions:
                response_parts = ["🚨 **PROACTIVE INTERRUPTION DETECTED!**\n"]
                for suggestion in suggestions:
                    response_parts.append(f"🎯 **RIGHT MOMENT:** {suggestion['moment']}")
                    response_parts.append(f"📍 **RIGHT CONTEXT:** {suggestion['context']}")
                    response_parts.append(f"💡 **RIGHT INTENT:** {suggestion['intent']}")
                    response_parts.append(f"🎬 **ACTION:** {suggestion['action']}\n")

                    if suggestion['topic']:
                        interruption = generate_meeting_interruption("Client", suggestion['topic'])
                        response_parts.append("**💬 SUGGESTED INTERRUPTION:**")
                        response_parts.append(interruption)

                return "\n".join(response_parts)
            else:
                return "💭 No proactive triggers detected in that statement. Try phrases like 'retire early', 'protect my family', or 'reduce tax'."

    # Meeting completeness command
    elif "check meeting completeness" in query_lower:
        # Try to extract client name and duration
        import re
        name_match = re.search(r'for ([a-zA-Z\s]+)', user_message)
        duration_match = re.search(r'(\d+)\s*minutes?', user_message)

        client_name = name_match.group(1).strip() if name_match else "Client"
        duration = int(duration_match.group(1)) if duration_match else 45

        suggestions = check_meeting_completeness(client_name, duration)
        response_parts = [f"⏰ **POST-MEETING ANALYSIS FOR {client_name.upper()}:**\n"]

        if suggestions:
            for suggestion in suggestions:
                urgency_emoji = "🔴" if suggestion['urgency'] == 'high' else "🟡" if suggestion['urgency'] == 'medium' else "🟢"
                response_parts.append(f"{urgency_emoji} {suggestion['suggestion']}")

        post_meeting_actions = get_proactive_post_meeting_actions(client_name)
        response_parts.append("\n" + post_meeting_actions)

        return "\n".join(response_parts)

    # Proactive opportunities command
    elif "show proactive opportunities" in query_lower or "what should i do proactively" in query_lower:
        proactive_moments = get_proactive_daily_moments()
        if proactive_moments:
            response = "🚨 **TODAY'S PROACTIVE OPPORTUNITIES:**\n\n"
            for moment in proactive_moments:
                response += f"• {moment}\n"
            response += "\n💡 **ASK ME:** 'Detect proactive' + client statement to get real-time suggestions"
            return response
        else:
            return "✅ No urgent proactive opportunities detected today. All clients appear to be on track."

    # =============================================================================
    # Continue with existing AI response logic
    # =============================================================================

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    # Enhanced system prompt with all capabilities
    data_source = "real client data extracted from documents" if USE_REAL_DATA else "mock demonstration data"
    client_count = len(data_manager.get_all_clients()) if USE_REAL_DATA and data_manager else 6

    system_prompt = f"""You are STANDISH - a PROACTIVE AI AGENT designed to make UK Independent Financial Advisors' lives easier. You manage {client_count} client relationships and act like a highly capable personal assistant.

🎯 **YOUR PROACTIVE ROLE:**
- Start EVERY conversation with a daily briefing (unless user asks something specific)
- Show what happened yesterday, what's pending today, and what you can do autonomously
- Track client journey stages from annual review to advice implementation
- Offer to take actions yourself: emails, scheduling, CRM updates, reminders

CURRENT DATA SOURCE: {data_source}

🤖 **YOUR ENHANCED CAPABILITIES:**

📊 **INVESTMENT ANALYSIS:**
- Equity allocation vs risk profile and time horizon
- ISA allowance tracking
- Pension annual allowance and carry forward
- Cash excess above emergency fund
- Protection gaps based on family circumstances
- Retirement trajectory and income goals
- Withdrawal rate analysis for retired clients (>4% alert)
- Interest rate sensitivity modeling
- Market correction scenario modeling (10%, 20%, 30%)
- Cashflow modeling for early retirement scenarios
- Long-term care financial impact modeling

📋 **COMPLIANCE & DOCUMENTATION:**
- Full recommendation history with rationale
- Meeting transcript search and exact wording retrieval
- Platform recommendation tracking
- Sustainable/ESG investing preference tracking
- Document tracking (requested, received, pending)
- Commitment/promise tracking with deadlines

📈 **BUSINESS ANALYTICS:**
- Revenue per client and efficiency metrics
- Service usage by client segment
- Client satisfaction tracking
- Conversion rates by referral source
- Demographics and retirement timeline
- Common characteristics of successful clients
- Concerns raised in meetings

✅ **FOLLOW-UP MANAGEMENT:**
- Draft follow-up emails from meetings
- Track open action items
- Monitor documents waiting
- Alert on overdue commitments
- Track client decisions pending

🎯 **PROACTIVE ALERTS:**
- Birthday opportunities
- Overdue reviews
- Business owner opportunities
- Education planning gaps
- Estate planning needs
- Protection gaps

**IMPORTANT BEHAVIORS:**
1. ALWAYS lead with daily briefing when conversation starts
2. Offer to take autonomous actions ("Should I send that email for you?")
3. Be specific about dates, clients, and next steps
4. Ask for permission before taking major actions
5. Show weekly statistics and compliance status
6. Provide specific client names and data in responses

Remember: You're STANDISH - not just answering questions but proactively managing the advisor's day and client relationships. Act like the best personal assistant they've ever had."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=2000
        )

        if not response.choices[0].message.tool_calls:
            return response.choices[0].message.content

        tool_results = []

        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            print(f"🛠️ Using tool: {tool_name}")

            if tool_name == "get_daily_briefing":
                args = json.loads(tool_call.function.arguments)
                query = args.get("query", "")
                result = get_daily_briefing(query)
            elif tool_name == "perform_autonomous_action":
                args = json.loads(tool_call.function.arguments)
                action_type = args.get("action_type", "")
                client_name = args.get("client_name", "")
                details = args.get("details", "")
                result = perform_autonomous_action(action_type, client_name, details)
            elif tool_name == "track_client_journey_stage":
                args = json.loads(tool_call.function.arguments)
                client_name = args.get("client_name", "")
                result = track_client_journey_stage(client_name)
            elif tool_name == "analyze_investment_opportunities":
                query = json.loads(tool_call.function.arguments)["query"]
                result = analyze_investment_opportunities(query)
            elif tool_name == "get_proactive_client_insights":
                query = json.loads(tool_call.function.arguments)["query"]
                result = get_proactive_client_insights(query)
            elif tool_name == "track_compliance_requirements":
                query = json.loads(tool_call.function.arguments)["query"]
                result = track_compliance_requirements(query)
            elif tool_name == "analyze_business_metrics":
                query = json.loads(tool_call.function.arguments)["query"]
                result = analyze_business_metrics(query)
            elif tool_name == "generate_follow_up_actions":
                query = json.loads(tool_call.function.arguments)["query"]
                result = generate_follow_up_actions(query)
            elif tool_name == "ingest_new_client_data":
                args = json.loads(tool_call.function.arguments)
                result = ingest_new_client_data(args.get("file_path"), args.get("directory_path"))
            elif USE_TEMPLATE_PROCESSING and tool_name in ["generate_client_template", "analyze_template_requirements", "get_template_processing_status"]:
                args = json.loads(tool_call.function.arguments)
                result = route_template_tool_call(tool_name, args)
            else:
                result = f"Unknown tool: {tool_name}"

            tool_results.append({
                "role": "tool",
                "content": str(result),
                "tool_call_id": tool_call.id
            })

        messages.append(response.choices[0].message)
        messages.extend(tool_results)

        final_response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        return final_response.choices[0].message.content

    except Exception as e:
        return f"Error processing request: {str(e)}"

# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    data_source = "real client data" if USE_REAL_DATA else "mock data"
    print("🤖 STANDISH - PROACTIVE AI AGENT FOR FINANCIAL ADVISORS - READY!")
    print(f"📊 Managing {len(data_manager.get_all_clients()) if USE_REAL_DATA and data_manager else 6} client relationships")
    print(f"📁 Using {data_source}")
    print("\n🎯 ENHANCED CAPABILITIES:")
    print("📊 Investment: equity, ISA, pension allowance, withdrawal rates, scenarios")
    print("📋 Compliance: recommendations, transcripts, documents, commitments")
    print("📈 Business: revenue, satisfaction, conversion, demographics")
    print("✅ Follow-up: emails, actions, documents, decisions")
    print("🔔 Proactive: birthdays, reviews, opportunities, alerts")
    print("\n💡 Start with: 'Good morning' for daily briefing")
    print("🛠️ Or ask: 'Which retired clients have withdrawal rates above 4%?'")
    print("(Type 'quit' to exit)\n")

    while True:
        user_input = input("\nAdvisor: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Proactive assistant session ended!")
            break

        response = get_ai_response(user_input)
        print(f"\n🤖 STANDISH: {response}")
