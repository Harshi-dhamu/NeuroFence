"""
Result Formatter

Formats scan results into:
- Dictionary
- JSON
- CSV
"""

import json
import csv


def format_as_dictionary(threat_score, severity, confidence, risk_level):
    """
    Returns scan result as a Python dictionary.
    """

    return {
        "Threat Score": threat_score,
        "Severity": severity,
        "Confidence": confidence,
        "Risk Level": risk_level
    }


def format_as_json(result):
    """
    Converts dictionary into JSON format.
    """

    return json.dumps(result, indent=4)


def format_as_csv(result, filename="scan_result.csv"):
    """
    Saves scan result into a CSV file.
    """

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(result.keys())
        writer.writerow(result.values())

    return filename


if __name__ == "__main__":

    result = format_as_dictionary(
        threat_score=50,
        severity="Medium",
        confidence=85,
        risk_level="Medium"
    )

    print("=" * 50)
    print("Dictionary Output")
    print("=" * 50)
    print(result)

    print("\nJSON Output")
    print("=" * 50)
    print(format_as_json(result))

    csv_file = format_as_csv(result)

    print("\nCSV File Created:", csv_file)