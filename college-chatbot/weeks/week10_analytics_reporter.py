"""Week 10: Analytics and improvement report demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.analytics import get_summary, suggest_improvements, log_interaction


def run_demo():
    """Print analytics summary and suggested improvements."""
    print("Week 10 - Analytics and Continuous Improvement\n")

    log_interaction("When are exams?", "exams", 0.84, "Exam details", False)
    log_interaction("Hostel fee?", "hostel", 0.76, "Hostel fee details", False)
    log_interaction("Random unrelated", "unknown", 0.11, "No confident answer", True)

    summary = get_summary()
    print("Summary:")
    print(summary)
    print("\nSuggestions:")
    for idx, item in enumerate(suggest_improvements(), start=1):
        print(f"{idx}. {item}")


if __name__ == "__main__":
    run_demo()
