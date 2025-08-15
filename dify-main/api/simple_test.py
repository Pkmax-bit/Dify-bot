import requests

print("Testing API endpoints...")

# Test apps list
try:
    r = requests.get("http://localhost:5001/console/api/apps")
    print(f"Apps API: Status {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        apps = data.get('data', [])
        print(f"Found {len(apps)} apps")
        if apps:
            app = apps[0]
            print(f"First app: {app.get('name')} - Site: {app.get('enable_site')} - API: {app.get('enable_api')}")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Error: {e}")
