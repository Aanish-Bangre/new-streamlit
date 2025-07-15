import os
from dotenv import load_dotenv
load_dotenv()
from apify_client import ApifyClient
from datetime import datetime

def scrape_google_maps(
    search_strings=None,
    location_query="New York, USA",
    max_places=50,
    language="en",
    api_token=None
):
    if api_token is None:
        api_token = os.environ.get("APIFY_API_TOKEN")
    """
    Scrape Google Maps places and return formatted data.
    Returns: dict with 'success', 'places', 'summary', 'raw_results' or 'error'.
    """
    try:
        client = ApifyClient(api_token)
        run_input = {
            "searchStringsArray": search_strings or ["restaurant"],
            "locationQuery": location_query,
            "maxCrawledPlacesPerSearch": max_places,
            "language": language,
            "searchMatching": "all",
            "placeMinimumStars": "",
            "website": "allPlaces",
            "skipClosedPlaces": False,
            "scrapePlaceDetailPage": False,
            "scrapeTableReservationProvider": False,
            "includeWebResults": False,
            "scrapeDirectories": False,
            "maxQuestions": 0,
            "scrapeContacts": False,
            "maximumLeadsEnrichmentRecords": 0,
            "maxReviews": 0,
            "reviewsSort": "newest",
            "reviewsFilterString": "",
            "reviewsOrigin": "all",
            "scrapeReviewsPersonalData": True,
            "maxImages": 0,  # FIXED: must be integer, not None
            "scrapeImageAuthors": False,
            "allPlacesNoSearchAction": "",
        }
        run = client.actor("nwua9Gu5YrADL7ZDj").call(run_input=run_input)
        if run is None:
            return {"error": "Failed to start the scraper. Please check your API token."}
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if not raw_results:
            return {"error": "No results found. Please try with different parameters."}
        places = []
        for idx, item in enumerate(raw_results, 1):
            places.append({
                "place_number": idx,
                "name": item.get("title", ""),
                "address": item.get("address", ""),
                "category": item.get("category", ""),
                "rating": item.get("totalScore", ""),
                "reviews": item.get("reviewsCount", 0),
                "url": item.get("url", ""),
                "website": item.get("website", ""),
                "phone": item.get("phone", ""),
                "raw_data": item
            })
        summary = {
            "total_places": len(places),
            "search_strings": search_strings,
            "location_query": location_query,
            "run_id": run.get('id'),
            "dataset_id": run.get('defaultDatasetId')
        }
        return {
            "success": True,
            "places": places,
            "summary": summary,
            "raw_results": raw_results
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# For testing
if __name__ == "__main__":
    results = scrape_google_maps()
    if results.get("success"):
        print(f"Scraped {results['summary']['total_places']} places.")
        for p in results['places']:
            print(f"{p['place_number']}: {p['name']} - {p['address']}")
    else:
        print(results.get("error"))