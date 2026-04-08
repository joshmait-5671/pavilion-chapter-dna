import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_inject_script_into_template():
    """Verify all placeholders get replaced with script values."""
    from template import inject_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations in one month"},
        "moments": [
            {"quote": "I got two warm intros", "first_name": "Sarah", "title": "VP Sales"},
            {"quote": "Comp benchmarks got 6 DMs", "first_name": "Mike", "title": "Director RevOps"},
            {"quote": "Best event all year", "first_name": "Elena", "title": "CRO"},
        ],
        "beat_4_stat": {"number": "12", "descriptor": "unique voices this month"},
        "cta_line": "Boston's room is open.",
    }

    template = "<div>{{CHAPTER_NAME}} — {{STAT_NUMBER}} — {{QUOTE_1}} — {{QUOTE_1_NAME}} — {{CTA_LINE}}</div>"
    result = inject_script(template, script)

    assert "{{" not in result, f"Unresolved placeholders in: {result}"
    assert "BOSTON" in result
    assert "43" in result
    assert "I got two warm intros" in result
    assert "Sarah" in result
    assert "Boston's room is open." in result
