from google.cloud import storage

client = storage.Client()
buckets = list(client.list_buckets())

print("Buckets accessible:", [b.name for b in buckets])
