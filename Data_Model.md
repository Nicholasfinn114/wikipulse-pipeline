# 4.4 Data Model (MongoDB Design)


## Schema Choice: Event-Based
We have chosen an **Event-Based Schema** (one document per Wikipedia edit).
- **Justification:** Unlike a grouped schema (which might store cou
nts per page), an event-based schema allows us to perform time-series analysis, track individual user behavior, and retain the original granularity of the data for future auditing.


## Indexes
To ensure low-latency analytics, the following indexes are implemented:
1. `event_id`: Unique index to prevent duplicates during stream retries.
2. `timestamp`: Descending index for fast time-window queries (e.g., "last 5 minutes").
3. `user`: To quickly aggregate activity per editor.
4. `title`: To identify trending pages across the global stream.
