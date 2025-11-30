import requests, time


PHONE = "+911234567890"
TOKEN = "YOUR_TOKEN_HERE"
SERVER = "http://127.0.0.1:5000"


def send_location(lat, lon):
url = SERVER + "/report_location"
headers = {"Authorization": f"Bearer {TOKEN}"}
data = {"phone": PHONE, "lat": lat, "lon": lon}
r = requests.post(url, json=data, headers=headers)
print(r.status_code, r.text)


if __name__ == "__main__":
coords = [(12.9716,77.5946), (12.9718,77.5948), (12.9720,77.5950)]
for lat,lon in coords:
send_location(lat, lon)
time.sleep(2)
