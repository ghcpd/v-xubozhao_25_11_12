
from flask import Flask, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    data = np.array([1, 2, 3])
    df = pd.DataFrame(data, columns=["numbers"])
    return jsonify({"sum": int(df["numbers"].sum())})

if __name__ == "__main__":
    app.run(debug=True)
