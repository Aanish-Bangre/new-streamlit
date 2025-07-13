from apify_client import ApifyClient
from datetime import datetime

def scrape_instagram_profile(profile_urls, results_limit=20, api_token="apify_api_u1bFd9lPhepZD1TERjMIMVNgj3ysMD12mcVn"):
    """
    Scrape Instagram profile(s) and return formatted data.
    Args:
        profile_urls (list): List of Instagram profile URLs
        results_limit (int): Number of posts to fetch
        api_token (str): Apify API token
    Returns:
        dict: {success, posts, summary, raw_results} or {error}
    """
    try:
        client = ApifyClient(api_token)
        run_input = {
            "directUrls": profile_urls,
            "resultsType": "posts",
            "resultsLimit": results_limit,
            "searchType": "hashtag",
            "searchLimit": 1,
            "addParentData": False,
        }
        run = client.actor("shu8hvrXbJbY3Eb9W").call(run_input=run_input)
        if run is None:
            return {"error": "Failed to start the scraper. Please check your API token."}
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        if not raw_results:
            return {"error": "No results found. Please try with different profile URLs."}
        posts = []
        for idx, post in enumerate(raw_results, 1):
            timestamp = post.get('timestamp')
            formatted_date = "Unknown"
            if timestamp and isinstance(timestamp, (int, float)):
                try:
                    formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = str(timestamp)
            hashtags_text = ""
            if post.get('hashtags'):
                hashtags_text = " ".join([f"#{tag}" for tag in post.get('hashtags', [])])
            posts.append({
                "post_number": idx,
                "username": post.get('ownerUsername', 'Unknown'),
                "full_name": post.get('ownerFullName', ''),
                "posted_date": formatted_date,
                "caption": post.get('caption', ''),
                "likes": post.get('likesCount', 0),
                "comments": post.get('commentsCount', 0),
                "shares": post.get('sharesCount', 0),
                "views": post.get('videoViewCount', 0),
                "hashtags": hashtags_text,
                "post_url": post.get('url', ''),
                "media_type": post.get('mediaType', ''),
                "image_url": post.get('imageUrl', ''),
                "video_url": post.get('videoUrl', ''),
                "raw_data": post
            })
        total_likes = sum(post.get('likesCount', 0) for post in raw_results)
        total_comments = sum(post.get('commentsCount', 0) for post in raw_results)
        total_shares = sum(post.get('sharesCount', 0) for post in raw_results)
        unique_users = len(set(post.get('ownerUsername', 'Unknown') for post in raw_results))
        summary = {
            "total_posts": len(raw_results),
            "unique_users": unique_users,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "run_id": run.get('id'),
            "dataset_id": run.get('defaultDatasetId')
        }
        return {
            "success": True,
            "posts": posts,
            "summary": summary,
            "raw_results": raw_results
        }
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# For testing
if __name__ == "__main__":
    results = scrape_instagram_profile(["https://www.instagram.com/humansofny/"], results_limit=5)
    if results.get("success"):
        print(f"Scraped {results['summary']['total_posts']} posts.")
        for p in results['posts']:
            print(f"{p['post_number']}: @{p['username']} - {p['likes']} likes")
    else:
        print(results.get("error"))