import requests
import json

API_KEY = "napi_7l5jp1v9g8ot8qxcwv1oa57dbew5b0jexcjjha9iccn9m60de28ezh7y10wqdcwq"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

res = requests.get("https://console.neon.tech/api/v2/organizations", headers=headers)
with open("neon_orgs.json", "w") as f:
    f.write(res.text)
