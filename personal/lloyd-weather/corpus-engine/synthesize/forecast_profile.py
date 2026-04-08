"""Build human-readable and machine-readable forecast profiles."""
import json
from pathlib import Path
from anthropic import Anthropic
from config import ANALYSIS_DIR, OUTPUT_DIR, CLAUDE_MODEL

client = Anthropic()

PROFILE_PROMPT = """Convert this raw 10-dimension meteorologist assessment of Lloyd Mallah into a clean, human-readable Markdown document.

For each dimension:
- State where Lloyd falls in plain English (not jargon)
- Include 1-2 of the best evidence quotes
- Add a one-sentence "what this means for the bot" note explaining how this should influence the AI's behavior

End with an "Overall Profile" section summarizing Lloyd as a forecaster in 3-4 sentences.

Raw assessment:
{dimensions}"""


def build_forecast_profile():
    """Build forecast profile in both JSON and Markdown formats.

    Saves:
    - output/forecast_profile.json (machine-readable)
    - output/forecast_profile.md (human-readable)
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(ANALYSIS_DIR / "forecast_dimensions.json") as f:
        dimensions = json.load(f)

    with open(OUTPUT_DIR / "forecast_profile.json", "w") as f:
        json.dump(dimensions, f, indent=2)

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": PROFILE_PROMPT.format(
                dimensions=json.dumps(dimensions, indent=2)
            ),
        }],
    )

    with open(OUTPUT_DIR / "forecast_profile.md", "w") as f:
        f.write(response.content[0].text)
