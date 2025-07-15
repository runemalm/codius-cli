import pytest
import sys
from io import StringIO
from codius.main import main
from codius.version import __version__


@pytest.mark.integration
def test_version_argument(monkeypatch):
    # Arrange: Simulate passing --version as CLI argument
    monkeypatch.setattr(sys, "argv", ["codius", "--version"])

    captured_output = StringIO()
    monkeypatch.setattr(sys, "stdout", captured_output)

    with pytest.raises(SystemExit) as exc_info:
        main()

    # Assert exit code is 0 (normal exit from --version)
    assert exc_info.value.code == 0

    # Assert correct version output
    output = captured_output.getvalue().strip()
    assert output == f"codius {__version__}"
