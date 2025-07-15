import os
from dotenv import load_dotenv
load_dotenv()
from apify_client import ApifyClient
from datetime import datetime

def scrape_website_content(
    start_urls=None,
    results_limit=20,
    save_markdown=True,
    api_token=None
):
    """
    Scrape website content and return formatted data.
    Returns: dict with 'success', 'pages', 'summary', 'raw_results' or 'error'.
    """
    if api_token is None:
        api_token = os.environ.get("APIFY_API_TOKEN")
    try:
        client = ApifyClient(api_token)
        run_input = {
            "startUrls": [{"url": url} for url in (start_urls or ["https://docs.apify.com/academy/web-scraping-for-beginners"])],
            "resultsLimit": results_limit,
            "saveMarkdown": save_markdown,
            # ... (other default params can be added as needed)
        }
        run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)
        if run is None:
            return {"error": "Failed to start the scraper. Please check your API token."}
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if not raw_results:
            return {"error": "No results found. Please try with different parameters."}
        pages = []
        for idx, item in enumerate(raw_results, 1):
            pages.append({
                "page_number": idx,
                "url": item.get("url", ""),
                "title": item.get("title", ""),
                "markdown": item.get("markdown", ""),
                "text": item.get("text", ""),
                "raw_data": item
            })
        summary = {
            "total_pages": len(pages),
            "start_urls": start_urls,
            "run_id": run.get('id'),
            "dataset_id": run.get('defaultDatasetId')
        }
        return {
            "success": True,
            "pages": pages,
            "summary": summary,
            "raw_results": raw_results
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# For testing
if __name__ == "__main__":
    results = scrape_website_content()
    if results.get("success"):
        print(f"Scraped {results['summary']['total_pages']} pages.")
        for p in results['pages']:
            print(f"{p['page_number']}: {p['title']} - {p['url']}")
    else:
        print(results.get("error"))