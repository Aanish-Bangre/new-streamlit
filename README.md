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

Set your API keys in a `.env` file.

---

## 🛠 Scraper Overview

| Platform    | Type            | Key Params                       |
| ----------- | --------------- | -------------------------------- |
| Instagram   | Hashtag/Profile | hashtags, profile\_urls          |
| Booking.com | Hotels          | search, max\_items, currency     |
| Twitter/X   | Tweets          | twitter\_handles, search\_terms  |
| Google Maps | Places          | search\_strings, location\_query |
| Website     | Content         | start\_urls, save\_markdown      |
| Facebook    | Posts           | profile\_urls                    |
| TripAdvisor | Reviews         | location\_query                  |
| Google News | Headlines       | search\_terms                    |

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
└── README.md
```

---

## 🔑 API Setup

* [Apify Token](https://console.apify.com/account/integrations)
* [Gemini API Key](https://makersuite.google.com/app/apikey) *(optional)*

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
