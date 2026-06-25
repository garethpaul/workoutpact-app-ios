#!/usr/bin/env python3
"""Regression coverage for hosted workflow parser infrastructure failures."""

import io
import unittest
from contextlib import redirect_stdout
from unittest import mock

import check_workoutpact_contracts


class WorkflowParserDiagnosticsTest(unittest.TestCase):
    def test_main_reports_parser_failure_without_semantic_workflow_results(self):
        output = io.StringIO()
        missing_ruby = FileNotFoundError(2, "No such file or directory", "ruby")

        with mock.patch.object(
            check_workoutpact_contracts.subprocess,
            "run",
            side_effect=missing_ruby,
        ) as run_parser, redirect_stdout(output):
            exit_code = check_workoutpact_contracts.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "WorkoutPact contract check failed:",
                "- workflow YAML parser unavailable: "
                "[Errno 2] No such file or directory: 'ruby'",
            ],
        )
        self.assertEqual(
            run_parser.call_count,
            1,
            "parser failure must stop semantic and hostile-mutation evaluation",
        )
        self.assertNotIn("checkout must disable", output.getvalue())
        self.assertNotIn("normalized case-insensitively", output.getvalue())
        self.assertNotIn("mutations must be rejected", output.getvalue())

    def test_main_stops_mutations_when_their_parser_infrastructure_fails(self):
        output = io.StringIO()
        parser_error = "workflow YAML parser unavailable during mutation review"

        with mock.patch.object(
            check_workoutpact_contracts,
            "checkout_credentials_are_isolated",
            side_effect=[(True, []), (False, [parser_error])],
        ) as review_workflow, redirect_stdout(output):
            exit_code = check_workoutpact_contracts.main()

        self.assertEqual(exit_code, 1)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "WorkoutPact contract check failed:",
                f"- {parser_error}",
            ],
        )
        self.assertEqual(
            review_workflow.call_count,
            2,
            "mutation parser failure must stop before remaining mutations",
        )
        self.assertNotIn(
            "checkout credential isolation mutations must be rejected",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()
