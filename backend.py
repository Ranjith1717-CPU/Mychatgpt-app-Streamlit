# 🤖 Simplified Digital Nirvana Chat Backend
# This version uses static content instead of web scraping to avoid dependency issues

# Import necessary libraries
import requests    # For making web requests
import json       # For handling JSON data
from openai import AzureOpenAI  # Official OpenAI Python library
import psycopg2   # For database connections
import streamlit as st  # For building the web app

# Replace with your actual OpenAI API key from https://platform.openai.com/api-keys
AZURE_OPENAI_API_KEY = “AHz5fOtxXHg0m0OYl9neAlfOnna79WBhvetPnnZ4nssRlZXiK9FBJQQJ99BIACYeBjFXJ3w3AAABACOGcHNC”

AZURE_OPENAI_ENDPOINT = “https://curious-01.openai.azure.com/”

AZURE_OPENAI_API_VERSION = “2024-12-01-preview”

AZURE_OPENAI_DEPLOYMENT_NAME = “Ranjith”

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
    """Get information about Digital Nirvana using static knowledge base"""
    print(f"🌐 Getting Digital Nirvana information for: {query}")
    
    # Comprehensive Digital Nirvana knowledge base
    knowledge_base = {
        "company": """
        Digital Nirvana is a leading provider of AI-powered media intelligence solutions. Founded with a mission to transform how broadcasters and media organizations manage, search, and monetize their content. The company specializes in automated metadata generation, transcription services, and media asset management solutions.
        
        Headquarters: Digital Nirvana serves clients globally with a focus on enterprise broadcast solutions.
        """,
        
        "products": """
        Digital Nirvana offers several key products:
        
        1. **MetadataIQ**: Enterprise-grade metadata automation platform for broadcast media
           - Automated metadata tagging using AI
           - Compliance monitoring and governance
           - Real-time content processing
           - Integration with major broadcast systems (Avid, Grass Valley, Telestream)
        
        2. **MonitorIQ**: Advanced transcription and monitoring solution
           - Real-time speech-to-text transcription
           - Alternative to Trint and other transcription services
           - Live content monitoring and compliance
           - Multi-language support
        
        3. **Media Asset Management Solutions**: Comprehensive content management and search capabilities
        """,
        
        "metadataiq": """
        MetadataIQ is Digital Nirvana's flagship product for automated metadata generation:
        
        Features:
        - AI-powered speech recognition and content analysis
        - Automated compliance tagging (political content, profanity, brand mentions)
        - Real-time processing for live broadcasts
        - Governance dashboard with quality scoring
        - Audit-ready outputs and full logging
        - Integration with existing broadcast workflows
        
        Benefits:
        - Reduces manual tagging time by 90%+
        - Ensures broadcast compliance automatically
        - Makes archived content searchable and monetizable
        - Supports major broadcast standards (FCC, GDPR, Ofcom)
        
        Industries served: Broadcasters, sports networks, news organizations, government media, public broadcasters
        """,
        
        "monitoriq": """
        MonitorIQ is Digital Nirvana's transcription and monitoring solution:
        
        Key Features:
        - Real-time speech-to-text transcription
        - Live content monitoring and alerts
        - Multi-speaker identification
        - Timestamp-accurate transcripts
        - API integration capabilities
        - Cloud and on-premises deployment
        
        Competitive Advantages:
        - More accurate than generic transcription services
        - Built specifically for broadcast and media workflows
        - Better handling of technical terminology and proper nouns
        - Enterprise-grade security and compliance
        
        Trint Alternative: MonitorIQ offers superior accuracy and broadcast-specific features compared to Trint
        """,
        
        "clients": """
        Digital Nirvana serves major broadcasters and media organizations including:
        
        - CBS - Uses MetadataIQ for content management and compliance
        - Fox Broadcasting - Leverages automated metadata for news and sports
        - Sinclair Broadcasting - Implements across multiple stations
        - Government agencies - For secure media monitoring
        - Public broadcasters - Content archival and search
        
        Client benefits reported:
        - 75% reduction in content preparation time
        - 99%+ compliance accuracy
        - Significant cost savings on manual processes
        - Improved content monetization opportunities
        """,
        
        "solutions": """
        Digital Nirvana provides solutions for:
        
        **Broadcasting:**
        - Live content monitoring and compliance
        - News content indexing and search
        - Sports highlight generation
        - Archive management and monetization
        
        **Media & Entertainment:**
        - Content library management
        - Rights management and tracking
        - Compliance monitoring
        - Multi-platform content distribution
        
        **Government & Public Sector:**
        - Secure media monitoring
        - Public records management
        - Compliance and audit trails
        - Multi-language content processing
        """,
        
        "contact": """
        Digital Nirvana Contact Information:
        
        Website: https://digital-nirvana.com/
        
        For Sales Inquiries: Contact through website or request a demo
        For Technical Support: support@digital-nirvana.com
        
        Services Available:
        - Product demos and consultations
        - Custom integration support
        - Training and onboarding
        - 24/7 technical support for enterprise clients
        - Custom development for specific workflow needs
        """
    }
    
    # Search through knowledge base for relevant information
    query_lower = query.lower()
    relevant_info = []
    
    # Check each category for relevant keywords
    if any(word in query_lower for word in ['company', 'about', 'digital nirvana', 'who', 'history']):
        relevant_info.append(knowledge_base['company'])
    
    if any(word in query_lower for word in ['product', 'solution', 'offer', 'service']):
        relevant_info.append(knowledge_base['products'])
    
    if any(word in query_lower for word in ['metadataiq', 'metadata', 'tagging', 'compliance']):
        relevant_info.append(knowledge_base['metadataiq'])
    
    if any(word in query_lower for word in ['monitoriq', 'transcription', 'trint', 'speech', 'monitor']):
        relevant_info.append(knowledge_base['monitoriq'])
    
    if any(word in query_lower for word in ['client', 'customer', 'cbs', 'fox', 'sinclair', 'user']):
        relevant_info.append(knowledge_base['clients'])
    
    if any(word in query_lower for word in ['contact', 'support', 'email', 'phone', 'reach']):
        relevant_info.append(knowledge_base['contact'])
    
    if any(word in query_lower for word in ['broadcast', 'media', 'government', 'entertainment']):
        relevant_info.append(knowledge_base['solutions'])
    
    # If no specific match, return general product info
    if not relevant_info:
        relevant_info = [knowledge_base['products'], knowledge_base['company']]
    
    return "\n\n".join(relevant_info)

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
            "description": "Get comprehensive information about Digital Nirvana, their products (MetadataIQ, MonitorIQ), services, clients, solutions, and company details. Use this for ANY question about Digital Nirvana, their offerings, or media intelligence solutions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The user's question or topic about Digital Nirvana to search for"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def get_ai_response(user_message):
    """Enhanced AI response handler with comprehensive Digital Nirvana knowledge"""
    print(f"You: {user_message}")
    
    client = client = AzureOpenAI(api_key=AZURE_API_KEY, 
    api_version=AZURE_API_VERSION, 
    azure_endpoint=AZURE_ENDPOINT)
    
    system_prompt = """You are a helpful AI assistant with comprehensive knowledge about Digital Nirvana and additional capabilities:

    **PRIMARY CAPABILITIES:**
    1. **Digital Nirvana Expertise**: Complete knowledge about Digital Nirvana's business including:
       - Company information, history, and mission
       - All products (MetadataIQ, MonitorIQ, etc.)
       - Solutions for broadcasting, media, transcription
       - Client testimonials and case studies (CBS, Fox, Sinclair)
       - Contact information and support options
       - Competitive advantages and positioning
    
    2. **Weather data**: Current weather for any city
    3. **Student profiles**: Database of student information
    4. **MetadataIQ FAQ**: Specific product FAQ responses

    **USAGE GUIDELINES:**
    
    - For ANY question about Digital Nirvana, their products, services, MonitorIQ, transcription, Trint alternatives, or media solutions → ALWAYS use get_digital_nirvana_info tool first
    
    - For specific MetadataIQ FAQ questions → use get_metadata_faq tool
    
    - For weather questions: get profiles first if needed, then weather
    
    - Always provide comprehensive, accurate responses based on the knowledge retrieved
    - Highlight key benefits and competitive advantages
    - Include relevant contact information when appropriate
    - Be knowledgeable about their enterprise focus and broadcast industry expertise"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # Main conversation loop
    while True:
        response = client.chat.completions.create(
            model="DEPLOYMENT_NAME",
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
    print("🤖 Digital Nirvana AI Assistant Started! (Type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = get_ai_response(user_input)
        print()  # Add spacing