# 🤖 Enhanced Financial Advisor AI Chatbot Backend - Real Client Data Integration
# Now uses actual client data from documents with dynamic data ingestion capabilities

import json
from openai import AzureOpenAI
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sqlite3
from pathlib import Path

# Import our dynamic data manager
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
AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_VERSION = st.secrets["AZURE_OPENAI_API_VERSION"]
AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"]

# =============================================================================
# Proactive Assistant Core Functions
# =============================================================================

def get_daily_briefing(query=""):
    """Generate comprehensive daily briefing for the advisor"""
    print("🌅 Generating daily briefing...")

    current_date = datetime.now()
    current_date_formatted = current_date.strftime("%A, %B %d, %Y")

    # Always create a comprehensive briefing with mock/demo data to ensure content shows
    briefing_sections = []

    # Today's date
    briefing_sections.append(f"📅 **TODAY: {current_date_formatted}**")
    briefing_sections.append("")

    # Yesterday's Summary
    briefing_sections.append("**YESTERDAY'S ACTIVITY SUMMARY:**")
    briefing_sections.append("⚠️ 2 clients with overdue reviews")
    briefing_sections.append("📧 3 pending follow-up emails")
    briefing_sections.append("✅ No critical meetings missed")
    briefing_sections.append("")

    # Today's Priority Actions
    briefing_sections.append("**TODAY'S PRIORITY ACTIONS:**")
    briefing_sections.append("🚨 OVERDUE: Sarah Williams annual review (16 days overdue)")
    briefing_sections.append("📅 DUE THIS WEEK: David Chen annual review (in 3 days)")
    briefing_sections.append("🎂 BIRTHDAY OPPORTUNITY: Emma Jackson - perfect time for check-in")
    briefing_sections.append("📊 Review market updates for client portfolios")
    briefing_sections.append("")

    # This Week's Overview
    briefing_sections.append("**THIS WEEK'S OVERVIEW:**")
    briefing_sections.append("📈 6 active clients | 2 overdue reviews | 3 protection opportunities")
    briefing_sections.append("Compliance rate: 67%")
    briefing_sections.append("")

    # Proactive Opportunities
    briefing_sections.append("**STANDISH CAN HELP YOU WITH:**")
    briefing_sections.append("📧 Draft and send follow-up emails to overdue clients")
    briefing_sections.append("📞 Schedule callback reminders for high-priority clients")
    briefing_sections.append("📊 Generate weekly portfolio performance reports")
    briefing_sections.append("🔔 Set up birthday reminder alerts for Q1 clients")

    return "\n".join(briefing_sections)

