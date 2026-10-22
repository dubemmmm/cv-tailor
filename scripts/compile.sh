#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 path/to/resume.tex" >&2
  exit 64
fi

for command in tectonic pdfinfo pdftotext; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Missing required command: $command. See README.md for installation steps." >&2
    exit 127
  fi
done

TEX="$1"
if [ ! -f "$TEX" ]; then
  echo "TeX file not found: $TEX" >&2
  exit 66
fi

DIR="$(dirname "$TEX")"

tectonic "$TEX" --outdir "$DIR" >/dev/null 2>"$DIR/compile.log" || {
  echo "COMPILE FAILED. Last lines of log:"
  tail -n 20 "$DIR/compile.log"
  exit 1
}

PDF="${TEX%.tex}.pdf"
PAGES=$(pdfinfo "$PDF" | awk '/^Pages:/ {print $2}')

# Bullets that wrap a few words onto an extra line (each one wastes a line).
ORPHANS=$(pdftotext -layout -f 1 -l 1 "$PDF" - | awk '
  /^[[:space:]]*$/ {next}
  { t=$0; sub(/^ +/, "", t) }
  inbullet && /^ +[^ •]/ && length(t) < 40 { print "  short last line: \"" t "\"" }
  { inbullet = ($0 ~ /^[[:space:]]*•/) || (inbullet && $0 ~ /^ +[^ •]/) }')

if [ "$PAGES" -gt 1 ]; then
  echo "OVERFLOW: $PAGES pages. Trim content."
  pdftotext -layout -f 2 -l 2 "$PDF" - | awk 'NF { print "  spilled: " $0 }'
  [ -n "$ORPHANS" ] && echo "Cheapest fixes (bullets that wrap only a few words):" && echo "$ORPHANS"
  exit 2
fi

# A project header (title | stack) must fit on one line: the next line after it must be a bullet.
WRAPPED=$(pdftotext -layout -f 1 -l 1 "$PDF" - | awk '
  /^Projects/ {p=1; next}
  /^(Research and Writing|Leadership|Certifications)/ {p=0}
  /^[[:space:]]*$/ {next}
  p && hdr && $0 !~ /^[[:space:]]*•/ { t=$0; sub(/^ +/, "", t); print "  wrapped header tail: \"" t "\"" }
  { hdr = p && ($0 ~ / \| /) && ($0 !~ /^[[:space:]]*•/) }')
if [ -n "$WRAPPED" ]; then
  echo "HEADER WRAP: a project's tech stack runs onto a second line. Shorten the stack in the header (keep it to the 3-4 most relevant tools)."
  echo "$WRAPPED"
  exit 3
fi

echo "OK: $PDF (1 page)"
[ -n "$ORPHANS" ] && echo "Note: these bullets wrap only a few words; tightening them frees lines:" && echo "$ORPHANS"
if [ -z "${NO_OPEN:-}" ]; then
  if command -v open >/dev/null 2>&1; then
    open -R "$PDF"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$PDF" >/dev/null 2>&1 || true
  fi
fi
exit 0
