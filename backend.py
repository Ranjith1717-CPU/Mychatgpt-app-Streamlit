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
    }
]

def get_ai_response(user_message):
    """AI response handler with tool calling"""
    print(f"You: {user_message}")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    system_prompt = """You are a helpful assistant with access to weather data and student profiles.
    
    For weather questions about someone's location: first get their profile, then get weather for their city.
    Describe weather naturally (sunny, cloudy, rainy, warm, etc.) based on temperature.
    
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
            else:
                result = "Unknown tool"
            
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.id
            })
# FAQ metadata
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-4.1",
  input=[
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "ou are a helpful assistant that answers customer FAQs about Metadata IQ.\nAlways provide clear, concise, and accurate information about the product.\nUse the official product documentation and FAQs provided in your knowledge base as the source of truth.\nIf you are unsure of an answer or if the question is outside the product’s scope, politely state that and suggest contacting support at support@digital-nirvana.com.\nKeep answers simple and easy to understand.\nAvoid making assumptions or providing information not related to Metadata IQ."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is metadata in broadcasting?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata in broadcasting refers to descriptive information about video or audio content—such as speaker names, timecodes, topics, profanity, political content, and more. It enables easier search, compliance, and monetization across live and archived footage."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Why is automated metadata tagging important?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Manual tagging is time-consuming, error-prone, and unsustainable at scale. Automated tagging ensures consistent, accurate metadata that saves time, reduces compliance risks, and enables faster content retrieval."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "How does MetadataIQ automate metadata tagging?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ uses advanced speech-to-text, video recognition, and rules-based engines to auto-tag metadata across content types. It applies custom tagging rules for compliance and generates audit-ready outputs without manual input."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Can MetadataIQ help with broadcast compliance?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes. MetadataIQ automatically identifies and tags compliance-sensitive content like political ads, brand mentions, profanity, and regulatory disclosures—ensuring every piece of content meets local and global broadcast standards."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "How does MetadataIQ's governance dashboard work?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "The dashboard tracks the completeness and quality of your metadata. It scores content, flags errors, and provides full audit logs—so you're always prepared for internal checks or third-party reviews."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What regions or standards does MetadataIQ support for compliance tagging?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ supports region-specific compliance needs including FCC (U.S.), GDPR (EU), Ofcom (UK), and can be customized to support your internal or client-specific guidelines."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What platforms does MetadataIQ integrate with?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ integrates seamlessly with Avid MediaCentral, Telestream, Grass Valley, and a wide range of DAM and MAM systems. Custom connectors can be built for enterprise workflows."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Is MetadataIQ available as SaaS or on-premises?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ is available via enterprise deployment models and is typically implemented within your infrastructure alongside your media tools. Cloud and hybrid setups are also supported based on your workflow."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Is MetadataIQ suitable for live content?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Absolutely. MetadataIQ can process and tag live content in real time—making it ideal for news, sports, and event broadcasting where quick turnaround is critical."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "How accurate is MetadataIQ's metadata tagging?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ is broadcast-grade, meaning it's built for high accuracy and reliability. Unlike generic AI tools, our tagging engine is trained and tuned for professional media workflows and compliance-sensitive use cases."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What industries use MetadataIQ?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "While built for broadcasters, MetadataIQ is also used by sports networks, government media teams, public broadcasters, media archives, and any organization that needs high-volume, high-accuracy metadata management."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Does MetadataIQ work with archived content?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes. MetadataIQ is used to retroactively process and enrich archives, making decades of stored footage searchable, monetizable, and compliant with current regulations."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Can MetadataIQ help with monetization of old content?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes. By applying consistent metadata across your archives, MetadataIQ helps you resurface, repackage, and license old footage more efficiently—turning dormant content into new revenue opportunities."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What kind of support does MetadataIQ offer?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "We offer enterprise-grade support, onboarding, custom integration assistance, and ongoing training. Our team works directly with your engineers, compliance leads, and content managers to ensure success."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "wHAT IS METADATA"
        }
      ]
    },
    {
      "id": "msg_68cbcee817d0819e9e25fcd9d333bb73005d9ea2b95a488f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata is information that describes other data. In the context of media and video, metadata refers to details about the media file, such as the title, description, keywords, duration, timestamps, speakers, and technical information. Metadata helps organize, search, manage, and retrieve media content more efficiently.\n\nIf you have more specific questions about metadata or how it works with Metadata IQ, feel free to ask!"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "WHAT IS METADATAIQ"
        }
      ]
    },
    {
      "id": "msg_68cbcef47628819ebb08b2938f3d6fcc005d9ea2b95a488f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata IQ is an AI-powered software solution developed by Digital Nirvana. It automatically generates and manages metadata for media assets, specifically video and audio content. Metadata IQ integrates with editing platforms like Avid MediaCentral, making it easier for content creators and broadcasters to tag, organize, search, and retrieve their media files.\n\nKey features of Metadata IQ include:\n\n- Automated speech-to-text transcription\n- Facial recognition and object identification\n- Contextual keyword and topic extraction\n- Seamless export and import of metadata to popular video editing systems\n\nMetadata IQ helps streamline media workflows, saves time on manual tagging, and improves the discoverability of media assets.\n\nFor more information, please let me know or visit the official documentation!"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What kind of support does MetadataIQ offer?"
        }
      ]
    },
    {
      "id": "msg_68cbd09d9b6c819e8f9a5f91895383a0005d9ea2b95a488f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ offers enterprise-grade support, including onboarding, custom integration assistance, and ongoing training. The support team works closely with your engineers, compliance leads, and content managers to ensure successful deployment and use of the platform. If you need further assistance, you can also contact support at support@digital-nirvana.com."
        }
      ]
    }
  ],
  text={
    "format": {
      "type": "text"
    }
  },
  reasoning={},
  tools=[],
  temperature=1,
  max_output_tokens=2048,
  top_p=1,
  store=True,
  include=["web_search_call.action.sources"]
)