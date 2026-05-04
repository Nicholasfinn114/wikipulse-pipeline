# 4.6 Technical Report


## Design Decisions
The decision to use **Google Cloud Pub/Sub** was made to ensure the system is "backpressure-aware." If Wikipedia traffic spikes, the ingestor won't overwhelm the database; instead, the messages will safely queue in Pub/Sub until the processor catches up.


## Trade-offs
We traded **immediate consistency** for **availability**. By using a messaging layer, there is a sub-second delay before an edit appears in the dashboard, but the system is far more resilient to network partitions than a direct-to-database connection.


## Challenges Encountered
The primary challenge was **deduplication**. Because SSE connections can drop and reconnect, we occasionally received the same edit twice. We solved this by using the `meta.id` from Wikimedia as a unique key in MongoDB.


## Scalability
The architecture scales horizontally. As data velocity increases, we can deploy multiple instances of `processor.py` as part of a single Pub/Sub consumer group to process messages in parallel.
