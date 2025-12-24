---
name: auditing-yes-no-calls
description: Re-check YES/NO decisions with evidence URLs. Use to reduce misclassification risk, especially NO calls.
allowed-tools: Read, Glob, Grep, Write, Edit, WebSearch, WebFetch, Task
---

# Auditing YES/NO Calls

## Audit scope
- Focus on rows where any of:
  - live_streaming is YES/NO
  - recorded_streaming is YES/NO
  - minutes_published is YES/NO

## Rules
1) For YES:
   - Ensure the corresponding URL is present
   - Prefer official website entry pages over random search results
2) For NO:
   - Confirm at least 2–3 discovery routes were attempted:
     - official site navigation AND
     - search query (and optionally site:<domain>)
   - If the original row lacks an audit trail in notes, downgrade NO -> UNKNOWN and add notes explaining why
3) Keep row order and column order unchanged.

## Output requirements
- Provide a summary:
  - audited row count
  - changed municipalities list
  - number of reversals (NO->UNKNOWN, YES->UNKNOWN, etc.)
