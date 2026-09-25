#!/usr/bin/env python3
"""
Copy matching text pairs from a CSV into an edition's config.js.

    python3 tools/csv_to_pairs.py scripture/pairs.csv scripture/config.js

CSV layout (as exported from Excel / Numbers):  number, left text, right text
  - rows without two texts (blank lines, a header row) are skipped
  - with only two columns, those two are the pair
Save the CSV as UTF-8 ("CSV UTF-8" in Excel) so the Chinese survives.

Only the block between the // PAIRS:BEGIN and // PAIRS:END lines in config.js is
rewritten; everything else in the file is left alone. Python 3 standard library only.
"""
import csv, json, sys

def read_pairs(path):
    pairs = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            cells = [c.strip() for c in row]
            a, b = (cells[1:3] if len(cells) >= 3 else cells[:2]) + ["", ""][: max(0, 2 - len(cells))]
            if a and b:
                pairs.append((a, b))
    return pairs

def main(csv_path, config_path):
    pairs = read_pairs(csv_path)
    if not pairs:
        sys.exit(f"No pairs found in {csv_path}")
    width = max(len(json.dumps(a, ensure_ascii=False)) for a, _ in pairs)
    lines = [f"  [{json.dumps(a, ensure_ascii=False) + ',':<{width + 1}} {json.dumps(b, ensure_ascii=False)}]"
             for a, b in pairs]
    block = "const PAIRS = [\n" + ",\n".join(lines) + "\n];\n"

    text = open(config_path, encoding="utf-8").read()
    start, end = text.find("// PAIRS:BEGIN"), text.find("// PAIRS:END")
    if start < 0 or end < 0:
        sys.exit(f"{config_path} has no // PAIRS:BEGIN ... // PAIRS:END markers")
    start = text.index("\n", start) + 1
    open(config_path, "w", encoding="utf-8", newline="\n").write(text[:start] + block + text[end:])
    print(f"Wrote {len(pairs)} pairs into {config_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
