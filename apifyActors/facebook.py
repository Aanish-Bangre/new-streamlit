from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_u1bFd9lPhepZD1TERjMIMVNgj3ysMD12mcVn")

# Prepare the Actor input
run_input = {
    "startUrls": [{ "url": "https://www.facebook.com/humansofnewyork/" }],
    "resultsLimit": 20,
    "captionText": False,
}

# Run the Actor and wait for it to finish
run = client.actor("KoJrdxJCTtpon81KY").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)