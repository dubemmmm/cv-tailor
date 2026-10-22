# CV Tailor

Goal: turn a job description into a tailored one-page CV using
`master/master_cv.md` as the only source of truth.

## Hard rules

- Never invent employers, titles, dates, metrics, tools, credentials, or projects.
- Only reorder, trim, reword, and emphasize facts in the master CV.
- Every metric in the output must appear in the master CV.
- Output must be exactly one page.
- Do not use em dashes. Keep wording direct and natural.
- Describe projects with what was built, the relevant stack, scale, and outcome.
- Read `master/eligibility.md` for private eligibility facts. If it is missing or
  contains unresolved placeholders, stop at the eligibility gate and ask the user.

## Recruiter principles

- Prove fit instead of listing duties. Put supported must-have skills in both
  Technical Skills and a bullet showing their use.
- Prefer: action verb + what + how + measurable result. Use only master-CV facts.
- Use 2 to 5 bullets per selected experience or project, each 1 to 2 lines.
- Show leadership through concrete actions and scale.
- Use recognizable headings, consistent formatting, plain-text credentials, and
  working links. Expand unfamiliar abbreviations on first use.
- Omit generic soft skills, objectives, references, photos, and unrelated content.
- Include coursework only when it is specialized and directly relevant.

## Ordering and sections

- Preserve reverse-chronological order unless relevance clearly calls for a
  different order and chronology remains unambiguous.
- Use the graduation date defined for the role type in `master/eligibility.md`.
- Do not include a Summary for software, data, or ML engineering roles. For a
  role outside those families, a master-true Summary may use at most two lines.
- Default section order: Education, Technical Skills, Experience, Projects,
  optional Research and Writing, optional Leadership and Involvement, and
  Certifications.
- Include only sections supported by the master CV. Certifications, when present,
  must be complete and must be the final section.
- Never add a Hackathons and Awards section unless the master CV contains it and
  it is directly relevant.
- Use at most three projects.

## Pipeline

Follow `.claude/commands/tailor.md`. Write generated files to
`output/<company>_<role>/`. The CV basename comes from the JD analyzer and must
contain no spaces or punctuation.

For multiple job URLs, follow `.claude/commands/tailor-batch.md`. Read one URL
per line from `jobs.txt` (or the supplied queue path), process jobs sequentially,
and write the aggregate result to `output/batch_summary.md`.
