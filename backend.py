# 🤖 Enhanced Azure OpenAI Digital Nirvana Chat Backend
# Comprehensive knowledge base covering all Digital Nirvana products and services

import requests
import json
from openai import AzureOpenAI
import psycopg2
import streamlit as st

# =============================================================================
# Azure OpenAI Configuration
# =============================================================================
AZURE_OPENAI_API_KEY = st.secrets["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"] 
AZURE_OPENAI_API_VERSION = st.secrets["AZURE_OPENAI_API_VERSION"]
AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["AZURE_OPENAI_DEPLOYMENT_NAME"]

# =============================================================================
# Database Configuration
# =============================================================================
DB_HOST = "aws-0-ap-south-1.pooler.supabase.com"
DB_PORT = 6543
DB_DATABASE = "postgres"
DB_USER = "postgres.ntqronyjnvuvqhbhpudn"
DB_PASSWORD = "RbUL1wu88gGuuDJ"

def get_weather(city):
    """Get current weather for a city"""
    print(f"🌤️ Getting weather for {city}...")
    
    url = f"http://api.weatherapi.com/v1/current.json?key=ca1073669c984fdf940100649251309&q={city}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            temp = data['current']['temp_c']
            condition = data['current']['condition']['text']
            return f"Weather in {city}: {condition}, {temp}°C"
    except:
        pass
    
    return f"Weather data not available for {city}"

def get_student_profiles():
    """Get all student data from Supabase"""
    print("📊 Getting student profiles...")
    
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_DATABASE, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM linkedin_profiles ORDER BY id")
    results = cursor.fetchall()
    conn.close()
    
    return str(results)

