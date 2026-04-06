import anthropic
from config import ANTHROPIC_API_KEY, FORGE_MODEL

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def ask_claude(system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> str:
    response = anthropic_client.messages.create(
        model=FORGE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response.content[0].text
