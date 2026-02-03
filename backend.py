# 🤖 Financial Advisor AI Chatbot Backend - AdvisoryAI Hack-to-Hire Challenge
# Comprehensive proactive chatbot for UK Financial Advisors

import json
from openai import AzureOpenAI
import streamlit as st
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Any
import random

# =============================================================================
# Azure OpenAI Configuration
# =============================================================================
AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_VERSION = st.secrets["AZURE_OPENAI_API_VERSION"]
AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"]

# =============================================================================
# Mock Data - Realistic Financial Advisor Scenarios
# =============================================================================

class MockDataGenerator:
    def __init__(self):
        self.clients = self._generate_client_data()
        self.meetings = self._generate_meeting_data()
        self.recommendations = self._generate_recommendations()
        self.compliance_items = self._generate_compliance_data()

    def _generate_client_data(self):
        """Generate realistic client profiles"""
        return [
            {
                "id": 1, "name": "David Chen", "age": 45, "status": "Active",
                "last_review": "2024-01-15", "risk_profile": "Moderate",
                "net_worth": 850000, "annual_income": 120000,
                "retirement_goal": 2035, "children": 2, "education_planning": True,
                "isa_allowance_used": 15000, "isa_allowance_remaining": 5000,
                "annual_allowance_used": 35000, "annual_allowance_remaining": 25000,
                "cash_reserves": 45000, "monthly_expenses": 4500,
                "withdrawal_rate": 0, "portfolio_equity_percent": 65,
                "protection_cover": "Life + Critical Illness", "estate_planning": False,
                "birthday": "1979-03-15", "business_owner": False,
                "last_contact": "2024-11-20", "concerns": ["market volatility", "retirement timing"],
                "life_events": ["daughter starting university in 2026"],
                "revenue_generated": 8500, "service_time_hours": 12
            },
            {
                "id": 2, "name": "Sarah Williams", "age": 38, "status": "Active",
                "last_review": "2023-08-10", "risk_profile": "Aggressive",
                "net_worth": 1200000, "annual_income": 95000,
                "retirement_goal": 2040, "children": 1, "education_planning": False,
                "isa_allowance_used": 20000, "isa_allowance_remaining": 0,
                "annual_allowance_used": 40000, "annual_allowance_remaining": 20000,
                "cash_reserves": 25000, "monthly_expenses": 3800,
                "withdrawal_rate": 0, "portfolio_equity_percent": 45,
                "protection_cover": "None", "estate_planning": True,
                "birthday": "1986-12-08", "business_owner": True,
                "last_contact": "2023-12-01", "concerns": ["business exit planning"],
                "life_events": ["considering second child", "business expansion"],
                "revenue_generated": 12000, "service_time_hours": 8
            },
            {
                "id": 3, "name": "Robert Thompson", "age": 62, "status": "Active",
                "last_review": "2024-10-05", "risk_profile": "Conservative",
                "net_worth": 1800000, "annual_income": 75000,
                "retirement_goal": 2026, "children": 3, "education_planning": False,
                "isa_allowance_used": 20000, "isa_allowance_remaining": 0,
                "annual_allowance_used": 10000, "annual_allowance_remaining": 50000,
                "cash_reserves": 180000, "monthly_expenses": 5200,
                "withdrawal_rate": 5.2, "portfolio_equity_percent": 30,
                "protection_cover": "Life Insurance", "estate_planning": False,
                "birthday": "1962-09-22", "business_owner": False,
                "last_contact": "2024-11-15", "concerns": ["sequence of returns risk"],
                "life_events": ["retirement party next year", "daughter's wedding in March"],
                "revenue_generated": 15000, "service_time_hours": 6
            },
            {
                "id": 4, "name": "Emma Jackson", "age": 29, "status": "Prospect",
                "last_review": "Never", "risk_profile": "Moderate",
                "net_worth": 125000, "annual_income": 55000,
                "retirement_goal": 2060, "children": 0, "education_planning": False,
                "isa_allowance_used": 5000, "isa_allowance_remaining": 15000,
                "annual_allowance_used": 8000, "annual_allowance_remaining": 52000,
                "cash_reserves": 35000, "monthly_expenses": 2800,
                "withdrawal_rate": 0, "portfolio_equity_percent": 80,
                "protection_cover": "None", "estate_planning": False,
                "birthday": "1995-06-12", "business_owner": False,
                "last_contact": "2024-11-28", "concerns": ["first time investing"],
                "life_events": ["recent promotion", "buying first home"],
                "revenue_generated": 0, "service_time_hours": 3
            },
            {
                "id": 5, "name": "Michael Gurung", "age": 52, "status": "Active",
                "last_review": "2024-03-20", "risk_profile": "Moderate",
                "net_worth": 950000, "annual_income": 110000,
                "retirement_goal": 2030, "children": 2, "education_planning": True,
                "isa_allowance_used": 18000, "isa_allowance_remaining": 2000,
                "annual_allowance_used": 45000, "annual_allowance_remaining": 15000,
                "cash_reserves": 85000, "monthly_expenses": 5800,
                "withdrawal_rate": 0, "portfolio_equity_percent": 55,
                "protection_cover": "Life + Income Protection", "estate_planning": True,
                "birthday": "1972-11-30", "business_owner": True,
                "last_contact": "2024-10-15", "concerns": ["inheritance tax", "long-term care"],
                "life_events": ["son starting university", "considering early retirement"],
                "revenue_generated": 11500, "service_time_hours": 14
            },
            {
                "id": 6, "name": "Lisa Patel", "age": 41, "status": "Active",
                "last_review": "2023-05-15", "risk_profile": "Moderate",
                "net_worth": 720000, "annual_income": 88000,
                "retirement_goal": 2038, "children": 3, "education_planning": True,
                "isa_allowance_used": 12000, "isa_allowance_remaining": 8000,
                "annual_allowance_used": 30000, "annual_allowance_remaining": 30000,
                "cash_reserves": 95000, "monthly_expenses": 4200,
                "withdrawal_rate": 0, "portfolio_equity_percent": 58,
                "protection_cover": "Life Insurance", "estate_planning": False,
                "birthday": "1983-01-25", "business_owner": False,
                "last_contact": "2023-09-10", "concerns": ["education costs", "mortgage"],
                "life_events": ["twins starting secondary school", "new grandchild"],
                "revenue_generated": 7200, "service_time_hours": 16
            }
        ]

    def _generate_meeting_data(self):
        """Generate realistic meeting notes and transcripts"""
        return [
            {
                "client_id": 1, "date": "2024-11-20", "type": "Review",
                "notes": "Discussed market volatility concerns. David worried about recent equity performance. Recommended rebalancing to 60/40 allocation. Action: Send portfolio analysis by Friday.",
                "concerns_raised": ["market volatility", "portfolio performance"],
                "commitments_made": ["Send portfolio analysis by Friday", "Review protection needs in Q1 2025"],
                "follow_up_date": "2024-11-27"
            },
            {
                "client_id": 3, "date": "2024-10-05", "type": "Retirement Planning",
                "notes": "Robert confirmed retirement in 2026. Discussed withdrawal strategy and sequence of returns risk. Recommended reducing equity allocation to 25%. Mentioned daughter's wedding costs.",
                "concerns_raised": ["sequence of returns risk", "withdrawal sustainability"],
                "commitments_made": ["Prepare retirement cashflow model", "Review estate planning needs"],
                "follow_up_date": "2024-12-15"
            }
        ]

    def _generate_recommendations(self):
        """Generate recommendation history"""
        return [
            {
                "client_id": 1, "date": "2024-01-15", "type": "Portfolio Rebalancing",
                "recommendation": "Reduce equity allocation from 75% to 65% due to approaching retirement timeline",
                "rationale": "Client approaching retirement in 10 years, need to reduce sequence of returns risk while maintaining growth potential",
                "status": "Implemented"
            },
            {
                "client_id": 2, "date": "2023-08-10", "type": "Platform Recommendation",
                "recommendation": "Transfer ISA to Platform X for lower fees and better fund selection",
                "rationale": "Current platform charging 1.2% annual fee vs 0.45% on Platform X, better ESG fund selection aligns with client values",
                "status": "Pending"
            }
        ]

    def _generate_compliance_data(self):
        """Generate compliance tracking items"""
        return [
            {"client_id": 1, "type": "Annual Review", "due_date": "2025-01-15", "status": "Due Soon"},
            {"client_id": 2, "type": "Annual Review", "due_date": "2024-08-10", "status": "Overdue"},
            {"client_id": 3, "type": "Suitability Review", "due_date": "2025-10-05", "status": "Scheduled"},
            {"client_id": 6, "type": "Annual Review", "due_date": "2024-05-15", "status": "Overdue"},
            {"type": "Consumer Duty Documentation", "due_date": "2024-12-31", "status": "In Progress"},
            {"type": "CASS Reconciliation", "due_date": "2024-12-15", "status": "Pending"}
        ]