def get_digital_nirvana_info(query):
    """
    Comprehensive Digital Nirvana knowledge base covering all products and services.
    Returns detailed information based on the query.
    """
    print(f"🌐 Getting Digital Nirvana information for: {query}")
    
    # COMPREHENSIVE DIGITAL NIRVANA KNOWLEDGE BASE
    knowledge_base = {
        "company": """Digital Nirvana Company Overview: Automate Workflows, Streamline Operations, Comply with Regulations, & Drive Insights with AI. Harness the power of AI for unparalleled efficiency. Our innovative solutions optimize processes, saving time and resources while delivering actionable intelligence. Digital Nirvana optimizes your media, data, and compliance workflows with advanced AI, turning time-consuming processes into seamless tasks. Core Products include MonitorIQ, MetadataIQ, and MediaServicesIQ. Bespoke Solutions accelerate delivery of critical business outcomes across Media & Entertainment, Financial Services, Education, Legal, Healthcare, and Technology Sectors. Website: https://digital-nirvana.com/""",
        
        "monitoriq": """MonitorIQ: The Ultimate Broadcast Signal Monitoring Tool. Meet MonitorIQ! The ultimate Content monitoring, Compliance Logging, and Verification Solution! Monitor ad performance issues, inconsistent service quality, compliance gaps, content monitoring challenges, and more in a single platform. Key Capabilities: 1) Ad Performance Verification & Sales Empowerment - Intuitive self-service tool for sales and executive teams, quickly spot-check ads, verify proof of performance, effortlessly reconcile traffic logs with aired recordings. 2) Quality of Experience (QoE) Monitoring - Proactive alarms for visual impairments, visibility into every transmission and delivery point, return path monitoring. 3) Compliance Logging - Track and report on loudness compliance, ensure closed caption compliance (CC608, CC708, international standards), real-time alerting. 4) Content Monitoring - Access 1 to 100+ channel recordings from any web browser, instant access to critical content and metadata, competitive ratings monitoring. URL: https://digital-nirvana.com/monitoriq-broadcasting-signal-monitoring/""",
        
        "metadataiq": """MetadataIQ: Enterprise-Grade Metadata Automation for Broadcasters. MetadataIQ Simplifies Your Broadcast Workflows and Keeps You Compliant On Air. The Backbone Of Broadcast Metadata Workflows. Automate metadata tagging, track quality, and meet broadcast standards at scale. Deeply Integrated, Natively Built - No Third-Party Hassles. Metadata automation inside Avid & Grass Valley, no extra plugins required. Key Features: Automated Metadata Tagging Engine, Compliance Tagging & Rules Engine (political ads, brand mentions, profanity), Broadcast-Grade Integrations (Avid MediaCentral, Telestream, Grass Valley), Real-Time Live Processing, Governance Dashboard & Quality Scoring, Batch Scheduling & Pipeline Automation. Trusted By: CBS, Fox Broadcasting, Sinclair Broadcasting. Supports FCC, GDPR, Ofcom compliance. Industries: Broadcasting, Production, News, Sports, Archives. URL: https://digital-nirvana.com/metadataiq-media-indexing-pam-mam/""",
        
        "mediaservicesiq": """MediaServicesIQ: AI/ML Content Optimization Platform. Transform your media management and content optimization with MediaServicesIQ. Unlock automated features like chapter marker generation, content summarization, music licensing identification, ad monitoring. Key Features: 1) Podcast Enhancement - Automatic chapter marker generation, content summarization and segmentation, automated content classification, keyword generation for enhanced SEO. 2) Music Licensing Management - Auto-identification of music content (artist, title, publisher), automated visibility into licensing status, quickly identify compliant and expired licenses. 3) Ad Monitoring & Revenue Optimization - Automate ad monitoring and reporting, extract brand, product, category information, maximize revenue with contextual ad insertion. URL: https://digital-nirvana.com/mediaservicesiq-ai-ml-content-optimization/""",
        
        "tranceiq": """TranceIQ: Transcription, Captioning & Subtitle Platform. Ultimate platform revolutionizing transcription, captioning, subtitle generation, and publishing. Core Capabilities: 1) Automated Transcript Generation - 50%+ efficiency improvement, 30+ native source languages, 90%+ accuracy levels. 2) Caption Creation - Automatically conform transcripts into captions, adherence to Amazon Prime, Netflix, Hulu style guidelines, improve accessibility for users anywhere. 3) Subtitle Generation & Localization - Auto-translate captions into 100+ languages, repurpose assets in different languages, expand global reach. 4) Publishing & Fulfillment - Deliver in all industry-supported formats, sidecar file or embedded options, direct API integration with enterprise systems. URL: https://digital-nirvana.com/tranceiq-transcription-captioning-subtitle/""",
        
        "media_enrichment": """Media Enrichment: Boost Productivity, Save Time, and Optimize Costs with AI-Powered Solutions. YES! Digital Nirvana provides comprehensive dubbing services through Subs N Dubs. Delivering highly accurate machine-generated and human-curated captions, subtitles, dubbing, media analysis, and media monitoring services. Services: 1) Subs N Dubs (AI-Powered Dubbing) - AI-powered subtitling and dubbing in 60+ languages, natural-sounding voiceovers, cultural adaptation, seamless localization for businesses, educators, media creators, global brands. 2) Captioning - Accurate closed captioning, live captioning, caption conformance, lecture captioning for all industries. 3) Transcription - Create accurate transcripts, tag metadata, integrate into content management systems, versatile across finance, healthcare, legal, technology, broadcasting. 4) Subtitling - Subtitles in 20+ languages, quick turnaround, localize translations from source language. Client Success: Hollywood powerhouse 24-48 hour turnaround, Spanish media giant reduced captioning from 15 hours to less than 2 hours. URL: https://digital-nirvana.com/media-enrichment-solutions/""",
        
        "cloud_engineering": """Cloud Engineering: Elevate Your Business with Scalable, Secure Cloud Solutions. Streamline operations and scale effortlessly with expert cloud strategies, seamless migrations, cutting-edge automation. Services: 1) Cloud Strategy, Design, Migration - Tailor-made cloud strategy, readiness assessments, hybrid architecture design, flawless migration, scalable infrastructure. 2) Cloud-Native Development and Automation - Accelerate business with cloud-native applications, containerization, CI/CD pipelines, serverless technologies, workflow automation. 3) Cloud Security, Management, Optimization - Compliance-driven security, advanced threat detection, cost optimization, proactive monitoring, right-sized resources. 4) Data Services and Cloud Integration - Cloud database migration, AI/ML integration, smart analytics pipelines, real-time insights. 5) Reliable Connectivity, Expert Guidance - Secure VPCs, hybrid connections, strategic advice, technology enablement. URL: https://digital-nirvana.com/cloud-engineering/""",
        
        "data_intelligence": """Data Intelligence: Turn Data Into Your Competitive Advantage. Transform unstructured data into actionable intelligence. Services: 1) Data Labeling - Deliver accurate annotations across text, images, audio, video. Optimize data to power AI models, improving prediction accuracy and performance. 2) Model Validation - Assess and verify predictive models to ensure accuracy on unseen data. Expert validation and hyperparameter tuning for peak performance. 3) Data Analytics - Turn complex datasets into actionable insights. Make informed decisions across various fields, from predictive analytics to detailed visualizations. 4) Prompt Engineering - Design tailored inputs that enable AI models to deliver precise, impactful results. Maximize accuracy and utility with expertly crafted prompts. 5) Data Wrangling - Transform and structure messy data into usable format. Ensure data is consistent, accurate, ready for in-depth analysis. URL: https://digital-nirvana.com/data-intelligence-solutions/""",
        
        "investment_research": """Investment Research: Empower Investment Decisions with Real-Time Financial Insights. Providing accurate, real-time financial event transcripts, summaries, in-depth market research. Services: 1) Financial Reporting Insights - Real-time insights from earnings calls, live-streaming transcripts, follow key points, identify trends, gauge sentiment. 2) Corporate Event Calendar - Accurate timely records of important financial events, precise corporate event tracking, comprehensive event data. 3) Insights and Summaries - Transform vast information into concise actionable insights, distill complex data into key takeaways, save time. 4) Market Intel & Research - Data analytics with industry expertise, analyze market size, customer behavior, competitor landscape. Client Success: Financial transcripts with best accuracy, 3-4 hour turnaround vs 6+ hours with competitors. URL: https://digital-nirvana.com/investment-research-solutions/""",
        
        "learning_management": """Learning Management: Elevate Assessments, Ensure Integrity, Improve Outcomes. Language LSRW and mathematics evaluation, performance assessments, scoring, grading, skill assessments. Services: 1) Comprehensive Academic Assessments - Holistic LSRW evaluations, constructive feedback, fast insightful reports, save educators time. 2) Content Development and Management - Engaging multimedia content, diverse assessments, seamless lifecycle management, align with curricular standards. 3) Advanced Lecture Captioning - AI-powered real-time transcription, captioning, multilingual translation for universities and schools, enhance inclusivity. 4) Adaptive Proctoring - Real-time monitoring, AI behavior analysis, secure in-person and online exams, prevent cheating. URL: https://digital-nirvana.com/learning-management-solutions/""",
        
        "clients": """Digital Nirvana Trusted Clients & Success Stories. Major Broadcasters: CBS, Fox Broadcasting, Sinclair Broadcasting, Tier-1 broadcasters globally. Client Success Stories: 1) Hollywood Media-Processing Powerhouse: 24-48 hour turnaround, exceeded expectations, 24/7 operations, ability to accommodate rush orders. 2) Financial Markets: Best accuracy imaginable, 3-4 hour turnaround vs 6+ hours with other providers. 3) Spanish Media Giant: Reduced captioning time from 15 hours to less than 2, game changer with multilingual translation. Proven Results: 75% reduction in content prep time, 99%+ compliance accuracy, significant cost savings.""",
        
        "contact": """Contact Digital Nirvana. Website: https://digital-nirvana.com/ Product Pages: MonitorIQ, MetadataIQ, MediaServicesIQ, TranceIQ, Media Enrichment, Cloud Engineering, Data Intelligence, Investment Research, Learning Management. Services: Product demos, custom integration support, training and onboarding, 24/7 technical support for enterprise clients, strategic advice and readiness assessments."""
    }
    
    # Intelligent query matching
    query_lower = query.lower()
    relevant_info = []
    
    # Product-specific queries
    if any(word in query_lower for word in ['monitoriq', 'monitor iq', 'signal monitoring', 'broadcast monitoring', 'ad verification', 'qoe', 'compliance logging']):
        relevant_info.append(knowledge_base['monitoriq'])
    
    if any(word in query_lower for word in ['metadataiq', 'metadata iq', 'metadata', 'tagging', 'compliance', 'governance', 'avid', 'grass valley']):
        relevant_info.append(knowledge_base['metadataiq'])
    
    if any(word in query_lower for word in ['mediaservicesiq', 'media services', 'chapter marker', 'podcast', 'music licensing', 'ad monitoring']):
        relevant_info.append(knowledge_base['mediaservicesiq'])
    
    if any(word in query_lower for word in ['tranceiq', 'trance iq']):
        relevant_info.append(knowledge_base['tranceiq'])
    
    if any(word in query_lower for word in ['transcription', 'transcribe', 'transcript']):
        relevant_info.append(knowledge_base['tranceiq'])
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['caption', 'captioning', 'closed caption', 'live caption']):
        relevant_info.append(knowledge_base['tranceiq'])
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['subtitle', 'subtitling', 'subtitles']):
        relevant_info.append(knowledge_base['tranceiq'])
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['dubbing', 'dub', 'dubs', 'voiceover', 'voice over', 'subs n dubs', 'subs and dubs']):
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['translation', 'translate', 'localization', 'localize', 'multilingual']):
        relevant_info.append(knowledge_base['tranceiq'])
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['media enrichment', 'enrichment service']):
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['cloud engineering', 'cloud migration', 'cloud strategy', 'cloud native', 'containerization', 'serverless', 'cloud security']):
        relevant_info.append(knowledge_base['cloud_engineering'])
    
    if any(word in query_lower for word in ['data intelligence', 'data wrangling', 'data labeling', 'data labelling', 'prompt engineering', 'model validation', 'analytics', 'ai model', 'machine learning']):
        relevant_info.append(knowledge_base['data_intelligence'])
    
    if any(word in query_lower for word in ['investment research', 'earnings call', 'financial reporting', 'market intel', 'corporate event', 'financial insight']):
        relevant_info.append(knowledge_base['investment_research'])
    
    if any(word in query_lower for word in ['learning management', 'academic assessment', 'proctoring', 'education', 'e-learning', 'lms', 'learning solution']):
        relevant_info.append(knowledge_base['learning_management'])
    
    if any(word in query_lower for word in ['company', 'about', 'digital nirvana', 'who', 'overview', 'what is']):
        relevant_info.append(knowledge_base['company'])
    
    if any(word in query_lower for word in ['product', 'solution', 'offer', 'service', 'all products']):
        relevant_info.extend([knowledge_base['company'], knowledge_base['monitoriq'], knowledge_base['metadataiq']])
    
    if any(word in query_lower for word in ['client', 'customer', 'cbs', 'fox', 'sinclair', 'who uses']):
        relevant_info.append(knowledge_base['clients'])
    
    if any(word in query_lower for word in ['contact', 'support', 'demo', 'reach', 'sales', 'inquiry']):
        relevant_info.append(knowledge_base['contact'])
    
    if not relevant_info:
        relevant_info = [knowledge_base['company']]
    
    seen = set()
    unique_info = []
    for item in relevant_info:
        if item not in seen:
            seen.add(item)
            unique_info.append(item)
    
    return " ".join(unique_info)

