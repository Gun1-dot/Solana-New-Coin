import requests
import json
from datetime import datetime, timezone

def get_new_solana_tokens():
    url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    response = requests.get(url)
    data = response.json()

    tokens = []
    now = datetime.now(timezone.utc)

    for pair in data['pairs']:
        if not pair.get('pairCreatedAt'):
            continue

        age_seconds = (now - datetime.fromtimestamp(pair['pairCreatedAt'] / 1000, timezone.utc)).total_seconds()
        if age_seconds > 3600:  # Only tokens younger than 1 hour
            continue

        token = {
            "name": pair['baseToken']['name'],
            "price": pair['priceUsd'],
            "volume": f"{int(float(pair['volume']['h1'])):,}",
            "age": f"{int(age_seconds // 60)} min"
        }
        tokens.append(token)

    # Sort by volume, take top 20
    top_20 = sorted(tokens, key=lambda x: int(x['volume'].replace(',', '')), reverse=True)[:20]

    # Save to JSON
    with open("data.json", "w") as f:
        json.dump(top_20, f, indent=2)

    print("✅ data.json updated with top 20 new tokens")

get_new_solana_tokens()
