"""Format SamarthSchool Action Guide responses for WhatsApp.

WhatsApp has a ~1600 character limit per message. This module splits
long Action Guide responses into multiple messages while preserving
readability and structure.
"""

import re


# WhatsApp single message limit (conservative)
MAX_MSG_LEN = 1500


def format_for_whatsapp(action_guide: str) -> list[str]:
    """Split an Action Guide into WhatsApp-sized messages.

    Strategy:
    - First message: child profile + summary
    - Subsequent messages: one scheme per message
    - Last message: disclaimer

    Returns a list of message strings, each ≤ MAX_MSG_LEN characters.
    """
    if len(action_guide) <= MAX_MSG_LEN:
        return [action_guide]

    # Try to split on scheme boundaries (━━━ markers)
    sections = re.split(r"(━━━.*?━+)", action_guide)

    messages = []
    current = ""

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # If adding this section would exceed limit, flush current
        if current and len(current) + len(section) + 2 > MAX_MSG_LEN:
            messages.append(current.strip())
            current = ""

        if current:
            current += "\n\n" + section
        else:
            current = section

    # Flush remaining
    if current.strip():
        messages.append(current.strip())

    # If still no splits worked, do hard character splits
    if not messages:
        messages = _hard_split(action_guide)

    return messages


def _hard_split(text: str) -> list[str]:
    """Fall back to splitting on newlines near the character limit."""
    messages = []
    lines = text.split("\n")
    current = ""

    for line in lines:
        if len(current) + len(line) + 1 > MAX_MSG_LEN:
            if current:
                messages.append(current)
            current = line
        else:
            current = current + "\n" + line if current else line

    if current:
        messages.append(current)

    return messages


def truncate_for_whatsapp(text: str, max_schemes: int = 3) -> str:
    """For very long guides, truncate to top N schemes with a note."""
    sections = re.split(r"━━━", text)

    if len(sections) <= max_schemes + 2:  # header + schemes + disclaimer
        return text

    # Keep header (first section) + top N schemes + disclaimer
    header = sections[0]
    schemes = sections[1:max_schemes + 1]
    disclaimer_candidates = [s for s in sections if "Disclaimer" in s or "अस्वीकरण" in s]
    disclaimer = disclaimer_candidates[-1] if disclaimer_candidates else ""

    result = header
    for s in schemes:
        result += "\n━━━" + s
    if disclaimer:
        total_schemes = len(sections) - 2  # minus header and disclaimer
        remaining = total_schemes - max_schemes
        if remaining > 0:
            result += f"\n\n📱 +{remaining} more schemes available. Reply 'more' for the full list."
        result += "\n━━━" + disclaimer

    return result
