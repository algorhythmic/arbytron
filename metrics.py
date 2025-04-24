from prometheus_client import Counter

# Number of quotes ingested
quotes_ingested = Counter("quotes_ingested", "Total number of market quotes ingested into the database")