# Tool definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_student_profiles", 
            "description": "Get all student profiles from database",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_digital_nirvana_info",
            "description": "Get comprehensive information about Digital Nirvana and ALL their products/services including MonitorIQ, MetadataIQ, MediaServicesIQ, TranceIQ, Media Enrichment, Cloud Engineering, Data Intelligence, Investment Research, Learning Management. Use for ANY question about Digital Nirvana.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The user's question about Digital Nirvana"}
                },
                "required": ["query"]
            }
        }
    }
]

def get_ai_response(user_message):
    """Azure OpenAI response handler - Streamlit compatible version"""
    print(f"You: {user_message}")
    
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )
    
    system_prompt = """You are a highly knowledgeable AI assistant specializing in Digital Nirvana's complete product portfolio and services. For ANY question about Digital Nirvana, their products, services, or solutions, ALWAYS use get_digital_nirvana_info tool. Provide comprehensive, detailed responses based on retrieved knowledge. Highlight key benefits, features, and competitive advantages."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    while True:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            tools=tools
        )
        
        if not response.choices[0].message.tool_calls:
            answer = response.choices[0].message.content
            print(f"AI: {answer}")
            return answer
        
        messages.append(response.choices[0].message)
        
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            print(f"🛠️ AI is using tool: {tool_name}")
            
            if tool_name == "get_weather":
                city = json.loads(tool_call.function.arguments)["city"]
                result = get_weather(city)
            elif tool_name == "get_student_profiles":
                result = get_student_profiles()
            elif tool_name == "get_digital_nirvana_info":
                query = json.loads(tool_call.function.arguments)["query"]
                result = get_digital_nirvana_info(query)
            else:
                result = "Unknown tool"
            
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })

if __name__ == "__main__":
    print("🤖 Enhanced Digital Nirvana Assistant Started!")
    print("(Type 'quit' to exit)\n")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = get_ai_response(user_input)
        print()