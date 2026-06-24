from flask import Flask, jsonify, request
import random
import time
import os

app = Flask(__name__)

room_states = {}


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def create_room_if_missing(room_name):
    if room_name not in room_states:
        room_states[room_name] = {
            "history": [],
            "last_alert_time": 0
        }


def generate_signal(history):
    if len(history) == 0:
        return random.randint(65, 75)

    previous_signal = history[-1]
    normal_change = random.randint(-2, 2)

    movement_event = random.random() < 0.12

    if movement_event:
        large_change = random.choice([-9, -8, -7, 7, 8, 9])
        new_signal = previous_signal + large_change
    else:
        new_signal = previous_signal + normal_change

    return clamp(new_signal, 40, 90)


@app.route("/")
def home():
    return jsonify({
        "message": "Smart Motion Custom Room Backend Running",
        "example": "/data?rooms=Bedroom,Bathroom,Garage"
    })


@app.route("/data")
def data():
    rooms_param = request.args.get("rooms", "")

    if rooms_param.strip() == "":
        requested_rooms = ["Bedroom"]
    else:
        requested_rooms = [
            room.strip()
            for room in rooms_param.split(",")
            if room.strip() != ""
        ]

    room_results = []

    for room_name in requested_rooms:
        create_room_if_missing(room_name)

        room_info = room_states[room_name]
        history = room_info["history"]

        signal = generate_signal(history)

        history.append(signal)

        if len(history) > 20:
            history.pop(0)

        movement = False
        alert = False

        if len(history) >= 2:
            diff = abs(history[-1] - history[-2])

            if diff >= 5:
                movement = True

                current_time = time.time()

                if current_time - room_info["last_alert_time"] > 10:
                    alert = True
                    room_info["last_alert_time"] = current_time

        room_results.append({
            "name": room_name,
            "signal": signal,
            "movement": movement,
            "alert": alert,
            "history": history
        })

    return jsonify({
        "rooms": room_results,
        "timestamp": time.time()
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)