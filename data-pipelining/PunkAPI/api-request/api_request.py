import requests

BASE_URL = "https://punkapi.online/v3/beers"

def fetch_all_beers(per_page=80):
    """
    Fetch details of all beers from Punk API (paginated).
    """
    all_beers = []
    page = 1
    while True:
        try:
            api_url = f"{BASE_URL}?page={page}&per_page={per_page}"
            response = requests.get(api_url)
            response.raise_for_status()
            beers = response.json()
            if not beers:  # no more beers
                break
            all_beers.extend(beers)
            print(f"✅ Retrieved page {page}, {len(beers)} beers")
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"An Error Occurred! {e}")
            break
    return all_beers

if __name__ == "__main__":
    beers_data = fetch_all_beers()
    print(f"\nTotal beers fetched: {len(beers_data)}\n")

    # Print sample (first 3 beers only, to avoid massive output)
    for beer in beers_data[:3]:
        print(f"ID: {beer['id']}, Name: {beer['name']}, ABV: {beer['abv']}")
