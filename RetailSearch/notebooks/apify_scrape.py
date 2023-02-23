from apify_client import ApifyClient
apify_client = ApifyClient('apify_api_798Yf5dd9Yn2Zcf8TORMMtq9KPbFcM0OGc3c')

# Start an actor and waits for it to finish
actor_call = apify_client.actor('john-doe/my-cool-actor').call()

# Fetch results from the actor's default dataset
dataset_items = apify_client.dataset(actor_call['defaultDatasetId']).list_items().items