from __future__ import annotations

import csv
import json
from pathlib import Path


class ExportService:

    def build_report(
        self,
        scan_result,
    ):
        """
        Convert ScanResult into a serializable dictionary.
        """

        if hasattr(scan_result, "to_dict"):
            return scan_result.to_dict()

        return {}

    def export_json(
        self,
        scan_result,
        file_path="report.json",
    ):
        """
        Export report as JSON.
        """

        report_data = self.build_report(
            scan_result
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report_data,
                file,
                indent=4,
                default=str,
            )

        return Path(file_path)

    def export_csv(
        self,
        scan_result,
        file_path="report.csv",
    ):
        """
        Export report as CSV.
        """

        report_data = self.build_report(
            scan_result
        )

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Field",
                    "Value",
                ]
            )

            for key, value in report_data.items():

                writer.writerow(
                    [
                        key,
                        str(value),
                    ]
                )

        return Path(file_path)

    def export_pdf(
        self,
        scan_result,
        file_path="report.pdf",
    ):
        """
        Placeholder PDF export.

        Can be replaced later with ReportLab.
        """

        report_data = self.build_report(
            scan_result
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "NEUROFENCE SCAN REPORT\n"
            )

            file.write(
                "=" * 40 + "\n\n"
            )

            for key, value in report_data.items():

                file.write(
                    f"{key}: {value}\n\n"
                )

        return Path(file_path)

    def save_report(
        self,
        scan_result,
        file_path="saved_report.json",
    ):
        """
        Save report to disk.
        """

        return self.export_json(
            scan_result,
            file_path,
        )