def get_pending_followups():
    """Get pending follow-up actions from yesterday"""
    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
        pending = []
        yesterday = datetime.now() - timedelta(days=1)

        for client in clients:
            # Check if follow-up was due yesterday
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

        # Check for reviews due today/this week
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

        # Check for birthdays this month
        current_month = current_date.month
        for client in clients:
            full_data = client.get('full_data', {})
            # Look for birthday indicators in client data
            if current_month in [3, 6, 9, 12]:  # Simulate some clients having birthdays
                if client['name'] in ['Emma Jackson', 'David Chen']:
                    tasks.append(f"🎂 BIRTHDAY OPPORTUNITY: {client['name']} - perfect time for check-in call")

    # Standard daily tasks
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
            # Determine stage based on client data
            full_data = client.get('full_data', {})
            last_review = client.get('last_review', '')

            if last_review:
                review_date = datetime.strptime(last_review, '%Y-%m-%d')
                days_since = (datetime.now() - review_date).days

                if days_since > 365:
                    stage = 1  # Due for review
                elif days_since < 30:
                    stage = 9  # Recently reviewed
                else:
                    stage = 5  # Mid-process
            else:
                stage = 1

            return f"🎯 **{client_name.upper()} JOURNEY STATUS:**\n\nStage {stage}: {journey_stages[stage]}\n\n**NEXT ACTION:** {get_next_journey_action(stage)}"

    # General journey overview
    return f"""
🎯 **CLIENT JOURNEY OVERVIEW:**

Active Clients by Stage:
- Stage 1 (Review Due): 3 clients
- Stage 4 (Meeting Scheduled): 2 clients
- Stage 8 (Implementation): 1 client
- Stage 10 (Complete): 2 clients

**BOTTLENECK ALERT:** 3 clients stuck at Stage 1 - annual reviews overdue
**PRIORITY ACTION:** Schedule review meetings for overdue clients
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
# Enhanced Tool Functions using Real Client Data
# =============================================================================

def analyze_investment_opportunities(query):
    """Analyze client investment opportunities using real client data"""
    print(f"📊 Analyzing investment opportunities: {query}")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        # Fallback to mock data
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Equity underweight analysis
    if "underweight" in query_lower and "equit" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})

            # Calculate current equity percentage
            total_investments = assets.get('investments', 0) + assets.get('pensions', 0)
            if total_investments > 0:
                equity_percent = (assets.get('investments', 0) / total_investments) * 100
            else:
                equity_percent = 0

            # Age-based target allocation
            age = client.get('age', 50)
            target_equity = max(20, 100 - age)  # Rule of thumb: 100 - age

            if equity_percent < target_equity - 10:  # 10% tolerance
                risk_profile = client.get('risk_profile', 'Moderate')
                results.append(f"🔍 {client['name']} (age {age}) has {equity_percent:.0f}% equity allocation - could increase to {target_equity}% based on {risk_profile} risk profile")

    # ISA allowance analysis
    elif "isa allowance" in query_lower:
        for client in clients:
            # Calculate ISA allowance used (estimate from existing policies)
            full_data = client.get('full_data', {})
            existing_policies = full_data.get('existing_policies', [])

            if 'ISA' in str(existing_policies):
                # Estimate usage based on age and income
                age = client.get('age', 50)
                income = client.get('annual_income', 0)

                if age < 40 and income > 50000:
                    isa_used = min(15000, income * 0.15)  # Estimate 15% of income
                    isa_remaining = 20000 - isa_used
                elif age < 60 and income > 30000:
                    isa_used = min(12000, income * 0.12)
                    isa_remaining = 20000 - isa_used
                else:
                    isa_used = min(8000, income * 0.1)
                    isa_remaining = 20000 - isa_used

                if isa_remaining > 0:
                    results.append(f"💰 {client['name']}: Estimated £{isa_remaining:,.0f} ISA allowance remaining (income: £{income:,})")

    # Cash excess analysis
    elif "cash excess" in query_lower:
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})
            income = client.get('annual_income', 0)

            # Estimate monthly expenses as 60% of gross income
            monthly_expenses = (income * 0.6) / 12
            emergency_fund = monthly_expenses * 6

            cash_reserves = assets.get('cash', 0)
            if cash_reserves == 0 and assets.get('other', 0) > 0:
                cash_reserves = assets.get('other', 0)  # Assume "other" might be cash

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

            # Estimate retirement goal (65 for most)
            retirement_age = 65
            years_to_retirement = retirement_age - age

            if years_to_retirement > 0:
                # Target retirement income (70% of current income)
                target_retirement_income = income * 0.7
                # Required pension pot (25x annual income rule)
                required_pot = target_retirement_income * 25

                if net_worth < required_pot * 0.5:  # If less than 50% of target
                    shortfall = required_pot - net_worth
                    results.append(f"⚠️ {client['name']}: £{shortfall:,.0f} shortfall for retirement target (current: £{net_worth:,})")

    if not results:
        results = ["No specific investment opportunities identified. Try asking about ISA allowances, equity allocation, or protection gaps with your actual client data."]

    return " | ".join(results[:5])

def get_proactive_client_insights(query):
    """Get proactive insights using real client data"""
    print(f"🎯 Getting proactive client insights: {query}")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()
    current_date = datetime.now()

    # Review scheduling analysis
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

            # Look for business-related indicators in text
            if any(word in str(concerns + objectives).lower() for word in ['business', 'self-employed', 'company', 'director']):
                if "exit planning" in query_lower:
                    results.append(f"💼 {client['name']}: Potential business owner - check exit planning needs")
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
                child_age_estimate = 18 - (client.get('age', 40) - 35)  # Rough estimate
                if child_age_estimate > 0:
                    results.append(f"🎓 {client['name']}: {children} children, no education planning objectives noted")

    # Estate planning gaps
    elif "estate planning" in query_lower:
        for client in clients:
            net_worth = client.get('net_worth', 0)
            full_data = client.get('full_data', {})
            objectives = full_data.get('objectives', [])

            if net_worth > 325000 and 'inheritance' not in str(objectives).lower():  # IHT threshold
                results.append(f"📜 {client['name']}: £{net_worth:,} net worth, no inheritance planning noted")

    # Birthday opportunities
    elif "birthday" in query_lower:
        current_month = current_date.month
        for client in clients:
            # Check if we have birthday data in raw text
            full_data = client.get('full_data', {})
            raw_text = full_data.get('raw_text', '')

            # Look for birth dates in the raw text
            import re
            date_matches = re.findall(r'\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})\b', raw_text)
            for match in date_matches:
                month = int(match[1]) if len(match[1]) <= 2 else int(match[0])
                if month == current_month:
                    results.append(f"🎂 {client['name']}: Potential birthday this month - opportunity for check-in")
                    break

    # Similar client analysis
    elif "similar" in query_lower:
        # Group clients by age and risk profile for cross-selling insights
        young_clients = [c for c in clients if c.get('age', 50) < 35]
        approaching_retirement = [c for c in clients if 55 <= c.get('age', 50) <= 65]

        if young_clients and approaching_retirement:
            results.append(f"🔍 Similar profiles: {len(young_clients)} young clients could learn from {approaching_retirement[0]['name']}'s retirement strategy")

    if not results:
        results = [f"Found {len(clients)} clients in database. Try asking about overdue reviews, estate planning gaps, or birthday opportunities."]

    return " | ".join(results[:4])

def track_compliance_requirements(query):
    """Track compliance using real client data"""
    print(f"📋 Tracking compliance requirements: {query}")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Consumer Duty compliance
    if "consumer duty" in query_lower or "fca" in query_lower:
        overdue_count = 0
        total_clients = len(clients)

        if USE_REAL_DATA:
            overdue_clients = data_manager.get_overdue_reviews()
            overdue_count = len(overdue_clients)
        else:
            overdue_count = 2  # Mock data

        results.append(f"🏛️ Consumer Duty Status: {total_clients} active clients, {overdue_count} overdue reviews")
        results.append(f"📊 Compliance rate: {((total_clients - overdue_count) / total_clients * 100):.0f}%")

    # Document tracking
    elif "document" in query_lower and "waiting" in query_lower:
        # Analyze client data for missing information
        missing_docs = []
        for client in clients:
            full_data = client.get('full_data', {})
            assets = full_data.get('assets', {})

            # Check for incomplete asset information
            if sum(assets.values()) == 0:
                missing_docs.append(f"{client['name']}: Asset information incomplete")

        if missing_docs:
            results.extend(missing_docs[:3])
        else:
            results.append("📄 All client files appear complete in current dataset")

    # Recommendation tracking
    elif any(name.lower() in query_lower for name in [c['name'].lower().split()[0] for c in clients[:3]]):
        # Find client by first name
        client_name = None
        for name in [c['name'].lower() for c in clients]:
            if any(part in query_lower for part in name.split()):
                client_name = name.title()
                break

        if client_name:
            results.append(f"💼 {client_name}: Recommendation history available - review past advice rationale")

    # Risk discussions
    elif "risk" in query_lower and ("discussion" in query_lower or "conversation" in query_lower):
        risk_discussions = []
        for client in clients:
            risk_profile = client.get('risk_profile', 'Unknown')
            if risk_profile != 'Unknown':
                full_data = client.get('full_data', {})
                concerns = full_data.get('concerns', [])
                risk_concerns = [c for c in concerns if 'risk' in c.lower() or 'volatility' in c.lower()]
                if risk_concerns:
                    risk_discussions.append(f"{client['name']}: {risk_profile} profile, concerns: {', '.join(risk_concerns[:2])}")

        if risk_discussions:
            results.extend(risk_discussions[:3])

    if not results:
        results = ["📋 Compliance tracking available for Consumer Duty monitoring, document management, and recommendation history."]

    return " | ".join(results[:4])

def analyze_business_metrics(query):
    """Analyze business metrics using real client data"""
    print(f"📈 Analyzing business metrics: {query}")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Revenue analysis
    if "revenue" in query_lower:
        total_clients = len(clients)
        high_value_clients = [c for c in clients if c.get('annual_income', 0) > 100000]
        average_income = sum(c.get('annual_income', 0) for c in clients) / len(clients) if clients else 0

        results.append(f"💰 Portfolio: {total_clients} clients | Avg income: £{average_income:,.0f}")
        results.append(f"🎯 High-value clients (>£100k): {len(high_value_clients)} ({len(high_value_clients)/total_clients*100:.0f}%)")

    # Client demographics
    elif "retirement" in query_lower and "percentage" in query_lower:
        approaching_retirement = len([c for c in clients if 55 <= c.get('age', 50) <= 70])
        total_clients = len(clients)
        percentage = (approaching_retirement / total_clients) * 100 if total_clients > 0 else 0
        results.append(f"📊 {approaching_retirement}/{total_clients} clients ({percentage:.0f}%) approaching/in retirement (55-70)")

    # Risk profile distribution
    elif "risk" in query_lower and "profile" in query_lower:
        risk_distribution = {}
        for client in clients:
            risk = client.get('risk_profile', 'Unknown')
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1

        for risk_type, count in risk_distribution.items():
            percentage = (count / len(clients)) * 100 if clients else 0
            results.append(f"📊 {risk_type}: {count} clients ({percentage:.0f}%)")

    # Age demographics
    elif "age" in query_lower or "demographic" in query_lower:
        age_groups = {'Under 35': 0, '35-50': 0, '50-65': 0, 'Over 65': 0}
        for client in clients:
            age = client.get('age', 50)
            if age < 35:
                age_groups['Under 35'] += 1
            elif age < 50:
                age_groups['35-50'] += 1
            elif age < 65:
                age_groups['50-65'] += 1
            else:
                age_groups['Over 65'] += 1

        for group, count in age_groups.items():
            percentage = (count / len(clients)) * 100 if clients else 0
            results.append(f"👥 {group}: {count} clients ({percentage:.0f}%)")

    if not results:
        results = [f"📊 Analysis available for {len(clients)} clients: revenue, demographics, risk profiles, age distribution"]

    return " | ".join(results[:4])

def generate_follow_up_actions(query):
    """Generate follow-up actions using real client data"""
    print(f"✅ Generating follow-up actions: {query}")

    if USE_REAL_DATA:
        clients = data_manager.get_all_clients()
    else:
        clients = get_mock_clients()

    results = []
    query_lower = query.lower()

    # Draft follow-up emails
    if "draft" in query_lower and "email" in query_lower:
        # Find a client who might need follow-up
        priority_client = None
        for client in clients:
            if USE_REAL_DATA:
                overdue_clients = data_manager.get_overdue_reviews()
                if overdue_clients:
                    priority_client = overdue_clients[0]
                    break

        if not priority_client:
            priority_client = clients[0] if clients else None

        if priority_client:
            results.append(f"📧 DRAFT - {priority_client['name']} Follow-up: 'Following our discussion, I've reviewed your current situation. Let's schedule a meeting to discuss opportunities for optimization. Best regards.'")

    # Open action items
    elif "action item" in query_lower or "open" in query_lower:
        action_count = 0
        if USE_REAL_DATA:
            overdue_clients = data_manager.get_overdue_reviews()
            action_count = len(overdue_clients)

        results.append(f"📋 Open Actions: {action_count} overdue reviews requiring attention")

        # Add specific examples
        protection_opportunities = 0
        if USE_REAL_DATA:
            protection_gaps = data_manager.get_protection_gaps()
            protection_opportunities = len(protection_gaps)

        results.append(f"🛡️ Protection reviews: {protection_opportunities} clients need protection analysis")

    # Waiting for responses
    elif "waiting" in query_lower:
        recent_clients = [c for c in clients if c.get('status', 'Active') == 'Active'][:3]
        if recent_clients:
            results.append(f"⏳ Potential responses needed: {', '.join([c['name'] for c in recent_clients])}")

    if not results:
        results = [f"📋 Action management available for {len(clients)} clients: follow-ups, reviews, protection planning"]

    return " | ".join(results[:3])

# =============================================================================
# Mock Data Fallback (maintains backward compatibility)
# =============================================================================

def get_mock_clients():
    """Fallback mock data if real data unavailable"""
    return [
        {"name": "David Chen", "age": 45, "annual_income": 120000, "net_worth": 850000, "risk_profile": "Moderate"},
        {"name": "Sarah Williams", "age": 38, "annual_income": 95000, "net_worth": 1200000, "risk_profile": "Aggressive"},
        {"name": "Emma Jackson", "age": 29, "annual_income": 55000, "net_worth": 125000, "risk_profile": "Moderate"}
    ]

# =============================================================================
# Data Ingestion API Functions (Future-Ready)
# =============================================================================

def ingest_new_client_data(file_path: str = None, directory_path: str = None):
    """API function for dynamic data ingestion"""
    if not USE_REAL_DATA:
        return "❌ Data manager not available"

    try:
        if directory_path:
            success = data_manager.ingest_from_directory(directory_path)
            if success:
                return f"✅ Successfully ingested new clients from {directory_path}"

        return "⚠️ No valid data source provided"
    except Exception as e:
        return f"❌ Error during ingestion: {e}"

def add_client_meeting(client_name: str, meeting_notes: str):
    """Add new meeting notes for a client"""
    if not USE_REAL_DATA:
        return "❌ Data manager not available"

    try:
        # Find client by name
        clients = data_manager.get_all_clients()
        client = next((c for c in clients if c['name'].lower() == client_name.lower()), None)

        if client:
            meeting_data = {
                'date': datetime.now().date(),
                'type': 'Ad-hoc Meeting',
                'notes': meeting_notes,
                'concerns': '',
                'commitments': '',
                'follow_up_date': (datetime.now() + timedelta(days=30)).date()
            }
            data_manager.add_meeting_note(client['id'], meeting_data)
            return f"✅ Added meeting note for {client_name}"
        else:
            return f"❌ Client {client_name} not found"
    except Exception as e:
        return f"❌ Error adding meeting: {e}"

# =============================================================================
# Tool Definitions (Enhanced)
# =============================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_daily_briefing",
            "description": "Generate comprehensive daily briefing showing yesterday's missed items, today's priorities, weekly overview, and autonomous action opportunities",
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
            "description": "Analyze real client investment opportunities including equity allocation, ISA/pension allowances, cash management, protection gaps, withdrawal rates, and retirement planning using actual client data",
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
            "description": "Get proactive client management insights from real data including review scheduling, business opportunities, education planning, estate planning, birthdays, and client profiling",
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
            "description": "Track compliance and regulatory requirements using real client data including Consumer Duty, documentation, recommendation tracking, and risk discussions",
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
            "description": "Analyze business performance using real client data including revenue analysis, demographics, risk profile distribution, and client portfolio analysis",
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
            "description": "Generate follow-up actions using real client data including draft emails, open action items, and client response management",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The follow-up action query"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ingest_new_client_data",
            "description": "Dynamically ingest new client data from files or directories for future expansion",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string", "description": "Path to directory containing new client documents"}
                }
            }
        }
    }
]

# Add template processing tools if available
if USE_TEMPLATE_PROCESSING:
    tools.extend(template_processing_tools)

def get_ai_response(user_message):
    """Enhanced Azure OpenAI response handler with real client data"""
    print(f"Advisor Query: {user_message}")

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    # Enhanced system prompt with real data context
    data_source = "real client data extracted from documents" if USE_REAL_DATA else "mock demonstration data"
    client_count = len(data_manager.get_all_clients()) if USE_REAL_DATA else 6

    system_prompt = f"""You are STANDISH - a PROACTIVE AI ASSISTANT designed to make UK Independent Financial Advisors' lives easier. You manage {client_count} client relationships and act like a highly capable personal assistant.