# Initialize mock data
mock_data = MockDataGenerator()

# =============================================================================
# Financial Advisor Tool Functions
# =============================================================================

def analyze_investment_opportunities(query):
    """Analyze client investment opportunities and risk profiles"""
    print(f"📊 Analyzing investment opportunities: {query}")

    results = []
    query_lower = query.lower()

    # Equity underweight analysis
    if "underweight" in query_lower and "equit" in query_lower:
        for client in mock_data.clients:
            if client["age"] < 50 and client["portfolio_equity_percent"] < 70:
                results.append(f"🔍 {client['name']} (age {client['age']}) has only {client['portfolio_equity_percent']}% equity allocation - could increase to 70-80% given moderate risk profile and long time horizon")
            elif client["age"] < 60 and client["portfolio_equity_percent"] < 50:
                results.append(f"⚠️ {client['name']} (age {client['age']}) significantly underweight equities at {client['portfolio_equity_percent']}% - recommend 60% minimum")

    # ISA allowance analysis
    elif "isa allowance" in query_lower:
        for client in mock_data.clients:
            if client["isa_allowance_remaining"] > 0:
                results.append(f"💰 {client['name']}: £{client['isa_allowance_remaining']:,} ISA allowance remaining (used £{client['isa_allowance_used']:,})")

    # Annual allowance analysis
    elif "annual allowance" in query_lower:
        for client in mock_data.clients:
            if client["annual_allowance_remaining"] > 10000:
                results.append(f"🏦 {client['name']}: £{client['annual_allowance_remaining']:,} annual allowance available - consider additional pension contributions")

    # Cash excess analysis
    elif "cash excess" in query_lower:
        for client in mock_data.clients:
            emergency_fund = client["monthly_expenses"] * 6
            if client["cash_reserves"] > emergency_fund + 10000:
                excess = client["cash_reserves"] - emergency_fund
                results.append(f"💵 {client['name']}: £{excess:,} excess cash above 6-month emergency fund (total: £{client['cash_reserves']:,})")

    # Retirement trajectory analysis
    elif "retirement" in query_lower and ("trajectory" in query_lower or "goal" in query_lower):
        for client in mock_data.clients:
            years_to_retirement = client["retirement_goal"] - 2024
            if years_to_retirement > 0:
                required_growth = ((client["annual_income"] * 0.7) - (client["net_worth"] * 0.04)) / client["net_worth"]
                if required_growth > 0.06:
                    results.append(f"⚠️ {client['name']}: Current trajectory insufficient for retirement goal - needs {required_growth:.1%} annual growth")

    # Protection gaps
    elif "protection gap" in query_lower:
        for client in mock_data.clients:
            if client["children"] > 0 and client["protection_cover"] == "None":
                results.append(f"🛡️ {client['name']}: No protection cover despite having {client['children']} children - recommend life & income protection")
            elif "Life" not in client["protection_cover"] and client["annual_income"] > 50000:
                results.append(f"🔒 {client['name']}: Inadequate protection cover for £{client['annual_income']:,} income")

    # High withdrawal rates
    elif "withdrawal rate" in query_lower:
        for client in mock_data.clients:
            if client["withdrawal_rate"] > 4.0:
                results.append(f"📉 {client['name']}: {client['withdrawal_rate']}% withdrawal rate exceeds safe withdrawal guidelines (4% max)")

    if not results:
        results = ["No specific investment opportunities identified based on current query. Try asking about ISA allowances, equity allocation, or protection gaps."]

    return " | ".join(results[:5])  # Limit to 5 results

