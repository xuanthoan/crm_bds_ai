"""Secret baseline guardrail: no secrets committed in the repository."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from secret_scan import scan_repo  # noqa: E402


class TestNoCommittedSecrets:
    def test_repository_has_no_secret_findings(self) -> None:
        findings = scan_repo(Path(ROOT))
        assert findings == [], (
            "secret scan findings (file : line [kind]):\n"
            + "\n".join(f"  {f.path} : {f.line} [{f.kind}]" for f in findings)
        )

    def test_no_env_file_is_committed(self) -> None:
        env_file = Path(ROOT) / ".env"
        assert not env_file.exists(), ".env must never be committed"
