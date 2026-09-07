from agent.tools.gmail_tools import format_processing_results, process_new_forms


def main():
    print("=== Paperwork Pilot Background Agent ===")
    print("Scanning the Forms inbox...\n")

    results = process_new_forms()

    print(format_processing_results(results))


if __name__ == "__main__":
    main()