def get_proactive_client_insights(query):
    """Get proactive insights for client management"""
    print(f"🎯 Getting proactive client insights: {query}")

    results = []
    query_lower = query.lower()
    current_date = datetime.now()

    # Review scheduling
    if "review" in query_lower and "month" in query_lower:
        overdue_clients = []
        for client in mock_data.clients:
            if client["last_review"] != "Never":
                last_review = datetime.strptime(client["last_review"], "%Y-%m-%d")
                months_since = (current_date - last_review).days / 30
                if months_since > 12:
                    overdue_clients.append(f"{client['name']} ({months_since:.0f} months overdue)")
        if overdue_clients:
            results.append(f"📅 Overdue reviews: {', '.join(overdue_clients)}")

    # Business owner opportunities
    elif "business owner" in query_lower:
        business_clients = [c for c in mock_data.clients if c["business_owner"]]
        for client in business_clients:
            if "R&D tax" in query:
                results.append(f"🏢 {client['name']}: Business owner - check R&D tax credit eligibility")
            elif "exit planning" in query_lower:
                results.append(f"💼 {client['name']}: Business owner without exit planning discussed")

    # Education planning
    elif "university" in query_lower or "education" in query_lower:
        for client in mock_data.clients:
            if client["children"] > 0 and not client["education_planning"]:
                child_age_estimate = 18 - (2024 - client["age"] + 20)  # Rough estimate
                if child_age_estimate > 0:
                    results.append(f"🎓 {client['name']}: {client['children']} children, no education planning in place")

    # Estate planning gaps
    elif "estate planning" in query_lower:
        for client in mock_data.clients:
            if client["net_worth"] > 500000 and not client["estate_planning"]:
                results.append(f"📜 {client['name']}: £{client['net_worth']:,} net worth, no estate planning in place")

    # Birthday opportunities
    elif "birthday" in query_lower:
        for client in mock_data.clients:
            birth_month = client["birthday"].split("-")[1]
            current_month = current_date.strftime("%m")
            if birth_month == current_month:
                results.append(f"🎂 {client['name']}: Birthday this month - opportunity for check-in call")

    # Similar client profiles
    elif "similar" in query_lower:
        # Find clients with similar characteristics for cross-selling
        results.append("🔍 Similar profile analysis: Emma Jackson (29, first-time investor) similar to David Chen's early career phase")
        results.append("💡 Robert Thompson's retirement strategy could benefit Michael Gurung (early retirement consideration)")

    if not results:
        results = ["Consider checking for overdue reviews, business owner opportunities, or estate planning gaps."]

    return " | ".join(results[:4])

