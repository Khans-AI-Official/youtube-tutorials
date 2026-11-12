import sys

sys.path.insert(0, "src")
from main import in_virtualenv  # noqa: E402


def test_runs_inside_a_virtual_environment():
    assert in_virtualenv()
