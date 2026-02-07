# STANDISH - Proactive AI Assistant for Financial Advisors

**Live Demo:** [https://ranjithchatgptapp.streamlit.app/](https://ranjithchatgptapp.streamlit.app/)

---

## Table of Contents

1. [Project Name](#project-name)
2. [Chosen Problem](#chosen-problem)
3. [Solution Overview](#solution-overview)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Environment Variables](#environment-variables)
7. [Setup Instructions](#setup-instructions)
8. [How to Run Locally](#how-to-run-locally)
9. [Features](#features)
10. [Architecture Deep Dive](#architecture-deep-dive)
11. [Core AI Functions](#core-ai-functions)
12. [Data Structures](#data-structures)
13. [Usage Guide](#usage-guide)
14. [Testing](#testing)

---

## Project Name

**STANDISH** - Proactive AI Assistant for UK Independent Financial Advisors (IFAs)

---

## Chosen Problem

### The Reactive Trap

UK Independent Financial Advisors face critical challenges that impact their practice:

| Problem | Impact |
|---------|--------|
| **60-70% time on admin** | Less time for actual client advice |
| **200+ clients to remember** | Important details get forgotten |
| **Buried opportunities** | Life events mentioned in meetings are lost |
| **Compliance anxiety** | FCA Consumer Duty requirements create stress |
| **Reactive firefighting** | Prevents proactive client management |

### The Memory Problem

- Advisors manage 200+ client relationships
- Life events mentioned in passing get forgotten
- Follow-up commitments never get calendared
- Compliance deadlines create constant anxiety
- No system to surface proactive opportunities

---

## Solution Overview

STANDISH is a **proactive AI assistant** that transforms how financial advisors work:

### What Makes STANDISH Different

| Traditional Chatbots | STANDISH |
|---------------------|----------|
| Wait for questions | Proactively provides daily briefings |
| Answer and forget | Tracks commitments and follow-ups |
| No context awareness | Understands client relationships |
| Manual action required | Takes autonomous actions with permission |

### Core Capabilities

1. **Proactive Daily Briefings** - Automatic morning summary with priorities
2. **Autonomous Actions** - Draft emails, schedule meetings, update CRM
3. **10-Stage Client Journey Tracking** - Visual workflow management
4. **Compliance Monitoring** - FCA Consumer Duty tracking
5. **Investment Analysis** - Equity gaps, allowances, withdrawal rates
6. **Meeting Intelligence** - Real-time suggestions during client conversations

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | Python 3.9+ | Core application logic |
| **AI/LLM** | Azure OpenAI (GPT-4) | Intelligent conversation and tool calling |
| **Database** | SQLite | Client data persistence |
| **Data Format** | JSON | Client data import/export |
| **Deployment** | Streamlit Cloud | Hosting and deployment |

### Python Dependencies

```
streamlit>=1.28.0
openai>=1.0.0
pandas>=2.0.0
python-dateutil>=2.8.0
```

---

## Project Structure

```
financial-advisor-chatbot/
├── app.py                  # Main Streamlit application (Frontend)
├── backend.py              # Core AI logic, tools, and functions
├── data_manager.py         # SQLite database management
├── document_processor.py   # Client document ingestion
├── requirements.txt        # Python dependencies
├── client_data.json        # Sample client data (optional)
├── advisor_data.db         # SQLite database (auto-generated)
├── README.md               # This file
└── .streamlit/
    └── secrets.toml        # Environment variables (create this)
```

### File Descriptions

| File | Description |
|------|-------------|
| `app.py` | Streamlit UI with daily briefings, quick actions, chat interface, sidebar dashboard |
| `backend.py` | Azure OpenAI integration, 8 AI tools, proactive agent layer, data stores |
| `data_manager.py` | SQLite CRUD operations, client caching, overdue detection |
| `document_processor.py` | PDF/text extraction for client onboarding |

---

## Environment Variables

STANDISH requires Azure OpenAI credentials. Create a `.streamlit/secrets.toml` file:

```toml
# Azure OpenAI Configuration (Required)
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-gpt4-deployment-name"
```

### How to Get Azure OpenAI Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy a GPT-4 model
4. Copy the API key and endpoint from "Keys and Endpoint"
5. Note your deployment name

### Environment Variable Details

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource endpoint | `https://myresource.openai.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2024-02-15-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your GPT-4 deployment name | `gpt-4-deployment` |

---

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Azure OpenAI access (with GPT-4 deployment)
- Git (optional, for cloning)

### Step 1: Clone or Download the Repository

```bash
# Option A: Clone with Git
git clone https://github.com/YOUR_USERNAME/financial-advisor-chatbot.git
cd financial-advisor-chatbot

# Option B: Download ZIP and extract
# Then navigate to the extracted folder
cd financial-advisor-chatbot
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Create the .streamlit directory
mkdir -p .streamlit

# Create secrets.toml file
# On Windows (PowerShell):
New-Item -Path ".streamlit/secrets.toml" -ItemType File

# On macOS/Linux:
touch .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your credentials:

```toml
AZURE_OPENAI_API_KEY = "your-api-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name"
```

### Step 5: (Optional) Add Sample Client Data

If you have client data in JSON format, place it in the project root as `client_data.json`. The system will automatically load it on startup.

---

## How to Run Locally

### Quick Start (3 Commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure secrets (edit the file with your credentials)
mkdir -p .streamlit && nano .streamlit/secrets.toml

# 3. Run the application
streamlit run app.py
```

### Detailed Run Instructions

**Step 1: Ensure virtual environment is activated**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Step 2: Verify dependencies are installed**
```bash
pip list | grep streamlit
pip list | grep openai
```

**Step 3: Run Streamlit application**
```bash
streamlit run app.py
```

**Step 4: Access the application**
- Open your browser to `http://localhost:8501`
- STANDISH will automatically show the daily briefing
- Use quick action buttons or chat naturally

### Expected Output on Startup

```
🚀 Starting Standish AI Assistant...
✅ Using real client data from documents
✅ Template processing integration enabled

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `API Key Error` | Check `.streamlit/secrets.toml` exists and has correct values |
| `Port already in use` | Run `streamlit run app.py --server.port 8502` |
| `Database error` | Delete `advisor_data.db` and restart |

---

## Features

### 1. Proactive Daily Briefings

Automatically displayed on page load:
- Yesterday's activity summary
- Today's priority actions
- Overdue commitments
- Pending documents
- Birthday opportunities

### 2. Autonomous Actions

Click-and-confirm actions:
- **Send Follow-up Email** - Draft personalized emails
- **Schedule Call** - Create meeting invites
- **Update CRM** - Log client interactions
- **Birthday Check** - Identify outreach opportunities

### 3. AI-Powered Analysis

| Analysis Type | What It Does |
|---------------|--------------|
| Investment Opportunities | Equity gaps, ISA allowance, cash excess |
| Withdrawal Rates | Flag retired clients with >4% withdrawal |
| Market Scenarios | Model 10/20/30% correction impact |
| Interest Rate Sensitivity | Mortgage renewal impact analysis |
| Cashflow Modeling | Early retirement projections |

### 4. Compliance Tracking

- Consumer Duty monitoring
- Recommendation history with rationale
- Meeting transcript search
- Document tracking
- Promise/commitment tracking

### 5. 10-Stage Client Journey

1. Annual Review Received
2. Pre-Meeting Prep
3. Meeting Scheduled
4. Meeting Conducted
5. Post-Meeting Analysis
6. Recommendations Prepared
7. Suitability Letter Sent
8. Implementation Started
9. Advice Implemented
10. Follow-up Scheduled

---

## Architecture Deep Dive

### Proactive Daily Briefings

STANDISH automatically greets you every morning with:
- **Yesterday's Summary**: Missed items, pending follow-ups
- **Today's Priorities**: Urgent reviews, birthdays, deadlines
- **Weekly Overview**: Client stats, compliance rates
- **Autonomous Opportunities**: Actions STANDISH can take for you

### Autonomous Action Capabilities

STANDISH can take actions on your behalf with your permission:
- **Email Management**: Draft and send follow-up emails, birthday messages
- **Calendar Management**: Schedule meetings, set reminders
- **CRM Updates**: Update client records, document interactions
- **Client Journey Tracking**: Monitor progress through 10-stage workflow
- **Report Generation**: Create portfolio summaries, compliance reports

### Advanced AI Integration

- **Azure OpenAI GPT-4**: Intelligent decision making and natural conversation
- **Proactive Function Calling**: STANDISH automatically chooses the right actions
- **Interactive Responses**: Every autonomous action includes Yes/No/Edit options
- **Context Awareness**: Maintains conversation flow across all interactions

---

## Core AI Functions

### `analyze_investment_opportunities()`

**Purpose**: Identify investment gaps and optimization opportunities

**Logic Flow**:
```python
# Equity Underweight Analysis
if client["age"] < 50 and client["portfolio_equity_percent"] < 70:
    flag_as_underweight()

# ISA Allowance Tracking
if client["isa_allowance_remaining"] > 0:
    suggest_maximization()

# Cash Excess Detection
emergency_fund = client["monthly_expenses"] * 6
if client["cash_reserves"] > emergency_fund + 10000:
    recommend_investment()
```

**Key Algorithms**:
- **Age-based equity allocation**: Under 50 = 70%+ equity, Under 60 = 50%+ equity
- **Emergency fund calculation**: 6 months expenses as baseline
- **Withdrawal rate monitoring**: Flag >4% as unsustainable

### `get_proactive_client_insights()`

**Purpose**: Surface proactive opportunities from client data

**Logic Flow**:
```python
# Review Overdue Detection
last_review = datetime.strptime(client["last_review"], "%Y-%m-%d")
months_since = (current_date - last_review).days / 30
if months_since > 12:
    flag_overdue_review()

# Business Owner Opportunities
if client["business_owner"]:
    suggest_relevant_services()
```

**Key Algorithms**:
- **Review scheduling**: 12+ months = overdue flag
- **Estate planning gaps**: >£500k net worth without planning
- **Education planning**: Children present but no education planning

### `track_compliance_requirements()`

**Purpose**: Monitor FCA compliance and documentation

**Logic Flow**:
```python
# Consumer Duty Tracking
overdue_reviews = filter_clients_by_review_date()
document_outstanding = track_client_documents()
recommendation_history = maintain_advice_audit_trail()
```

**Key Features**:
- **Consumer Duty monitoring**: Annual review tracking
- **Documentation management**: Outstanding client documents
- **Recommendation audit trail**: Full rationale tracking

### `analyze_business_metrics()`

**Purpose**: Business intelligence and performance analytics

**Logic Flow**:
```python
# Revenue Efficiency
efficiency = client["revenue_generated"] / client["service_time_hours"]

# Client Demographics
approaching_retirement = count_clients_retiring_within_5_years()
percentage = (approaching_retirement / total_clients) * 100
```

**Key Metrics**:
- **Revenue per hour**: Efficiency measurement
- **Demographic analysis**: Retirement timeline tracking
- **Service utilization**: Most/least used services

### `generate_follow_up_actions()`

**Purpose**: Action item management and client communication

**Features**:
- **Email drafting**: Template generation for follow-ups
- **Action tracking**: Open commitments monitoring
- **Client response management**: Waiting for decisions tracking

---

## Data Structures

### Client Profile Schema

```python
{
    "id": int,
    "name": str,
    "age": int,
    "risk_profile": "Conservative|Moderate|Aggressive",
    "net_worth": int,
    "annual_income": int,
    "retirement_goal": int,  # Year
    "isa_allowance_remaining": int,
    "annual_allowance_remaining": int,
    "cash_reserves": int,
    "monthly_expenses": int,
    "portfolio_equity_percent": int,
    "protection_cover": str,
    "estate_planning": bool,
    "business_owner": bool,
    "concerns": List[str],
    "life_events": List[str]
}
```

### Query Processing Logic

**Investment Queries:**
- **"underweight equities"** → Age-based allocation analysis
- **"ISA allowance"** → Available allowance identification
- **"cash excess"** → Emergency fund + 6 months calculation
- **"protection gaps"** → Coverage vs. family circumstances

**Proactive Queries:**
- **"overdue reviews"** → 12+ months since last review
- **"business owners"** → B2B service opportunities
- **"estate planning"** → Net worth threshold analysis
- **"birthdays"** → Current month birthday matches

**Compliance Queries:**
- **"consumer duty"** → FCA requirement tracking
- **"recommendations made"** → Audit trail retrieval
- **"documents waiting"** → Outstanding paperwork tracking

---

## Usage Guide

### Sample Queries

**Investment Analysis:**
```
"Which clients are underweight equities?"
"Show me ISA allowance remaining for all clients"
"Which retired clients have withdrawal rates above 4%?"
```

**Proactive Insights:**
```
"Who has overdue reviews?"
"Show me birthday opportunities this month"
"Which clients need estate planning?"
```

**Compliance:**
```
"Pull every recommendation I made to David Chen"
"What documents am I waiting for?"
"What did I promise to send the Jackson family?"
```

**Autonomous Actions:**
```
"Send follow-up email to Sarah Williams"
"Schedule annual review for David Chen"
"Update CRM for Emma Jackson"
```

### Proactive Experience

#### Daily Briefing (Automatic on Page Load)
```
📅 TODAY: Tuesday, February 05, 2026

YESTERDAY'S ACTIVITY SUMMARY:
⚠️ 2 clients with overdue reviews
📧 3 pending follow-up emails
✅ No critical meetings missed

TODAY'S PRIORITY ACTIONS:
🚨 OVERDUE: Sarah Williams annual review (16 days overdue)
📅 DUE THIS WEEK: David Chen annual review (in 3 days)
🎂 BIRTHDAY OPPORTUNITY: Emma Jackson - perfect check-in opportunity

STANDISH CAN HELP YOU WITH:
📧 Draft and send follow-up emails to overdue clients
📞 Schedule callback reminders for high-priority clients
📊 Generate weekly portfolio performance reports
```

#### Autonomous Action Flow
1. **Click Action Button** → 📧 Send Follow-up Email
2. **STANDISH Prepares Action** → Shows draft email with details
3. **Interactive Choice** → ✅ Yes, Do It | ✏️ Edit | ❌ Cancel
4. **Confirmation & Execution** → Action completed with feedback

#### Proactive Decision Making
- **Morning Briefing**: Automatically shown on page load
- **Intelligent Routing**: STANDISH chooses appropriate tools based on context
- **Permission-Based Actions**: Always asks before taking significant actions
- **Follow-up Management**: Tracks commitments and suggests next steps

---

## Testing

### Proactive Briefing Tests

```
✅ Open the app → Automatic daily briefing displays
✅ Shows yesterday's summary, today's priorities, weekly stats
✅ Displays STANDISH's autonomous action opportunities
✅ Includes current date and personalized content
```

### Autonomous Action Tests

```
✅ Click "📧 Send Follow-up Email" → Draft appears with interactive buttons
✅ Click "📞 Schedule Call" → Meeting details with Yes/No/Edit options
✅ Click "📋 Update CRM" → Update preview with confirmation choices
✅ Click "🎂 Birthday Check" → Opportunity identification with actions
```

### Interactive Response Tests

```
✅ Every autonomous action includes: ✅ Yes, Do It | ✏️ Edit | ❌ Cancel
✅ Confirmation messages appear when actions are approved
✅ Edit option redirects to main chat for modifications
✅ Cancel option clears the action and returns to ready state
```

### Quick Action Button Tests

```
✅ "📧 Draft Follow-up Emails" → Shows email drafts for overdue clients
✅ "📅 Schedule Reviews" → Lists clients needing review scheduling
✅ "🎯 Client Journey Status" → Displays 10-stage workflow progress
✅ "🔄 Refresh Briefing" → Reloads daily briefing with updated info
```

---

## Performance Characteristics

### Response Time Optimization
- **Function-based routing**: Direct tool selection vs. sequential processing
- **Result limiting**: Maximum 5 results per query for performance
- **Context management**: Efficient conversation state handling

### Scalability Considerations
- **Mock data structure**: Easily extensible for more clients
- **Tool modularity**: Individual functions can be enhanced independently
- **Query optimization**: Pattern matching for fast intent recognition

---

## Key Differentiators

### Immediate Value
- **Zero Learning Curve**: Open app → Get daily briefing automatically
- **Instant Actions**: Click button → STANDISH drafts email/schedules meeting
- **Smart Suggestions**: STANDISH tells you what needs attention today
- **FCA Compliance**: Built-in Consumer Duty tracking and documentation

### Business Impact
- **60% Time Savings**: Automated admin tasks and proactive insights
- **100% Compliance**: Never miss review deadlines or documentation
- **Enhanced Client Service**: Proactive outreach and opportunity identification
- **Reduced Stress**: STANDISH manages your calendar and commitments

---

## Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path to `app.py`
5. Add secrets in Settings → Secrets (same format as `secrets.toml`)
6. Deploy

---

## License

MIT License

---

## Support

For issues or questions:
- Review inline documentation in `backend.py` and `app.py`
- Check the troubleshooting section above
- Open an issue on GitHub

---

**STANDISH** - *"Doesn't just answer questions - manages your day and grows your practice."*
