import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_validate_script_valid():
    """A correctly structured script passes validation."""
    from generate_script import validate_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations in one month"},
        "moments": [
            {"quote": "Quote 1", "first_name": "Sarah", "title": "VP Sales"},
            {"quote": "Quote 2", "first_name": "Mike", "title": "Director RevOps"},
            {"quote": "Quote 3", "first_name": "Elena", "title": "CRO"},
        ],
        "beat_4_stat": {"number": "12", "descriptor": "unique voices this month"},
        "cta_line": "Boston's room is open.",
    }
    assert validate_script(script) == True


def test_validate_script_wrong_moment_count():
    """Script with != 3 moments fails validation."""
    from generate_script import validate_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations"},
        "moments": [
            {"quote": "Quote 1", "first_name": "Sarah", "title": "VP Sales"},
        ],
        "beat_4_stat": {"number": "12", "descriptor": "unique voices"},
        "cta_line": "Boston's room is open.",
    }
    assert validate_script(script) == False


def test_validate_script_missing_field():
    """Script missing required field fails validation."""
    from generate_script import validate_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations"},
        "moments": [],
    }
    assert validate_script(script) == False
