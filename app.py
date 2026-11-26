from flask import Flask, render_template, redirect, url_for, request, flash, Response
from datetime import datetime, timezone
from pathlib import Path
import json
import csv
import io
from lab import Lab

app = Flask(__name__)
app.secret_key = "change-this-for-local-development"
lab = Lab(Path("data"))

@app.route("/")
def index():
    return render_template("index.html",
        clients=lab.clients,
        events=lab.events[:12],
        stats=lab.stats())

@app.post("/demo/<client_id>")
def demo(client_id):
    if lab.add_demo_events(client_id):
        flash(f"Synthetic telemetry added for {client_id}.", "success")
    else:
        flash("Unknown lab endpoint.", "error")
    return redirect(url_for("index"))

@app.post("/demo-all")
def demo_all():
    count = lab.add_demo_events_to_all()
    flash(f"Added synthetic telemetry to {count} lab endpoints.", "success")
    return redirect(url_for("index"))

@app.route("/clients")
def clients():
    return render_template("clients.html", clients=lab.clients)

@app.route("/events")
def events():
    severity = request.args.get("severity", "ALL").upper()
    rows = lab.events
    if severity in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        rows = [e for e in rows if e["severity"] == severity]
    return render_template("events.html", events=rows, severity=severity)

@app.route("/detections")
def detections():
    return render_template("detections.html", detections=lab.detect())

@app.route("/export.csv")
def export_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "timestamp", "client_id", "event_type", "severity", "description"
    ])
    writer.writeheader()
    for event in lab.events:
        writer.writerow(event)
    return Response(output.getvalue(), mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=lab_events.csv"})

@app.post("/reset")
def reset():
    lab.reset()
    flash("Lab data reset.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Local-only development server. Do not expose this training dashboard publicly.
    app.run(host="127.0.0.1", port=5000, debug=True)
