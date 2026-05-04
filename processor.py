import json
from google.cloud import pubsub_v1
from pymongo import MongoClient, UpdateOne
from datetime import datetime

# Configuration
SUBSCRIPTION_ID = "wiki-processor-sub"
MONGO_URI = "mongodb://localhost:27017/"
db = MongoClient(MONGO_URI)['wikipulse']
collection = db['edits']

def process_message(message):
    try:
        data = json.loads(message.data.decode('utf-8'))
        
        # 1. Transform & Clean
        processed_event = {
            "event_id": data.get("meta", {}).get("id"),
            "timestamp": datetime.fromtimestamp(data.get("timestamp", 0)),
            "user": data.get("user", "Unknown"),
            "title": data.get("title", "No Title"),
            "bot": data.get("bot", False),
            "server_name": data.get("server_name"),
            "length_change": data.get("length", {}).get("new", 0) - data.get("length", {}).get("old", 0)
        }

        # 2. Deduplication & Upsert (Using event_id)
        if processed_event["event_id"]:
            collection.update_one(
                {"event_id": processed_event["event_id"]},
                {"$set": processed_event},
                upsert=True
            )
        
        message.ack()
    except Exception as e:
        print(f"Error processing: {e}")
        message.nack()

def start_processing():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("wikipulse-project", SUBSCRIPTION_ID)
    
    print("Listening for messages...")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_message)
    
    with subscriber:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()

if __name__ == "__main__":
    start_processing()
