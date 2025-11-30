# server.py
# Location Sharing System (Consent-Based)


A simple Flask server + Python client location reporting system.
Works on Termux, Kali Linux, Ubuntu, Windows.


## Install
pip install -r requirements.txt


## Run server
python3 server.py


## Register phone
curl -X POST -H "Content-Type: application/json" -d '{"phone":"+911234567890","label":"Device"}' http://127.0.0.1:5000/register


## Use client
python3 client_send.py
