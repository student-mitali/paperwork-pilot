from agent.tools.profile_tools import load_profile


FIELD_LABELS = {
    "full_name": "Full name",
    "date_of_birth": "Date of birth",
    "address": "Address",
    "phone": "Phone number",
    "email": "Email address",
    "guardian_name": "Guardian name",
    "college_roll_number": "College roll number",
}


def prefill_form(form_fields: list[str], profile: dict | None = None) -> dict:
    """
    Fill requested form fields using the saved demo profile.

    Returns:
    - prefilled: values safely found in the profile
    - missing: values that require user input
    - needs_confirmation: True if the user must review the result
    """
    if profile is None:
        profile = load_profile()

    prefilled = {}
    missing = []

    for field in form_fields:
        value = profile.get(field)

        if value:
            prefilled[field] = value
        else:
            missing.append(field)

    return {
        "prefilled": prefilled,
        "missing": missing,
        "needs_confirmation": len(missing) > 0,
    }


def format_prefill_result(result: dict) -> str:
    """Format the autofill result so it is easy to read in the terminal."""
    lines = ["=== Form Autofill Result ===", "", "Pre-filled fields:"]

    if result["prefilled"]:
        for field, value in result["prefilled"].items():
            label = FIELD_LABELS.get(field, field.replace("_", " ").title())
            lines.append(f"- {label}: {value}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("Fields needing user input:")

    if result["missing"]:
        for field in result["missing"]:
            label = FIELD_LABELS.get(field, field.replace("_", " ").title())
            lines.append(f"- {label}")
    else:
        lines.append("- None")

    lines.append("")
    if result["needs_confirmation"]:
        lines.append("Action: Notify the user to review the missing fields.")
    else:
        lines.append("Action: Form can be prepared for final user confirmation.")

    return "\n".join(lines)