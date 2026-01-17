#!/usr/bin/env python3
"""Filter a large token list into a usable subset for Vosk.

Produces a cleaned, deduplicated token file suitable for use as a custom
vocabulary/grammar. By default this will limit to the first N usable tokens
if `-n` is provided.

Usage:
    python3 scripts/filter_tokens.py vosk_custom_words_10000.txt -o vosk_custom_words_usable.txt -n 1500
"""
from pathlib import Path
import re
import argparse

ALLOWED_RE = re.compile(r"^[a-z0-9']+$")  # allow lowercase letters, digits, apostrophe

def clean_token(tok: str) -> str:
    tok = tok.strip().lower()
    # remove surrounding punctuation
    tok = tok.strip(".,;:()[]{}\"'`)" )
    # collapse whitespace
    tok = re.sub(r"\s+", " ", tok)
    return tok

def is_usable(tok: str, allow_phrases: bool) -> bool:
    if not tok:
        return False
    if len(tok) <= 1:
        return False
    if len(tok) > 40:
        return False
    # Skip obvious urls or tokens with / or @ or other symbols
    if any(ch in tok for ch in "@/\\#%&*+=<>$"):
        return False
    # Numeric-only tokens longer than 6 are likely IDs
    if tok.isnumeric() and len(tok) > 6:
        return False
    if " " in tok and not allow_phrases:
        return False
    parts = tok.split()
    for p in parts:
        if not ALLOWED_RE.match(p):
            return False
    return True

def main():
    p = argparse.ArgumentParser(description="Filter a large token list into usable tokens for Vosk.")
    p.add_argument("input", help="Input token file (one token per line)")
    p.add_argument("-o", "--output", default="vosk_custom_words_usable.txt")
    p.add_argument("-n", "--max-tokens", type=int, default=0,
                   help="If >0, limit output to this many tokens (keeps first seen usable tokens).")
    p.add_argument("--keep-phrases", action="store_true",
                   help="Allow multiword phrases (default: disabled).")
    args = p.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"Input file not found: {inp}")
        raise SystemExit(2)

    seen = set()
    out = []
    text = inp.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        tok = clean_token(line)
        if is_usable(tok, args.keep_phrases) and tok not in seen:
            seen.add(tok)
            out.append(tok)
            if args.max_tokens > 0 and len(out) >= args.max_tokens:
                break

    Path(args.output).write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {len(out)} usable tokens to {args.output}")

if __name__ == '__main__':
    main()
