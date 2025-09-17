# 🤖 AI Chatbot Frontend - Part 1: Simple Chat UI
#
# NOTE FOR ENTIRE EXERCISE:
# This frontend file (app.py) will NOT change throughout the 7-part tutorial.
# You will only work on different backend.py logic files for each part.
# When your initial backend.py is ready, uncomment lines 15-16 below to connect to your AI backend.

import streamlit as st
from backend import get_ai_response

print("🚀 Starting chatbot...")

# Configure the web page appearance
st.set_page_config(page_title="My First GPT Chat App", page_icon="🤖")
st.title("🤖 My First GPT Chat App")

# Create text input area for user messages
user_message = st.text_area("Your message:", height=100)

# Handle send button click
if st.button("📤 Send") and user_message:
     
    with st.spinner("Connecting to OpenAI..."):
        response = get_ai_response(user_message)
    

    # Display the conversation
    st.markdown("**You:**")
    st.write(user_message)

    
    st.markdown("**AI:**")
    st.write(response)
    
    
    
    
    
    
# --- Show Latest Commit Message ---
# This snippet displays the last commit message at the bottom-right of the Streamlit app.
# It first checks if a 'commit.txt' file exists (useful for deployments),
# otherwise it falls back to reading the latest commit from git.
# If neither is available, it shows a default message.
# No need to deep dive – just a simple way to know what version of code is running.


import subprocess, os
from pathlib import Path
 
