import json
import uuid
from datetime import datetime, timezone

def review_gate_v1(report, decision, reviewer_note=""):
    if decision not in {"approve", "edit", "reject"}:
        raise ValueError(f"Invalid decision: {decision}")
    upd = dict(report)
    upd["review_decision"] = decision
    upd["reviewer_note"] = reviewer_note
    upd["external_use_allowed"] = (decision == "approve")
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": upd.get("run_id", str(uuid.uuid4())),
        "region": upd.get("region", "UNKNOWN"),
        "decision": decision,
        "reviewer_note": reviewer_note
    }
    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")
    return upd

if __name__ == "__main__":
    sample = {"region": "Guntur", "content": "Summary"}
    for d, n in [("approve", "ok"), ("edit", "refine"), ("reject", "redo")]:
        review_gate_v1(sample, d, n)
