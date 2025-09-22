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
        

        # FAQ response function using OpenAI chat completions
        def get_faq_response(question):
            """Get an FAQ answer about Metadata IQ using OpenAI chat completion."""
            client = OpenAI(api_key=OPENAI_API_KEY)
            faq_system_prompt = (
                "You are a helpful assistant that answers customer FAQs about Metadata IQ. "
                "Always provide clear, concise, and accurate information about the product. "
                "Use the official product documentation and FAQs provided in your knowledge base as the source of truth. "
                "If you are unsure of an answer or if the question is outside the product’s scope, politely state that and suggest contacting support at support@digital-nirvana.com. "
                "Keep answers simple and easy to understand. "
                "Avoid making assumptions or providing information not related to Metadata IQ."
            )
            messages = [
                {"role": "system", "content": faq_system_prompt},
                {"role": "user", "content": question}
            ]
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=512
            )
            return response.choices[0].message.content
          "text": "We offer enterprise-grade support, onboarding, custom integration assistance, and ongoing training. Our team works directly with your engineers, compliance leads, and content managers to ensure success."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is metadata in broadcasting?\n\n"
        }
      ]
    },
    {
      "id": "msg_68cce3f04688819cbcbc471e4b6d9301003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "In broadcasting, metadata refers to additional information about video or audio content. This can include details like speaker names, timecodes, topics, as well as indicators of specific types of content such as profanity, political content, and more. This metadata is crucial for easy search, content organization, compliance with broadcasting standards, and monetization of content, especially in live and archived footage."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Why is automated metadata tagging important?\n\n"
        }
      ]
    },
    {
      "id": "msg_68cce3f69cb0819c8a86ffbe684e7eb4003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Automated metadata tagging is important for several reasons:\n\n1. Efficiency: Manual tagging is time-consuming and becomes increasingly difficult as the volume of content grows. Automated tagging saves time and increases efficiency.\n\n2. Accuracy: Manual tagging can lead to errors or inconsistencies. An automated system can ensure consistent, accurate metadata across all your content.\n\n3. Compliance: Automated tagging can identify and flag potentially sensitive or compliance-related content, minimizing the risk of non-compliance.\n\n4. Improved Search and Retrieval: Automated tagging enables better content searchability and retrieval by accurately categorizing data.\n\n5. Monetization: Accurate metadata tagging can help in better content organization and monetization."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "How does MetadataIQ automate metadata tagging?\n\n"
        }
      ]
    },
    {
      "id": "msg_68cce402acb8819c9387936ec3d92fad003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ automates metadata tagging through the use of advanced speech-to-text, video recognition, and rules-based engines. This allows it to recognize and automatically tag various elements in the content, reducing the need for manual input. \n\nMetadataIQ can apply custom tagging rules specified by the user, which is particularly beneficial for compliance with broadcast regulations. The system also generates comprehensive outputs that are audit-ready, saving users from potentially labor-intensive compliance processes."
        }
      ]
    },
    {
      "id": "msg_68cce40601b8819c81d3e47210b070dd003dd2b1dbb0d51c",
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
      "id": "msg_68cce40df9d0819c9b8f2722384052fc003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ can help significantly with broadcast compliance. It can automatically identify and tag content that may be sensitive to compliance issues such as political ads, brand mentions, profanity, and regulatory disclosures. By doing so, it ensures all content meets the requirements of local and global broadcast standards. This automated process reduces the risk of non-compliance and the potential penalties that may result from it."
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
      "id": "msg_68cce41d43f0819cb655b6c62b012baa003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ's Governance Dashboard offers a comprehensive overview of your content's metadata. It checks the quality and completeness of your metadata, assigns scores to your content, and flags any errors for correction. The dashboard also provides a full audit log, which is essential for regulatory compliance and internal checks. Essentially, it helps manage and organize your metadata, giving you a clearer understanding of your content's compliance and performance."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What regions or standards does MetadataIQ support for compliance tagging?\n\n"
        }
      ]
    },
    {
      "id": "msg_68cce429c984819ca0f9346d953e37a4003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ supports compliance needs for several regions and standards including the FCC for U.S. regulation, GDPR for the European Union, and Ofcom for the UK. Additionally, it can be customized to adhere to your internal protocols or specific regulations required by your clients. It's designed to be flexible so you can maintain compliance across various regulatory environments."
        }
      ]
    },
    {
      "id": "msg_68cce42c96fc819c8f12702bc27920f1003dd2b1dbb0d51c",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ supports region-specific compliance needs including FCC (U.S.), GDPR (EU), Ofcom (UK), and can be customized to support your internal or client-specific guidelines. It's an adaptable system that can be configured to meet the unique requirements of various stakeholders."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What platforms does MetadataIQ integrate with?\n\n"
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