from detection_fuzzer.api import (
    run_scan,
    calculate_score,
    generate_scan_report,
)


class DetectionService:
    def run_detection(self, prompt: str):
        report = run_scan(prompt)

        score, severity, confidence, risk_level = (
            calculate_score(prompt)
        )

        detailed_report = generate_scan_report(prompt)

        return {
            "report": report,
            "score": score,
            "severity": severity,
            "confidence": confidence,
            "risk_level": risk_level,
            "detailed_report": detailed_report,
        }