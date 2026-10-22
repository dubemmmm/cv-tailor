---
description: Tailor a CV to a job description (URL, file path, or pasted text)
argument-hint: <url | file path | pasted JD>
---

Input: $ARGUMENTS

Follow these steps in order.

1. Read `CLAUDE.md`, `master/master_cv.md`, and `master/eligibility.md`. If either
   private master file is missing, direct the user to the README setup steps and
   stop. Get the JD from the URL, file path, or pasted input. If a URL cannot be
   read completely, use available browser tooling to retrieve the actual posting.

2. Run the `jd-analyzer` subagent on the JD and candidate name from the master
   CV. Use its folder slug as `<company>_<role>` and basename as `<cv_name>`.
   Save the raw JD to `output/<company>_<role>/jd.txt` and the analysis to
   `output/<company>_<role>/analysis.md`.

3. Compare every hard eligibility requirement with `master/eligibility.md` and
   the master CV. Mark a requirement BLOCKER only when the profile clearly fails
   it and UNKNOWN when the needed profile value is unknown. If there is a BLOCKER
   or UNKNOWN, show the requirement and exact JD quote, then ask whether to
   continue. In a batch, skip affected jobs, finish the others, and report skips.
   Never alter a date or claim to pass this gate.

4. Run in parallel, each with the analysis and master CV: `ats-critic`,
   `impact-critic`, and `honesty-critic` in Mode 1. Save their notes as
   `notes_ats.md`, `notes_impact.md`, and `notes_honesty_redlines.md`.

5. Run `tailor` with the master CV, analysis, critic notes, and
   `templates/cv_template.tex`. It writes `<cv_name>.tex` in the output folder.

6. Run `NO_OPEN=1 bash scripts/compile.sh <path-to-tex>`.
   - Exit 2: send the spill and short-line hints to `tailor`; recompile, at most
     three rounds.
   - Exit 3: ask `tailor` to shorten the wrapped project tool list; recompile.

7. Run `recruiter-critic` on the compiled PDF and source plus the analysis,
   master CV, and honesty red lines. Send its edits to `tailor` for one revision,
   recompile, and save the review as `notes_recruiter.md`.

8. Run `honesty-critic` in Mode 2 on the final source. For FAIL, request targeted
   fixes, recompile, and verify again, at most two rounds. Save `verify.md`.

9. Report the final PDF path, a short change summary, unsupported JD gaps, and
   eligibility concerns. Reveal or open the PDF only if the user requests it.
