<<<<<<< Updated upstream
# 🤖 AI-Powered Multi-Scraper Dashboard

A powerful Streamlit application that combines web scraping capabilities with AI-powered natural language processing to make data extraction as simple as having a conversation.

## ✨ Features

### 🎯 AI-Powered Chat Interface
- **Natural Language Processing**: Chat with the AI to run scrapers using everyday language
- **Intent Recognition**: Automatically detects which scraper to use based on your request
- **Smart Parameter Extraction**: AI understands and extracts relevant parameters from your messages
- **Gemini AI Integration**: Powered by Google's Gemini 2.0 Flash for intelligent conversation

### 🕸️ Multi-Platform Scraping
- **Instagram**: Scrape posts by hashtags and user profiles
- **Booking.com**: Extract hotel information, prices, and reviews
- **Twitter/X**: Gather tweets, search terms, and user content
- **Google Maps**: Find places, businesses, and location data
- **Website Content**: Extract and parse web page content
- **Facebook**: Scrape Facebook posts and profiles
- **Google News**: Gather news articles and headlines
- **TripAdvisor**: Extract reviews and business information

### 📊 Rich Data Visualization
- **Interactive Dashboards**: View results in beautiful, interactive tables
- **Data Export**: Download results as CSV or JSON files
- **Real-time Analytics**: Get instant summaries and statistics
- **Filtering & Sorting**: Advanced data manipulation capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- Apify API token
- Gemini API key (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd new-streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using uv (recommended)
   uv sync
   ```

3. **Set up API keys**
   - Get your [Apify API token](https://console.apify.com/account/integrations)
   - Get your [Gemini API key](https://makersuite.google.com/app/apikey) (optional)

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 💬 How to Use

### AI Chatbot Interface

Simply chat with the AI using natural language:

```
User: "Find hotels in Paris on Booking.com"
AI: 🎯 Intent Detected: Searching for hotels in Paris on Booking.com
     ✅ Booking.com Scraping Complete!
     🏨 Summary: 10 hotels found in Paris
     Price Range: $50 - $500 USD
```

**Example Conversations:**
- "Scrape Instagram posts with hashtag #travel"
- "Get tweets from @elonmusk about AI"
- "Find restaurants in New York on Google Maps"
- "Extract content from https://docs.apify.com"
- "Search for hotels in Tokyo with max 15 results"

### Manual Dashboard

For advanced users, use the manual dashboard to:
- Configure scraping parameters directly
- View detailed results and analytics
- Export data in multiple formats
- Filter and sort results

## 🔧 Available Scrapers

### 📱 Instagram Scrapers
- **Hashtag Scraper**: Extract posts by hashtags
  - Parameters: hashtags, results_limit
  - Example: `["#travel", "#photography"]`
- **Profile Scraper**: Scrape user profile posts
  - Parameters: profile_urls, results_limit
  - Example: `["https://instagram.com/username"]`

### 🏨 Booking.com Scraper
- **Hotel Search**: Find hotels with detailed information
  - Parameters: search, max_items, currency, rooms, adults, children, min_max_price
  - Example: `search="New York", max_items=10, currency="USD"`

### 🐦 Twitter/X Scraper
- **Tweet Extraction**: Gather tweets and user content
  - Parameters: start_urls, search_terms, twitter_handles, max_items
  - Example: `twitter_handles=["@elonmusk"], max_items=20`

### 🌐 Website Content Scraper
- **Content Extraction**: Parse and extract web page content
  - Parameters: start_urls, results_limit, save_markdown
  - Example: `start_urls=["https://docs.apify.com"]`

### 📍 Google Maps Scraper
- **Place Search**: Find businesses and locations
  - Parameters: search_strings, location_query, max_places
  - Example: `search_strings=["restaurant"], location_query="New York, USA"`

## 📊 Data Output

Each scraper returns structured data including:

- **Summary Statistics**: Total items, unique users, engagement metrics
- **Detailed Results**: Complete data with all extracted fields
- **Export Options**: CSV and JSON download capabilities
- **Visual Analytics**: Interactive charts and tables

## 🛠️ Technical Architecture

### Core Technologies
- **Streamlit**: Web application framework
- **Apify**: Web scraping platform with pre-built actors
- **Gemini AI**: Natural language processing and intent recognition
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization

### Project Structure
```
new-streamlit/
├── app.py                 # Main Streamlit application
├── apifyActors/          # Scraper modules
│   ├── instagram_hashtage.py
│   ├── instagram.py
│   ├── booking.py
│   ├── tweet.py
│   ├── website_content.py
│   ├── google_maps.py
│   ├── facebook.py
│   ├── google_news.py
│   └── trip_advisor.py
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

## 🔑 API Configuration

### Required APIs

1. **Apify API Token**
   - Sign up at [Apify Console](https://console.apify.com/)
   - Navigate to Account → Integrations → API tokens
   - Copy your token and paste it in the app

2. **Gemini API Key** (Optional)
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Enable the Gemini API in your Google Cloud Console

## 🎨 Features in Detail

### AI Chatbot Capabilities
- **Natural Language Understanding**: Processes complex requests in plain English
- **Context Awareness**: Remembers conversation history and preferences
- **Error Handling**: Provides helpful suggestions when requests fail
- **Multi-Modal Support**: Handles various input formats and parameters

### Data Processing
- **Real-time Processing**: Instant results with progress indicators
- **Data Validation**: Ensures data quality and completeness
- **Format Conversion**: Automatic conversion between data formats
- **Error Recovery**: Graceful handling of API failures and timeouts

### User Experience
- **Responsive Design**: Works on desktop and mobile devices
- **Dark/Light Mode**: Automatic theme detection
- **Keyboard Shortcuts**: Quick access to common functions
- **Export Options**: Multiple download formats (CSV, JSON, Excel)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd new-streamlit

# Install development dependencies
uv sync --dev

# Run in development mode
streamlit run app.py --server.port 8501
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Apify**: For providing powerful web scraping actors
- **Google**: For the Gemini AI platform
- **Streamlit**: For the excellent web app framework
- **Open Source Community**: For the amazing tools and libraries

## 📞 Support

- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community discussions for help and ideas
- **Documentation**: Check the inline help and tooltips in the app

## 🔮 Roadmap

- [ ] Add more scraping platforms (LinkedIn, TikTok, etc.)
- [ ] Implement advanced analytics and reporting
- [ ] Add scheduled scraping capabilities
- [ ] Create mobile app version
- [ ] Add team collaboration features
- [ ] Implement data visualization dashboards

---

**Made with ❤️ for the data community**

*Transform your web scraping workflow with AI-powered intelligence!*
=======
# 🤖 AI-Powered Multi-Scraper Dashboard

A powerful Streamlit application that combines web scraping capabilities with AI-powered natural language processing to make data extraction as simple as having a conversation.

## ✨ Features

### 🎯 AI-Powered Chat Interface
- **Natural Language Processing**: Chat with the AI to run scrapers using everyday language
- **Intent Recognition**: Automatically detects which scraper to use based on your request
- **Smart Parameter Extraction**: AI understands and extracts relevant parameters from your messages
- **Gemini AI Integration**: Powered by Google's Gemini 2.0 Flash for intelligent conversation

### 🕸️ Multi-Platform Scraping
- **Instagram**: Scrape posts by hashtags and user profiles
- **Booking.com**: Extract hotel information, prices, and reviews
- **Twitter/X**: Gather tweets, search terms, and user content
- **Google Maps**: Find places, businesses, and location data
- **Website Content**: Extract and parse web page content
- **Facebook**: Scrape Facebook posts and profiles
- **Google News**: Gather news articles and headlines
- **TripAdvisor**: Extract reviews and business information

### 📊 Rich Data Visualization
- **Interactive Dashboards**: View results in beautiful, interactive tables
- **Data Export**: Download results as CSV or JSON files
- **Real-time Analytics**: Get instant summaries and statistics
- **Filtering & Sorting**: Advanced data manipulation capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- Apify API token
- Gemini API key (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd new-streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using uv (recommended)
   uv sync
   ```

3. **Set up API keys**
   - Get your [Apify API token](https://console.apify.com/account/integrations)
   - Get your [Gemini API key](https://makersuite.google.com/app/apikey) (optional)

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 💬 How to Use

### AI Chatbot Interface

Simply chat with the AI using natural language:

```
User: "Find hotels in Paris on Booking.com"
AI: 🎯 Intent Detected: Searching for hotels in Paris on Booking.com
     ✅ Booking.com Scraping Complete!
     🏨 Summary: 10 hotels found in Paris
     Price Range: $50 - $500 USD
```

**Example Conversations:**
- "Scrape Instagram posts with hashtag #travel"
- "Get tweets from @elonmusk about AI"
- "Find restaurants in New York on Google Maps"
- "Extract content from https://docs.apify.com"
- "Search for hotels in Tokyo with max 15 results"

### Manual Dashboard

For advanced users, use the manual dashboard to:
- Configure scraping parameters directly
- View detailed results and analytics
- Export data in multiple formats
- Filter and sort results

## 🔧 Available Scrapers

### 📱 Instagram Scrapers
- **Hashtag Scraper**: Extract posts by hashtags
  - Parameters: hashtags, results_limit
  - Example: `["#travel", "#photography"]`
- **Profile Scraper**: Scrape user profile posts
  - Parameters: profile_urls, results_limit
  - Example: `["https://instagram.com/username"]`

### 🏨 Booking.com Scraper
- **Hotel Search**: Find hotels with detailed information
  - Parameters: search, max_items, currency, rooms, adults, children, min_max_price
  - Example: `search="New York", max_items=10, currency="USD"`

### 🐦 Twitter/X Scraper
- **Tweet Extraction**: Gather tweets and user content
  - Parameters: start_urls, search_terms, twitter_handles, max_items
  - Example: `twitter_handles=["@elonmusk"], max_items=20`

### 🌐 Website Content Scraper
- **Content Extraction**: Parse and extract web page content
  - Parameters: start_urls, results_limit, save_markdown
  - Example: `start_urls=["https://docs.apify.com"]`

### 📍 Google Maps Scraper
- **Place Search**: Find businesses and locations
  - Parameters: search_strings, location_query, max_places
  - Example: `search_strings=["restaurant"], location_query="New York, USA"`

## 📊 Data Output

Each scraper returns structured data including:

- **Summary Statistics**: Total items, unique users, engagement metrics
- **Detailed Results**: Complete data with all extracted fields
- **Export Options**: CSV and JSON download capabilities
- **Visual Analytics**: Interactive charts and tables

## 🛠️ Technical Architecture

### Core Technologies
- **Streamlit**: Web application framework
- **Apify**: Web scraping platform with pre-built actors
- **Gemini AI**: Natural language processing and intent recognition
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization

### Project Structure
```
new-streamlit/
├── app.py                 # Main Streamlit application
├── apifyActors/          # Scraper modules
│   ├── instagram_hashtage.py
│   ├── instagram.py
│   ├── booking.py
│   ├── tweet.py
│   ├── website_content.py
│   ├── google_maps.py
│   ├── facebook.py
│   ├── google_news.py
│   └── trip_advisor.py
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

## 🔑 API Configuration

### Required APIs

1. **Apify API Token**
   - Sign up at [Apify Console](https://console.apify.com/)
   - Navigate to Account → Integrations → API tokens
   - Copy your token and paste it in the app

2. **Gemini API Key** (Optional)
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Enable the Gemini API in your Google Cloud Console

## 🎨 Features in Detail

### AI Chatbot Capabilities
- **Natural Language Understanding**: Processes complex requests in plain English
- **Context Awareness**: Remembers conversation history and preferences
- **Error Handling**: Provides helpful suggestions when requests fail
- **Multi-Modal Support**: Handles various input formats and parameters

### Data Processing
- **Real-time Processing**: Instant results with progress indicators
- **Data Validation**: Ensures data quality and completeness
- **Format Conversion**: Automatic conversion between data formats
- **Error Recovery**: Graceful handling of API failures and timeouts

### User Experience
- **Responsive Design**: Works on desktop and mobile devices
- **Dark/Light Mode**: Automatic theme detection
- **Keyboard Shortcuts**: Quick access to common functions
- **Export Options**: Multiple download formats (CSV, JSON, Excel)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd new-streamlit

# Install development dependencies
uv sync --dev

# Run in development mode
streamlit run app.py --server.port 8501
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Apify**: For providing powerful web scraping actors
- **Google**: For the Gemini AI platform
- **Streamlit**: For the excellent web app framework
- **Open Source Community**: For the amazing tools and libraries

## 📞 Support

- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community discussions for help and ideas
- **Documentation**: Check the inline help and tooltips in the app

## 🔮 Roadmap

- [ ] Add more scraping platforms (LinkedIn, TikTok, etc.)
- [ ] Implement advanced analytics and reporting
- [ ] Add scheduled scraping capabilities
- [ ] Create mobile app version
- [ ] Add team collaboration features
- [ ] Implement data visualization dashboards

---

**Made with ❤️ for the data community**

*Transform your web scraping workflow with AI-powered intelligence!*
>>>>>>> Stashed changes
