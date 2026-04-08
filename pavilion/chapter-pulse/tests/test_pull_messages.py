import json
import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_save_messages_creates_json():
    """Verify save_messages writes a valid JSON file with expected structure."""
    from pull_messages import save_messages

    messages = [
        {"user": "U123", "text": "Hello Boston", "ts": "1710000000.000000", "display_name": "Sarah", "title": "VP Sales"},
        {"user": "U456", "text": "Great event last night", "ts": "1710000001.000000", "display_name": "Mike", "title": "Director RevOps"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        path = save_messages(messages, "boston", "2026-03", tmpdir, display_name="Boston")
        assert os.path.exists(path)
        with open(path) as f:
            data = json.load(f)
        assert data["chapter"] == "boston"
        assert data["display_name"] == "Boston"
        assert data["month"] == "2026-03"
        assert data["message_count"] == 2
        assert data["unique_posters"] == 2
        assert len(data["messages"]) == 2


def test_threshold_check_below():
    """Verify threshold returns False when under 30 messages."""
    from pull_messages import check_threshold
    assert check_threshold([], "boston", 30) == False


def test_threshold_check_above():
    """Verify threshold returns True when at or above 30 messages."""
    from pull_messages import check_threshold
    msgs = [{"text": f"msg {i}"} for i in range(30)]
    assert check_threshold(msgs, "boston", 30) == True
