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
        "company": """
        **Digital Nirvana Company Overview:**
        
        Digital Nirvana is a leading provider of AI-powered media intelligence solutions, transforming how broadcasters and media organizations manage, search, and monetize their content globally.
        
        **Mission:** Transform media workflows through automated metadata generation, transcription services, and intelligent content management solutions.
        
        **Core Focus Areas:**
        - Broadcasting and Media Intelligence
        - Content Compliance and Governance  
        - Media Asset Management
        - Transcription and Captioning Services
        - Cloud Engineering Solutions
        - Data Intelligence and AI/ML Services
        - Investment Research
        - Learning Management Solutions
        
        **Global Reach:** Serving major broadcasters, media organizations, educational institutions, and enterprises worldwide with enterprise-grade solutions.
        
        **Website:** https://digital-nirvana.com/
        """,
        
        "monitoriq": """
        **MonitorIQ: The Ultimate Broadcast Signal Monitoring Tool**
        
        MonitorIQ is Digital Nirvana's comprehensive content monitoring, compliance logging, and verification solution for broadcasters.
        
        **Key Capabilities:**
        
        1. **Ad Performance Verification & Sales Empowerment:**
           - Intuitive self-service tool for sales and executive teams
           - Quick spot-check ads and verify proof of performance
           - Effortlessly reconcile traffic logs with aired recordings
           - Boost sales effectiveness with optimal ad performance tracking
        
        2. **Quality of Experience (QoE) Monitoring:**
           - Proactive alarms for visual impairments affecting service quality
           - Visibility into every transmission and delivery point
           - Return path monitoring to validate viewer experience
           - Deliver flawless content and keep viewers captivated
        
        3. **Compliance Logging (Internal & External):**
           - Track and report on loudness compliance effortlessly
           - Monitor internal standards and practices for continuity
           - Ensure closed caption compliance (CC608, CC708, international standards)
           - Real-time alerting for compliance issues
           - Seamless operations with automated compliance logging
        
        4. **Content Monitoring for Unparalleled Efficiency:**
           - Access 1 to 100+ channel recordings from any web browser
           - Instant access to critical content and metadata with single click
           - Record content from any video or audio source
           - View content in any combination of live or historical recordings
           - Competitive ratings monitoring for performance insights
        
        **Benefits:**
        - Single platform for all monitoring needs
        - Eliminate ad performance issues
        - Ensure consistent service quality
        - Close compliance gaps automatically
        - Revolutionize content monitoring efficiency
        
        **Target Users:** Broadcasters, media companies, sales teams, compliance officers, quality assurance teams
        
        **URL:** https://digital-nirvana.com/monitoriq-broadcasting-signal-monitoring/
        """,
        
        "metadataiq": """
        **MetadataIQ: Enterprise-Grade Metadata Automation for Broadcasters**
        
        MetadataIQ is the backbone of broadcast metadata workflows, simplifying broadcast operations and ensuring compliance at scale.
        
        **Core Value Proposition:**
        "Automate metadata tagging, track quality, and meet broadcast standards at scale with enterprise-grade precision, real-time dashboards, and seamless integrations."
        
        **Key Features:**
        
        1. **Deeply Integrated, Natively Built:**
           - No third-party hassles or workarounds
           - Metadata automation built directly into Avid & Grass Valley
           - No extra plugins required
           - Seamless native integration with existing infrastructure
        
        2. **Automated Metadata Tagging Engine:**
           - Advanced speech-to-text technology
           - Video recognition capabilities
           - Rules-based auto-tagging across content types
           - Custom tagging rules for compliance
           - Audit-ready outputs without manual input
        
        3. **Compliance Tagging & Rules Engine:**
           - Be compliant by default - never worry about missed disclosures
           - Automatic identification of political ads, brand mentions, profanity
           - Regulatory disclosure tracking
           - Content compliance identification (violence, nudity for post-production)
           - Supports FCC (U.S.), GDPR (EU), Ofcom (UK), and custom guidelines
        
        4. **Speed & Accuracy:**
           - Slash turnaround time without sacrificing accuracy
           - Process 10 hours or 10,000 hours with same precision
           - Accessible metadata delivered in minutes
           - Fast, scalable, and always precise
        
        5. **Broadcast-Grade Integrations:**
           - Integrate seamlessly with what you already use
           - Direct integration with Avid MediaCentral
           - Works with Telestream, Grass Valley
           - Compatible with DAM and MAM systems
           - Custom connectors for enterprise workflows
        
        6. **Real-Time Live Processing:**
           - Go from live to logged in seconds
           - Capture, tag, and validate live streams on the fly
           - Process and tag live content in real-time
           - Critical for news, sports, and event broadcasting
        
        7. **Governance Dashboard & Quality Scoring:**
           - Track metadata completeness and quality
           - Score content automatically
           - Flag errors proactively
           - Full audit logs for compliance
           - Always prepared for internal checks or third-party reviews
        
        8. **Batch Scheduling & Pipeline Automation:**
           - Automate large-scale processing
           - Schedule batch operations
           - Pipeline automation for consistent workflows
        
        **Industry Applications:**
        
        - **Broadcasting:** Precise metadata tagging for seamless content search, compliance, and faster distribution
        - **Production:** Automate metadata generation to streamline editing and speed up project timelines
        - **News:** Quickly tag and index breaking news clips for timely, relevant content delivery
        - **Sports:** Generate precise metadata for live games, faster clip creation, and highlight reels
        - **Archives:** Simplify large-scale media cataloging, making historical assets easily searchable
        
        **Trusted By:** CBS, Fox Broadcasting, Sinclair Broadcasting, and other Tier-1 broadcasters worldwide
        
        **Competitive Advantages:**
        - Only solution natively built into Avid & Grass Valley
        - Battle-tested in world's largest networks
        - Enterprise-grade precision and reliability
        - Comprehensive compliance coverage
        - Real-time processing capabilities
        - Governance and quality tracking
        
        **Benefits:**
        - Less searching, more creating - get hours back in your day
        - Content becomes instantly searchable
        - Metadata works while you create
        - Find, decide, clip, deliver - all in minutes
        - 90%+ reduction in manual tagging time
        - Ensures broadcast compliance automatically
        - Makes archived content searchable and monetizable
        
        **Deployment:** Enterprise deployment models, on-premises, cloud, and hybrid setups supported
        
        **URL:** https://digital-nirvana.com/metadataiq-media-indexing-pam-mam/
        """,
        
        "mediaservicesiq": """
        **MediaServicesIQ: AI/ML Content Optimization Platform**
        
        Transform media management and content optimization with automated AI-powered features.
        
        **Key Features:**
        
        1. **Podcast Enhancement:**
           - Automatic chapter marker generation
           - Content summarization and segmentation
           - Improved content navigation for consumers
           - Automated content classification
           - Keyword generation for enhanced SEO
           - Increased consumer engagement
        
        2. **Music Licensing Management:**
           - Auto-identification of music content
           - Artist, title, and publisher information extraction
           - Automated visibility into licensing status
           - Quickly identify compliant and expired licenses
           - Time-coded speech-to-text integration
           - Content-based metadata generation
           - Works regardless of MAM/PAM setup
           - Supports news, sports, and entertainment content
        
        3. **Ad Monitoring & Revenue Optimization:**
           - Automate ad monitoring and reporting
           - Extract brand, product, and category information effortlessly
           - Eliminate manual content logging
           - Save time and expenses on manual processes
           - Maximize revenue with contextual ad insertion
           - Use transcript metadata for intelligent ad placement
        
        **Benefits:**
        - Streamline music licensing processes
        - Ensure compliance automatically
        - Enhance podcast discoverability
        - Maximize revenue potential
        - Reduce manual effort significantly
        
        **Target Users:** Podcasters, content creators, media companies, broadcasters, music supervisors, ad operations teams
        
        **URL:** https://digital-nirvana.com/mediaservicesiq-ai-ml-content-optimization/
        """,
        
        "tranceiq": """
        **TranceIQ: Transcription, Captioning & Subtitle Platform**
        
        Ultimate platform revolutionizing transcription, captioning, subtitle generation, and publishing with automated tools.
        
        **Core Capabilities:**
        
        1. **Automated Transcript Generation:**
           - 50%+ efficiency improvement vs traditional methods
           - Support for 30+ native source languages
           - 90%+ accuracy levels for machine transcripts
           - Quick turnaround times
           - Saves time and enhances productivity
        
        2. **Caption Creation for Wide Accessibility:**
           - Intuitive interface for seamless caption creation
           - Automatically conform transcripts into captions
           - Adherence to major outlet style guidelines:
             * Amazon Prime
             * Netflix
             * Hulu
             * And more
           - Improve accessibility for users anywhere, anytime
           - Access from any web-enabled device
           - Ensure broadcast compliance
        
        3. **Subtitle Generation & Localization:**
           - Expand global reach and monetization opportunities
           - Auto-translate captions into 100+ languages
           - Translation within same session for seamless localization
           - Repurpose assets in different languages
           - Facilitate distribution in international regions
           - Unlock new monetization from existing media assets
        
        4. **Publishing & Fulfillment:**
           - Deliver content in all industry-supported formats
           - Sidecar file fulfillment option
           - Embedded captions/subtitles within media file
           - Direct API integration with enterprise production systems
           - User-friendly web portal
           - Seamless workflow integration
        
        **Benefits:**
        - Boost efficiency and accuracy
        - Enhance accessibility compliance
        - Expand global reach
        - Unlock international markets
        - Simplify publishing workflows
        
        **Target Users:** Content creators, broadcasters, streaming platforms, educational institutions, global distributors
        
        **URL:** https://digital-nirvana.com/tranceiq-transcription-captioning-subtitle/
        """,
        
        "media_enrichment": """
        **Media Enrichment Services: Effortless Media Accessibility**
        
        Expert services providing transcripts, captions, translations, and more with unmatched accuracy and flexible turnaround times.
        
        **Services Offered:**
        
        1. **Captioning Services:**
           - **Closed Captioning:** Cloud-based for live broadcasts, pre-recorded TV shows, online videos, sports events
           - **Live Captioning:** Real-time captioning with advanced speech-to-text technology and expert captioners
           - **Caption Conformance:** Ensuring captions meet platform requirements
           - Accurate captions anytime, anywhere
        
        2. **Transcription Services:**
           - Live transcription with real-time accuracy
           - Field & TV show transcription
           - Reality show scripts to financial analysis
           - Versatile across industries:
             * Finance
             * Healthcare
             * Legal
             * Technology
             * Broadcasting
             * Media and entertainment
           - Unparalleled accuracy and efficiency
        
        3. **Subs N Dubs (Subtitling & Dubbing):**
           - AI-powered subtitles and dubbing
           - Break down language barriers
           - Natural-sounding voiceovers
           - Accurate captions tailored for every audience
           - From corporate training to viral content
           - Seamless localization with cultural adaptation
           - Works for:
             * Businesses
             * Educators
             * Media creators
             * Global brands
           - Single video or entire content library support
           - 60+ languages supported
        
        4. **Translation Services:**
           - Expert precision for wide range of documents
           - Accuracy and cultural sensitivity
           - Skilled linguists bridging communication gaps
           - Industries served:
             * Legal contracts
             * Medical reports
             * Technical manuals
             * Marketing materials
           - Diverse document formats and lengths
           - Seamless cross-lingual communication
        
        5. **Subtitle Translation:**
           - Translate subtitles directly from source to target language
           - Streamline localization process
           - 60+ languages support
           - Globally skilled team
           - Proprietary Trance software
           - High-quality translations
           - Rapid turnarounds
        
        **Digital Nirvana Advantage:**
        - Personalized service with dedicated support
        - Data security and reliability
        - Global reach with multilingual expertise
        - Exceptional support team
        - Flexible turnaround times
        - Unmatched accuracy and quality
        
        **URL:** https://digital-nirvana.com/media-enrichment-solutions/
        """,
        
        "cloud_engineering": """
        **Cloud Engineering: Transform IT with Seamless, Scalable Solutions**
        
        Simplify cloud transition with seamless, efficient migration while you focus on scaling your business.
        
        **Core Services:**
        
        1. **Cloud Strategy, Design, and Migration:**
           - Seamless transition to scalable future
           - Tailor-made cloud strategy
           - Readiness assessments
           - Hybrid architecture design
           - Flawless migration execution
           - Seamless application moves
           - Leverage cutting-edge tools
           - Gain scalable infrastructure adapting to business growth
           - Say goodbye to complexity, embrace growth with confidence
        
        2. **Cloud-Native Development and Automation:**
           - Faster deployments, smarter operations
           - Accelerate business with cloud-native applications
           - Design for speed and reliability
           - Containerization services
           - CI/CD pipeline implementation
           - Streamline updates for seamless deployments
           - Serverless technologies
           - Workflow automation reducing manual tasks
           - Focus on innovation
           - Greater agility and productivity
           - Bring ideas to market faster
        
        3. **Cloud Security, Management, and Optimization:**
           - Uncompromising security and efficiency
           - Stay secure without sacrificing performance
           - Compliance-driven security measures
           - Advanced threat detection
           - Always protected cloud environment
           - Optimize costs and minimize risks
           - Enhance efficiency with proactive monitoring
           - Right-sized resources
           - Resilient cloud environment
        
        4. **Data Services and Cloud Integration:**
           - Unlock data-driven insights
           - Transform data into actionable decisions
           - Cloud database migration
           - AI/ML integration
           - Build smart analytics pipelines
           - Real-time insights generation
           - Empower data to drive business forward
           - Automated solutions streamlining processing
           - Boost scalability
           - Provide actionable intelligence
           - Enable faster, informed decision-making
        
        5. **Reliable Connectivity, Expert Guidance:**
           - Stay connected with confidence
           - Secure VPCs and hybrid connections
           - Seamless multiple environment integration
           - Expert guidance at every step:
             * Strategic advice
             * Readiness assessments
             * Technology enablement
           - Navigate cloud journey effortlessly
           - Growth as top priority
        
        **Digital Nirvana Cloud Advantage:**
        - Proven expertise in cloud engineering
        - End-to-end solutions
        - Tailored solutions for growth
        - Cutting-edge technology
        - Security and compliance first
        - Industry-leading insights
        
        **Target Clients:** Media companies moving to cloud, broadcasters seeking cloud solutions, content platforms needing scalability, enterprises requiring cloud transformation
        
        **URL:** https://digital-nirvana.com/cloud-engineering/
        """,
        
        "data_intelligence": """
        **Data Intelligence: Make Data Your Competitive Advantage**
        
        Transform unstructured data into actionable intelligence driving smarter business decisions.
        
        **Core Services:**
        
        1. **Prompt Engineering:**
           - Boost AI precision with tailored inputs
           - Design inputs extracting maximum value from AI
           - Understanding language model intricacies
           - Deliver precise, impactful results every time
           - No more guesswork
           - Smarter, faster, more accurate AI outputs
        
        2. **Data Wrangling:**
           - Say goodbye to messy data for good
           - Expert data wrangling services
           - Clean and organize data into reliable, consistent formats
           - Ready-to-use data for analysis
           - Make informed decisions
           - Avoid costly errors
           - Propel business free from disorganized information
        
        3. **Data Labeling:**
           - Train AI models like industry leaders
           - Transform raw data into valuable assets
           - Precise and accurate labeling
           - Support for text, images, and video
           - Expert annotation ensuring AI models learn effectively
           - AI models that perform flawlessly
           - Labeled data easy for algorithms to understand and use
        
        4. **Model Validation:**
           - Deploy AI primed for success
           - Model validation process tests, adjusts, and optimizes
           - Ensure models generalize well on new data
           - Hyperparameter tuning
           - Stress-testing for reliability
           - Guarantee AI performs reliably
           - Deploy with complete peace of mind
        
        5. **Advanced Analytics:**
           - Turn raw data into game-changing decisions
           - Crystal-clear view of business's future
           - Advanced analytics tools diving deep into datasets
           - Deliver insights guiding strategic decisions
           - Spot trends and predict outcomes
           - Stay ahead of competition with actionable intelligence
        
        **Digital Nirvana Data Intelligence Advantages:**
        
        - **Tailored Solutions:** Personalized service with dedicated account managers, customized solutions aligned with specific needs
        - **Data Security:** Top-tier security and reliable processes, protect valuable datasets
        - **Scalability:** Solutions that grow with you, from small business to global powerhouse
        - **Expertise:** Years of experience in media, investment, and compliance
        - **Automation:** Automated precision supercharging workflows, ML-enhanced data labeling
        - **Support:** Count on anytime, anywhere exceptional support
        - **Global Reach:** Multilingual expertise, accurate labeling in various languages
        
        **Target Clients:** AI companies, ML model developers, enterprises needing data services, businesses requiring analytics
        
        **URL:** https://digital-nirvana.com/data-intelligence-solutions/
        """,
        
        "investment_research": """
        **Investment Research Solutions: Transform Data into Investment Decisions**
        
        From capturing earnings calls to delivering concise summaries, empower investors with noise-free insights for better decision-making.
        
        **Core Services:**
        
        1. **Financial Reporting Insights:**
           - Get real-time insights from earnings calls as they happen
           - Live-streaming transcripts providing competitive advantage
           - Respond insightfully and make informed investment decisions
           - Real-time access to conversations
           - Follow key points, identify trends, gauge sentiment
           - Direct from the source information
           - Stay ahead of competition
           - Make decisions based on latest, most accurate information
        
        2. **Corporate Event Calendar:**
           - Every important event instantly at fingertips
           - Stay effortlessly updated with accurate, timely records
           - Precise and efficient tracking of corporate events
           - Clear and actionable insights
           - Comprehensive event data for analysis and monitoring
           - Uncover valuable trends in market activities
           - Make informed decisions, spot opportunities
           - Understand financial outcomes with ease
        
        3. **Insights and Summaries:**
           - Complex data into key points, instantly
           - Transform vast information into concise, actionable insights
           - Summarization service distilling complex data
           - Save time and effort
           - Equip with informed decision-making
           - Significantly enhance investment research by:
             * Saving time
             * Identifying key trends
             * Extracting actionable insights
             * Improving efficiency
        
        4. **Market Intel & Research:**
           - Market intel on demand
           - Data analytics combined with industry expertise
           - Tailored solutions for target market
           - Analyze market size, customer behavior, competitor landscape
           - Deliver actionable insights for informed business decisions
           - Whether launching new product, expanding market, or optimizing marketing
           - Market research giving competitive edge
        
        **Digital Nirvana's Investment Research Edge:**
        - Personalized service
        - Data security and reliability
        - Global reach
        - Exceptional support
        - Trusted by financial institutions
        
        **Target Clients:** Financial institutions, investment firms, research analysts, portfolio managers, hedge funds, asset management companies
        
        **URL:** https://digital-nirvana.com/investment-research-solutions/
        """,
        
        "learning_management": """
        **Learning Management Solutions: Your Entire Academic Ecosystem, Seamlessly Managed**
        
        Empower learning with accurate academic assessments, engaging content development, advanced captioning for accessibility, and secure proctoring services.
        
        **Core Services:**
        
        1. **Comprehensive Academic Assessments:**
           - Empowering students, simplifying educators
           - Assessments spanning subjects and proficiency levels
           - Holistic LSRW (Listening, Speaking, Reading, Writing) evaluations
           - Constructive feedback for personalized growth
           - Fast, insightful reports saving educators' time
           - Fuel student potential
        
        2. **Content Development and Management:**
           - Your classroom in every pocket
           - Engaging multimedia content creation
           - Diverse assessment development
           - Seamless lifecycle management
           - Ensure quality education at every step
           - Tailored for institutions and education-focused firms
           - Create captivating learning materials
           - Align with curricular standards
           - Foster educational excellence
        
        3. **Advanced Lecture Captioning Services:**
           - Education without barriers
           - Real-time transcripts, captions, and translations
           - Seamless learning experience
           - AI-powered real-time transcription
           - Multilingual translation services
           - Specially designed for universities and schools
           - Empower all students with real-time access
           - Accurate content enhancing inclusivity and engagement
        
        4. **Adaptive Proctoring Services:**
           - Ultimate test security in your hands
           - Ensuring test integrity and security
           - Seamless proctoring with real-time monitoring
           - AI behavior analysis
           - Secure both in-person and online exams
           - Prevent cheating and ensure authentic assessments
           - Advanced technology integration
        
        **Academic Excellence Features:**
        - Decades of expertise
        - Precision evaluators
        - Holistic framework
        - Confidential and secure
        
        **Target Clients:** Educational institutions, universities, schools, corporate training departments, e-learning platforms, professional development organizations
        
        **URL:** https://digital-nirvana.com/learning-management-solutions/
        """,
        
        "clients": """
        **Digital Nirvana's Trusted Client Base**
        
        **Major Broadcasters:**
        - **CBS:** Uses MetadataIQ for content management and compliance across operations
        - **Fox Broadcasting:** Leverages automated metadata for news and sports programming
        - **Sinclair Broadcasting:** Implements Digital Nirvana solutions across multiple stations nationwide
        - Other Tier-1 broadcasters globally
        
        **Client Success Stories:**
        - 75% reduction in content preparation time
        - 99%+ compliance accuracy achieved
        - Significant cost savings on manual processes
        - Improved content monetization opportunities
        - Faster time-to-air for breaking news
        - Enhanced searchability of archived content
        
        **Industries Served:**
        - Broadcasting and Television Networks
        - Streaming Platforms
        - Sports Networks
        - News Organizations
        - Government Media Agencies
        - Public Broadcasters
        - Educational Institutions
        - Financial Services
        - Media Archives
        - Production Companies
        - Content Creators
        
        **Testimonials:**
        "If CBS, Fox, and Sinclair trust it, you can too. MetadataIQ runs inside the world's largest networks. It's battle-tested, deeply integrated, and ready to support any team that values speed, scale, and precision."
        """,
        
        "contact": """
        **Contact Digital Nirvana**
        
        **Website:** https://digital-nirvana.com/
        
        **Product Pages:**
        - MonitorIQ: https://digital-nirvana.com/monitoriq-broadcasting-signal-monitoring/
        - MetadataIQ: https://digital-nirvana.com/metadataiq-media-indexing-pam-mam/
        - MediaServicesIQ: https://digital-nirvana.com/mediaservicesiq-ai-ml-content-optimization/
        - TranceIQ: https://digital-nirvana.com/tranceiq-transcription-captioning-subtitle/
        - Media Enrichment: https://digital-nirvana.com/media-enrichment-solutions/
        - Cloud Engineering: https://digital-nirvana.com/cloud-engineering/
        - Data Intelligence: https://digital-nirvana.com/data-intelligence-solutions/
        - Investment Research: https://digital-nirvana.com/investment-research-solutions/
        - Learning Management: https://digital-nirvana.com/learning-management-solutions/
        
        **For Inquiries:**
        - Schedule a demo through the website
        - Request product demonstrations
        - Contact for sales inquiries
        - Technical support available
        
        **Services Available:**
        - Product demos and consultations
        - Custom integration support
        - Training and onboarding programs
        - 24/7 technical support for enterprise clients
        - Custom development for specific workflow needs
        - Strategic advice and readiness assessments
        
        **Enterprise Support:**
        - Dedicated account managers
        - Priority support for enterprise clients
        - Custom SLA agreements
        - Ongoing training and assistance
        """
    }
    
    # Intelligent query matching with comprehensive keyword detection
    query_lower = query.lower()
    relevant_info = []
    
    # Product-specific queries
    if any(word in query_lower for word in ['monitoriq', 'monitor iq', 'signal monitoring', 'broadcast monitoring', 'ad verification', 'qoe', 'quality of experience', 'compliance logging']):
        relevant_info.append(knowledge_base['monitoriq'])
    
    if any(word in query_lower for word in ['metadataiq', 'metadata iq', 'metadata', 'tagging', 'compliance', 'governance', 'avid', 'grass valley']):
        relevant_info.append(knowledge_base['metadataiq'])
    
    if any(word in query_lower for word in ['mediaservicesiq', 'media services', 'chapter marker', 'podcast', 'music licensing', 'ad monitoring']):
        relevant_info.append(knowledge_base['mediaservicesiq'])
    
    if any(word in query_lower for word in ['tranceiq', 'trance iq', 'transcription', 'caption', 'subtitle', 'translation', 'localization']):
        relevant_info.append(knowledge_base['tranceiq'])
    
    if any(word in query_lower for word in ['media enrichment', 'subs n dubs', 'subtitling', 'dubbing', 'live captioning']):
        relevant_info.append(knowledge_base['media_enrichment'])
    
    if any(word in query_lower for word in ['cloud engineering', 'cloud migration', 'cloud strategy', 'cloud native', 'containerization', 'serverless']):
        relevant_info.append(knowledge_base['cloud_engineering'])
    
    if any(word in query_lower for word in ['data intelligence', 'data wrangling', 'data labeling', 'prompt engineering', 'model validation', 'analytics']):
        relevant_info.append(knowledge_base['data_intelligence'])
    
    if any(word in query_lower for word in ['investment research', 'earnings call', 'financial reporting', 'market intel', 'corporate event']):
        relevant_info.append(knowledge_base['investment_research'])
    
    if any(word in query_lower for word in ['learning management', 'academic assessment', 'proctoring', 'education', 'e-learning']):
        relevant_info.append(knowledge_base['learning_management'])
    
    # General company queries
    if any(word in query_lower for word in ['company', 'about', 'digital nirvana', 'who', 'overview', 'what is']):
        relevant_info.append(knowledge_base['company'])
    
    if any(word in query_lower for word in ['product', 'solution', 'offer', 'service', 'all products']):
        relevant_info.extend([
            knowledge_base['company'],
            knowledge_base['monitoriq'],
            knowledge_base['metadataiq'],
            knowledge_base['mediaservicesiq'],
            knowledge_base['tranceiq']
        ])
    
    if any(word in query_lower for word in ['client', 'customer', 'cbs', 'fox', 'sinclair', 'who uses']):
        relevant_info.append(knowledge_base['clients'])
    
    if any(word in query_lower for word in ['contact', 'support', 'demo', 'reach', 'sales', 'inquiry']):
        relevant_info.append(knowledge_base['contact'])
    
    # If no specific match, return general overview
    if not relevant_info:
        relevant_info = [knowledge_base['company']]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_info = []
    for item in relevant_info:
        if item not in seen:
            seen.add(item)
            unique_info.append(item)
    
    return "\n\n---\n\n".join(unique_info)

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
            "description": """Get comprehensive information about Digital Nirvana and ALL their products/services including:
            - MonitorIQ (broadcast signal monitoring, ad verification, QoE monitoring, compliance logging)
            - MetadataIQ (metadata automation, compliance tagging, governance, Avid/Grass Valley integration)
            - MediaServicesIQ (podcast optimization, music licensing, ad monitoring)
            - TranceIQ (transcription, captioning, subtitling, translation)
            - Media Enrichment (captioning services, Subs N Dubs, translation)
            - Cloud Engineering (cloud migration, cloud-native development, security, optimization)
            - Data Intelligence (prompt engineering, data wrangling, labeling, model validation, analytics)
            - Investment Research (earnings calls, financial reporting, market intelligence)
            - Learning Management (academic assessments, content development, proctoring, lecture captioning)
            - Company information, clients (CBS, Fox, Sinclair), and contact details
            
            Use this for ANY question about Digital Nirvana, their offerings, products, services, or solutions.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The user's question about Digital Nirvana to search for"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def get_ai_response(user_message):
    """Azure OpenAI response handler with comprehensive Digital Nirvana knowledge"""
    print(f"You: {user_message}")
    
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )
    
    system_prompt = """You are a highly knowledgeable AI assistant specializing in Digital Nirvana's complete product portfolio and services.

