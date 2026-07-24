from detection_engine import (
    run_scan,
    calculate_score,
    generate_report,
)


class DetectionService:

    def run_detection(self, prompt):

        report = run_scan(prompt)

        score, severity, confidence, risk_level = (
            calculate_score(prompt)
        )

        detailed_report = generate_report(prompt)

        return {
            "report": report,
            "score": score,
            "severity": severity,
            "confidence": confidence,
            "risk_level": risk_level,
            "detailed_report": detailed_report,
        }