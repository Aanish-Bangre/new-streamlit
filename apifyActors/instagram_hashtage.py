from apify_client import ApifyClient
import json
from datetime import datetime

def scrape_instagram_posts(api_token, hashtags, results_limit=20):
    """
    Scrape Instagram posts for given hashtags and return formatted data
    
    Args:
        api_token (str): Apify API token
        hashtags (list): List of hashtags to scrape
        results_limit (int): Maximum number of results
    
    Returns:
        dict: Formatted data with posts and summary
    """
    try:
        # Initialize client
        client = ApifyClient(api_token)
        
        # Prepare run input
        run_input = {
            "hashtags": hashtags,
            "resultsType": "posts",
            "resultsLimit": results_limit,
        }
        
        # Run the Actor
        run = client.actor("apify/instagram-hashtag-scraper").call(run_input=run_input)
        
        if run is None:
            return {"error": "Failed to start the scraper. Please check your API token."}
        
        # Fetch results
        raw_results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        if not raw_results:
            return {"error": "No results found. Please try with different hashtags."}
        
        # Format the data
        formatted_posts = []
        for post in raw_results:
            # Format timestamp
            timestamp = post.get('timestamp')
            formatted_date = "Unknown"
            if timestamp and isinstance(timestamp, (int, float)):
                try:
                    formatted_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = str(timestamp)
            
            # Format hashtags
            hashtags_text = ""
            if post.get('hashtags'):
                hashtags_text = " ".join([f"#{tag}" for tag in post.get('hashtags', [])])
            
            # Create formatted post
            formatted_post = {
                "post_number": len(formatted_posts) + 1,
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
                "raw_data": post  # Keep original data for reference
            }
            formatted_posts.append(formatted_post)
        
        # Calculate summary
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
        
        # Save raw results to file
        with open("instagram_results.json", "w", encoding="utf-8") as f:
            json.dump(raw_results, f, indent=4, ensure_ascii=False)
        
        return {
            "success": True,
            "posts": formatted_posts,
            "summary": summary,
            "raw_results": raw_results
        }
        
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# For testing the module directly
if __name__ == "__main__":
    # Test the scraper
    api_token = "apify_api_u1bFd9lPhepZD1TERjMIMVNgj3ysMD12mcVn"
    hashtags = ["Goa"]
    results = scrape_instagram_posts(api_token, hashtags, 5)
    
    if results.get("success"):
        print(f"Successfully scraped {results['summary']['total_posts']} posts")
        for post in results['posts']:
            print(f"Post {post['post_number']}: @{post['username']} - {post['likes']} likes")
    else:
        print(f"Error: {results.get('error')}")