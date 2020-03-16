from expiringdict import ExpiringDict

albums_cache = ExpiringDict(max_age_seconds=10000, max_len=200)
