import os
from dotenv import load_dotenv
load_dotenv()
from apify_client import ApifyClient

api_token = os.environ.get("APIFY_API_TOKEN")
client = ApifyClient(api_token)

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