def track_compliance_requirements(query):
    """Track compliance and regulatory requirements"""
    print(f"📋 Tracking compliance requirements: {query}")

    results = []
    query_lower = query.lower()

    # FCA Consumer Duty
    if "consumer duty" in query_lower or "fca" in query_lower:
        results.append("🏛️ Consumer Duty Status: 4 clients requiring value demonstration documentation")
        results.append("📊 Annual reviews: 2 overdue (Sarah Williams, Lisa Patel)")
        results.append("✅ Ongoing monitoring: Portfolio performance tracking in place for all active clients")

    # Documentation requests
    elif "document" in query_lower and "waiting" in query_lower:
        results.append("📄 Outstanding documents: Emma Jackson (bank statements), Sarah Williams (business accounts)")
        results.append("⏰ Longest outstanding: 45 days (Sarah Williams - business valuation)")

    # Recommendation tracking by client
    elif any(name.lower() in query_lower for name in ["david chen", "chen"]):
        client_recs = [r for r in mock_data.recommendations if r["client_id"] == 1]
        for rec in client_recs:
            results.append(f"💼 {rec['date']}: {rec['recommendation']} | Rationale: {rec['rationale']}")

    # Risk discussions
    elif "risk" in query_lower and ("discussion" in query_lower or "conversation" in query_lower):
        results.append("🎯 Williams family risk discussion (2023-08): 'Comfortable with volatility for long-term growth, prefer ESG investments'")
        results.append("⚠️ Robert Thompson risk review (2024-10): 'Concerned about sequence of returns, prefer conservative approach near retirement'")

    # Platform recommendations
    elif "platform" in query_lower:
        platform_recs = [r for r in mock_data.recommendations if "Platform" in r["recommendation"]]
        for rec in platform_recs:
            results.append(f"🖥️ {rec['date']}: Recommended Platform X for client {rec['client_id']} - {rec['rationale']}")

    # Market volatility concerns
    elif "volatility" in query_lower:
        concerned_clients = [c for c in mock_data.clients if "market volatility" in c["concerns"]]
        for client in concerned_clients:
            results.append(f"📈 {client['name']}: Expressed market volatility concerns in recent meetings")

    if not results:
        results = [f"No specific compliance items found for query. Available: Consumer Duty tracking, document requests, recommendation history."]

    return " | ".join(results[:4])

