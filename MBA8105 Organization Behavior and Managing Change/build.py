#!/usr/bin/env python3
"""Build MBA8105_Notes.html from MBA8105_Notes.md (self-contained, offline-renderable)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "MBA8105_Notes.md")
DST = os.path.join(HERE, "MBA8105_Notes.html")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>MBA 8105 — Notes</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-light.css">
<style>
  :root { color-scheme: light; }
  html { scroll-behavior: smooth; }
  body { margin: 0; background: #f6f8fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
  #toolbar { position: sticky; top: 0; z-index: 10; background: #fff; border-bottom: 1px solid #d0d7de; padding: 12px 24px; display: flex; align-items: center; gap: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
  #toolbar h1 { font-size: 14px; margin: 0; color: #57606a; font-weight: 500; }
  .badge { background: #ddf4ff; color: #0969da; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: 500; }
  .markdown-body { box-sizing: border-box; max-width: 980px; margin: 20px auto; padding: 40px 56px; background: #fff; border: 1px solid #d0d7de; border-radius: 6px; }
  @media (max-width: 767px) { .markdown-body { padding: 16px; margin: 0; border-radius: 0; border-left: none; border-right: none; } }
  .markdown-body table { display: table; width: 100%; }
  .markdown-body th { background: #f6f8fa; }
  .markdown-body blockquote { border-left: 4px solid #0969da; }
  .markdown-body h2, .markdown-body h3, .markdown-body h4 { scroll-margin-top: 64px; }
  #content a.toc-link { color: #0969da; text-decoration: none; }
  #content a.toc-link:hover { text-decoration: underline; }
  #toc-toggle { margin-left: auto; cursor: pointer; padding: 4px 10px; background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; font-size: 12px; }
  #toc { position: fixed; top: 60px; right: 20px; width: 290px; max-height: calc(100vh - 80px); overflow-y: auto; background: #fff; border: 1px solid #d0d7de; border-radius: 6px; padding: 16px; font-size: 13px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); display: none; }
  #toc.visible { display: block; }
  #toc h3 { margin: 0 0 8px 0; font-size: 12px; color: #57606a; text-transform: uppercase; }
  #toc ul { list-style: none; padding: 0; margin: 0; }
  #toc li { margin: 4px 0; }
  #toc a { color: #0969da; text-decoration: none; }
  #toc a:hover { text-decoration: underline; }
  #toc .lvl-2 { padding-left: 0; font-weight: 500; }
  #toc .lvl-3 { padding-left: 12px; color: #57606a; }
  #toc .lvl-4 { padding-left: 24px; color: #8c959f; font-size: 12px; }
</style>
</head>
<body>
<div id="toolbar">
  <h1>MBA 8105 — Organization Behavior and Managing Change</h1>
  <span class="badge" id="status">Loading…</span>
  <button id="toc-toggle">📑 目录</button>
</div>
<nav id="toc"><h3>Table of Contents</h3><ul id="toc-list"></ul></nav>
<article id="content" class="markdown-body"></article>
<script type="text/markdown" id="md-source">
__MARKDOWN_HERE__
</script>
<script>
  const md = document.getElementById('md-source').textContent;
  marked.setOptions({ gfm: true, breaks: false });
  const article = document.getElementById('content');
  article.innerHTML = marked.parse(md);
  document.getElementById('status').textContent = 'Loaded · ' + md.length.toLocaleString() + ' chars';

  const headings = article.querySelectorAll('h2, h3, h4');
  const numToId = {};
  let idCounter = 0;
  headings.forEach(h => {
    if (!h.id) h.id = 'h-' + (idCounter++);
    const m = h.textContent.match(/^\s*([0-9]+(?:\.[0-9]+)?)/);
    if (m && !(m[1] in numToId)) numToId[m[1]] = h.id;
  });

  const tocList = document.getElementById('toc-list');
  headings.forEach(h => {
    const li = document.createElement('li');
    li.className = 'lvl-' + h.tagName[1];
    const a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    li.appendChild(a);
    tocList.appendChild(li);
  });

  const tocHeading = Array.from(article.querySelectorAll('h2')).find(h => h.textContent.includes('目录'));
  if (tocHeading) {
    let el = tocHeading.nextElementSibling;
    while (el && el.tagName !== 'TABLE') el = el.nextElementSibling;
    if (el) {
      el.querySelectorAll('tbody tr').forEach(tr => {
        const cells = tr.children;
        if (cells.length < 2) return;
        const num = cells[0].textContent.trim();
        const id = numToId[num];
        if (id) {
          const a = document.createElement('a');
          a.className = 'toc-link'; a.href = '#' + id; a.innerHTML = cells[1].innerHTML;
          cells[1].innerHTML = ''; cells[1].appendChild(a);
          const a2 = document.createElement('a');
          a2.className = 'toc-link'; a2.href = '#' + id; a2.innerHTML = cells[0].innerHTML;
          cells[0].innerHTML = ''; cells[0].appendChild(a2);
        }
      });
    }
  }

  document.getElementById('toc-toggle').addEventListener('click', () => {
    document.getElementById('toc').classList.toggle('visible');
  });
</script>
</body>
</html>
"""

def main():
    with open(SRC, "r", encoding="utf-8") as f:
        md = f.read()
    safe = md.replace("</script>", "<\\/script>")
    html = TEMPLATE.replace("__MARKDOWN_HERE__", safe)
    with open(DST, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built {os.path.basename(DST)} — MD: {len(md):,} chars, HTML: {len(html):,} chars")

if __name__ == "__main__":
    main()
