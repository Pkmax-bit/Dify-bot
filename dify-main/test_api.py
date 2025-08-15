import requests

# Test API connection
try:
    response = requests.get("http://localhost:5001/console/api/apps")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        apps = data.get('data', [])
        print(f"Found {len(apps)} apps:")
        for app in apps:
            print(f"  - {app['name']} (Site: {app.get('enable_site')}, API: {app.get('enable_api')})")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
