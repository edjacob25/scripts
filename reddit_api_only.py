import requests

r = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    data={"grant_type": "https://oauth.reddit.com/grants/installed_client", "device_id": "DO_NOT_TRACK_THIS_DEVICE"},
    auth=("ZJKlJzbFxkGauA", ""),
    headers={"User-agent": "Muzei for reddit 0.1"},
)

token = r.json()["access_token"]

r2 = requests.get(
    "https://api.reddit.com/r/earthporn",
    headers={"User-agent": "Muzei for reddit 0.1", "Authentication": "bearer {}".format(token)},
)
