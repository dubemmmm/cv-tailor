---
description: Tailor a separate CV for every job URL in a queue file
argument-hint: [path to job list; defaults to jobs.txt]
---

Queue file: $ARGUMENTS

Process the queue sequentially. Do not tailor different jobs in parallel. The
critic agents within one job may still run in parallel as described in
`.claude/commands/tailor.md`.

1. Read `CLAUDE.md`, `.claude/commands/tailor.md`, `master/master_cv.md`, and
   `master/eligibility.md` once before starting. If either private master file is
   missing or incomplete, direct the user to the README setup steps and stop.

2. Use the file named in `$ARGUMENTS`, or `jobs.txt` when no argument was given.
   Read it without modifying it. Trim whitespace, ignore blank lines and lines
   whose first non-whitespace character is `#`, and validate that every remaining
   line is an `http://` or `https://` URL. Report invalid lines and continue with
   valid ones.

3. De-duplicate URLs while preserving their first-seen order. Treat URLs as the
   same when they differ only in common tracking parameters such as `utm_*`,
   `fbclid`, `gclid`, `gh_src`, or `jr_id`. Preserve functional identifiers such
   as `jobId`, `gh_jid`, and `ashby_jid`.

4. For each unique URL, in file order:
   - Announce progress as `[current/total] URL`.
   - Retrieve the complete job description. Use available browser tooling when
     a direct fetch is incomplete or blocked.
   - Follow steps 2 through 8 of `.claude/commands/tailor.md` for this job.
   - Apply batch eligibility behavior: when a requirement is BLOCKER or UNKNOWN,
     record the exact requirement and JD quote, skip that job, and continue. Do
     not pause the whole batch for confirmation.
   - If a prior output folder contains a final PDF and `verify.md` says PASS,
     record it as already completed and do not overwrite it. If the folder is
     incomplete, resume from the earliest missing or failed pipeline step.
   - If the posting is closed, unavailable, missing its description, or a job
     fails after the allowed compile or verification retries, record the reason
     and continue to the next URL.

5. Write `output/batch_summary.md` with the run date and a row for every input:
   URL, company and role when known, status (`completed`, `already completed`,
   `skipped`, `failed`, `duplicate`, or `invalid`), final PDF path when present,
   and a concise reason for any non-completed status.

6. Finish with totals by status and links or paths to every completed PDF. Do not
   open PDFs during a batch unless the user explicitly asks.
