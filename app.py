from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

data = []

@app.route('/')
def home():
    return "API PRO OK"

@app.route('/send', methods=['POST'])
def send():
    value = float(request.json.get("value"))
    data.append(value)
    return jsonify({"status": "added", "total": len(data)})

@app.route('/predict', methods=['GET'])
def predict():
    if len(data) < 5:
        return jsonify({
    "info": "données insuffisantes",
    "prediction": 2.0
})

    arr = np.array(data)

    # 📊 Moyenne + médiane
    mean = np.mean(arr)
    median = np.median(arr)

    # 📉 Derniers tours
    last = arr[-10:]

    # 🔻 Multiplicateurs faibles
    low = np.sum(last < 2)

    # 🔺 Multiplicateurs élevés
    high = np.sum(last > 3)

    # 📈 Tendance
    trend = np.polyfit(range(len(last)), last, 1)[0]

    # 🧠 LOGIQUE PRO
    if low >= 6:
        pred = 4.5
        reason = "many low → high coming"
    elif high >= 5:
        pred = 1.8
        reason = "many high → crash soon"
    elif trend > 0:
        pred = 3.5
        reason = "uptrend"
    elif trend < 0:
        pred = 2.0
        reason = "downtrend"
    else:
        pred = (mean + median) / 2
        reason = "stable average"

    return jsonify({
        "prediction": round(pred, 2),
        "mean": round(mean, 2),
        "median": round(median, 2),
        "trend": round(trend, 3),
        "low_count": int(low),
        "high_count": int(high),
        "reason": reason
    })
