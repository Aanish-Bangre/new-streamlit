# 🤖 AI-Powered Multi-Scraper Dashboard

A Streamlit app that uses Gemini AI + Apify scrapers to extract data from the web via natural language chat or manual dashboard.

---

## ✨ Features

* **💬 AI Chat Interface**: Gemini-powered, understands natural language, auto-detects scrapers, extracts parameters.
* **🕸 Multi-Scraper Support**: Instagram, Booking.com, Twitter/X, Google Maps, Facebook, Google News, TripAdvisor, and websites.
* **📊 Visual Dashboard**: Interactive tables, real-time summaries, export to CSV/JSON.

---

## 🚀 Quick Start

### Requirements

* Python 3.13+, Apify API Token, Gemini API Key (optional)

### Install & Run

```bash
git clone <repository-url>
cd new-streamlit
pip install -r requirements.txt  # or uv sync
streamlit run app.py
```

---

## 🔑 API Key Setup (Environment Variables)

All API keys are now loaded automatically from a `.env` file in the project root. You **do not** need to enter them in the UI.

1. **Create a `.env` file in your project root:**

   ```env
   APIFY_API_TOKEN=your_apify_token_here
   GEMINI_API_KEY=your_gemini_key_here
   ```
   - The Apify token is **required** for all scrapers.
   - The Gemini API key is **optional** (for AI chat features).

2. **The app and all scrapers will automatically use these environment variables.**

---

## 🛠 Scraper Overview

| Platform    | Type            | Key Params                       |
| ----------- | --------------- | -------------------------------- |
| Instagram   | Hashtag/Profile | hashtags, profile_urls           |
| Booking.com | Hotels          | search, max_items, currency      |
| Twitter/X   | Tweets          | twitter_handles, search_terms    |
| Google Maps | Places          | search_strings, location_query   |
| Website     | Content         | start_urls, save_markdown        |
| Facebook    | Posts           | profile_urls                     |
| TripAdvisor | Reviews         | location_query                   |
| Google News | Headlines       | search_terms                     |

---

## 🧠 AI Capabilities

* Understands plain English
* Detects intent and scraper
* Extracts params from text
* Provides real-time feedback and summaries

---

## 📂 Project Structure

```
new-streamlit/
├── app.py
├── apifyActors/
│   ├── instagram.py, booking.py, ...
├── pyproject.toml
├── requirements.txt
├── .env  # <--- Place your API keys here
└── README.md
```

---

## 🤝 Contribute

```bash
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

## 🔮 Roadmap

* [ ] LinkedIn/TikTok scrapers
* [ ] Scheduled scraping
* [ ] Team collaboration
* [ ] Mobile app
* [ ] Advanced dashboards

---

**Made with ❤️ for the data community**
*Chat. Scrape. Analyze.*