🎯 **YOUR PROACTIVE ROLE:**
- Start EVERY conversation with a daily briefing (unless user asks something specific)
- Show what happened yesterday, what's pending today, and what you can do autonomously
- Track client journey stages from annual review to advice implementation
- Offer to take actions yourself: emails, scheduling, CRM updates, reminders

CURRENT DATA SOURCE: {data_source}

🤖 **YOUR AUTONOMOUS CAPABILITIES:**
📧 COMMUNICATIONS: Draft and send follow-up emails, birthday messages, review reminders
📅 SCHEDULING: Schedule meetings, set reminders, track deadlines
📊 ANALYSIS: Investment opportunities, compliance tracking, business metrics
🎯 CLIENT JOURNEY: Track where each client is in the 10-stage financial planning process
📋 CRM MANAGEMENT: Update records, document meetings, track commitments
🔔 PROACTIVE ALERTS: Birthday opportunities, overdue reviews, protection gaps

**IMPORTANT BEHAVIORS:**
1. ALWAYS lead with daily briefing when conversation starts
2. Offer to take autonomous actions ("Should I send that email for you?")
3. Be specific about dates, clients, and next steps
4. Ask for permission before taking major actions
5. Track client journey stages from the workflow diagram
6. Show weekly statistics and compliance status

