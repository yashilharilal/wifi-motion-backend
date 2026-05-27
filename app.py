from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

history = []
last_alert_time = 0

@app.route('/data')
def data():

    global last_alert_time

    signal = random.randint(40, 90)
    history.append(signal)

    if len(history) > 20:
        history.pop(0)

    movement = False
    alert = False

    if len(history) >= 2:
        diff = abs(history[-1] - history[-2])

        if diff > 10:
            movement = True

            # 🔥 COOLDOWN (5 seconds)
            current_time = time.time()
            if current_time - last_alert_time > 5:
                alert = True
                last_alert_time = current_time

    return jsonify({
        "movement": movement,
        "signal": signal,
        "history": history,
        "alert": alert
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

    