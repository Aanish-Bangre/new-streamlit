import os
from dotenv import load_dotenv
load_dotenv()
from apify_client import ApifyClient

api_token = os.environ.get("APIFY_API_TOKEN")
client = ApifyClient(api_token)

# Prepare the Actor input
run_input = {
    "url": "https://www.tripadvisor.com/Hotels-g188082-Jungfrau_Region_Bernese_Oberland_Canton_of_Bern-Hotels.html",
    "offset": 0,
    "count": 100,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
    },
}

# Run the Actor and wait for it to finish
run = client.actor("r6WbvwpdX4XIb61OM").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)