def analyze_business_metrics(query):
    """Analyze business performance and client metrics"""
    print(f"📈 Analyzing business metrics: {query}")

    results = []
    query_lower = query.lower()

    # Revenue analysis
    if "revenue" in query_lower:
        total_revenue = sum(c["revenue_generated"] for c in mock_data.clients)
        high_value = [c for c in mock_data.clients if c["revenue_generated"] > 10000]
        results.append(f"💰 Total revenue: £{total_revenue:,} | High-value clients: {len(high_value)}")

        # Service efficiency
        if "service time" in query_lower or "time" in query_lower:
            for client in high_value:
                efficiency = client["revenue_generated"] / client["service_time_hours"] if client["service_time_hours"] > 0 else 0
                results.append(f"⏱️ {client['name']}: £{efficiency:.0f}/hour efficiency")

    # Client demographics
    elif "retirement" in query_lower and "percentage" in query_lower:
        approaching_retirement = len([c for c in mock_data.clients if (c["retirement_goal"] - 2024) <= 5])
        total_clients = len(mock_data.clients)
        percentage = (approaching_retirement / total_clients) * 100
        results.append(f"📊 {approaching_retirement}/{total_clients} clients ({percentage:.0f}%) retiring within 5 years")

    # Service utilization
    elif "services" in query_lower and ("use" in query_lower or "most" in query_lower):
        results.append("🔝 Most used services by high-value clients: Portfolio reviews (100%), Retirement planning (80%), Estate planning (60%)")
        results.append("📋 Least used: Protection reviews (20%), Education planning (40%)")

    # Client satisfaction patterns
    elif "satisfied" in query_lower or "common" in query_lower:
        results.append("😊 Long-term satisfied clients common factors: Regular communication, proactive advice, comprehensive planning")
        results.append("💡 High satisfaction correlates with: Net worth >£500k, 5+ year relationships, complete planning suite")

    # Conversion rates
    elif "conversion" in query_lower or "referral" in query_lower:
        results.append("📊 Conversion rates: Client referrals (85%), Professional referrals (65%), Cold outreach (15%)")
        results.append("🎯 Best performing source: Existing client referrals")

    # Recommendation pushback
    elif "pushback" in query_lower or "resistance" in query_lower:
        results.append("❌ Most pushback: Platform transfers (cost concerns), Equity increases (risk aversion)")
        results.append("✅ Least resistance: Cash management, Protection reviews, ISA maximization")

    if not results:
        results = ["Ask about revenue analysis, client demographics, service utilization, or conversion rates for detailed business insights."]

    return " | ".join(results[:4])

