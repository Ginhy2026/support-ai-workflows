#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from validate_second_brain_handoff import inspect


class HandoffVerifierTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        subprocess.run(["git", "init", str(self.repo)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        (self.repo / "README.md").write_text("# Test\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-m", "base"], check=True, capture_output=True)
        self.base = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def commit(self) -> str:
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-m", "change"], check=True, capture_output=True)
        return subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()

    def test_accepts_pending_candidate_addition(self) -> None:
        path = self.repo / "knowledge-intake" / "feishu" / "candidate.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\ntype: knowledge-candidate\ncandidate_status: pending\n---\n", encoding="utf-8")
        report = inspect(self.repo, self.base, self.commit())
        self.assertTrue(report["valid"])

    def test_rejects_formal_edit_and_active_candidate(self) -> None:
        (self.repo / "README.md").write_text("# Changed\n", encoding="utf-8")
        path = self.repo / "knowledge-intake" / "feishu" / "candidate.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\ntype: knowledge-candidate\ncandidate_status: pending\nstatus: active\n---\n",
            encoding="utf-8",
        )
        report = inspect(self.repo, self.base, self.commit())
        self.assertFalse(report["valid"])
        self.assertTrue(any("path_outside_intake" in error for error in report["errors"]))
        self.assertTrue(any("candidate_marked_active" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
