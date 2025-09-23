# 🤖 Part 2: Basic OpenAI Chat Backend
# This creates a simple connection to OpenAI's GPT-3.5 model
# Your app will send user messages to OpenAI and get AI responses back

# Import necessary libraries
import requests    # For making web requests (used in later parts)
import json       # For handling JSON data (used in later parts)
from openai import OpenAI  # Official OpenAI Python library#
import psycopg2   # For database connections (used in later parts)
import streamlit as st  # For building the web app (used in later parts)
# Replace with your actual OpenAI API key from https://platform.openai.com/api-keys
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# =============================================================================
# You do not have to modify above text once API keys are added
# Any further steps will be pasted below (replace completely)
# =============================================================================
# Database Configuration
DB_HOST = "aws-0-ap-south-1.pooler.supabase.com"
DB_PORT = 6543
DB_DATABASE = "postgres"
DB_USER = "postgres.ntqronyjnvuvqhbhpudn"
DB_PASSWORD = "RbUL1wu88gGuuDJ"

def get_weather(city):
    """Get current weather for a city"""
    print(f"🌤️ Getting weather for {city}...")
    
    # Using WeatherAPI.com with your API key
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

def get_metadata_faq(question):
    """Get FAQ responses about Metadata IQ"""
    print(f"📋 Getting FAQ response for: {question}")
    
    # FAQ knowledge base
    faq_responses = {
        "What is metadata in broadcasting?": "Metadata in broadcasting refers to descriptive information about video or audio content—such as speaker names, timecodes, topics, profanity, political content, and more. It enables easier search, compliance, and monetization across live and archived footage.",
        "Why is automated metadata tagging important?": "Manual tagging is time-consuming, error-prone, and unsustainable at scale. Automated tagging ensures consistent, accurate metadata that saves time, reduces compliance risks, and enables faster content retrieval.",
        "How does MetadataIQ automate metadata tagging?": "MetadataIQ uses advanced speech-to-text, video recognition, and rules-based engines to auto-tag metadata across content types. It applies custom tagging rules for compliance and generates audit-ready outputs without manual input.",
        "Can MetadataIQ help with broadcast compliance?": "Yes. MetadataIQ automatically identifies and tags compliance-sensitive content like political ads, brand mentions, profanity, and regulatory disclosures—ensuring every piece of content meets local and global broadcast standards.",
        "How does MetadataIQ's governance dashboard work?": "The dashboard tracks the completeness and quality of your metadata. It scores content, flags errors, and provides full audit logs—so you're always prepared for internal checks or third-party reviews.",
        "What regions or standards does MetadataIQ support for compliance tagging?": "MetadataIQ supports region-specific compliance needs including FCC (U.S.), GDPR (EU), Ofcom (UK), and can be customized to support your internal or client-specific guidelines.",
        "What platforms does MetadataIQ integrate with?": "MetadataIQ integrates seamlessly with Avid MediaCentral, Telestream, Grass Valley, and a wide range of DAM and MAM systems. Custom connectors can be built for enterprise workflows.",
        "Is MetadataIQ available as SaaS or on-premises?": "MetadataIQ is available via enterprise deployment models and is typically implemented within your infrastructure alongside your media tools. Cloud and hybrid setups are also supported based on your workflow.",
        "Is MetadataIQ suitable for live content?": "Absolutely. MetadataIQ can process and tag live content in real time—making it ideal for news, sports, and event broadcasting where quick turnaround is critical.",
        "How accurate is MetadataIQ's metadata tagging?": "MetadataIQ is broadcast-grade, meaning it's built for high accuracy and reliability. Unlike generic AI tools, our tagging engine is trained and tuned for professional media workflows and compliance-sensitive use cases.",
        "What industries use MetadataIQ?": "While built for broadcasters, MetadataIQ is also used by sports networks, government media teams, public broadcasters, media archives, and any organization that needs high-volume, high-accuracy metadata management.",
        "Does MetadataIQ work with archived content?": "Yes. MetadataIQ is used to retroactively process and enrich archives, making decades of stored footage searchable, monetizable, and compliant with current regulations.",
        "Can MetadataIQ help with monetization of old content?": "Yes. By applying consistent metadata across your archives, MetadataIQ helps you resurface, repackage, and license old footage more efficiently—turning dormant content into new revenue opportunities.",
        "What kind of support does MetadataIQ offer?": "We offer enterprise-grade support, onboarding, custom integration assistance, and ongoing training. Our team works directly with your engineers, compliance leads, and content managers to ensure success."
    }
    
    # Find exact match first
    if question in faq_responses:
        return faq_responses[question]
    
    # Find partial matches (case insensitive)
    question_lower = question.lower()
    for faq_question, answer in faq_responses.items():
        if any(word in faq_question.lower() for word in question_lower.split() if len(word) > 3):
            return f"Based on your question, here's relevant information:\n\n{answer}"
    
    return "I don't have specific FAQ information for that question. Please contact support at support@digital-nirvana.com for more details."

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
            "name": "get_metadata_faq",
            "description": "Get FAQ responses about Metadata IQ product questions",
            "parameters": {
                "type": "object",
                "properties": {"question": {"type": "string", "description": "The FAQ question to look up"}},
                "required": ["question"]
            }
        }
    }
]

def get_ai_response(user_message):
    """AI response handler with tool calling"""
    print(f"You: {user_message}")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    system_prompt = """You are a helpful assistant with access to three main capabilities:
    1. Weather data for any city
    2. Student profiles from a database  
    3. Metadata IQ product FAQ information
    
    IMPORTANT: For ANY question about MetadataIQ, metadata, broadcasting, compliance, governance dashboard, or similar topics - ALWAYS use the get_metadata_faq tool first. Do not refuse to answer these questions.
    
    For weather questions about someone's location: first get their profile, then get weather for their city.
    Describe weather naturally (sunny, cloudy, rainy, warm, etc.) based on temperature.
    
    For Metadata IQ/metadata/broadcasting questions: ALWAYS use the get_metadata_faq tool to provide accurate product information. Pass the user's question directly to the tool.
    
    When presenting student information, ALWAYS format it exactly like this:
    
    **[Name]** - [Company]  
    [Background info - total experience, PM experience, specialization, etc.]  
    LinkedIn: [actual URL]  
    Calendar: [actual URL]  
    
    Example:
    **John Doe** - Tech Company  
    15 years total experience, 8 years in PM. Specializes in AI and Machine Learning.  
    LinkedIn: https://www.linkedin.com/in/johndoe/  
    Calendar: https://calendly.com/johndoe/meeting"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # Main conversation loop
    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools
        )
        
        # No tool calls - return final answer
        if not response.choices[0].message.tool_calls:
            answer = response.choices[0].message.content
            print(f"AI: {answer}")
            return answer
        
        # Add assistant message
        messages.append(response.choices[0].message)
        
        # Execute all tool calls
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            print(f"🛠️ AI is using tool: {tool_name}")
            
            if tool_name == "get_weather":
                city = json.loads(tool_call.function.arguments)["city"]
                result = get_weather(city)
            elif tool_name == "get_student_profiles":
                result = get_student_profiles()
            elif tool_name == "get_metadata_faq":
                question = json.loads(tool_call.function.arguments)["question"]
                result = get_metadata_faq(question)
            else:
                result = "Unknown tool"
            
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })

# Example usage loop
if __name__ == "__main__":
    print("🤖 AI Assistant Started! (Type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = get_ai_response(user_input)
        print()  # Add spacing