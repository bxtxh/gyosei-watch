#!/usr/bin/env python3
import re
import sys
import csv
from pathlib import Path

ALLOWED = {"YES", "NO", "UNKNOWN", "ToBeInvestigated"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

COLUMNS = [
    "prefecture","subprefecture","municipality_type","municipality_name_ja",
    "live_streaming","recorded_streaming","video_platform","video_page_url",
    "minutes_published","minutes_format","minutes_url","latest_minutes_date","notes"
]

def err(errors, muni, col, msg):
    errors.append(f"{muni} | {col}: {msg}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_csv.py <municipalities.csv>", file=sys.stderr)
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(2)

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        if cols != COLUMNS:
            print("ERROR: column order mismatch.", file=sys.stderr)
            print("Expected:", COLUMNS, file=sys.stderr)
            print("Actual  :", cols, file=sys.stderr)
            sys.exit(1)

        errors = []
        rows = list(reader)

        for r in rows:
            muni = r.get("municipality_name_ja", "(unknown)")

            # Value columns
            for col in ["live_streaming","recorded_streaming","minutes_published"]:
                v = (r.get(col) or "").strip()
                if v not in ALLOWED:
                    err(errors, muni, col, f"must be one of {sorted(ALLOWED)}, got '{v}'")

            # URL requirements for YES
            live = (r.get("live_streaming") or "").strip()
            rec  = (r.get("recorded_streaming") or "").strip()
            vid_url = (r.get("video_page_url") or "").strip()
            if (live == "YES" or rec == "YES") and not vid_url:
                err(errors, muni, "video_page_url", "required when live_streaming or recorded_streaming is YES")

            minutes = (r.get("minutes_published") or "").strip()
            min_url = (r.get("minutes_url") or "").strip()
            if minutes == "YES" and not min_url:
                err(errors, muni, "minutes_url", "required when minutes_published is YES")

            # Date format
            d = (r.get("latest_minutes_date") or "").strip()
            if d:
                if d not in {"UNKNOWN","ToBeInvestigated"} and not DATE_RE.match(d):
                    err(errors, muni, "latest_minutes_date", "must be YYYY-MM-DD or UNKNOWN/ToBeInvestigated or empty")
            else:
                # empty is only ok if minutes_published=NO
                if minutes != "NO":
                    # allow empty when genuinely not applicable? we keep strict.
                    err(errors, muni, "latest_minutes_date", "empty only allowed when minutes_published=NO (otherwise use UNKNOWN/ToBeInvestigated)")

        print(f"Rows: {len(rows)}")
        if errors:
            print(f"Errors: {len(errors)}")
            for e in errors[:20]:
                print(" -", e)
            if len(errors) > 20:
                print(f"... and {len(errors)-20} more")
            sys.exit(1)

        print("OK: validation passed")

if __name__ == "__main__":
    main()