st.markdown(f"<div style='position:fixed; bottom:20px; right:20px; color:gray; font-size:15px; opacity:0.8;'>{(Path(__file__).parent / 'commit.txt').read_text().strip() if (Path(__file__).parent / 'commit.txt').exists() else subprocess.getoutput('git log -1 --pretty=%B') if os.path.exists(Path(__file__).parent / '.git') else 'No commit info'}</div>", unsafe_allow_html=True)

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
          "text": "What is metadatiq"
        }
      ]
    },
    {
      "id": "msg_0464d0a6bd3271550068ca5087d11081a0bf3a403bf47f40ee",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata IQ is an on-premises, AI-powered tool developed by Digital Nirvana. It automates the generation, enrichment, and management of metadata for video and audio content. By integrating with Avid® MediaCentral | Production Management, Metadata IQ helps users easily tag, index, and organize their media assets, making content discovery, editing, and production workflows more efficient.\n\nIf you have more specific questions about its features or usage, feel free to ask!"
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
      "id": "msg_0464d0a6bd3271550068ca5e91a36c81a0af6722303ff7fb47",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "In broadcasting, metadata refers to information about media content, such as video or audio files. This information can include details like:\n\n- Title, description, and keywords\n- Date and time of creation or broadcast\n- Names of people involved (e.g., anchors, interviewees)\n- Locations and events\n- Technical details (e.g., format, duration, aspect ratio)\n- Usage rights and restrictions\n\nMetadata helps broadcasters efficiently organize, search for, and retrieve media assets. It also supports automated workflows, content distribution, compliance, and archiving.\n\nIf you’d like to know how Metadata IQ manages metadata in broadcasting, please let me know!"
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
      "id": "msg_0464d0a6bd3271550068ca5ea0582881a0aba3c8d5a5641368",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Automated metadata tagging is important because it:\n\n1. **Saves Time and Labor**: Automatically adding metadata eliminates the need for manual tagging, which is time-consuming and prone to errors.\n\n2. **Improves Searchability**: Rich, accurate metadata makes it easy to find and retrieve media assets quickly.\n\n3. **Enhances Workflow Efficiency**: Automated tagging streamlines production, editing, and archiving processes, allowing teams to work faster and more effectively.\n\n4. **Ensures Consistency**: Automated tools apply standardized metadata, reducing inconsistencies that can occur with manual entry.\n\n5. **Supports Compliance and Rights Management**: Proper metadata helps track content usage and ensures compliance with legal and licensing requirements.\n\nMetadata IQ automates the metadata generation process, bringing all these benefits to media organizations and broadcasters.\n\nIf you have more questions about automated metadata tagging or how Metadata IQ works, feel free to ask!"
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
      "id": "msg_0464d0a6bd3271550068ca5ea887e081a081c7f21e19c1e7de",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata IQ automates metadata tagging by using artificial intelligence (AI) and machine learning (ML) technologies. Here’s how it works:\n\n1. **Content Ingestion**: Metadata IQ ingests video or audio files from your media workflows.\n\n2. **AI-Powered Analysis**: The tool automatically analyzes the content to detect and extract useful information, such as spoken words (speech-to-text), face and object recognition, scene changes, and more.\n\n3. **Metadata Generation**: Based on this analysis, Metadata IQ generates rich and accurate metadata tags, including keywords, descriptions, timestamps, speakers, and other relevant details.\n\n4. **Integration with Avid**: The tool integrates directly with Avid® MediaCentral | Production Management, so the generated metadata is added to your media assets within your existing workflows.\n\n5. **Search and Retrieval**: With detailed metadata automatically applied, it becomes much easier to search, find, and manage your media content.\n\nIf you need more technical details or have a specific use case, feel free to ask!"
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
      "id": "msg_0464d0a6bd3271550068ca5eb9e19481a097d2198721ef7ab4",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, Metadata IQ can help with broadcast compliance. By automatically generating detailed and accurate metadata for your media content, Metadata IQ makes it easier to:\n\n- Track and log broadcast content \n- Identify sensitive material or restricted content\n- Ensure that required information is tagged for regulatory purposes\n- Retrieve specific content quickly for review or reporting\n\nAccurate metadata supports broadcasters in meeting legal, ethical, and contractual requirements by providing clear records of what was aired and making compliance workflows more efficient.\n\nIf you have specific compliance needs, you can contact support at support@digital-nirvana.com for more detailed guidance."
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
      "id": "msg_0464d0a6bd3271550068ca5ec5c34481a0a3b238e5c97537d6",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "The Metadata IQ governance dashboard provides a centralized interface for users to monitor and manage the metadata generation process. Through the dashboard, you can:\n\n- **Track Progress**: View real-time status updates of media files being processed.\n- **Monitor Quality**: Check the quality and accuracy of generated metadata.\n- **Manage Workflows**: Oversee and control metadata extraction jobs or batches.\n- **Audit Activity**: Review logs and activity history for governance and compliance purposes.\n\nThis dashboard helps ensure transparency, accountability, and quality control in your metadata workflows.\n\nIf you need more detailed information about the governance dashboard features, please contact support@digital-nirvana.com."
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
      "id": "msg_0464d0a6bd3271550068ca5ecd9ed081a09f12c57d1ed9e09d",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata IQ is designed to help with compliance needs, but the specific regions or regulatory standards supported for compliance tagging may depend on your organization’s setup and requirements. Metadata IQ’s automated metadata generation and integration with Avid® MediaCentral help facilitate compliance workflows commonly used in broadcasting, such as content logging and reporting.\n\nHowever, for detailed information about supported regions or specific legal standards (such as FCC in the US, Ofcom in the UK, or others), please contact support@digital-nirvana.com. They can provide the most accurate and up-to-date information based on your compliance requirements."
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
      "id": "msg_0464d0a6bd3271550068ca5eeccdb881a0a0ce9b613842711f",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Metadata IQ is designed to integrate primarily with **Avid® MediaCentral | Production Management** (formerly known as Avid Interplay). This integration allows users to seamlessly generate, enrich, and manage metadata within their existing Avid media workflows.\n\nIf you need information about integration with additional platforms, please contact support@digital-nirvana.com for the latest compatibility details."
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
      "id": "msg_0464d0a6bd3271550068ca5f5d33c481a09cff712a16b95fbc",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "MetadataIQ is primarily used in the broadcast and media industries, including:\n\n- Television networks and stations\n- News organizations\n- Sports broadcasters\n- Media production and post-production houses\n- Content archives and libraries\n\nThese organizations use MetadataIQ to automate metadata generation, improve content searchability, streamline workflows, and support compliance efforts."
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
      "id": "msg_0464d0a6bd3271550068ca5f82c61881a0a813e9c59597fc22",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ works with archived content. You can use MetadataIQ to process and enrich metadata for existing or previously archived video and audio files. This helps improve searchability, organization, and retrieval of legacy media assets within your library or archive."
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
      "id": "msg_0464d0a6bd3271550068ca5f8ca2b481a0bcfa6ad1d3c38caa",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Yes, MetadataIQ can help with the monetization of old content. By automatically generating rich, accurate metadata for archived media, it makes it easier to search, discover, and repurpose valuable content. This improved organization enables you to identify opportunities to reuse and license historical footage, clips, or programs, increasing the potential for monetization."
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
          "text": "We offer enterprise-grade support, onboarding, custom integration assistance, and ongoing training. Our team works directly with your engineers, compliance leads, and content managers to ensure success.\nMetadataIQ offers dedicated customer support to help with setup, configuration, troubleshooting, and ongoing usage. Support is available through:\n\n- **Email:** You can reach the support team at support@digital-nirvana.com for assistance with any questions or technical issues.\n- **Documentation and FAQs:** Official product documentation and FAQs are available to guide users through installation, integration, and everyday operation.\n\nFor specific or complex needs, the support team can provide personalized guidance and solutions."
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