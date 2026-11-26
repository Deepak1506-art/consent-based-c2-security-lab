# Consent-Based RAT & C2 Behaviour Analysis Lab

A ready-to-run local Python/Flask project for studying endpoint inventory,
command-and-control terminology, malware-behaviour indicators, event logging,
and defensive detection.

## Safety and scope

This is a **defensive training lab**, not a deployable remote-access trojan.
It uses fictional endpoints and synthetic events. It does not:
- connect to or control remote computers;
- execute remote shell commands or arbitrary Python;
- capture keystrokes, webcam, microphone, or screen content;
- install persistence or modify operating-system startup settings;
- transfer files from another device.

The dashboard runs on `127.0.0.1` (your own computer) only.

## Requirements

- Python 3.9+
- pip

## Setup (Windows)

Open Command Prompt or the VS Code terminal in this folder:

```bash
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Setup (Linux/macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Demo

1. Open the dashboard.
2. Click **Add sample events** beside an endpoint, or **Generate demo telemetry for all**.
3. Open **Event Logs** and filter by severity.
4. Open **Detections** to see defensive recommendations.
5. Use **Export events as CSV** to download the lab telemetry.

## Project structure

```text
consent_based_c2_lab/
├── app.py
├── lab.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── clients.html
│   ├── events.html
│   └── detections.html
├── static/
│   └── style.css
├── tests/
│   └── test_lab.py
└── data/                 # created automatically
    └── events.jsonl
```

## Technologies

Python, Flask, HTTP routing on localhost, JSONL logging, CSV export, HTML,
CSS, and rule-based event analysis.

## Learning outcomes

- Endpoint inventory and client identification
- C2 concepts and centralized event visibility
- Event severity and defensive triage
- Persistent audit logs and CSV reporting
- Malware-behaviour indicators and detection recommendations

## Testing

```bash
python -m unittest discover -s tests -v
```

## Portfolio description

**Python-Based C2 Behaviour Analysis and Threat Detection Lab**

Developed a local Flask dashboard that models endpoint inventory and common
remote-access-threat indicators using synthetic telemetry. Implemented
centralized event logging, severity filtering, CSV export, and rule-based
defensive recommendations. The project demonstrates Python application
development, web routing, structured logging, and practical security analysis.
