# Data Use & Public-Safety Rules

The one dataset that ships with this repo is:

```text
data/raw/content_refresh_anonymized.csv
```

It is a small, **anonymized** slice of FlyRank content-performance data — one row per
pseudonymized content item, with observed search/engagement metrics, content metadata,
age/freshness fields, and derived comparison windows.

## What has already been removed

The starter export contains **no**:

- client names
- domains
- URLs
- page titles
- keywords or raw search queries
- product-rule flags used as composite scores you should trust blindly

Only hashed `content_id` / `client_id` labels plus numeric and categorical metrics remain.

Rate columns (`ctr`, `engagement_rate`, `scroll_rate`, `ai_traffic_pct`, `trend_pct`) are
percentages on a 0–100 scale: `ctr = 0.76` means 0.76%, not 76%.

The hashed IDs are pseudonyms derived from FlyRank-internal database identifiers. They
contain no public information, but treat them as pseudonymous, not anonymous: use them
for grouping and joining only, never as model features, and never attempt to map them back.


