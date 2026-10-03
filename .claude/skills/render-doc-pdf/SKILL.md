---
name: render-doc-pdf
description: Render a CANBridge project Markdown doc (docs/Anwenderdokumentation.md, docs/CodeReview_Report.md, or similar) into a styled PDF matching the project's established green-branded house style. Use this whenever the user asks to convert a .md file to PDF, mentions "PDF wandeln", "als PDF rendern", "PDF neu erzeugen", or asks to update/regenerate one of these PDFs after editing the source Markdown - including proactively, without being asked, whenever you yourself just finished editing one of these .md files and its paired .pdf exists in the same docs/ folder, since a stale or plain/unstyled PDF next to a styled one is a recurring source of confusion in this project.
---

# Render a project doc to a styled PDF

This pipeline produces the exact look already used for `docs/Anwenderdokumentation.pdf`
and `docs/CodeReview_Report.pdf`: dark-green headings/accent, A4 print margins,
a dark terminal-style block for code, light-green blockquote callouts. It exists
because plain browser "Print to PDF" output (no CSS, visible URL/timestamp/page
chrome) does not match the house style and has repeatedly needed to be redone.

## Why two preprocessing steps are needed

`python-markdown` is stricter than GitHub/CommonMark about two things these docs
rely on: a bullet list directly under a lead-in sentence (no blank line), and a
multi-line `- **Label:** ...` bullet with an indented fenced code block under it.
Both render wrong (literal `- ` text, or code leaking out of its block) unless
normalized first. `scripts/preprocess_md.py` fixes exactly these three cases -
read its module docstring for the details if a new doc hits a fourth case.

## Steps

1. Make sure a scratch venv with `markdown` installed exists. If you don't already
   have one from earlier in this session, create one in the scratchpad directory:
   ```bash
   python3 -m venv /tmp/.../scratchpad/mdvenv   # use the actual scratchpad path
   /tmp/.../scratchpad/mdvenv/bin/pip install markdown
   ```

2. Preprocess the source Markdown (always do this - skipping it is what causes
   the rendering bugs described above):
   ```bash
   mdvenv/bin/python scripts/preprocess_md.py <doc>.md /tmp/.../scratchpad/<doc>.pre.md
   ```

3. Render to styled HTML:
   ```bash
   mdvenv/bin/python scripts/render_html.py /tmp/.../scratchpad/<doc>.pre.md /tmp/.../scratchpad/<doc>.html
   ```
   The title shown in the PDF's `<title>` tag is taken from the document's first
   `# H1` heading automatically.

4. Print to PDF with headless Chrome (the flags matter - without
   `--no-pdf-header-footer` Chrome adds a URL/date/page-number header and footer
   that does not belong in a delivered document):
   ```bash
   google-chrome --headless --no-sandbox --disable-gpu \
     --print-to-pdf=<doc-dir>/<doc>.pdf --no-pdf-header-footer \
     "file:///tmp/.../scratchpad/<doc>.html"
   ```

5. Open the resulting PDF (e.g. with `pdftotext -layout` or by reading a page as
   an image) and sanity-check headings, code blocks, and tables actually
   rendered - don't just trust that Chrome exited 0. Then commit the `.pdf`
   alongside the `.md` it was rendered from.

## When editing the .md yourself

If you edit `docs/Anwenderdokumentation.md` or `docs/CodeReview_Report.md` as
part of other work, re-render the paired PDF through this same pipeline before
committing, even if the user didn't explicitly ask for the PDF this time - an
edited .md with a now-stale .pdf sitting next to it in the same commit is worse
than no PDF update at all.
