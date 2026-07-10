
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
app = Flask(__name__)
CORS(app)

devices = {}
temperatureData = {
    "Z1T1": 0,
    "Z1H1": 0,
    "Z2T1": 0,
    "Z2H1": 0,
    "Z3T1": 0,
    "Z3H1": 0,
    "Z4T1": 0,
    "Z4H1": 0
}
@app.route('/update', methods=['POST'])
def update():

    data = request.get_json()

    deviceName = data['deviceName']
    status = data['status']

    print("Received:", deviceName, status)

    if deviceName not in devices:
        devices[deviceName] = {
            "status": 0 if status == 2 else status,
            "lastSeen": time.time()
        }
    else:
        devices[deviceName]["lastSeen"] = time.time()

        if status != 2:
            devices[deviceName]["status"] = status
        else:
            print("Heartbeat received, keeping previous status")

    print("Current devices =", devices)

    return "OK", 200

@app.route('/updateTemperature', methods=['POST'])
def updateTemperature():

    global temperatureData

    data = request.get_json()

    temperatureData.update(data)

    print("Temperature Data:", temperatureData)

    return "OK", 200
@app.route('/api/devices')
def api_devices():

    print("Sending devices =", devices)

    result = []

    for device, info in devices.items():

        currentStatus = info["status"]

        if time.time() - info["lastSeen"] > 15:
            currentStatus = -1

        result.append({
            "deviceName": device,
            "status": currentStatus
        })

    response = jsonify(result)

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
@app.route('/api/temperature')
def api_temperature():

    return jsonify(temperatureData)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
