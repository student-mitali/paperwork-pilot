import json
from pathlib import Path

PROFILE_PATH = Path("data/profile.json")


def load_profile() -> dict:
    """
    Read the demo user profile from data/profile.json.
    This profile is used to pre-fill common form fields.
    """
    if not PROFILE_PATH.exists():
        return {}

    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_profile_summary() -> str:
    """
    Return a safe summary of the demo profile.
    Do not store real sensitive identity data in this public repository.
    """
    profile = load_profile()

    if not profile:
        return "No demo profile found."

    name = profile.get("full_name", "Unknown")
    email = profile.get("email", "Not provided")
    city = profile.get("address", "Not provided")

    return (
        f"Demo profile loaded successfully.\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Address: {city}"
    )