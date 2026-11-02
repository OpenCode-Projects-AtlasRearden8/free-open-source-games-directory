#!/usr/bin/env python3
"""Link and HTML sanity checker for the Free Open-Source Games Directory.

Checks, for every HTML file found under the given roots:
  1. Internal links (href/src) resolve to real files.
  2. External links (http/https) return a 2xx or 3xx status.
  3. Basic HTML structure parses without errors (stdlib parser mode).

No third-party dependencies. No data leaves the machine except HEAD/GET
requests to publicly published project sites.
"""

import html.parser
import os
import re
import sys
import time
import urllib.request
import urllib.error

LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""", re.IGNORECASE)
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "linkcheck/1.0 (static site verification)"}


def find_html_files(roots):
    files = []
    for root in roots:
        base = os.path.join(SITE_ROOT, root)
        if not os.path.exists(base):
            print(f"WARN: root missing: {base}")
            continue
        if os.path.isfile(base):
            files.append(base)
            continue
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                if name.lower().endswith((".html", ".htm")):
                    files.append(os.path.join(dirpath, name))
    return sorted(files)


class TagParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.open_stack = []
        self.errors = []
        self.void = {"meta", "link", "br", "img", "hr", "input", "source"}

    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.open_stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if not self.open_stack:
            self.errors.append(f"line {self.getpos()[0]}: closing </{tag}> with empty stack")
            return
        open_tag, pos = self.open_stack.pop()
        if open_tag != tag:
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> does not match <{open_tag}> opened at line {pos[0]}"
            )


def check_external(url):
    attempts = 3
    last_err = ""
    for attempt in range(attempts):
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status, None
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 405, 501):
                # HEAD refused; retry with GET
                try:
                    req = urllib.request.Request(url, headers=UA, method="GET")
                    with urllib.request.urlopen(req, timeout=20) as resp:
                        return resp.status, None
                except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as exc2:
                    last_err = str(exc2)
            else:
                last_err = str(exc)
        except (urllib.error.URLError, OSError, TimeoutError, ValueError) as exc:
            last_err = str(exc)
        time.sleep(1.5 * (attempt + 1))  # transient timeouts/rate limits happen
    return None, last_err


def main():
    roots = sys.argv[1:] or ["site", "docs"]
    html_files = find_html_files(roots)
    if not html_files:
        print("FAIL: no HTML files found")
        return 1

    internal_errors = []
    parse_errors = []
    external_bad = []
    external_checked = {}

    for path in html_files:
        rel = os.path.relpath(path, SITE_ROOT)
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()

        # --- internal links
        for url in LINK_RE.findall(content):
            if url.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = url.split("#")[0]
            if not target:
                continue  # pure fragment link; parser would flag broken ids only
            real = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(real):
                internal_errors.append(f"{rel}: broken internal link -> {url}")

        # --- structural parse
        parser = TagParser()
        try:
            parser.feed(content)
            parser.close()
        except Exception as exc:  # noqa: BLE001 - report, do not crash the run
            parse_errors.append(f"{rel}: parse exception: {exc}")
        for unclosed, pos in parser.open_stack:
            # html.parser leaves void elements off the stack; anything else is bad
            parse_errors.append(f"{rel}: unclosed <{unclosed}> opened at line {pos[0]}")
        parse_errors.extend(f"{rel}: {msg}" for msg in parser.errors)

    # --- external links (deduped)
    seen = set()
    for path in html_files:
        rel = os.path.relpath(path, SITE_ROOT)
        with open(path, encoding="utf-8") as handle:
            content = handle.read()
        for url in LINK_RE.findall(content):
            if not url.startswith(("http://", "https://")):
                continue
            if url in seen:
                continue
            seen.add(url)
            if url in external_checked:
                continue
            status, err = check_external(url)
            if status is not None and 200 <= status < 400:
                external_checked[url] = f"{status}"
                print(f"  OK  {status}  {url}")
            else:
                external_checked[url] = f"ERR {err}"
                external_bad.append(url)
                print(f"  BAD        {url} -> {err}")
            time.sleep(0.2)  # be polite

    print()
    print(f"Files parsed        : {len(html_files)}")
    print(f"External links OK   : {len([u for u in external_checked if not str(external_checked[u]).startswith('ERR')])}")
    print(f"External links bad  : {len(external_bad)}")

    problems = []
    problems += [f"INTERNAL: {m}" for m in internal_errors]
    problems += [f"PARSE   : {m}" for m in parse_errors]
    problems += [f"EXTERNAL: {u}" for u in external_bad]

    if problems:
        print(f"\nFailures ({len(problems)}):")
        for line in problems:
            print(f"  - {line}")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
