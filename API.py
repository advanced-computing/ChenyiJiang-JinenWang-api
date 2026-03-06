import csv
import io

import duckdb
import pandas as pd
from flask import Flask, Response, jsonify, make_response, request

from data_clean import load_and_clean_data

app = Flask(__name__)

df = load_and_clean_data("data.csv")


@app.route("/")
def index():
    return "Welcome to my API! Check the README for usage."


@app.route("/data", methods=["GET"])
def list_records():
    conn = duckdb.connect("my_database.db")
    df = conn.sql("SELECT * FROM loan_data").df()
    conn.close()

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


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    username = data.get("username")
    age = data.get("age")
    country = data.get("country")

    if not username or not age or not country:
        return jsonify({"error": "Missing username, age, or country"}), 400

    conn = duckdb.connect("my_database.db")

    conn.execute(
        "INSERT INTO users (username, age, country) VALUES (?, ?, ?)",
        (username, age, country),
    )
    conn.close()

    return jsonify({"message": f"User '{username}' successfully added!"}), 201


@app.route("/users/stats", methods=["GET"])
def get_user_stats():
    conn = duckdb.connect("my_database.db")

    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    avg_age = conn.execute("SELECT AVG(age) FROM users").fetchone()[0]
    if avg_age is None:
        avg_age = 0
    else:
        avg_age = round(avg_age, 1)

    top_countries_data = conn.execute("""
        SELECT country, COUNT(*) as user_count 
        FROM users 
        GROUP BY country 
        ORDER BY user_count DESC 
        LIMIT 3
    """).fetchall()

    conn.close()

    top_countries = [{"country": row[0], "count": row[1]} for row in top_countries_data]

    return jsonify(
        {
            "total_users": total_users,
            "average_age": avg_age,
            "top_countries": top_countries,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
