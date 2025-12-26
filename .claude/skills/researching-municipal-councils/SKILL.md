---
name: researching-municipal-councils
description: Fill municipalities.csv by researching official council livestream/archives and minutes with evidence URLs. Use when cells are ToBeInvestigated or UNKNOWN.
allowed-tools: Read, Edit, Write, Glob, Grep, WebSearch, WebFetch, Task
---

# Researching Municipal Councils

## Rules (must)
- ToBeInvestigated: not checked yet
- UNKNOWN: checked but cannot confirm
- YES/NO only with clear evidence
- If YES then the corresponding URL must be non-empty
- NO requires checking at least 2–3 routes; write a short audit trail in notes
- Do not confuse minutes with summaries/newsletters
- latest_minutes_date must be YYYY-MM-DD or UNKNOWN/ToBeInvestigated

## Completion report (must)
- After finishing edits to a municipalities.csv, report progress as a percent.
- Completion = rows with no `ToBeInvestigated` in these fields: live_streaming, recorded_streaming, minutes_published, latest_minutes_date.
- Progress formula: `(completed_rows / total_rows) * 100`, rounded to 1 decimal place.
- Output: `Progress: XX.X% (completed/total rows)`; include the CSV path.
