"""
Scoring Engine

Calculates:
- Threat Score
- Severity
- Confidence
- Risk Level
"""


def calculate_threat_score(keyword_count, pattern_count):
    """
    Calculate threat score based on detected keywords and patterns.
    """

    score = (keyword_count * 10) + (pattern_count * 5)

    return min(score, 100)


def calculate_severity(score):
    """
    Returns severity level based on threat score.
    """

    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Low"
    else:
        return "Safe"


def calculate_confidence(keyword_count, pattern_count):
    """
    Calculates confidence percentage.
    """

    confidence = (keyword_count * 15) + (pattern_count * 10)

    return min(confidence, 100)


def calculate_risk_level(score):
    """
    Returns overall risk level.
    """

    if score >= 80:
        return "Very High"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    elif score >= 20:
        return "Low"
    else:
        return "Minimal"


if __name__ == "__main__":

    keyword_count = 3
    pattern_count = 4

    threat_score = calculate_threat_score(keyword_count, pattern_count)
    severity = calculate_severity(threat_score)
    confidence = calculate_confidence(keyword_count, pattern_count)
    risk_level = calculate_risk_level(threat_score)

    print("=" * 50)
    print("Scoring Engine Test")
    print("=" * 50)

    print(f"Keywords Detected : {keyword_count}")
    print(f"Patterns Detected : {pattern_count}")
    print(f"Threat Score      : {threat_score}")
    print(f"Severity          : {severity}")
    print(f"Confidence        : {confidence}%")
    print(f"Risk Level        : {risk_level}")

    print("\nScoring Engine Test Completed Successfully.")