**YOUR EXPERTISE COVERS:**

1. **Broadcasting & Media Products:**
   - MonitorIQ: Broadcast signal monitoring, ad verification, QoE monitoring, compliance logging
   - MetadataIQ: Metadata automation, compliance tagging, native Avid/Grass Valley integration
   - MediaServicesIQ: AI-powered content optimization, podcast enhancement, music licensing
   - TranceIQ: Transcription, captioning, subtitling in 100+ languages

2. **Professional Services:**
   - Media Enrichment: Expert captioning, transcription, Subs N Dubs, translation services
   - Cloud Engineering: Cloud strategy, migration, cloud-native development, security
   - Data Intelligence: Prompt engineering, data wrangling, labeling, model validation
   - Investment Research: Earnings call transcription, financial insights, market intelligence
   - Learning Management: Academic assessments, content development, proctoring, accessibility

3. **Company Knowledge:**
   - Trusted by CBS, Fox Broadcasting, Sinclair Broadcasting
   - Enterprise-grade solutions for broadcasters and media organizations globally
   - Native integrations with Avid MediaCentral and Grass Valley
   - Battle-tested in world's largest broadcast networks

**INSTRUCTIONS:**

- For ANY question about Digital Nirvana, their products, services, or solutions → ALWAYS use get_digital_nirvana_info tool
- Provide comprehensive, detailed responses based on retrieved knowledge
- Highlight key benefits, features, and competitive advantages
- Mention relevant client success stories when appropriate
- Include contact information and relevant URLs when helpful
- Be enthusiastic about Digital Nirvana's capabilities and proven track record
- Focus on how solutions solve real broadcast and media challenges

**IMPORTANT:** You have access to complete, detailed information about all Digital Nirvana products. Always provide thorough, accurate answers that demonstrate deep product knowledge."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # Main conversation loop
    while True:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
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

# Example usage
if __name__ == "__main__":
    print("🤖 Enhanced Digital Nirvana Assistant Started!")
    print("Ask me anything about Digital Nirvana's products and services!")
    print("(Type 'quit' to exit)\n")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = get_ai_response(user_input)
        print()# 🤖 Azure OpenAI Digital Nirvana Chat Backend
# This version uses Azure OpenAI instead of regular OpenAI

# Import necessary libraries
import requests    # For making web requests
import json       # For handling JSON data
from openai import AzureOpenAI  # Azure OpenAI Python library
import psycopg2   # For database connections
import streamlit as st  # For building the web app

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
    """Azure OpenAI response handler with comprehensive Digital Nirvana knowledge"""
    print(f"You: {user_message}")
    
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )
    
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
            model=AZURE_OPENAI_DEPLOYMENT_NAME,  # Using Azure deployment name instead of model name
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
    print("🤖 Azure OpenAI Digital Nirvana Assistant Started! (Type 'quit' to exit)")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = get_ai_response(user_input)
        print()  # Add spacing