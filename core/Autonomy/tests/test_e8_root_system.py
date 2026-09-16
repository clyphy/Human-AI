from pathlib import Path
import subprocess
import sys


def test_e8_standalone_verifier_passes():
    project_root = Path(__file__).resolve().parents[1]
    verifier = project_root / "tests" / "verify_e8_root_system.py"

    result = subprocess.run(
        [sys.executable, str(verifier)],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"Verifier failed with exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )

    assert "E8 verification passed." in result.stdout
