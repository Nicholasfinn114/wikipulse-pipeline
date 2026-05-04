import json
import requests
from sseclient import SSEClient
from google.cloud import pubsub_v1

# Configuration
STREAM_URL = 'https://stream.wikimedia.org/v2/stream/recentchange'
PROJECT_ID = "wikipulse-project"
TOPIC_ID = "wiki-raw-edits"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def ingest_stream():
    print(f"Connecting to {STREAM_URL}...")
    messages = SSEClient(STREAM_URL)
    
    for msg in messages:
        if msg.event == 'message':
            try:
                event_data = json.loads(msg.data)
                # Filter for only edit events if necessary
                if event_data.get('type') == 'edit':
                    data_str = json.dumps(event_data).encode("utf-8")
                    publisher.publish(topic_path, data_str)
            except ValueError:
                continue

if __name__ == "__main__":
    ingest_stream()
