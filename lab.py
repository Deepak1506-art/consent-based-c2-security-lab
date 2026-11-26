from datetime import datetime, timezone
from pathlib import Path
import json

class Lab:
    """Fictional endpoint inventory and synthetic security telemetry."""
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.data_dir / "events.jsonl"
        self.clients = [
            {"client_id": "LAB-001", "hostname": "TRAINING-WIN-01",
             "platform": "Windows 11", "status": "ONLINE", "consent": "LAB SIMULATION"},
            {"client_id": "LAB-002", "hostname": "TRAINING-LINUX-01",
             "platform": "Ubuntu 24.04", "status": "ONLINE", "consent": "LAB SIMULATION"},
            {"client_id": "LAB-003", "hostname": "TRAINING-WIN-02",
             "platform": "Windows 10", "status": "OFFLINE", "consent": "LAB SIMULATION"},
        ]
        self.events = self._load_events()

    def _load_events(self):
        if not self.log_file.exists():
            return []
        rows = []
        for line in self.log_file.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return rows

    def _record(self, client_id, event_type, severity, description):
        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "client_id": client_id,
            "event_type": event_type,
            "severity": severity,
            "description": description,
        }
        self.events.insert(0, row)
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")

    def add_demo_events(self, client_id):
        if client_id not in {c["client_id"] for c in self.clients}:
            return False
        samples = [
            ("UNUSUAL_STARTUP_ENTRY", "HIGH",
             "Synthetic indicator: an unfamiliar startup entry was reported."),
            ("SUSPICIOUS_NETWORK_PATTERN", "MEDIUM",
             "Synthetic indicator: repeated outbound connections in sample telemetry."),
            ("INPUT_MONITORING_INDICATOR", "CRITICAL",
             "Synthetic indicator: possible input-monitoring behaviour."),
            ("MEDIA_DEVICE_ACCESS_INDICATOR", "HIGH",
             "Synthetic indicator: unexpected camera or microphone access."),
            ("SCREEN_CAPTURE_INDICATOR", "HIGH",
             "Synthetic indicator: screen-capture behaviour was reported."),
            ("UNUSUAL_PROCESS_ACTIVITY", "MEDIUM",
             "Synthetic indicator: an unrecognized process name appeared in sample data."),
        ]
        for kind, severity, description in samples:
            self._record(client_id, kind, severity, description)
        return True

    def add_demo_events_to_all(self):
        count = 0
        for client in self.clients:
            if self.add_demo_events(client["client_id"]):
                count += 1
        return count

    def detect(self):
        """Simple rule-based triage over synthetic event records."""
        rules = {
            "UNUSUAL_STARTUP_ENTRY": ("Review authorized startup inventory", "HIGH"),
            "SUSPICIOUS_NETWORK_PATTERN": ("Review destination, frequency and process owner", "MEDIUM"),
            "INPUT_MONITORING_INDICATOR": ("Investigate unexpected input-monitoring access", "CRITICAL"),
            "MEDIA_DEVICE_ACCESS_INDICATOR": ("Verify camera/microphone access against user consent", "HIGH"),
            "SCREEN_CAPTURE_INDICATOR": ("Verify screen-capture activity and application authorization", "HIGH"),
            "UNUSUAL_PROCESS_ACTIVITY": ("Validate process publisher, path and execution context", "MEDIUM"),
        }
        findings = []
        for event in self.events:
            if event["event_type"] in rules:
                action, priority = rules[event["event_type"]]
                findings.append({**event, "recommended_action": action, "priority": priority})
        return findings

    def stats(self):
        return {
            "endpoints": len(self.clients),
            "online": sum(c["status"] == "ONLINE" for c in self.clients),
            "events": len(self.events),
            "high": sum(e["severity"] in {"HIGH", "CRITICAL"} for e in self.events),
        }

    def reset(self):
        self.events = []
        if self.log_file.exists():
            self.log_file.unlink()
