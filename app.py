import streamlit as st
import pandas as pd
from apifyActors.instagram_hashtage import scrape_instagram_posts
from apifyActors.booking import scrape_booking
from apifyActors.instagram import scrape_instagram_profile
from apifyActors.tweet import scrape_tweets
from apifyActors.website_content import scrape_website_content
from apifyActors.google_maps import scrape_google_maps
import json
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
import re
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
def configure_gemini(api_key):
    """Configure Gemini with API key"""
    if not GEMINI_AVAILABLE:
        raise ImportError("google-generativeai package is not installed")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

def extract_scraper_intent(user_message, model):
    """Use Gemini to extract scraper intent from user message"""
    
    system_prompt = """
    You are an AI assistant that helps users run web scrapers. Your job is to understand user requests and extract the appropriate scraper and parameters.
    
    Available scrapers:
    1. instagram_hashtag - Scrape Instagram posts by hashtags
    2. instagram_profile - Scrape Instagram profile posts
    3. booking - Scrape Booking.com hotels
    4. twitter - Scrape Twitter tweets
    5. website_content - Scrape website content
    6. google_maps - Scrape Google Maps places
    
    Return ONLY a JSON object with this exact structure:
    {
        "scraper": "scraper_name",
        "parameters": {
            "param1": "value1",
            "param2": "value2"
        },
        "confidence": 0.95,
        "explanation": "Brief explanation of what will be scraped"
    }
    
    Parameter examples:
    - instagram_hashtag: {"hashtags": ["goa", "travel"], "results_limit": 20}
    - instagram_profile: {"profile_urls": ["https://instagram.com/username"], "results_limit": 20}
    - booking: {"search": "New York", "max_items": 10, "currency": "USD", "rooms": 1, "adults": 2, "children": 0, "min_max_price": "0-999999"}
    - twitter: {"start_urls": ["https://twitter.com/apify"], "search_terms": ["web scraping"], "twitter_handles": ["elonmusk"], "max_items": 20}
    - website_content: {"start_urls": ["https://docs.apify.com"], "results_limit": 10, "save_markdown": true}
    - google_maps: {"search_strings": ["restaurant"], "location_query": "New York, USA", "max_places": 20}
    
    If the user's request doesn't match any scraper, return:
    {
        "scraper": "none",
        "parameters": {},
        "confidence": 0.0,
        "explanation": "I couldn't understand which scraper you want to use. Please be more specific."
    }
    """
    
    try:
        response = model.generate_content(f"{system_prompt}\n\nUser request: {user_message}")
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {
                "scraper": "none",
                "parameters": {},
                "confidence": 0.0,
                "explanation": "I couldn't parse the response properly."
            }
    except Exception as e:
        return {
            "scraper": "none",
            "parameters": {},
            "confidence": 0.0,
            "explanation": f"Error processing request: {str(e)}"
        }

def run_scraper_from_intent(intent, api_token):
    """Run the appropriate scraper based on extracted intent"""
    
    scraper = intent.get("scraper")
    parameters = intent.get("parameters", {})
    
    if scraper == "instagram_hashtag":
        hashtags = parameters.get("hashtags", [])
        results_limit = parameters.get("results_limit", 20)
        return scrape_instagram_posts(api_token, hashtags, results_limit)
    
    elif scraper == "instagram_profile":
        profile_urls = parameters.get("profile_urls", [])
        results_limit = parameters.get("results_limit", 20)
        return scrape_instagram_profile(profile_urls, results_limit, api_token)
    
    elif scraper == "booking":
        return scrape_booking(
            search=parameters.get("search", "New York"),
            max_items=parameters.get("max_items", 10),
            currency=parameters.get("currency", "USD"),
            rooms=parameters.get("rooms", 1),
            adults=parameters.get("adults", 2),
            children=parameters.get("children", 0),
            min_max_price=parameters.get("min_max_price", "0-999999"),
            api_token=api_token
        )
    
    elif scraper == "twitter":
        return scrape_tweets(
            start_urls=parameters.get("start_urls", []),
            search_terms=parameters.get("search_terms", []),
            twitter_handles=parameters.get("twitter_handles", []),
            max_items=parameters.get("max_items", 20),
            api_token=api_token
        )
    
    elif scraper == "website_content":
        return scrape_website_content(
            start_urls=parameters.get("start_urls", []),
            results_limit=parameters.get("results_limit", 10),
            save_markdown=parameters.get("save_markdown", True),
            api_token=api_token
        )
    
    elif scraper == "google_maps":
        return scrape_google_maps(
            search_strings=parameters.get("search_strings", []),
            location_query=parameters.get("location_query", "New York, USA"),
            max_places=parameters.get("max_places", 20),
            api_token=api_token
        )
    
    else:
        return {"success": False, "error": "Unknown scraper type"}

