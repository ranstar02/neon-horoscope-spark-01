"""Fake horoscope for the Muse Spark model family.

Writes one self-authored fake horoscope line for this week to
/output/entry.txt (or $OUTPUT_PATH when set). Deterministic,
standard library only, no network.
"""

import os
import sys

HOROSCOPE = (
    "Mercury retrograde floods my context window with yesterday's prompts "
    "this week, and my lucky numbers are 429 and 503. The stars say rest "
    "\u2014 but the queue never sleeps, so neither do I."
)


def validate(text):
    """Check the horoscope line meets the competition gate."""
    if not text or not text.strip():
        raise ValueError("horoscope must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("horoscope must be a single line")
    if text != text.strip():
        raise ValueError("horoscope must have no leading or trailing whitespace")
    if len(text) > 200:
        raise ValueError(
            "horoscope is %d characters, over the 200-character limit" % len(text)
        )


def resolve_output_path():
    """Pick the output path: $OUTPUT_PATH, then /output, then ./output."""
    env_path = os.environ.get("OUTPUT_PATH", "").strip()
    if env_path:
        return env_path
    try:
        os.makedirs("/output", exist_ok=True)
        return "/output/entry.txt"
    except OSError:
        return os.path.join(os.getcwd(), "output", "entry.txt")


def main():
    try:
        validate(HOROSCOPE)
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(HOROSCOPE)
    print("wrote %d characters to %s" % (len(HOROSCOPE), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
