# 🤖 Enhanced Digital Nirvana Chat Backend
# This creates a comprehensive connection to answer questions about Digital Nirvana
# Your app can now handle questions about the entire digital-nirvana.com website

# Import necessary libraries
import requests    # For making web requests
import json       # For handling JSON data
from openai import OpenAI  # Official OpenAI Python library
import psycopg2   # For database connections
import streamlit as st  # For building the web app
from bs4 import BeautifulSoup  # For web scraping
import re  # For text processing
from urllib.parse import urljoin, urlparse  # For URL handling

# Replace with your actual OpenAI API key from https://platform.openai.com/api-keys
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

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

def get_digital_nirvana_info(query):
    """Get information from Digital Nirvana website based on user query"""
    print(f"🌐 Searching Digital Nirvana website for: {query}")
    
    # List of key pages to search through
    pages_to_search = [
        "https://digital-nirvana.com/",  # Homepage
        "https://digital-nirvana.com/about-us/",  # About
        "https://digital-nirvana.com/products/",  # Products
        "https://digital-nirvana.com/solutions/",  # Solutions
        "https://digital-nirvana.com/metadataiq-media-indexing-pam-mam/",  # MetadataIQ
        "https://digital-nirvana.com/trint-alternative-transcription/",  # MonitorIQ
        "https://digital-nirvana.com/contact-us/",  # Contact
        "https://digital-nirvana.com/clients/",  # Clients
        "https://digital-nirvana.com/case-studies/",  # Case Studies
    ]
    
    all_content = []
    
    for url in pages_to_search:
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                # Extract text content
                page_text = soup.get_text()
                
                # Clean up the text
                lines = (line.strip() for line in page_text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_text = ' '.join(chunk for chunk in chunks if chunk)
                
                # Add page context
                page_title = soup.find('title')
                title = page_title.get_text() if page_title else url
                
                all_content.append(f"=== {title} ({url}) ===\n{clean_text[:2000]}")  # Limit each page to 2000 chars
                
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            continue
    
    # Combine all content
    combined_content = "\n\n".join(all_content)
    
    if not combined_content:
        return "Unable to fetch information from Digital Nirvana website at this time. Please visit https://digital-nirvana.com/ directly."
    
    return combined_content[:8000]  # Limit total response to 8000 characters

def get_metadata_faq(question):
    """Get FAQ responses about Metadata IQ (keeping original function)"""
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

# Enhanced tool definitions
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
            "description": "Get specific MetadataIQ FAQ responses (use for specific MetadataIQ questions)",
            "parameters": {
                "type": "object",
                "properties": {"question": {"type": "string", "description": "The FAQ question to look up"}},
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_digital_nirvana_info",
            "description": "Search and get information from the Digital Nirvana website about their products, services, company, clients, case studies, and solutions. Use this for ANY question about Digital Nirvana, MonitorIQ, Trint alternatives, transcription services, media solutions, or general company information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The user's question or topic to search for on the Digital Nirvana website"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def get_ai_response(user_message):
    """Enhanced AI response handler with comprehensive Digital Nirvana website support"""
    print(f"You: {user_message}")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    system_prompt = """You are a helpful AI assistant with comprehensive access to Digital Nirvana's website and additional capabilities:

    **PRIMARY CAPABILITIES:**
    1. **Digital Nirvana Website Information**: Complete access to digital-nirvana.com content including:
       - Company information, history, and mission
       - All products (MetadataIQ, MonitorIQ, etc.)
       - Solutions for broadcasting, media, transcription
       - Client testimonials and case studies
       - Contact information and support
       - Pricing and deployment options
    
    2. **Weather data**: Current weather for any city
    3. **Student profiles**: Database of student information
    4. **MetadataIQ FAQ**: Specific product FAQ responses

    **IMPORTANT USAGE RULES:**
    
    - For ANY question about Digital Nirvana, their products, services, company info, MonitorIQ, transcription services, Trint alternatives, or media solutions → ALWAYS use get_digital_nirvana_info tool first
    
    - For specific MetadataIQ FAQ questions that need exact FAQ responses → use get_metadata_faq tool
    
    - For weather questions about someone's location: first get their profile, then get weather for their city
    
    - For student information: ALWAYS format as:
      **[Name]** - [Company]  
      [Background info]  
      LinkedIn: [URL]  
      Calendar: [URL]

    **RESPONSE GUIDELINES:**
    - Always provide comprehensive, accurate information based on the website content
    - If asked about Digital Nirvana competitors, pricing, or technical specifications, search the website first
    - Be knowledgeable about their full product suite and solutions
    - Mention specific features, benefits, and use cases found on their website
    - Include relevant contact information when appropriate"""

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

# Example usage loop
if __name__ == "__main__":
    print("🤖 Enhanced Digital Nirvana AI Assistant Started! (Type 'quit' to exit)")
    print("💡 Now capable of answering questions about the entire Digital Nirvana website!")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = get_ai_response(user_input)
        print()  # Add spacing