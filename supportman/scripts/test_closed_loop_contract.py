from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class ClosedLoopContractTests(unittest.TestCase):
    def test_supportman_defaults_to_dual_source_retrieval(self):
        skill = read("supportman/SKILL.md")
        self.assertIn("use both available knowledge channels by default", skill)
        self.assertIn("$second-brain-reader", skill)
        self.assertIn("state exactly what could not be checked", skill)

    def test_supportman_only_suggests_candidate_handoff(self):
        skill = read("supportman/SKILL.md")
        contract = read("supportman/references/closed-loop.md")
        self.assertIn("Do not create a candidate unless the user agrees", skill)
        self.assertIn("第二大脑反馈建议", contract)
        self.assertIn("feishu-knowledge-capture", contract)

    def test_reader_and_capture_keep_write_boundaries(self):
        reader = read("second-brain-reader/SKILL.md")
        capture = read("feishu-knowledge-capture/SKILL.md")
        self.assertIn("Never modify the AI publication repository", reader)
        self.assertIn("If the user has not explicitly agreed", capture)
        self.assertIn("Never turn SupportMan's recommendation into a candidate unless the user confirmed", capture)

    def test_customer_reply_tone_is_natural_but_safe(self):
        skill = read("supportman/SKILL.md")
        self.assertIn("natural spoken business language", skill)
        self.assertIn("Do not make the reply casual at the cost of precision, safety, or respect", skill)


if __name__ == "__main__":
    unittest.main()
