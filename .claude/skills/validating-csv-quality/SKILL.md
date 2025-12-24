---
name: validating-csv-quality
description: Validate municipalities.csv schema, allowed values, URL requirements for YES, and date formats. Use before commits/PRs or after large edits.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(python:*), Bash(python3:*), Bash(uv:*), Bash(pip:*), Bash(pip3:*), Task
---

# Validating CSV Quality

## What to validate
1) Column order is unchanged
2) Allowed values are only: YES / NO / UNKNOWN / ToBeInvestigated
   - Exception: URL/date fields may be empty only when the corresponding flag is NO
3) If live_streaming=YES or recorded_streaming=YES then video_page_url must be non-empty
4) If minutes_published=YES then minutes_url must be non-empty
5) latest_minutes_date must be YYYY-MM-DD or UNKNOWN or ToBeInvestigated (or empty when minutes_published=NO)
6) Never delete rows. Never reorder rows.

## How to run
- Prefer running `python3 scripts/validate_csv.py <path-to-csv>`
- If scripts/validate_csv.py does not exist, create it in this session and then run it.

## Output requirements
- Print a concise report listing:
  - total rows
  - number of errors
  - first ~20 errors with row identifiers (municipality_name_ja) and column names
- If errors exist: fix the CSV and re-run validation until clean.
