from flask import Flask, jsonify
import random
import time
import os

app = Flask(__name__)

history = []
last_alert_time = 0


@app.route('/data')
def data():
    global last_alert_time

    # Smooth simulated WiFi signal
    if len(history) == 0:
        signal = 70
    else:
        signal = history[-1] + random.randint(-3, 3)
        signal = max(40, min(90, signal))

    history.append(signal)

    if len(history) > 20:
        history.pop(0)

    movement = False
    alert = False

    if len(history) >= 2:
        diff = abs(history[-1] - history[-2])

        # Lower threshold because signal is now smoother
        if diff > 2:
            movement = True

            current_time = time.time()

            # Alert only once every 10 seconds
            if current_time - last_alert_time > 10:
                alert = True
                last_alert_time = current_time

    return jsonify({
        "movement": movement,
        "signal": signal,
        "history": history,
        "alert": alert,
        "timestamp": time.time()
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)