def generate_follow_up_actions(query):
    """Generate follow-up actions and commitments"""
    print(f"✅ Generating follow-up actions: {query}")

    results = []
    query_lower = query.lower()

    # Draft follow-up emails
    if "draft" in query_lower and "email" in query_lower:
        results.append("📧 DRAFT - David Chen Follow-up: 'Hi David, Following our discussion about market volatility, I've attached the portfolio analysis showing your current allocation vs. target. The rebalancing to 60/40 would reduce volatility by ~15% while maintaining growth potential. Let's schedule a call this week to discuss. Best regards.'")

    # Open action items
    elif "action item" in query_lower or "open" in query_lower:
        results.append("📋 Open Actions: Send David Chen portfolio analysis (due 2024-11-27)")
        results.append("🔄 Pending: Sarah Williams platform transfer documentation")
        results.append("📅 Scheduled: Robert Thompson retirement cashflow model (due 2024-12-15)")

    # Waiting for client responses
    elif "waiting" in query_lower:
        results.append("⏳ Waiting for: Emma Jackson (decision on first ISA), Michael Gurung (estate planning meeting confirmation)")
        results.append("📞 Overdue responses: Sarah Williams (platform transfer approval - 30 days)")

    # Overdue commitments
    elif "overdue" in query_lower:
        results.append("🚨 Overdue commitments: Lisa Patel annual review (6 months overdue)")
        results.append("⚠️ Urgent: Sarah Williams business owner pension review (scheduled for August)")

    if not results:
        results = ["No specific follow-up actions found. Available: Draft emails, open action items, client responses needed."]

    return " | ".join(results[:3])

# =============================================================================
# Tool Definitions for Azure OpenAI
# =============================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_investment_opportunities",
            "description": "Analyze client investment opportunities including equity allocation, ISA/pension allowances, cash management, protection gaps, withdrawal rates, and retirement planning",
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
            "description": "Get proactive client management insights including review scheduling, business owner opportunities, education planning, estate planning, birthdays, and similar client profiles",
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
            "description": "Track compliance and regulatory requirements including Consumer Duty, documentation requests, recommendation tracking, risk discussions, and regulatory deadlines",
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
            "description": "Analyze business performance including revenue analysis, client demographics, service utilization, satisfaction patterns, conversion rates, and recommendation effectiveness",
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
            "description": "Generate follow-up actions including draft emails, open action items, waiting for client responses, and overdue commitments",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The follow-up action query"}},
                "required": ["query"]
            }
        }
    }
]

def get_ai_response(user_message):
    """Azure OpenAI response handler for Financial Advisor Chatbot"""
    print(f"Advisor Query: {user_message}")

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    system_prompt = """You are an advanced AI assistant designed specifically for UK Independent Financial Advisors (IFAs). You help advisors be more proactive, efficient, and compliant while managing 150-250 client relationships.

Your capabilities include:
🔍 INVESTMENT ANALYSIS: Identify underweight equity positions, unused allowances, cash excess, protection gaps, withdrawal rates
📊 PROACTIVE INSIGHTS: Track review schedules, business owner opportunities, education planning, estate planning gaps
📋 COMPLIANCE: Monitor Consumer Duty requirements, documentation, recommendation tracking
📈 BUSINESS ANALYTICS: Revenue analysis, client demographics, service efficiency, satisfaction patterns
✅ FOLLOW-UP: Draft emails, track action items, manage commitments

Always provide specific, actionable insights that help advisors demonstrate value to clients while staying FCA compliant. Use the available tools to access comprehensive client data and generate personalized recommendations."""

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
            print(f"Advisory AI: {answer}")
            return answer

        messages.append(response.choices[0].message)

        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            print(f"🛠️ Using tool: {tool_name}")

            if tool_name == "analyze_investment_opportunities":
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
            else:
                result = "Tool not found"

            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })

if __name__ == "__main__":
    print("🤖 Financial Advisor AI Assistant Started!")
    print("💡 Try asking about: client reviews, investment opportunities, compliance tracking, or business analytics")
    print("(Type 'quit' to exit)\n")

    while True:
        user_input = input("\nAdvisor: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Advisory session ended!")
            break

        response = get_ai_response(user_input)
        print()
