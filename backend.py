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
          "text": You are a helpful assistant that answers customer FAQs about Metadata IQ.\nAlways provide clear, concise, and accurate information about the product.\nUse the official product documentation and FAQs provided in your knowledge base as the source of truth.\nIf you are unsure of an answer or if the question is outside the product’s scope, politely state that and suggest contacting support at support@digital-nirvana.com.\nKeep answers simple and easy to understand.\nAvoid making assumptions or providing information not related to Metadata IQ."
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
          "text": "What is metadata in broadcasting?"
        }
      ]
    },
    {
      "id": "msg_68d1152beac0819fa724b8042b56df100627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata in broadcasting is information that describes your audio or video content. Examples include program titles, speaker names, topics, keywords, timecodes, and compliance details. This data makes it easier to search, manage, and ensure regulatory compliance for broadcast content."
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
      "id": "msg_68d115335260819f82058bb042b794640627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Automated metadata tagging is important because it saves time, reduces human error, and ensures consistent, accurate tagging across large volumes of content. This makes it easier to find, manage, and ensure compliance of your media assets quickly and efficiently."
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
      "id": "msg_68d115388ce4819f9ed1e772a81c53640627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ automates metadata tagging by using technologies like speech-to-text, video recognition, and rules-based engines. It processes your audio and video content, applies custom tagging rules for compliance, and generates audit-ready metadata without the need for manual input."
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
      "id": "msg_68d1153ff9f8819fb1aa66afc905d3ff0627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ can help with broadcast compliance. It automatically identifies and tags compliance-sensitive content such as political ads, brand mentions, profanity, and regulatory disclosures, making it easier to meet local and global broadcast standards."
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
      "id": "msg_68d1154783e8819f88c3b31189f658df0627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ’s governance dashboard provides a centralized view of your metadata’s completeness and quality. It scores your content, highlights any errors or gaps, and maintains detailed audit logs. This helps you monitor compliance, streamline quality checks, and prepare for internal or external reviews."
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
      "id": "msg_68d1154e2168819fb20eee81751701bd0627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ supports compliance tagging for various regional and international standards, including FCC (U.S.), GDPR (EU), Ofcom (UK), and can be tailored to meet your specific internal or client compliance requirements."
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
      "id": "msg_68d11554c5ac819faf9c95a6e82f784d0627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ integrates with platforms such as Avid MediaCentral, Telestream, Grass Valley, and many leading DAM and MAM systems. Custom integrations can also be developed to fit your specific enterprise workflow needs."
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
      "id": "msg_68d1155c1ab4819f89b9a583d6ef1c120627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ can be deployed on-premises, in the cloud, or as a hybrid solution, depending on your workflow and infrastructure requirements. This flexibility ensures it fits smoothly into your existing media environment."
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
      "id": "msg_68d11561ff68819fb68d666f4addab0c0627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ is suitable for live content. It can process and tag live audio and video in real time, making it ideal for news, sports, events, and other live broadcast scenarios where immediate metadata generation is essential."
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
      "id": "msg_68d115673688819fb166104b8891f8ab0627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ delivers broadcast-grade accuracy and reliability. Its metadata tagging is specifically designed and tuned for professional media workflows and compliance requirements, ensuring consistently high-quality results compared to generic AI solutions."
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
      "id": "msg_68d1156ba464819f9d530384031958990627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ is used by broadcasters, sports networks, government media organizations, public broadcasters, media archives, and any industry that requires accurate, large-scale metadata management for audio and video content."
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
      "id": "msg_68d115725fb4819f89dd2b7e01bf03690627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ works with archived content. It can process and enrich existing archives, making old footage searchable, compliant, and ready for new opportunities such as repurposing or monetization."
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
      "id": "msg_68d115776d18819f81eee9cc9d8658f30627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ can help with monetization of old content. By applying accurate and consistent metadata to your archived footage, it makes it easier to search, discover, and license historical content, unlocking new revenue opportunities from your existing media library."
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
      "id": "msg_68d115806870819f942244fa2adb68900627e616ed5f0a0f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ offers enterprise-grade support, including onboarding, custom integration assistance, ongoing training, and troubleshooting. Our support team works closely with your technical and content teams to ensure smooth implementation and optimal use of the platform. For additional help, you can contact support at support@digital-nirvana.com."
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