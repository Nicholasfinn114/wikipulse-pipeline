# WikiPulse Pipeline


## 4.1 System Design
The WikiPulse pipeline is designed to capture global Wikipedia edits as they happen, process them for insights, and store them for low-latency analytics.


### Architecture Overview
1.  **Source:** Wikimedia EventStreams (SSE) provides a live feed of JSON events.
2.  **Ingestion Layer:** A Python producer connects to the stream and publishes raw events to Google Cloud Pub/Sub.
3.  **Messaging Layer:** Pub/Sub acts as a buffer to handle high throughput and decouple the producer from the consumer.
4.  **Processing Layer:** A Python consumer validates data, cleans noise (bots), deduplicates events using `event_id`, and transforms timestamps.
5.  **Storage Layer:** MongoDB stores events as independent documents to support flexible schema evolution.
6.  **Analytics Layer:** MongoDB Aggregation Framework is used to generate real-time metrics.



## 4.5 Analytical Queries
Below are the MongoDB queries used to extract insights:


### 1. Top Edited Pages (Last Hour)
```javascript
db.edits.aggregate([
  { $match: { timestamp: { $gte: new Date(ISODate().getTime() - 1000 * 60 * 60) } } },
  { $group: { _id: "$title", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]);
