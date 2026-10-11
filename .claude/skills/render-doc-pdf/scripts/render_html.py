"""
Converts a (preprocessed) Markdown file into a self-contained, print-ready HTML
page using the CANBridge house style - the same look as docs/Anwenderdokumentation.pdf
and docs/CodeReview_Report.pdf: a dark-green accent, A4 print margins, a dark
terminal-style block for fenced code, and light green callout boxes for
blockquotes.

Also cleans up two things no markdown renderer handles on its own:
- `[text](file://...)` links (meaningless in a standalone PDF) become inline
  code showing just the path, instead of a dead link.
- A handful of inline LaTeX snippets (\\mathbf, \\text, \\le, \\pm, etc. - easy
  to end up with when a doc author pastes in a formula) get flattened to plain
  text, since no MathJax is loaded here and raw TeX commands would otherwise
  show up verbatim.

Usage: python render_html.py <input.md> <output.html>
(Run preprocess_md.py on the input first for anything but a very simple doc -
see SKILL.md.)
"""
import re
import sys
import markdown

src_path = sys.argv[1]
out_html_path = sys.argv[2]

with open(src_path, "r", encoding="utf-8") as f:
    md_text = f.read()

# Strip YAML frontmatter if present
md_text = re.sub(r"^---\n.*?\n---\n", "", md_text, count=1, flags=re.DOTALL)


def strip_file_links(m):
    return f"`{m.group(1)}`"


md_text = re.sub(r"\[`([^`]+)`\]\(file://[^)]+\)", strip_file_links, md_text)
md_text = re.sub(r"\[([^\]]+)\]\(file://[^)]+\)", strip_file_links, md_text)


def latex_to_plain(expr):
    expr = expr.strip()
    expr = re.sub(r"\\text\{([^{}]*)\}", r"\1", expr)      # innermost braces first -
    expr = re.sub(r"\\mathbf\{([^{}]*)\}", r"\1", expr)    # \text{} nests inside \mathbf{}
    expr = re.sub(r"\^\{([^{}]*)\}", r"^\1", expr)
    expr = expr.replace("\\,", " ").replace("\\pm", "\u00b1")
    expr = expr.replace("\\le", "\u2264").replace("\\ge", "\u2265")
    expr = re.sub(r"\s+", " ", expr).strip()
    return expr


md_text = re.sub(r"\$\$(.+?)\$\$", lambda m: latex_to_plain(m.group(1)), md_text, flags=re.S)
md_text = re.sub(r"\$(.+?)\$", lambda m: latex_to_plain(m.group(1)), md_text)

html_body = markdown.markdown(md_text, extensions=["extra", "sane_lists", "toc"])

title_match = re.search(r"^#\s+(.+)$", md_text, flags=re.M)
title = title_match.group(1).strip() if title_match else "Dokument"

html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{ size: A4; margin: 22mm 18mm 20mm 18mm; }}
  body {{
    font-family: "Segoe UI", Helvetica, Arial, sans-serif;
    color: #1a1a1a;
    line-height: 1.5;
    font-size: 11pt;
  }}
  h1 {{
    font-size: 22pt;
    border-bottom: 3px solid #0a5c36;
    padding-bottom: 6px;
    margin-top: 0;
  }}
  h1:not(:first-of-type) {{ page-break-before: always; }}
  h2 {{
    font-size: 15pt;
    color: #0a5c36;
    border-bottom: 1px solid #cfd8d4;
    padding-bottom: 3px;
    margin-top: 28px;
  }}
  h3 {{ font-size: 12.5pt; color: #14532d; margin-top: 20px; }}
  h4 {{ font-size: 11.5pt; color: #14532d; margin-top: 16px; }}
  code {{
    background: #f0f3f1;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
    font-size: 9.5pt;
  }}
  pre {{
    background: #16281f;
    color: #d9f2e6;
    padding: 10px 12px;
    border-radius: 5px;
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 9pt;
    line-height: 1.4;
  }}
  pre code {{ background: none; padding: 0; color: inherit; }}
  blockquote {{
    border-left: 4px solid #0a5c36;
    background: #f4faf6;
    margin: 14px 0;
    padding: 6px 14px;
    color: #204030;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0 20px 0;
    font-size: 10pt;
  }}
  th, td {{
    border: 1px solid #c9d3ce;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
  }}
  th {{ background: #e7f2ec; }}
  hr {{ border: none; border-top: 1px solid #cfd8d4; margin: 22px 0; }}
  ul, ol {{ margin: 6px 0; padding-left: 24px; }}
  li {{ margin: 3px 0; }}
  a {{ color: #0a5c36; }}
  strong {{ color: #0a3d24; }}
  @media print {{
    h2 {{ break-after: avoid; }}
    h3, h4 {{ break-after: avoid; }}
    pre, table, blockquote {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", out_html_path)