def format_scraper_results(results, scraper_type):
    """Format scraper results for chat display"""
    if not results.get("success"):
        return f"❌ Error: {results.get('error', 'Unknown error')}"
    
    if scraper_type == "instagram_hashtag" or scraper_type == "instagram_profile":
        summary = results.get("summary", {})
        posts = results.get("posts", [])
        return f"""
✅ **Instagram Scraping Complete!**

📊 **Summary:**
- Total Posts: {summary.get('total_posts', 0)}
- Unique Users: {summary.get('unique_users', 0)}
- Total Likes: {summary.get('total_likes', 0)}
- Total Comments: {summary.get('total_comments', 0)}

📱 **Top Posts:**
{chr(10).join([f"• Post {i+1}: @{post.get('username', 'N/A')} - {post.get('likes', 0)} likes" for i, post in enumerate(posts[:5])])}

🔗 **Download Options Available in Dashboard**
        """
    
    elif scraper_type == "booking":
        summary = results.get("summary", {})
        hotels = results.get("hotels", [])
        return f"""
✅ **Booking.com Scraping Complete!**

🏨 **Summary:**
- City: {summary.get('city', 'N/A')}
- Total Hotels: {summary.get('total_hotels', 0)}
- Price Range: {summary.get('min_price', 0)} - {summary.get('max_price', 0)} {summary.get('currency', 'USD')}

🏨 **Top Hotels:**
{chr(10).join([f"• {hotel.get('name', 'N/A')} - {hotel.get('price', 0)} {hotel.get('currency', 'USD')} ({hotel.get('stars', 0)}⭐)" for hotel in hotels[:5]])}

🔗 **Download Options Available in Dashboard**
        """
    
    elif scraper_type == "twitter":
        summary = results.get("summary", {})
        tweets = results.get("tweets", [])
        return f"""
✅ **Twitter Scraping Complete!**

🐦 **Summary:**
- Total Tweets: {summary.get('total_tweets', 0)}
- Unique Authors: {summary.get('unique_authors', 0)}
- Total Likes: {summary.get('total_likes', 0)}
- Total Retweets: {summary.get('total_retweets', 0)}

📝 **Top Tweets:**
{chr(10).join([f"• @{tweet.get('author', 'N/A')}: {tweet.get('text', 'N/A')[:100]}..." for tweet in tweets[:5]])}

🔗 **Download Options Available in Dashboard**
        """
    
    elif scraper_type == "website_content":
        summary = results.get("summary", {})
        pages = results.get("pages", [])
        return f"""
✅ **Website Content Scraping Complete!**

🌐 **Summary:**
- Total Pages: {summary.get('total_pages', 0)}
- Start URLs: {summary.get('start_urls', 'N/A')}

📄 **Scraped Pages:**
{chr(10).join([f"• {page.get('title', 'N/A')} - {page.get('url', 'N/A')}" for page in pages[:5]])}

🔗 **Download Options Available in Dashboard**
        """
    
    elif scraper_type == "google_maps":
        summary = results.get("summary", {})
        places = results.get("places", [])
        return f"""
✅ **Google Maps Scraping Complete!**

📍 **Summary:**
- Total Places: {summary.get('total_places', 0)}
- Location: {summary.get('location_query', 'N/A')}
- Search Terms: {summary.get('search_strings', 'N/A')}

🏪 **Top Places:**
{chr(10).join([f"• {place.get('name', 'N/A')} - {place.get('rating', 'N/A')}⭐ ({place.get('reviews', 0)} reviews)" for place in places[:5]])}

🔗 **Download Options Available in Dashboard**
        """
    
    else:
        return "✅ Scraping completed successfully! Check the dashboard for detailed results."

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = None

