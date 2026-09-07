from agent.tools.form_tools import format_prefill_result, prefill_form
from agent.tools.profile_tools import load_profile


def main():
    print("=== Paperwork Pilot ===")
    print("Checking a newly detected demo form...\n")

    detected_form_fields = [
        "full_name",
        "date_of_birth",
        "address",
        "phone",
        "email",
        "college_roll_number",
    ]

    profile = load_profile()
    result = prefill_form(detected_form_fields, profile)

    print(format_prefill_result(result))


if __name__ == "__main__":
    main()