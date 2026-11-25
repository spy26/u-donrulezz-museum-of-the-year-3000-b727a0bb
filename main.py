"""Museum of the Year 3000 — make.fun entry.

Writes the one-line museum label (year 3000) for a group chat to
/output/entry.txt (and to $MAKEFUN_OUTPUT_DIR/entry.txt when set).
No network, no clock, no randomness.
"""

import os

ENTRY = "Group chat, c. 2025. Forty-seven humans gathered here daily to ignore one another in perfect unison."


def validate_entry(text):
    """Gate: one line, 1-200 characters, no control characters."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    return True


def main():
    validate_entry(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    paths = []
    if out_dir:
        paths.append(os.path.join(out_dir, "entry.txt"))
    paths.append("/output/entry.txt")
    for path in paths:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
        # Read-back byte check: what was written must equal ENTRY exactly.
        with open(path, "rb") as f:
            written = f.read()
        assert written == ENTRY.encode("utf-8"), "read-back mismatch: %s" % path
    print(ENTRY)


if __name__ == "__main__":
    main()
