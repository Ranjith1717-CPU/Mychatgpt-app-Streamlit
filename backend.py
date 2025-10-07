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
        
        **Tagline:** Automate Workflows, Streamline Operations, Comply with Regulations, & Drive Insights with AI
        
        **Mission:** Harness the power of AI for unparalleled efficiency. Our innovative solutions optimize processes, saving time and resources while delivering actionable intelligence.
        
        **What We Do:** Digital Nirvana optimizes your media, data, and compliance workflows with advanced AI, turning time-consuming processes into seamless tasks.
        
        **Core Products:**
        - MonitorIQ: Ensures your broadcasts stay compliant and high-quality by monitoring, analyzing, and storing your content seamlessly, letting you focus on engaging your audience
        - MetadataIQ: Boosts content discoverability by automating media metadata creation, making it easier to organize, find, and repurpose assets within your media management systems
        - MediaServicesIQ: Enhances your content's performance with automated workflows for summarization, ad tracking, and licensing, allowing you to optimize media management effortlessly
        
        **Bespoke Solutions:**
        Accelerating the delivery of critical business outcomes across the Media & Entertainment, Financial Services, Education, Legal, Healthcare, and Technology Sectors.
        
        - Media Enrichment: Boost Productivity, Save Time, and Optimize Costs with AI-Powered Solutions
        - Cloud Engineering: Elevate Your Business with Scalable, Secure Cloud Solutions
        - Data Intelligence: Turn Data Into Your Competitive Advantage with Intelligent Data Solutions
        - Investment Research: Empower Your Investment Decisions with Real-Time Financial Insights and Summaries
        - Learning Management: Elevate assessments, Ensure integrity, improve outcomes, and streamline learning management
        
        **Industries Transformed:**
        - Media & Entertainment: Optimize productivity and reduce costs with AI-powered captions, subtitles, dubbing, media analysis, and monitoring
        - Financial Services: Access precise transcription and AI-driven insights for investor calls, earnings reports, and compliance
        - Education: Enrich learning with captions, secure proctoring, and engaging multimedia content
        - Legal, Healthcare, and Technology sectors
        
        **Website:** https://digital-nirvana.com/
        
        **Company Values:** Innovation, Efficiency, Accuracy, Customer Success, AI-Powered Solutions
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
        **Media Enrichment: Boost Productivity, Save Time, and Optimize Costs with AI-Powered Solutions**
        
        **Overview:**
        Delivering highly accurate machine-generated and human-curated captions, subtitles, dubbing, media analysis, and media monitoring services, our solutions empower diverse industries to elevate their content accessibility, global reach, and audience engagement. From enhancing media workflows to providing actionable insights, we transform businesses and streamline daily operations with precision and efficiency.
        
        **YES! Digital Nirvana provides comprehensive dubbing services through Subs N Dubs.**
        
        Expert services providing dubbing, transcripts, captions, translations, and more with unmatched accuracy and flexible turnaround times.
        
        **Services Offered:**
        
        1. **Subs N Dubs (AI-Powered Subtitling & Dubbing) - DUBBING SERVICES:**
           - **YES - Digital Nirvana provides professional dubbing services**
           - **AI-powered subtitling and dubbing solution that transforms content into multiple languages with precision**
           - Break down language barriers effortlessly for businesses, educators, media creators, and global brands
           - From corporate training videos to viral content, Subs N Dubs delivers natural-sounding voiceovers and accurate captions tailored for every audience
           
           **Dubbing Capabilities:**
           - Natural-sounding voiceovers for videos
           - AI-powered voice dubbing in 60+ languages
           - Cultural adaptation ensuring messages resonate authentically
           - Professional voice talent for high-quality dubbing
           - Transform content from single videos to entire content libraries
           - Seamless localization for global audiences
           - Whether it's a single video or an entire content library, Subs N Dubs ensures seamless localization with cultural adaptation, so your message lands right every time, everywhere
           - Experience global reach without the traditional hassle
           
           **Key Features:**
           - Transform content from single videos to entire libraries
           - Seamless localization ensuring messages land right every time
           - Cultural adaptation for authentic communication
           - Quick turnaround times without compromising quality
           - Experience global reach without traditional hassle
           
           **Ideal For:**
           - Businesses expanding globally
           - Educators creating multilingual content
           - Media creators reaching international audiences
           - Global brands
           - Corporate training videos
           - Viral content localization
           - Entertainment content dubbing
           - E-learning courses
           - Marketing videos
           
           **Languages:** 60+ languages supported with globally skilled team and professional voice talent
        
        2. **Captioning Services:**
           - **Accurate Captions Anytime, Anywhere**
           - **Accurate closed captioning, live captioning, caption conformance, and lecture captioning for all industries**
           - Delivering cloud-based closed captioning for live broadcasts, pre-recorded TV shows, online videos, sports events, and more with advanced speech-to-text technology and expert captioners
           
           **Types of Captioning:**
           - **Closed Captioning:** Cloud-based for live broadcasts, pre-recorded content
           - **Live Captioning:** Real-time captioning with expert captioners
           - **Caption Conformance:** Ensuring captions meet platform requirements and style guidelines
           - **Lecture Captioning:** Specialized for educational content
           
           For all industries including broadcasting, education, entertainment, corporate
        
        3. **Transcription Services:**
           - **Create accurate transcripts and index them with video content**
           - **Tag metadata and integrate it into content management systems**
           - From reality show scripts to financial analysis, our versatile transcription services deliver unparalleled accuracy and efficiency
           
           **Applications:**
           - Live transcription with real-time accuracy for immediate documentation
           - Field & TV show transcription
           - Reality show scripts
           - Financial analysis
           
           **Industries:**
           - Finance
           - Healthcare
           - Legal
           - Technology
           - Broadcasting
           - Media and entertainment
           
           Unparalleled accuracy and efficiency across all industries
        
        4. **Subtitling Services:**
           - **Subtitles in over 20 languages with quick turnaround times**
           - **Localize translations directly from the source language**
           - Streamline your process by translating subtitles directly from the source language to your desired language
           - Enhancing localization and reliability without compromising quality or speed
           - Experience seamless subtitling in over 60+ languages with our globally skilled team and proprietary Trance software
           - Ensuring high-quality translations and rapid turnarounds
        
        5. **Translation Services:**
           - **Your words, their language**
           - Translate a wide range of documents with expert precision
           - Ensuring accuracy and cultural sensitivity
           - Our skilled linguists bridge communication gaps across industries:
             * Legal contracts
             * Medical reports
             * Technical manuals
             * Marketing materials
           - Diverse document formats and lengths
           - Precise translations that meet your requirements
           - Seamless cross-lingual communication
        
        **Digital Nirvana Advantage:**
        - Personalized service with dedicated support
        - Data security and reliability
        - Global reach with multilingual expertise (60+ languages)
        - Exceptional support team (24/7 operations)
        - Flexible turnaround times
        - Unmatched accuracy and quality
        - Technology-aided workflow with experienced professionals
        - Ability to accommodate rush orders and change requests
        
        **URL:** https://digital-nirvana.com/media-enrichment-solutions/
        """
        
        2. **Captioning Services:**
           - **Accurate Captions Anytime, Anywhere**
           - **Closed Captioning:** Cloud-based for live broadcasts, pre-recorded TV shows, online videos, sports events
           - **Live Captioning:** Real-time captioning with advanced speech-to-text technology and expert captioners
           - **Caption Conformance:** Ensuring captions meet platform requirements and style guidelines
           - Accurate closed captioning, live captioning, caption conformance, and lecture captioning
           - For all industries including broadcasting, education, entertainment
        
        3. **Transcription Services:**
           - **Create accurate transcripts and index them with video content**
           - Tag metadata and integrate into content management systems
           - Live transcription with real-time accuracy for immediate documentation
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
        
        4. **Subtitling Services:**
           - **Subtitles in over 20 languages with quick turnaround times**
           - Localize translations directly from the source language
           - Experience seamless subtitling in 60+ languages
           - Globally skilled team with proprietary Trance software
           - High-quality translations with rapid turnarounds
           - Quick turnaround times for urgent projects
        
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
        **Cloud Engineering: Elevate Your Business with Scalable, Secure Cloud Solutions**
        
        **Overview:**
        Streamline your operations and scale effortlessly with expert cloud strategies, seamless migrations, and cutting-edge automation. Our cloud engineering services enable businesses to optimize performance, enhance security, and reduce costs, delivering a future-ready infrastructure that grows with you.
        
        Transform your IT with seamless, scalable Cloud Engineering solutions. We simplify your cloud transition with seamless, efficient migration, allowing you to focus on scaling your business while we handle the technical complexities.
        
        **Core Services:**
        
        1. **Cloud Strategy, Design, and Migration:**
           - **Seamless Transition to a Scalable Future**
           - Transform your business with a tailor-made cloud strategy
           - From readiness assessments to hybrid architecture design, we ensure a flawless migration
           - Why wait for the future? Move your applications seamlessly, leverage cutting-edge tools, and gain a scalable infrastructure that adapts to your business growth
           - Say goodbye to complexity and embrace growth with confidence
           
           **What We Provide:**
           - Readiness assessments
           - Hybrid architecture design
           - Flawless migration execution
           - Seamless application moves
           - Cutting-edge tools and technologies
           - Scalable infrastructure adapting to business growth
        
        2. **Cloud-Native Development and Automation:**
           - **Faster Deployments, Smarter Operations**
           - Accelerate your business with cloud-native applications designed for speed and reliability
           - Our containerization and CI/CD pipelines streamline updates for seamless deployments
           - Transform your workflows with serverless technologies and automation, reducing manual tasks so you can focus on innovation
           - Achieve greater agility, boost productivity, and bring your ideas to market faster
           
           **Technologies & Solutions:**
           - Cloud-native application development
           - Containerization services
           - CI/CD pipeline implementation
           - Streamlined updates and deployments
           - Serverless technologies
           - Workflow automation
           - Reduced manual tasks
           - Focus on innovation
           - Greater agility and productivity
           - Faster time to market
        
        3. **Cloud Security, Management, and Optimization:**
           - **Uncompromising Security and Efficiency**
           - Stay secure without sacrificing performance
           - Our compliance-driven security measures and advanced threat detection ensure your cloud environment is always protected
           - Optimize costs, minimize risks, and enhance efficiency with proactive monitoring and right-sized resources
           - Get a cloud environment that's as resilient as your business ambitions
           
           **Security & Optimization Features:**
           - Compliance-driven security measures
           - Advanced threat detection
           - Always protected cloud environment
           - Cost optimization
           - Risk minimization
           - Proactive monitoring
           - Right-sized resources
           - Enhanced efficiency
           - Resilient cloud environment
        
        4. **Data Services and Cloud Integration:**
           - **Unlock Data-Driven Insights**
           - Transform your data into actionable decisions
           - From cloud database migration to AI/ML integration, we help you build smarter analytics pipelines for real-time insights
           - Empower your data to drive your business forward
           - Our automated solutions streamline processing, boost scalability, and provide actionable intelligence, enabling faster, more informed decision-making
           
           **Data Solutions:**
           - Cloud database migration
           - AI/ML integration
           - Smart analytics pipelines
           - Real-time insights generation
           - Automated data processing solutions
           - Boosted scalability
           - Actionable intelligence
           - Faster, informed decision-making
        
        5. **Reliable Connectivity, Expert Guidance:**
           - **Stay Connected with Confidence**
           - Our secure VPCs and hybrid connections ensure seamless multiple environment integration
           - Get expert guidance at every step, from strategic advice and readiness assessments to technology enablement
           - We're here to help you navigate your cloud journey effortlessly with your growth as our top priority
           
           **Support & Guidance:**
           - Secure VPCs
           - Hybrid connections
           - Seamless multi-environment connectivity
           - Expert guidance at every step
           - Strategic advice
           - Readiness assessments
           - Technology enablement
           - Navigate cloud journey effortlessly
           - Growth as top priority
        
        **Digital Nirvana Cloud Engineering Advantage:**
        - Proven expertise in cloud engineering
        - End-to-end solutions
        - Tailored solutions for growth
        - Cutting-edge technology
        - Security and compliance first
        - Industry-leading insights
        - Future-ready infrastructure
        - Optimize performance, enhance security, reduce costs
        
        **Target Clients:** Media companies moving to cloud, broadcasters seeking cloud solutions, content platforms needing scalability, enterprises requiring cloud transformation
        
        **URL:** https://digital-nirvana.com/cloud-engineering/
        """,
        
        "data_intelligence": """
        **Data Intelligence: Make Data Your Competitive Advantage**
        
        Digital Nirvana's Data Intelligence services transform unstructured data into actionable intelligence driving smarter business decisions.
        
        **Core Services:**
        
        1. **Data Labeling:**
           - **Deliver accurate annotations across text, images, audio, and video**
           - Digital Nirvana's labeling services ensure your data is optimized to power AI models
           - Improving prediction accuracy and performance
           - Train AI models like industry leaders
           - Transform raw data into valuable assets
           - Precise and accurate labeling
           - Support for text, images, audio, and video
           - Expert annotation ensuring AI models learn effectively
           - AI models that perform flawlessly
           - Labeled data easy for algorithms to understand and use
        
        2. **Model Validation:**
           - **Assess and verify predictive models to ensure accuracy on unseen data**
           - With expert validation and hyperparameter tuning, we optimize your AI models for peak performance
           - Delivering dependable results
           - Deploy AI primed for success
           - Model validation process tests, adjusts, and optimizes
           - Ensure models generalize well on new data
           - Hyperparameter tuning
           - Stress-testing for reliability
           - Guarantee AI performs reliably
           - Deploy with complete peace of mind
        
        3. **Data Analytics:**
           - **Turn complex datasets into actionable insights**
           - Digital Nirvana's solutions help you make informed decisions across various fields
           - From predictive analytics to detailed visualizations
           - Crystal-clear view of business's future
           - Advanced analytics tools diving deep into datasets
           - Deliver insights guiding strategic decisions
           - Spot trends and predict outcomes
           - Stay ahead of competition with actionable intelligence
           - Transform vast amounts of information into concise, actionable insights
        
        4. **Prompt Engineering:**
           - **Design tailored inputs that enable AI models to deliver precise, impactful results**
           - Maximize the accuracy and utility of your AI with expertly crafted prompts that drive success
           - Boost AI precision with tailored inputs
           - Design inputs extracting maximum value from AI
           - Understanding language model intricacies
           - Deliver precise, impactful results every time
           - No more guesswork
           - Smarter, faster, more accurate AI outputs
        
        5. **Data Wrangling:**
           - **Transform and structure messy data into a usable format**
           - Ensure your data is consistent, accurate, and ready for in-depth analysis
           - Paving the way for smarter business decisions
           - Say goodbye to messy data for good
           - Expert data wrangling services
           - Clean and organize data into reliable, consistent formats
           - Ready-to-use data for analysis
           - Make informed decisions
           - Avoid costly errors
           - Propel business free from disorganized information
        
        **Digital Nirvana Data Intelligence Advantages:**
        
        - **Tailored Solutions:** Personalized service with dedicated account managers, customized solutions aligned with specific needs
        - **Data Security:** Top-tier security and reliable processes, protect valuable datasets
        - **Scalability:** Solutions that grow with you, from small business to global powerhouse
        - **Expertise:** Years of experience in media, investment, and compliance
        - **Automation:** Automated precision supercharging workflows, ML-enhanced data labeling
        - **Support:** Count on anytime, anywhere exceptional support
        - **Global Reach:** Multilingual expertise, accurate labeling in various languages
        
        **Target Clients:** AI companies, ML model developers, enterprises needing data services, businesses requiring analytics, organizations building AI/ML solutions
        
        **URL:** https://digital-nirvana.com/data-intelligence-solutions/
        """,
        
        "investment_research": """
        **Investment Research: Empower Your Investment Decisions with Real-Time Financial Insights and Summaries**
        
        **Overview:**
        Providing accurate, real-time financial event transcripts, summaries, and in-depth market research. Our solutions streamline investment research, helping you make quick, informed decisions that keep you ahead in the market.
        
        Transform Data into Investment Decisions Seamlessly. From capturing every word of earnings calls with live transcription to delivering concise summaries, we empower investors with noise-free insights for better decision-making. Stay ahead with our comprehensive research solutions.
        
        **Core Services:**
        
        1. **Financial Reporting Insights (Earnings Insights, Instantly):**
           - **Get real-time insights from earnings calls as they happen**
           - Our live-streaming transcripts provide the advantage you need to respond insightfully and make informed investment decisions
           - Don't wait for the news
           - With real-time access to the conversation, you can follow key points, identify trends, and gauge sentiment directly from the source
           - Stay ahead of the competition by making informed decisions based on the latest and most accurate information
           
           **Benefits:**
           - Real-time earnings call insights
           - Live-streaming transcripts
           - Follow key points as they happen
           - Identify trends immediately
           - Gauge sentiment directly from source
           - Make informed investment decisions instantly
           - Stay ahead of competition
           - Latest and most accurate information
        
        2. **Corporate Event Calendar (Every Important Event, Instantly at Your Fingertips):**
           - **Stay effortlessly updated with accurate and timely records of all important financial events**
           - Our calendaring services provide precise and efficient tracking of corporate events, offering you clear and actionable insights
           - Comprehensive event data helps you analyze, monitor, and uncover valuable trends in market activities
           - Get the information you need to make informed decisions, spot opportunities, and understand financial outcomes - all with ease
           
           **Features:**
           - Accurate and timely records of financial events
           - Precise corporate event tracking
           - Efficient calendaring services
           - Clear and actionable insights
           - Comprehensive event data
           - Analyze and monitor market activities
           - Uncover valuable trends
           - Make informed decisions
           - Spot opportunities
           - Understand financial outcomes with ease
        
        3. **Insights and Summaries (Complex Data into Key Points, Instantly):**
           - **Transform vast amounts of information into concise, actionable insights**
           - Our summarization service distills complex data into key takeaways, saving time and effort while equipping you with informed decision-making
           - Summarization significantly enhances investment research by:
             * Saving time
             * Identifying key trends
             * Extracting actionable insights
             * Improving efficiency
           
           **Value Proposition:**
           - Transform vast information into concise insights
           - Distill complex data into key takeaways
           - Save time and effort
           - Equip with informed decision-making capabilities
           - Significantly enhance investment research
           - Extract actionable insights from complex datasets
        
        4. **Market Intel & Research (Market Intel, On Demand):**
           - **Data analytics combined with industry expertise to provide tailored solutions for your target market**
           - By analyzing market size, customer behavior, and competitor landscape, we deliver actionable insights to help you make informed business decisions
           - Whether launching a new product, expanding into a new market, or optimizing your marketing strategy, our market research will give you a competitive edge
           
           **Research Capabilities:**
           - Data analytics with industry expertise
           - Tailored solutions for target market
           - Market size analysis
           - Customer behavior insights
           - Competitor landscape analysis
           - Actionable insights delivery
           - Support for:
             * Launching new products
             * Expanding into new markets
             * Optimizing marketing strategies
           - Competitive edge in decision-making
        
        **Digital Nirvana's Investment Research Edge:**
        - Personalized service
        - Data security and reliability
        - Global reach
        - Exceptional support
        - Real-time access to financial information
        - Accurate transcripts (best accuracy imaginable)
        - Quick turnaround: 3-4 hours vs 6+ hours with other providers
        - Noise-free insights
        - Comprehensive research solutions
        - Trusted by financial institutions
        
        **Target Clients:** Financial institutions, investment firms, research analysts, portfolio managers, hedge funds, asset management companies, investor relations teams
        
        **URL:** https://digital-nirvana.com/investment-research-solutions/
        """,
        
        "learning_management": """
        **Learning Management: Elevate Assessments, Ensure Integrity, Improve Outcomes, and Streamline Learning Management**
        
        **Overview:**
        Language LSRW and mathematics evaluation, performance assessments, scoring, grading, and skill assessments. Streamline evaluation processes, ensure accurate scoring, and gain valuable performance and skill development insights.
        
        Your Entire Academic Ecosystem, Seamlessly Managed. Empower learning with accurate academic assessments, engaging content development, advanced captioning for accessibility, and secure proctoring services.
        
        **Core Services:**
        
        1. **Comprehensive Academic Assessments:**
           - **Empowering Students, Simplifying Educators: Comprehensive Academic Assessments**
           - Assessments span subjects and proficiency levels, providing holistic LSRW evaluations and constructive feedback for personalized growth
           - Fast, insightful reports save educators' time and fuel student potential
           - Language LSRW (Listening, Speaking, Reading, Writing) evaluation
           - Mathematics evaluation
           - Performance assessments
           - Scoring and grading services
           - Skill assessments
           
           **Benefits:**
           - Holistic LSRW evaluations
           - Constructive feedback for personalized growth
           - Fast, insightful reports
           - Save educators' time
           - Fuel student potential
           - Streamline evaluation processes
           - Ensure accurate scoring
           - Gain valuable performance insights
           - Track skill development
        
        2. **Content Development and Management:**
           - **Your Classroom in Every Pocket: Content Development and Management**
           - Engaging multimedia content, diverse assessments, and seamless lifecycle management
           - Our service ensures quality education at every step
           - Tailored for institutions and education-focused firms
           - We create captivating learning materials that align with curricular standards and foster educational excellence
           
           **What We Provide:**
           - Engaging multimedia content creation
           - Diverse assessment development
           - Seamless content lifecycle management
           - Quality education at every step
           - Captivating learning materials
           - Align with curricular standards
           - Foster educational excellence
           - Tailored for educational institutions
           - Support for education-focused firms
        
        3. **Advanced Lecture Captioning Services:**
           - **Education Without Barriers: Real-Time Transcripts, Captions, and Translations**
           - Experience seamless learning with Digital Nirvana's AI-powered real-time transcription, captioning, and multilingual translation services specially designed for universities and schools
           - Empower all students with real-time access to accurate content, enhancing inclusivity and engagement
           
           **Accessibility Features:**
           - AI-powered real-time transcription
           - Live captioning for lectures
           - Multilingual translation services
           - Specially designed for universities and schools
           - Real-time access to accurate content
           - Enhance inclusivity
           - Improve engagement
           - Remove learning barriers
           - Support diverse student needs
        
        4. **Adaptive Proctoring Services:**
           - **Ultimate Test Security in Your Hands: Ensuring Test Integrity and Security**
           - Experience seamless proctoring with real-time monitoring and AI behavior analysis
           - Secure both in-person and online exams, preventing cheating and ensuring authentic assessments with advanced technology integration
           
           **Proctoring Capabilities:**
           - Seamless proctoring experience
           - Real-time monitoring
           - AI behavior analysis
           - Secure in-person exams
           - Secure online exams
           - Prevent cheating
           - Ensure authentic assessments
           - Advanced technology integration
           - Test integrity guaranteed
           - Ultimate test security
        
        **Academic Excellence Features:**
        - **Decades of Expertise:** Years of experience in educational assessment and content development
        - **Precision Evaluators:** Accurate scoring and detailed performance insights
        - **Holistic Framework:** Comprehensive approach to learning management
        - **Confidential and Secure:** Data protection and privacy for all educational content
        
        **Target Clients:** Educational institutions, universities, schools, colleges, corporate training departments, e-learning platforms, professional development organizations, EdTech companies
        
        **URL:** https://digital-nirvana.com/learning-management-solutions/
        """,
        
        "clients": """
        **Digital Nirvana's Trusted Client Base & Success Stories**
        
        **Major Broadcasters:**
        - **CBS:** Uses MetadataIQ for content management and compliance across operations
        - **Fox Broadcasting:** Leverages automated metadata for news and sports programming
        - **Sinclair Broadcasting:** Implements Digital Nirvana solutions across multiple stations nationwide
        - Other Tier-1 broadcasters globally
        
        **Client Success Stories:**
        
        **1. Hollywood Media-Processing Powerhouse - Closed Captioning Success:**
        "Digital Nirvana's technology-aided workflow and highly experienced captioners have been successfully delivering captions according to customer requirements and within the required turnaround time of 24 to 48 hours. In fact, thanks to 24/7 operations and a strong customer support team, Digital Nirvana has been able to exceed customer expectations in terms of output quality, delivery time, and the ability to accommodate rush orders and change requests. It has enabled us to redeploy personnel to other core functions instead of spending valuable time on vendor management, project monitoring, and QC."
        
        **2. Financial Markets - Transcription Solutions:**
        "Digital Nirvana proved that when we cover the same call for multiple companies, we have various teams in place making numerous transcripts of the same call. Their scoring technique shows that they were able to offer financial transcripts with the best accuracy imaginable. They can turn complete transcripts around very quickly, usually within three to four hours compared to six hours or more with other providers."
        
        **3. Spanish Media Giant - AI-Enabled Multilingual Translation:**
        "We chose Digital Nirvana's for captioning solutions based on their unique capabilities: Ability to generate translations almost instantly using existing closed-caption files and then export new, publish-ready sidecar files for OTT platforms. A rapid turnaround time that is virtually unheard of in the captioning industry, with the ability to reduce the captioning time for a specific program from 15 hours to less than two and the ability to view caption streams for multiple languages in a single interface is a game changer."
        
        **Proven Results:**
        - 75% reduction in content preparation time
        - 99%+ compliance accuracy achieved
        - Significant cost savings on manual processes
        - Improved content monetization opportunities
        - Faster time-to-air for breaking news
        - Enhanced searchability of archived content
        - 24/7 operations with exceptional customer support
        - Ability to handle rush orders and change requests
        - 3-4 hour turnaround for financial transcripts vs 6+ hours with competitors
        - Captioning time reduced from 15 hours to less than 2 hours
        
        **Industries Served:**
        - Broadcasting and Television Networks
        - Streaming Platforms (OTT)
        - Sports Networks
        - News Organizations
        - Government Media Agencies
        - Public Broadcasters
        - Educational Institutions
        - Financial Services
        - Media Archives
        - Production Companies
        - Content Creators
        
        **Why Clients Choose Digital Nirvana:**
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
    
    if any(word in query_lower for word in ['tranceiq', 'trance iq']):
        relevant_info.append(knowledge_base['tranceiq'])
    
    # Captioning, transcription, subtitling, dubbing - can be in both TranceIQ and Media Enrichment
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

def get_ai_response(user_message, conversation_history=None):
    """Azure OpenAI response handler with comprehensive Digital Nirvana knowledge and conversation continuity"""
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
   - Media Enrichment: Expert captioning, transcription, Subs N Dubs (AI-powered subtitling & dubbing in 60+ languages), translation services
   - Cloud Engineering: Cloud strategy, migration, cloud-native development, security
   - Data Intelligence: Prompt engineering, data wrangling, data labeling, model validation, advanced analytics
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
- **CONVERSATION CONTINUITY:** When user says "yes", "tell me more", "continue", "go on", or similar affirmative responses, expand on the previous topic with additional details
- Keep track of context and provide natural follow-up information

**IMPORTANT:** You have access to complete, detailed information about all Digital Nirvana products. Always provide thorough, accurate answers that demonstrate deep product knowledge."""

    # Initialize messages with conversation history if provided
    if conversation_history:
        messages = conversation_history.copy()
        messages.append({"role": "user", "content": user_message})
    else:
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
            return answer, messages  # Return both answer and conversation history
        
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
    
    conversation_history = None
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response, conversation_history = get_ai_response(user_input, conversation_history)
        print()