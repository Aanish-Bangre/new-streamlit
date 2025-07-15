import os
from dotenv import load_dotenv
load_dotenv()
from apify_client import ApifyClient
from datetime import datetime

def scrape_booking(search="New York", max_items=10, property_type="none", sort_by="distance_from_search", stars_count_filter="any", currency="USD", language="en-gb", rooms=1, adults=2, children=0, min_max_price="0-999999", api_token=None):
    """
    Scrape Booking.com for hotels and return formatted data.
    Returns: dict with 'success', 'hotels', 'summary', 'raw_results' or 'error'.
    """
    if api_token is None:
        api_token = os.environ.get("APIFY_API_TOKEN")
    try:
        client = ApifyClient(api_token)
        run_input = {
            "search": search,
            "maxItems": max_items,
            "propertyType": property_type,
            "sortBy": sort_by,
            "starsCountFilter": stars_count_filter,
            "currency": currency,
            "language": language,
            "rooms": rooms,
            "adults": adults,
            "children": children,
            "minMaxPrice": min_max_price,
        }
        run = client.actor("oeiQgfg5fsmIJB7Cn").call(run_input=run_input)
        if run is None:
            return {"error": "Failed to start the scraper. Please check your API token."}
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if not raw_results:
            return {"error": "No results found. Please try with different search parameters."}
        hotels = []
        for idx, item in enumerate(raw_results, 1):
            hotels.append({
                "hotel_number": idx,
                "name": item.get("name", "Unknown"),
                "address": item.get("address", ""),
                "city": item.get("city", ""),
                "country": item.get("country", ""),
                "price": item.get("price", "N/A"),
                "currency": item.get("currency", ""),
                "stars": item.get("stars", "N/A"),
                "review_score": item.get("reviewScore", "N/A"),
                "review_count": item.get("reviewCount", "N/A"),
                "url": item.get("url", ""),
                "image": item.get("mainPhotoUrl", ""),
                "raw_data": item
            })
        summary = {
            "total_hotels": len(hotels),
            "city": search,
            "min_price": min([float(h["price"]) for h in hotels if h["price"] not in (None, "N/A", "")], default="N/A"),
            "max_price": max([float(h["price"]) for h in hotels if h["price"] not in (None, "N/A", "")], default="N/A"),
            "currency": currency
        }
        return {
            "success": True,
            "hotels": hotels,
            "summary": summary,
            "raw_results": raw_results
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# For testing
if __name__ == "__main__":
    results = scrape_booking()
    if results.get("success"):
        print(f"Scraped {results['summary']['total_hotels']} hotels.")
        for h in results['hotels']:
            print(f"{h['hotel_number']}: {h['name']} - {h['price']} {h['currency']}")
    else:
        print(results.get("error"))