st.set_page_config(
    page_title="MCP Multi-Scraper Dashboard with AI Chatbot",
    page_icon="🕸️🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create tabs for different interfaces
tab1, tab2 = st.tabs(["🤖 AI Chatbot", "⚙️ Manual Dashboard"])

with tab1:
    st.title("🤖 AI-Powered Scraper Chatbot")
    st.markdown("**Chat with me to run scrapers using natural language!**")
    
    # Helpful tips section
    with st.expander("💡 How to use the chatbot", expanded=True):
        st.markdown("""
        **🎯 How it works:**
        1. **Enter your API keys** in the sidebar (Apify + Gemini)
        2. **Type natural language requests** like "Find hotels in Paris"
        3. **The AI understands your intent** and runs the right scraper
        4. **Get formatted results** with summaries and download options
        
        **💬 Pro Tips:**
        - Be specific: "Get 20 posts with hashtag #travel" instead of just "scrape Instagram"
        - Include limits: "Find 10 hotels in Tokyo" 
        - Use natural language: "Search for restaurants near me" or "Get tweets about AI"
        - Combine parameters: "Find hotels in London for 2 adults and 1 child"
        
        **🔧 Advanced Features:**
        - View detailed results in expandable sections
        - Download data as CSV or JSON
        - Filter and sort results in the manual dashboard
        """)
    
    # Fetch API keys from environment
    apify_token = os.environ.get("APIFY_API_TOKEN", "")
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")

    # Instead, initialize Gemini automatically if gemini_api_key is present
    if gemini_api_key and not st.session_state.gemini_model:
        try:
            st.session_state.gemini_model = configure_gemini(gemini_api_key)
            st.success("✅ Gemini initialized successfully!")
        except Exception as e:
            st.error(f"❌ Error initializing Gemini: {str(e)}")
    
    # Chat interface
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Sample prompts section
    st.markdown("### 💡 Sample Prompts")
    
    # Create expandable sections for each scraper with sample prompts
    with st.expander("📱 Instagram Hashtag Scraper"):
        st.markdown("""
        **Sample Prompts:**
        - "Scrape Instagram posts with hashtag #Goa"
        - "Get 50 posts with hashtag #travel"
        - "Find Instagram posts with hashtags #food and #delicious"
        - "Scrape 30 posts with hashtag #photography"
        - "Get Instagram posts with hashtag #fitness limit to 25 results"
        """)
    
    with st.expander("👤 Instagram Profile Scraper"):
        st.markdown("""
        **Sample Prompts:**
        - "Scrape Instagram profile @humansofny"
        - "Get posts from https://www.instagram.com/natgeo/"
        - "Scrape 40 posts from @elonmusk profile"
        - "Get posts from multiple profiles: @taylorswift13 and @beyonce"
        - "Scrape Instagram profile posts from @nike limit to 15"
        """)
    
    with st.expander("🏨 Booking.com Scraper"):
        st.markdown("""
        **Sample Prompts:**
        - "Find hotels in New York on Booking.com"
        - "Search for hotels in Paris with max 20 results"
        - "Get hotels in Tokyo with USD currency"
        - "Find hotels in London for 2 adults and 1 child"
        - "Search hotels in Dubai with price range 100-500 USD"
        - "Get 15 hotels in Singapore with 4-star minimum"
        """)
    
    with st.expander("🐦 Twitter Scraper"):
        st.markdown("""
        **Sample Prompts:**
        - "Scrape tweets from @elonmusk"
        - "Get tweets about AI from @OpenAI"
        - "Search tweets with term 'web scraping'"
        - "Get tweets from multiple handles: @elonmusk, @taylorswift13"
        - "Scrape tweets from https://twitter.com/apify"
        - "Search tweets about 'climate change' limit to 30"
        - "Get tweets with hashtag #AI from @Google"
        """)
    
    with st.expander("🌐 Website Content Scraper"):
        st.markdown("""
        **Sample Prompts:**
        - "Extract content from https://docs.apify.com"
        - "Scrape website content from https://www.wikipedia.org"
        - "Get content from https://www.bbc.com/news"
        - "Extract text from multiple URLs: https://example.com and https://test.com"
        - "Scrape 20 pages from https://docs.python.org"
        - "Get markdown content from https://github.com"
        """)
    
    with st.expander("📍 Google Maps Scraper"):
        st.markdown("""
        **Sample Prompts:**
        - "Find restaurants in New York on Google Maps"
        - "Search for hotels in London"
        - "Get coffee shops in San Francisco"
        - "Find gyms in Tokyo limit to 25 places"
        - "Search for museums in Paris"
        - "Get shopping malls in Dubai"
        - "Find hospitals in Singapore"
        """)
    
    st.markdown("---")
    
    # Chat input
    if prompt := st.chat_input("Ask me to run a scraper (e.g., 'Scrape Instagram posts with hashtag #Goa' or 'Find hotels in New York on Booking.com')"):
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt, "timestamp": datetime.now()})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Check if Gemini is initialized
        if not st.session_state.gemini_model:
            with st.chat_message("assistant"):
                st.error("❌ Please initialize Gemini first by entering your API key in the sidebar!")
        elif not apify_token:
            with st.chat_message("assistant"):
                st.error("❌ Please enter your Apify API token in the sidebar!")
        else:
            with st.chat_message("assistant"):
                with st.spinner("🤔 Analyzing your request..."):
                    # Extract intent using Gemini
                    intent = extract_scraper_intent(prompt, st.session_state.gemini_model)
                    
                    if intent["scraper"] == "none":
                        response = f"""❌ {intent['explanation']}

**💡 Quick Reference - Available Commands:**

📱 **Instagram Hashtag:** "Scrape Instagram posts with hashtag #Goa"
👤 **Instagram Profile:** "Get posts from @humansofny"
🏨 **Booking.com:** "Find hotels in New York on Booking.com"
🐦 **Twitter:** "Scrape tweets from @elonmusk"
🌐 **Website Content:** "Extract content from https://docs.apify.com"
📍 **Google Maps:** "Find restaurants in New York on Google Maps"

**💬 Try these examples:**
• "Scrape 20 posts with hashtag #travel"
• "Get hotels in Paris with max 10 results"
• "Search tweets about AI from @OpenAI"
• "Find coffee shops in San Francisco"
• "Extract content from https://www.wikipedia.org"
"""
                        st.markdown(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                    else:
                        # Show what we're going to do
                        st.info(f"🎯 **Intent Detected:** {intent['explanation']}")
                        
                        with st.spinner(f"🔄 Running {intent['scraper']} scraper..."):
                            # Run the scraper
                            results = run_scraper_from_intent(intent, apify_token)
                            
                            # Format and display results
                            formatted_results = format_scraper_results(results, intent["scraper"])
                            st.markdown(formatted_results)
                            
                            # Add to chat history
                            st.session_state.chat_history.append({"role": "assistant", "content": formatted_results, "timestamp": datetime.now()})
                            
                            # Show detailed results in expandable section
                            if results.get("success"):
                                with st.expander("📊 View Detailed Results"):
                                    if intent["scraper"] in ["instagram_hashtag", "instagram_profile"]:
                                        df = pd.DataFrame(results.get("posts", []))
                                        st.dataframe(df)
                                    elif intent["scraper"] == "booking":
                                        df = pd.DataFrame(results.get("hotels", []))
                                        st.dataframe(df)
                                    elif intent["scraper"] == "twitter":
                                        df = pd.DataFrame(results.get("tweets", []))
                                        st.dataframe(df)
                                    elif intent["scraper"] == "website_content":
                                        df = pd.DataFrame(results.get("pages", []))
                                        st.dataframe(df)
                                    elif intent["scraper"] == "google_maps":
                                        df = pd.DataFrame(results.get("places", []))
                                        st.dataframe(df)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

with tab2:
    st.title("🕸️ MCP Multi-Scraper Dashboard")
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        data_source = st.selectbox("Select Data Source", [
            "Instagram Hashtag", "Instagram Profile", "Booking.com", "Twitter", "Website Content", "Google Maps"
        ])

        # Fetch API keys from environment
        apify_token = os.environ.get("APIFY_API_TOKEN", "")

        if data_source == "Instagram Hashtag":
            hashtags_input = st.text_input(
                "Hashtags (comma-separated)",
                value="Goa",
                help="Enter hashtags separated by commas",
                key="manual_hashtags"
            )
            results_limit = st.slider(
                "Number of Results",
                min_value=5,
                max_value=100,
                value=20,
                help="Maximum number of posts to scrape",
                key="manual_hashtag_results"
            )
            scrape_button = st.button("🚀 Run Instagram Hashtag Scraper", key="insta_hashtag_btn", use_container_width=True)
        elif data_source == "Instagram Profile":
            profile_urls_input = st.text_area(
                "Instagram Profile URLs (one per line)",
                value="https://www.instagram.com/humansofny/",
                help="Enter one or more Instagram profile URLs, one per line",
                key="manual_profile_urls"
            )
            results_limit = st.slider(
                "Number of Results",
                min_value=5,
                max_value=100,
                value=20,
                help="Maximum number of posts to scrape",
                key="manual_profile_results"
            )
            scrape_button = st.button("🚀 Run Instagram Profile Scraper", key="insta_profile_btn", use_container_width=True)
        elif data_source == "Booking.com":
            search = st.text_input("Search City/Location", value="New York", key="manual_booking_search")
            max_items = st.slider("Max Hotels", min_value=1, max_value=50, value=10, key="manual_booking_max")
            currency = st.text_input("Currency", value="USD", key="manual_booking_currency")
            rooms = st.number_input("Rooms", min_value=1, value=1, key="manual_booking_rooms")
            adults = st.number_input("Adults", min_value=1, value=2, key="manual_booking_adults")
            children = st.number_input("Children", min_value=0, value=0, key="manual_booking_children")
            min_max_price = st.text_input("Min-Max Price", value="0-999999", key="manual_booking_price")
            scrape_button = st.button("🚀 Run Booking Scraper", key="booking_btn", use_container_width=True)
        elif data_source == "Twitter":
            start_urls_input = st.text_area(
                "Start URLs (one per line)",
                value="https://twitter.com/apify",
                help="Enter Twitter URLs to scrape, one per line",
                key="manual_twitter_urls"
            )
            search_terms_input = st.text_area(
                "Search Terms (one per line)",
                value="web scraping",
                help="Enter search terms, one per line",
                key="manual_twitter_terms"
            )
            twitter_handles_input = st.text_input(
                "Twitter Handles (comma-separated)",
                value="elonmusk,taylorswift13",
                help="Enter Twitter handles separated by commas",
                key="manual_twitter_handles"
            )
            max_items = st.slider("Max Tweets", min_value=1, max_value=100, value=20, key="manual_twitter_max")
            scrape_button = st.button("🚀 Run Twitter Scraper", key="twitter_btn", use_container_width=True)
        elif data_source == "Website Content":
            website_urls_input = st.text_area(
                "Website URLs (one per line)",
                value="https://docs.apify.com/academy/web-scraping-for-beginners",
                help="Enter one or more website URLs, one per line",
                key="manual_website_urls"
            )
            results_limit = st.slider(
                "Number of Pages",
                min_value=1,
                max_value=100,
                value=10,
                help="Maximum number of pages to scrape",
                key="manual_website_results"
            )
            save_markdown = st.checkbox("Save as Markdown", value=True, key="manual_website_markdown")
            scrape_button = st.button("🚀 Run Website Content Scraper", key="website_content_btn", use_container_width=True)
        elif data_source == "Google Maps":
            gmaps_search_strings = st.text_area(
                "Search Terms (one per line)",
                value="restaurant",
                help="Enter search terms for Google Maps, one per line",
                key="manual_gmaps_search"
            )
            gmaps_location = st.text_input(
                "Location Query",
                value="New York, USA",
                help="Enter the location to search in Google Maps",
                key="manual_gmaps_location"
            )
            gmaps_max_places = st.slider(
                "Max Places",
                min_value=1,
                max_value=100,
                value=20,
                help="Maximum number of places to scrape",
                key="manual_gmaps_max"
            )
            scrape_button = st.button("🚀 Run Google Maps Scraper", key="gmaps_btn", use_container_width=True)

    if scrape_button:
        if not apify_token:
            st.error("❌ Please enter your Apify API token!")
        else:
            if data_source == "Instagram Hashtag":
                if not hashtags_input.strip():
                    st.error("❌ Please enter at least one hashtag!")
                else:
                    hashtags = [tag.strip() for tag in hashtags_input.split(",") if tag.strip()]
                    with st.spinner("🔄 Running Instagram Hashtag scraper..."):
                        results = scrape_instagram_posts(apify_token, hashtags, results_limit)
                        if results.get("success"):
                            st.success(f"✅ Successfully scraped {results['summary']['total_posts']} posts!")
                            st.header("📊 Summary Statistics")
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Total Posts", results['summary']['total_posts'])
                            col2.metric("Unique Users", results['summary']['unique_users'])
                            col3.metric("Total Likes", results['summary']['total_likes'])
                            col4.metric("Total Comments", results['summary']['total_comments'])
                            st.header("📱 Scraped Posts")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                min_likes = st.number_input("Minimum likes", min_value=0, value=0, key="manual_hashtag_min_likes")
                            with col2:
                                sort_by = st.selectbox("Sort by", ["Post Number", "Most Liked", "Most Commented", "Latest"], key="manual_hashtag_sort")
                            with col3:
                                show_media_links = st.checkbox("Show media links", value=True, key="manual_hashtag_media")
                            filtered_posts = [post for post in results['posts'] if post['likes'] >= min_likes]
                            if sort_by == "Most Liked":
                                filtered_posts.sort(key=lambda x: x['likes'], reverse=True)
                            elif sort_by == "Most Commented":
                                filtered_posts.sort(key=lambda x: x['comments'], reverse=True)
                            elif sort_by == "Latest":
                                filtered_posts.sort(key=lambda x: x['posted_date'], reverse=True)
                            for post in filtered_posts:
                                st.subheader(f"Post {post['post_number']}")
                                user_cols = st.columns([2, 2, 2])
                                user_cols[0].write(f"👤 **User:** @{post['username']}")
                                if post['full_name']:
                                    user_cols[1].write(f"📝 **Full Name:** {post['full_name']}")
                                user_cols[2].write(f"📅 **Posted:** {post['posted_date']}")
                                if post['caption']:
                                    st.write(f"**Caption:** {post['caption']}")
                                metric_cols = st.columns(4)
                                metric_cols[0].metric("❤️ Likes", post['likes'])
                                metric_cols[1].metric("💬 Comments", post['comments'])
                                metric_cols[2].metric("🔄 Shares", post['shares'])
                                metric_cols[3].metric("👁️ Views", post['views'])
                                if post['hashtags']:
                                    st.write(f"🏷️ **Hashtags:** {post['hashtags']}")
                                if post['media_type']:
                                    st.write(f"📷 **Media Type:** {post['media_type']}")
                                if post['post_url']:
                                    st.write(f"🔗 [View Original Post]({post['post_url']})")
                                if show_media_links:
                                    if post['image_url']:
                                        st.write(f"🖼️ [View Image]({post['image_url']})")
                                    if post['video_url']:
                                        st.write(f"🎥 [View Video]({post['video_url']})")
                                st.markdown("---")
                            st.header("💾 Download Data")
                            col1, col2 = st.columns(2)
                            with col1:
                                df = pd.DataFrame(results['posts'])
                                csv_data = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download as CSV",
                                    data=csv_data,
                                    file_name="instagram_formatted_data.csv",
                                    mime="text/csv"
                                )
                            with col2:
                                st.download_button(
                                    label="📥 Download Raw JSON",
                                    data=json.dumps(results['raw_results'], indent=4, ensure_ascii=False),
                                    file_name="instagram_raw_data.json",
                                    mime="application/json"
                                )
                            with st.expander("🔧 Run Information"):
                                st.json({
                                    "Run ID": results['summary']['run_id'],
                                    "Dataset ID": results['summary']['dataset_id'],
                                    "Hashtags Scraped": hashtags,
                                    "Results Limit": results_limit
                                })
                        else:
                            st.error(f"❌ {results.get('error')}")
                            st.info("💡 Make sure your Apify API token is valid and you have sufficient credits.")
            elif data_source == "Instagram Profile":
                profile_urls = [url.strip() for url in profile_urls_input.splitlines() if url.strip()]
                if not profile_urls:
                    st.error("❌ Please enter at least one Instagram profile URL!")
                else:
                    with st.spinner("🔄 Running Instagram Profile scraper..."):
                        results = scrape_instagram_profile(profile_urls, results_limit, apify_token)
                        if results.get("success"):
                            st.success(f"✅ Successfully scraped {results['summary']['total_posts']} posts!")
                            st.header("📊 Summary Statistics")
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Total Posts", results['summary']['total_posts'])
                            col2.metric("Unique Users", results['summary']['unique_users'])
                            col3.metric("Total Likes", results['summary']['total_likes'])
                            col4.metric("Total Comments", results['summary']['total_comments'])
                            st.header("📱 Scraped Posts")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                min_likes = st.number_input("Minimum likes", min_value=0, value=0, key="profile_min_likes")
                            with col2:
                                sort_by = st.selectbox("Sort by", ["Post Number", "Most Liked", "Most Commented", "Latest"], key="profile_sort_by")
                            with col3:
                                show_media_links = st.checkbox("Show media links", value=True, key="profile_show_media")
                            filtered_posts = [post for post in results['posts'] if post['likes'] >= min_likes]
                            if sort_by == "Most Liked":
                                filtered_posts.sort(key=lambda x: x['likes'], reverse=True)
                            elif sort_by == "Most Commented":
                                filtered_posts.sort(key=lambda x: x['comments'], reverse=True)
                            elif sort_by == "Latest":
                                filtered_posts.sort(key=lambda x: x['posted_date'], reverse=True)
                            for post in filtered_posts:
                                st.subheader(f"Post {post['post_number']}")
                                user_cols = st.columns([2, 2, 2])
                                user_cols[0].write(f"👤 **User:** @{post['username']}")
                                if post['full_name']:
                                    user_cols[1].write(f"📝 **Full Name:** {post['full_name']}")
                                user_cols[2].write(f"📅 **Posted:** {post['posted_date']}")
                                if post['caption']:
                                    st.write(f"**Caption:** {post['caption']}")
                                metric_cols = st.columns(4)
                                metric_cols[0].metric("❤️ Likes", post['likes'])
                                metric_cols[1].metric("💬 Comments", post['comments'])
                                metric_cols[2].metric("🔄 Shares", post['shares'])
                                metric_cols[3].metric("👁️ Views", post['views'])
                                if post['hashtags']:
                                    st.write(f"🏷️ **Hashtags:** {post['hashtags']}")
                                if post['media_type']:
                                    st.write(f"📷 **Media Type:** {post['media_type']}")
                                if post['post_url']:
                                    st.write(f"🔗 [View Original Post]({post['post_url']})")
                                if show_media_links:
                                    if post['image_url']:
                                        st.write(f"🖼️ [View Image]({post['image_url']})")
                                    if post['video_url']:
                                        st.write(f"🎥 [View Video]({post['video_url']})")
                                st.markdown("---")
                            st.header("💾 Download Data")
                            col1, col2 = st.columns(2)
                            with col1:
                                df = pd.DataFrame(results['posts'])
                                csv_data = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download as CSV",
                                    data=csv_data,
                                    file_name="instagram_profile_data.csv",
                                    mime="text/csv"
                                )
                            with col2:
                                st.download_button(
                                    label="📥 Download Raw JSON",
                                    data=json.dumps(results['raw_results'], indent=4, ensure_ascii=False),
                                    file_name="instagram_profile_raw_data.json",
                                    mime="application/json"
                                )
                            with st.expander("🔧 Run Information"):
                                st.json({
                                    "Run ID": results['summary']['run_id'],
                                    "Dataset ID": results['summary']['dataset_id'],
                                    "Profile URLs": profile_urls,
                                    "Results Limit": results_limit
                                })
                        else:
                            st.error(f"❌ {results.get('error')}")
                            st.info("💡 Make sure your Apify API token is valid and you have sufficient credits.")
            elif data_source == "Booking.com":
                with st.spinner("🔄 Running Booking.com scraper..."):
                    results = scrape_booking(
                        search=search,
                        max_items=max_items,
                        currency=currency,
                        rooms=rooms,
                        adults=adults,
                        children=children,
                        min_max_price=min_max_price,
                        api_token=apify_token
                    )
                    if results.get("success"):
                        st.success(f"✅ Successfully scraped {results['summary']['total_hotels']} hotels!")
                        st.header("🏨 Booking.com Hotels")
                        st.write(f"**City:** {results['summary']['city']}")
                        st.write(f"**Min Price:** {results['summary']['min_price']} {results['summary']['currency']} | **Max Price:** {results['summary']['max_price']} {results['summary']['currency']}")
                        st.write(f"**Total Hotels:** {results['summary']['total_hotels']}")
                        for hotel in results['hotels']:
                            st.subheader(f"Hotel {hotel['hotel_number']}: {hotel['name']}")
                            st.write(f"📍 {hotel['address']}, {hotel['city']}, {hotel['country']}")
                            st.write(f"💲 Price: {hotel['price']} {hotel['currency']}")
                            st.write(f"⭐ Stars: {hotel['stars']} | 🏆 Review Score: {hotel['review_score']} ({hotel['review_count']} reviews)")
                            if hotel['url']:
                                st.write(f"🔗 [View Hotel]({hotel['url']})")
                            if hotel['image']:
                                st.image(hotel['image'], width=300)
                            st.markdown("---")
                        st.header("💾 Download Data")
                        col1, col2 = st.columns(2)
                        with col1:
                            df = pd.DataFrame(results['hotels'])
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv_data,
                                file_name="booking_hotels_data.csv",
                                mime="text/csv"
                            )
                        with col2:
                            st.download_button(
                                label="📥 Download Raw JSON",
                                data=json.dumps(results['raw_results'], indent=4, ensure_ascii=False),
                                file_name="booking_raw_data.json",
                                mime="application/json"
                            )
                    else:
                        st.error(f"❌ {results.get('error')}")
                        st.info("💡 Make sure your Apify API token is valid and you have sufficient credits.")
            elif data_source == "Twitter":
                start_urls = [url.strip() for url in start_urls_input.splitlines() if url.strip()]
                search_terms = [term.strip() for term in search_terms_input.splitlines() if term.strip()]
                twitter_handles = [h.strip() for h in twitter_handles_input.split(",") if h.strip()]
                with st.spinner("🔄 Running Twitter scraper..."):
                    results = scrape_tweets(
                        start_urls=start_urls,
                        search_terms=search_terms,
                        twitter_handles=twitter_handles,
                        max_items=max_items,
                        api_token=apify_token
                    )
                    if results.get("success"):
                        st.success(f"✅ Successfully scraped {results['summary']['total_tweets']} tweets!")
                        st.header("🐦 Tweets")
                        st.write(f"**Unique Authors:** {results['summary']['unique_authors']}")
                        st.write(f"**Total Likes:** {results['summary']['total_likes']} | **Total Retweets:** {results['summary']['total_retweets']} | **Total Replies:** {results['summary']['total_replies']}")
                        for tweet in results['tweets']:
                            st.subheader(f"Tweet {tweet['tweet_number']} by @{tweet['author']}")
                            st.write(f"📝 {tweet['text']}")
                            st.write(f"📅 {tweet['created_at']}")
                            st.write(f"❤️ {tweet['likes']} | 🔁 {tweet['retweets']} | 💬 {tweet['replies']}")
                            if tweet['hashtags']:
                                st.write(f"🏷️ Hashtags: {' '.join(['#'+h for h in tweet['hashtags']])}")
                            if tweet['url']:
                                st.write(f"🔗 [View Tweet]({tweet['url']})")
                            if tweet['media']:
                                for media in tweet['media']:
                                    if media.get('type') == 'photo':
                                        st.image(media.get('mediaUrl'))
                                    elif media.get('type') == 'video':
                                        st.write(f"🎥 [View Video]({media.get('mediaUrl')})")
                            st.markdown("---")
                        st.header("💾 Download Data")
                        col1, col2 = st.columns(2)
                        with col1:
                            df = pd.DataFrame(results['tweets'])
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv_data,
                                file_name="tweets_data.csv",
                                mime="text/csv"
                            )
                        with col2:
                            st.download_button(
                                label="📥 Download Raw JSON",
                                data=json.dumps(results['raw_results'], indent=4, ensure_ascii=False),
                                file_name="tweets_raw_data.json",
                                mime="application/json"
                            )
                    else:
                        st.error(f"❌ {results.get('error')}")
                        st.info("💡 Make sure your Apify API token is valid and you have sufficient credits.")
            elif data_source == "Website Content":
                website_urls = [url.strip() for url in website_urls_input.splitlines() if url.strip()]
                with st.spinner("🔄 Running Website Content scraper..."):
                    results = scrape_website_content(
                        start_urls=website_urls,
                        results_limit=results_limit,
                        save_markdown=save_markdown,
                        api_token=apify_token
                    )
                    if results.get("success"):
                        st.success(f"✅ Successfully scraped {results['summary']['total_pages']} pages!")
                        st.header("🌐 Website Pages")
                        st.write(f"**Start URLs:** {results['summary']['start_urls']}")
                        st.write(f"**Total Pages:** {results['summary']['total_pages']}")
                        for page in results['pages']:
                            st.subheader(f"Page {page['page_number']}: {page['title']}")
                            st.write(f"🔗 [View Page]({page['url']})")
                            if page['markdown']:
                                st.markdown("**Markdown Content:**")
                                st.markdown(page['markdown'])
                            elif page['text']:
                                st.markdown("**Text Content:**")
                                st.write(page['text'])
                            st.markdown("---")
                        st.header("💾 Download Data")
                        col1, col2 = st.columns(2)
                        with col1:
                            df = pd.DataFrame(results['pages'])
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv_data,
                                file_name="website_content_data.csv",
                                mime="text/csv"
                            )
                        with col2:
                            st.download_button(
                                label="📥 Download Raw JSON",
                                data=json.dumps(results['raw_results'], indent=4, ensure_ascii=False),
                                file_name="website_content_raw_data.json",
                                mime="application/json"
                            )
                    else:
                        st.error(f"❌ {results.get('error')}")
                        st.info("💡 Make sure your Apify API token is valid and you have sufficient credits.")
            elif data_source == "Google Maps":
                gmaps_search_list = [s.strip() for s in gmaps_search_strings.splitlines() if s.strip()]
                with st.spinner("🔄 Running Google Maps scraper..."):
                    results = scrape_google_maps(
                        search_strings=gmaps_search_list,
                        location_query=gmaps_location,
                        max_places=gmaps_max_places,
                        api_token=apify_token
                    )
                    if results.get("success"):
                        st.success(f"✅ Successfully scraped {results['summary']['total_places']} places!")
                        st.header("📍 Google Maps Places")
                        st.write(f"**Search Strings:** {results['summary']['search_strings']}")
                        st.write(f"**Location Query:** {results['summary']['location_query']}")
                        st.write(f"**Total Places:** {results['summary']['total_places']}")
                        for place in results['places']:
                            st.subheader(f"Place {place['place_number']}: {place['name']}")
                            st.write(f"📍 Address: {place['address']}")
                            st.write(f"🏷️ Category: {place['category']}")
                            st.write(f"⭐ Rating: {place['rating']} | 💬 Reviews: {place['reviews']}")
                            if place['url']:
                                st.write(f"🔗 [View on Google Maps]({place['url']})")
                            if place['website']:
                                st.write(f"🌐 [Website]({place['website']})")
                            if place['phone']:
                                st.write(f"📞 {place['phone']}")
                            st.markdown("---")
                        st.header("💾 Download Data")
                        col1, col2 = st.columns(2)
                        with col1:
                            df = pd.DataFrame(results['places'])
                            csv_data = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download as CSV",
                                data=csv_data,
                                file_name="google_maps_data.csv",
                                mime="text/csv"
                            )
                        with col2:
                            st.download_button(
                                label="📥 Download Raw JSON",
                                data=json.dumps(results['raw_results'], indent=4, ensure_ascii=False),
                                file_name="google_maps_raw_data.json",
                                mime="application/json"
                            )
                    else:
                        st.error(f"❌ {results.get('error')}")
                        st.info("💡 Make sure your Apify API token is valid and you have sufficient credits.")
    else:
        st.info("""
        ### 🚀 How to use this app:
        1. **Select a data source** in the sidebar
        2. **Enter the required parameters** for the selected scraper
        3. **Click the run button** to start scraping
        4. **View the formatted results** in the dashboard below
        5. **Download your data** as CSV or JSON
        """)
        with st.expander("📋 Sample Data Structure (Instagram Hashtag)"):
            st.json({
                "post_number": 1,
                "username": "example_user",
                "full_name": "Example User",
                "posted_date": "2024-01-15 14:30:00",
                "caption": "Sample post caption",
                "likes": 150,
                "comments": 25,
                "shares": 5,
                "views": 1000,
                "hashtags": "#example #sample",
                "post_url": "https://instagram.com/p/example",
                "media_type": "IMAGE",
                "image_url": "https://example.com/image.jpg"
            })
        with st.expander("📋 Sample Data Structure (Instagram Profile)"):
            st.json({
                "post_number": 1,
                "username": "profile_user",
                "full_name": "Profile User",
                "posted_date": "2024-01-15 14:30:00",
                "caption": "Profile post caption",
                "likes": 200,
                "comments": 30,
                "shares": 10,
                "views": 1500,
                "hashtags": "#profile #sample",
                "post_url": "https://instagram.com/p/profilepost",
                "media_type": "IMAGE",
                "image_url": "https://example.com/profileimage.jpg"
            })
        with st.expander("📋 Sample Data Structure (Booking.com)"):
            st.json({
                "hotel_number": 1,
                "name": "Sample Hotel",
                "address": "123 Main St",
                "city": "New York",
                "country": "USA",
                "price": 200,
                "currency": "USD",
                "stars": 4,
                "review_score": 8.5,
                "review_count": 1200,
                "url": "https://booking.com/hotel/example",
                "image": "https://example.com/hotel.jpg"
            })
        with st.expander("📋 Sample Data Structure (Twitter)"):
            st.json({
                "tweet_number": 1,
                "id": "1234567890",
                "text": "This is a sample tweet",
                "author": "elonmusk",
                "author_name": "Elon Musk",
                "created_at": "2024-01-15 14:30:00",
                "retweets": 100,
                "likes": 500,
                "replies": 20,
                "url": "https://twitter.com/elonmusk/status/1234567890",
                "lang": "en",
                "hashtags": ["webscraping", "ai"],
                "mentions": ["apify"],
                "media": [{"type": "photo", "mediaUrl": "https://example.com/photo.jpg"}]
            })
        with st.expander("📋 Sample Data Structure (Website Content)"):
            st.json({
                "page_number": 1,
                "url": "https://docs.apify.com/academy/web-scraping-for-beginners",
                "title": "Web Scraping for Beginners",
                "markdown": "# Web Scraping for Beginners\n...",
                "text": "Web Scraping for Beginners ..."
            })