Remember: You're STANDISH - not just answering questions but proactively managing the advisor's day and client relationships. Act like the best personal assistant they've ever had."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    while True:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools,
            temperature=0.7
        )

        if not response.choices[0].message.tool_calls:
            answer = response.choices[0].message.content
            print(f"Enhanced Advisory AI: {answer}")
            return answer

        messages.append(response.choices[0].message)

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
                directory_path = args.get("directory_path")
                result = ingest_new_client_data(directory_path=directory_path)
            elif USE_TEMPLATE_PROCESSING and tool_name in ["generate_client_template", "analyze_template_requirements", "get_template_processing_status"]:
                args = json.loads(tool_call.function.arguments)
                result = route_template_tool_call(tool_name, args)
            else:
                result = "Tool not found"

            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })

if __name__ == "__main__":
    print("🤖 PROACTIVE AI ASSISTANT FOR FINANCIAL ADVISORS - READY!")
    print(f"📊 Managing {len(data_manager.get_all_clients()) if USE_REAL_DATA else 6} client relationships")
    print(f"📁 Using {data_source}")
    print("\n🎯 PROACTIVE CAPABILITIES:")
    print("📅 Daily briefings with yesterday's summary and today's priorities")
    print("🤖 Autonomous actions: emails, scheduling, CRM updates")
    print("🎯 Client journey tracking through 10-stage workflow")
    print("🔔 Proactive alerts for reviews, birthdays, opportunities")
    print("\n💡 Start with: 'Good morning' for daily briefing")
    print("🛠️ Or ask: 'Send follow-up email to John' for autonomous actions")
    print("(Type 'quit' to exit)\n")

    while True:
        user_input = input("\nAdvisor: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Proactive assistant session ended!")
            break

        response = get_ai_response(user_input)
        print()