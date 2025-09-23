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
from openai import OpenAI
import time

class MetadataIQAssistant:
    def __init__(self, assistant_id):
        self.client = OpenAI()
        self.assistant_id = assistant_id
        self.thread_id = None
        
    def start_conversation(self):
        """Start a new conversation thread"""
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
        return self.thread_id
    
    def send_message(self, message):
        """Send a message and get response from the assistant"""
        if not self.thread_id:
            self.start_conversation()
            
        try:
            # Add user message to thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role="user",
                content=message
            )
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread_id,
                assistant_id=self.assistant_id
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress']:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                # Get messages
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id,
                    order="asc"
                )
                
                # Return the latest assistant message
                latest_message = messages.data[0]
                if latest_message.role == "assistant":
                    return latest_message.content[0].text.value
                    
            elif run.status == 'failed':
                return f"Error: {run.last_error}"
                
        except Exception as e:
            return f"Exception: {e}"
    
    def get_conversation_history(self):
        """Get the full conversation history"""
        if not self.thread_id:
            return []
            
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id,
            order="asc"
        )
        
        conversation = []
        for message in reversed(messages.data):
            conversation.append({
                "role": message.role,
                "content": message.content[0].text.value,
                "timestamp": message.created_at
            })
        
        return conversation

# Usage example
if __name__ == "__main__":
    # Initialize the assistant (replace with your actual assistant ID)
    assistant = MetadataIQAssistant("asst_jC4nilY4HWxTtLwGTgy8qoFV
    
    print("MetadataIQ Assistant is ready!")
    print("Type 'quit' to exit, 'history' to see conversation history")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'history':
            history = assistant.get_conversation_history()
            for msg in history:
                print(f"{msg['role'].title()}: {msg['content']}")
            continue
            
        response = assistant.send_message(user_input)
        print(f"Assistant: {response}")