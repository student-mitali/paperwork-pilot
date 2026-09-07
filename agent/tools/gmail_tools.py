import json
import shutil
from datetime import datetime
from pathlib import Path

from agent.tools.form_tools import prefill_form
from agent.tools.profile_tools import load_profile


INCOMING_DIR = Path("data/incoming_forms")
PENDING_REVIEW_DIR = Path("data/pending_reviews")
PROCESSED_DIR = Path("data/processed_forms")


def process_new_forms() -> list[dict]:
    """
    Simulate a Gmail background poller.

    Each JSON file in data/incoming_forms represents a newly detected
    Gmail message containing a form. The function auto-fills available
    details, creates a pending-review record if needed, and moves the
    source message to processed_forms.
    """
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    PENDING_REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    profile = load_profile()
    processed_results = []

    for form_path in INCOMING_DIR.glob("*.json"):
        with form_path.open("r", encoding="utf-8") as file:
            incoming_form = json.load(file)

        required_fields = incoming_form.get("required_fields", [])
        autofill_result = prefill_form(required_fields, profile)

        review_record = {
            "review_id": f"review-{incoming_form['email_id']}",
            "status": "needs_user_review"
            if autofill_result["needs_confirmation"]
            else "ready_for_confirmation",
            "created_at": datetime.now().isoformat(),
            "source_email": {
                "email_id": incoming_form.get("email_id"),
                "from": incoming_form.get("from"),
                "subject": incoming_form.get("subject"),
                "received_at": incoming_form.get("received_at"),
                "deadline": incoming_form.get("deadline"),
                "source": incoming_form.get("source"),
            },
            "form_type": incoming_form.get("form_type"),
            "required_fields": required_fields,
            "prefilled": autofill_result["prefilled"],
            "missing": autofill_result["missing"],
            "needs_confirmation": autofill_result["needs_confirmation"],
        }

        review_path = PENDING_REVIEW_DIR / f"{incoming_form['email_id']}_review.json"

        with review_path.open("w", encoding="utf-8") as file:
            json.dump(review_record, file, indent=2)

        destination = PROCESSED_DIR / form_path.name
        shutil.move(str(form_path), str(destination))

        processed_results.append({
            "subject": incoming_form.get("subject"),
            "review_path": str(review_path),
            "missing": autofill_result["missing"],
            "status": review_record["status"],
        })

    return processed_results


def format_processing_results(results: list[dict]) -> str:
    """Format background-processing outcomes for the terminal."""
    if not results:
        return "No new forms found in the Gmail Forms inbox."

    lines = ["=== Background Form Processing ==="]

    for result in results:
        lines.append("")
        lines.append(f"Detected: {result['subject']}")
        lines.append(f"Status: {result['status']}")
        lines.append(f"Missing fields: {', '.join(result['missing']) or 'None'}")
        lines.append(f"Review record: {result['review_path']}")

    return "\n".join(lines)