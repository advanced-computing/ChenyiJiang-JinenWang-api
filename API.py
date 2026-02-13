import csv
import io

import pandas as pd
from flask import Flask, Response, jsonify, make_response, request

app = Flask(__name__)


df = pd.read_csv("data.csv")


@app.route("/")
def index():
    return "Welcome to my API! Check the README for usage."


@app.route("/data", methods=["GET"])
def list_records():
    results = df.copy()

    for key, value in request.args.items():
        if key in ["limit", "offset", "format"]:
            continue

        if key in results.columns:
            results = results[results[key].astype(str) == value]

    try:
        limit = int(request.args.get("limit", 10000))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        limit = 10000
        offset = 0

    if offset < len(results):
        results = results[offset : offset + limit]
    else:
        results = results[0:0]

    output_format = request.args.get("format", "json").lower()

    if output_format == "csv":
        return Response(
            results.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=data.csv"},
        )
    else:
        return Response(results.to_json(orient="records"), mimetype="application/json")


@app.route("/data/<id>", methods=["GET"])
def get_record(id):
    try:
        lookup_id = int(id)
    except ValueError:
        lookup_id = id

    record = df[df["id"] == lookup_id]

    if record.empty:
        return jsonify({"error": "Record not found"}), 404

    return Response(record.to_json(orient="records"), mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
