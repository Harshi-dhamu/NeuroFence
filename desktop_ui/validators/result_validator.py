from __future__ import annotations


class ResultValidator:
    REQUIRED_FIELDS = [
        "model_name",
        "framework",
        "architecture",
        "threat_score",
        "risk_level",
        "scan_duration",
        "overall_status",
    ]

    @classmethod
    def validate(cls, result):
        errors = []

        if result is None:
            errors.append("Scan result is empty.")
            return errors

        for field in cls.REQUIRED_FIELDS:
            if not hasattr(result, field):
                errors.append(f"Missing field: {field}")

        try:
            if result.threat_score < 0:
                errors.append("Threat score cannot be negative.")

            if result.threat_score > 100:
                errors.append("Threat score cannot exceed 100.")
        except Exception:
            errors.append("Threat score is invalid.")

        return errors