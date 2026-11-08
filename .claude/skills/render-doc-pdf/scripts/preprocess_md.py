"""
Normalizes a Markdown file so python-markdown renders it the way GitHub/CommonMark
would, before handing it to render_html.py. Fixes three mismatches between
python-markdown's stricter list/paragraph rules and how these docs are actually
written:

1. A bullet list directly under a lead-in sentence (no blank line between them)
   gets swallowed into that paragraph as literal "- " text instead of becoming
   a list, because python-markdown (unlike GitHub) won't let a list interrupt
   an immediately preceding paragraph without a blank line first.

2. A multi-line bullet of the form "- **Label:** text\\n  more text\\n  ```code```"
   (common in review-style docs: "- **Problem:** ...", "- **Fix:** ..." under a
   finding) often fails to render its fenced code block as a real <pre> at all -
   python-markdown's list-continuation handling is inconsistent about it,
   especially for numbered sub-items nested inside the bullet. Flattening each
   such bullet into a plain "**Label:**" paragraph (dedenting its continuation
   lines) sidesteps the problem entirely and reads just as well in print.

3. Any fenced code block left at a non-zero indentation afterward (e.g. still
   nested under a numbered sub-step) gets normalized to its own fence-marker's
   indentation baseline and wrapped in blank lines, so it always ends up as a
   standalone block instead of leaking into surrounding text as inline code.

Usage: python preprocess_md.py <input.md> <output.md>
"""
import re
import sys

src_path = sys.argv[1]
out_path = sys.argv[2]

lines = open(src_path, encoding="utf-8").read().split("\n")

# --- Fix 1: blank line before a list that directly follows a paragraph ---
list_item_re = re.compile(r"^(?:-|\d+\.)\s")
fixed = []
prev_was_list_item = False
for line in lines:
    is_list_item = bool(list_item_re.match(line))
    if is_list_item and not prev_was_list_item and fixed and fixed[-1].strip() != "":
        fixed.append("")
    fixed.append(line)
    if line.strip() != "":
        prev_was_list_item = is_list_item
lines = fixed

# --- Fix 2: flatten multi-line "- **Label:** ..." bullets into paragraphs ---
# Only bullets that actually have indented continuation lines are touched -
# a plain single-line "- **Key:** value" bullet (e.g. a metadata list) is left
# as a real list item, since there's nothing fragile about those.
label_re = re.compile(r"^- \*\*(.+?)\*\*:?\s*(.*)$")

out = []
i = 0
n = len(lines)
while i < n:
    line = lines[i]
    m = label_re.match(line)
    has_continuation = m is not None and (i + 1) < n and lines[i + 1].startswith("  ")
    if m and has_continuation:
        label, rest = m.group(1).rstrip(":"), m.group(2)
        if out and out[-1].strip() != "":
            out.append("")
        out.append(f"**{label}:** {rest}".rstrip())
        out.append("")
        i += 1
        while i < n and (lines[i].startswith("  ") or lines[i].strip() == ""):
            if lines[i].strip() == "":
                out.append("")
            else:
                out.append(lines[i][2:])
            i += 1
        continue
    out.append(line)
    i += 1

text = "\n".join(out)

# --- Fix 3: normalize any fenced code block still left indented ---
lines2 = text.split("\n")
out2 = []
in_code = False
fence_indent = 0
for idx, line in enumerate(lines2):
    stripped = line.strip()
    is_fence = stripped.startswith("```")
    if is_fence and not in_code:
        fence_indent = len(line) - len(line.lstrip(" "))
        if out2 and out2[-1].strip() != "":
            out2.append("")
        out2.append(line[fence_indent:])
        in_code = True
    elif is_fence and in_code:
        out2.append(line[fence_indent:] if line.startswith(" " * fence_indent) else line.lstrip())
        in_code = False
        nxt = lines2[idx + 1] if idx + 1 < len(lines2) else ""
        if nxt.strip() != "":
            out2.append("")
    elif in_code:
        out2.append(line[fence_indent:] if line.startswith(" " * fence_indent) else line)
    else:
        out2.append(line)

open(out_path, "w", encoding="utf-8").write("\n".join(out2))
print("wrote", out_path)
