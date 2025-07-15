import os
from dotenv import load_dotenv
load_dotenv()
from apify_client import ApifyClient
from datetime import datetime

def scrape_tweets(
    start_urls=None,
    search_terms=None,
    twitter_handles=None,
    conversation_ids=None,
    max_items=100,
    sort="Latest",
    tweet_language="en",
    author=None,
    in_reply_to=None,
    mentioning=None,
    geotagged_near=None,
    within_radius=None,
    geocode=None,
    place_object_id=None,
    minimum_retweets=None,
    minimum_favorites=None,
    minimum_replies=None,
    start=None,
    end=None,
    api_token=None
):
    """
    Scrape tweets and return formatted data.
    Returns: dict with 'success', 'tweets', 'summary', 'raw_results' or 'error'.
    """
    if api_token is None:
        api_token = os.environ.get("APIFY_API_TOKEN")
    try:
        client = ApifyClient(api_token)
        run_input = {
            "startUrls": start_urls or [],
            "searchTerms": search_terms or [],
            "twitterHandles": twitter_handles or [],
            "conversationIds": conversation_ids or [],
            "maxItems": max_items,
            "sort": sort,
            "tweetLanguage": tweet_language,
            "customMapFunction": "(object) => { return {...object} }",
        }
        # Only add optional fields if they are not None or empty
        if author:
            run_input["author"] = author
        if in_reply_to:
            run_input["inReplyTo"] = in_reply_to
        if mentioning:
            run_input["mentioning"] = mentioning
        if geotagged_near:
            run_input["geotaggedNear"] = geotagged_near
        if within_radius:
            run_input["withinRadius"] = within_radius
        if geocode:
            run_input["geocode"] = geocode
        if place_object_id:
            run_input["placeObjectId"] = place_object_id
        if minimum_retweets is not None:
            run_input["minimumRetweets"] = minimum_retweets
        if minimum_favorites is not None:
            run_input["minimumFavorites"] = minimum_favorites
        if minimum_replies is not None:
            run_input["minimumReplies"] = minimum_replies
        if start:
            run_input["start"] = start
        if end:
            run_input["end"] = end
        run = client.actor("61RPP7dywgiy0JPD0").call(run_input=run_input)
        if run is None:
            return {"error": "Failed to start the scraper. Please check your API token."}
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if not raw_results:
            return {"error": "No results found. Please try with different parameters."}
        tweets = []
        for idx, item in enumerate(raw_results, 1):
            created_at = item.get('createdAt')
            formatted_date = "Unknown"
            if created_at:
                try:
                    formatted_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = str(created_at)
            tweets.append({
                "tweet_number": idx,
                "id": item.get("id", ""),
                "text": item.get("fullText", ""),
                "author": item.get("author", {}).get("username", ""),
                "author_name": item.get("author", {}).get("name", ""),
                "created_at": formatted_date,
                "retweets": item.get("retweetCount", 0),
                "likes": item.get("favoriteCount", 0),
                "replies": item.get("replyCount", 0),
                "url": item.get("url", ""),
                "lang": item.get("lang", ""),
                "hashtags": item.get("hashtags", []),
                "mentions": item.get("userMentions", []),
                "media": item.get("media", []),
                "raw_data": item
            })
        summary = {
            "total_tweets": len(tweets),
            "unique_authors": len(set(t["author"] for t in tweets)),
            "total_likes": sum(t["likes"] for t in tweets),
            "total_retweets": sum(t["retweets"] for t in tweets),
            "total_replies": sum(t["replies"] for t in tweets),
            "run_id": run.get('id'),
            "dataset_id": run.get('defaultDatasetId')
        }
        return {
            "success": True,
            "tweets": tweets,
            "summary": summary,
            "raw_results": raw_results
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# For testing
if __name__ == "__main__":
    results = scrape_tweets(
        start_urls=["https://twitter.com/apify"],
        search_terms=["web scraping"],
        twitter_handles=["elonmusk"],
        max_items=5
    )
    if results.get("success"):
        print(f"Scraped {results['summary']['total_tweets']} tweets.")
        for t in results['tweets']:
            print(f"{t['tweet_number']}: @{t['author']} - {t['likes']} likes")
    else:
        print(results.get("error"))