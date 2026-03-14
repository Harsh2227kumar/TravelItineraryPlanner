"""Week 6: Entity extraction demo."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.entities import extract_entities


def run_demo():
    """Run sample entity extraction for week 6."""
    print("Week 6 - Entity Extraction")
    samples = [
        "When is the SEM 5 CS301 exam on March 15th?",
        "Show timetable for semester 6",
        "What is the fee?",
    ]

    for query in samples:
        entities = extract_entities(query)
        print(f"Query: {query}")
        print(f"Entities: {entities}\n")


if __name__ == "__main__":
    run_demo()
