from flask import Flask, render_template, request, jsonify, redirect, session
from models import (
    create_table,
    add_shipment,
    get_shipment,
    update_shipment,
    delete_shipment,
    get_tracking_history,
    get_dashboard_counts
)
import sqlite3
app = Flask(__name__)
app.secret_key = "cargo_flow_secret_key"

create_table()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect("/login")
    return render_template("admin.html")


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json

    username = data["username"]
    password = data["password"]

    if username == "admin" and password == "1234":
        session["admin_logged_in"] = True
        return jsonify({"message": "Login Successful"})

    return jsonify({"error": "Invalid username or password"})


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/api/add", methods=["POST"])
def api_add():
    data = request.json

    added = add_shipment(
        data["tracking_id"],
        data["sender"],
        data["receiver"],
        data["status"],
        data["location"]
    )

    if added:
        return jsonify({
            "message": "Shipment Added Successfully"
        })

    return jsonify({
        "error": "Tracking ID already exists. Use Update Shipment instead."
    })


@app.route("/api/track/<tracking_id>")
def api_track(tracking_id):
    shipment = get_shipment(tracking_id)

    if shipment:
        return jsonify({
            "tracking_id": shipment["tracking_id"],
            "sender": shipment["sender"],
            "receiver": shipment["receiver"],
            "status": shipment["status"],
            "location": shipment["location"],
            "updated_at": shipment["updated_at"]
        })

    return jsonify({
        "error": "Shipment Not Found"
    })



@app.route("/api/update", methods=["PUT"])
def api_update():
    data = request.json

    updated = update_shipment(
        data["tracking_id"],
        data["status"],
        data["location"]
    )

    if updated:
        return jsonify({
            "message": "Shipment Updated Successfully"
        })

    return jsonify({
        "error": "Shipment Not Found"
    })

@app.route("/api/delete/<tracking_id>", methods=["DELETE"])
def delete_shipment_api(tracking_id):
    deleted = delete_shipment(tracking_id)

    if deleted:
        return jsonify({
            "message": "Shipment Deleted Successfully"
        })

    return jsonify({
        "error": "Shipment Not Found"
    })

@app.route("/api/history/<tracking_id>")
def api_history(tracking_id):
    history = get_tracking_history(tracking_id)

    return jsonify([
        {
            "status": item["status"],
            "location": item["location"],
            "updated_at": item["updated_at"]
        }
        for item in history
    ])


@app.route("/api/dashboard")
def api_dashboard():
    return jsonify(get_dashboard_counts())



if __name__ == "__main__":
    app.run(debug=True)