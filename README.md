# CV Tailor

CV Tailor is a local-first Claude Code workflow that turns a master CV and a
job description into an honest, ATS-aware, one-page PDF. It analyzes the role,
checks eligibility, asks specialist agents to critique the draft, compiles it
with LaTeX, and verifies every final claim against the master CV.

Your CV, eligibility profile, job descriptions, and generated applications are
ignored by Git by default.

## What you need

- Python 3.10 or newer
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Tectonic](https://tectonic-typesetting.github.io/) for LaTeX compilation
- Poppler (`pdfinfo` and `pdftotext`) for one-page and layout checks

On macOS, install the system tools with `brew install tectonic poppler`. On
Debian or Ubuntu, install Poppler with `sudo apt install poppler-utils` and
follow Tectonic's installation instructions for your platform.

## Quick start

```bash
git clone <repository-url>
cd cv-tailor
make setup
```

Then:

1. Put one text-based PDF CV in `master/inbox/`.
2. Run `make import-cv`.
3. Carefully review `master/master_cv.md`. Complex columns and headings may need
   manual cleanup after PDF extraction.
4. Run `cp master/eligibility.example.md master/eligibility.md`, then replace
   every placeholder in the copied file.
5. Customize the header placeholders and PDF metadata in
   `templates/cv_template.tex`, keeping its layout commands intact.
6. Start Claude Code in the repository and run:

   ```text
   /tailor <job-description URL, file path, or pasted text>
   ```

To tailor resumes for several postings, create a private job queue and run the
batch command:

```bash
cp jobs.example.txt jobs.txt
# Add one job URL per line to jobs.txt
```

```text
/tailor-batch
```

Claude processes the URLs in order, creates a separate resume for each eligible
role, continues past closed or blocked jobs, and writes a run report to
`output/batch_summary.md`. You can pass another queue path with
`/tailor-batch path/to/jobs.txt`.

The finished `.tex`, PDF, analysis, and review notes are written beneath
`output/<company>_<role>/`.

To import from another location or replace an earlier import:

```bash
.venv/bin/python scripts/import_cv.py /path/to/cv.pdf --force
```

## Repository layout

```text
.claude/                 Claude Code command and specialist agent prompts
jobs.example.txt         Example multi-job queue (copy to private jobs.txt)
master/
  inbox/                 Drop a private source PDF here
  eligibility.example.md Eligibility profile template
scripts/
  import_cv.py            PDF-to-Markdown importer
  compile.sh              LaTeX compile and one-page validation
templates/
  cv_template.tex         Generic CV layout to customize
tests/                    Importer tests
output/                   Generated applications (created locally, ignored)
```

## Useful commands

```bash
make setup       # create .venv and install Python dependencies
make init-jobs   # create a private jobs.txt queue from the example
make import-cv   # import the only PDF in master/inbox/
make test        # run unit tests
make check       # run tests and script sanity checks
```

Compile a `.tex` file directly with:

```bash
NO_OPEN=1 bash scripts/compile.sh path/to/resume.tex
```

Exit code `2` means the PDF exceeds one page; exit code `3` means a project
header wrapped. The command prints targeted hints for both cases.

## Privacy and accuracy

- The PDF importer runs locally and makes no network requests.
- `master/inbox/`, `master/master_cv.md`, `master/eligibility.md`, `jobs.txt`,
  `output/`, and PDF files under `templates/` are ignored by Git.
- Before pushing, run `git status` and make sure no personal document is staged.
- The importer is not OCR. If it reports almost no text, run OCR on a scanned
  PDF first.
- Generated CVs still require human review. Never submit claims you cannot
  verify from your master CV.

## License

[MIT](LICENSE)
