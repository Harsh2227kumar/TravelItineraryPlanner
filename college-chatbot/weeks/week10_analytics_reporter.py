"""Week 10: Analytics and improvement report demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.analytics import get_analytics_summary, suggest_improvements


def run_demo():
    """Print analytics summary and suggested improvements."""
    print("Week 10 - Analytics and Continuous Improvement\n")

    summary = get_analytics_summary()
    print("Summary:")
    print(summary)
    print("\nSuggestions:")
    for idx, item in enumerate(suggest_improvements(), start=1):
        print(f"{idx}. {item}")


if __name__ == "__main__":
    run_demo()
