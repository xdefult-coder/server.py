from flask import Flask, request, jsonify, abort
from datetime import datetime
import uuid


app = Flask(__name__)


USERS = {}
LOCATIONS = {}


def require_json(req):
if not req.is_json:
abort(400, "Expecting JSON")


@app.route("/register", methods=["POST"])
def register():
require_json(request)
data = request.get_json()
phone = data.get("phone")
label = data.get("label", "")
if not phone:
abort(400, "phone required")
token = str(uuid.uuid4())
USERS[phone] = {"token": token, "label": label}
LOCATIONS.setdefault(phone, [])
return jsonify({"phone": phone, "token": token, "label": label})


@app.route("/report_location", methods=["POST"])
def report_location():
require_json(request)
auth = request.headers.get("Authorization", "")
if not auth.startswith("Bearer "):
abort(401, "Missing token")
token = auth.split()[1]
data = request.get_json()
phone = data.get("phone")
lat = data.get("lat")
lon = data.get("lon")
if not (phone and lat is not None and lon is not None):
abort(400, "phone, lat, lon required")
user = USERS.get(phone)
if not user or user.get("token") != token:
abort(403, "Invalid token")
entry = {"lat": float(lat), "lon": float(lon), "ts": datetime.utcnow().isoformat()}
LOCATIONS.setdefault(phone, []).append(entry)
LOCATIONS[phone] = LOCATIONS[phone][-100:]
return jsonify({"status": "ok", "entry": entry})


@app.route("/get_location/<phone>", methods=["GET"])
def get_location(phone):
token = request.args.get("token") or request.headers.get("Authorization", "").replace("Bearer ", "")
user = USERS.get(phone)
if not user or user.get("token") != token:
abort(403, "Invalid token")
return jsonify({"phone": phone, "label": user.get("label"), "last_locations": LOCATIONS.get(phone, [])})


if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000)
