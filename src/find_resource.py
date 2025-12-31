import requests
import json

def find_resource():
    url = "https://data.gov.sg/api/action/package_search"
    params = {
        "q": "Resale flat prices based on registration date from Jan-2017 onwards",
        "rows": 5
    }
    
    resp = requests.get(url, params=params)
    print(f"Status: {resp.status_code}")
    try:
        data = resp.json()
    except:
        print(f"Not JSON: {resp.text[:500]}")
        return

    if data.get('success'):
        print(f"Found {data['result']['count']} packages.")
        for pkg in data['result']['results']:
            print(f"\nPackage: {pkg['title']} (ID: {pkg['id']})")
            for res in pkg['resources']:
                print(f"  - Resource: {res['name']}")
                print(f"    ID: {res['id']}")
                print(f"    Format: {res['format']}")
    else:
        print("Search failed.")

if __name__ == "__main__":
    find_resource()
