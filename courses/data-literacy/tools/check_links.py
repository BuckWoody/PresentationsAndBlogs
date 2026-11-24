"""
Checks every external link in the workshop's markdown files.

Usage:   python3 tools/check_links.py            (needs Python 3.9 or later and an internet connection)
         python3 tools/check_links.py --quiet     (print only the links that need attention)

Each link gets one of these results:
  OK           the page answered, at the address you linked
  MOVED        the page answered, but at a different address. This is the case that matters most:
               a page that was retired often "redirects" to a home page and looks fine to a quick glance
  BLOCKED      the site refused an automated request (common for large sites). Open it in a browser
  FAILED       the address did not answer, or the page was not found

The script exits with a non-zero code if anything FAILED or MOVED, so you can use it before publishing.
"""
import concurrent.futures
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = re.compile(r"""https?://[^\s"<>\]`]+""")
SKIP = ("http://127.0.0.1", "http://localhost")
HEADERS = {"User-Agent": "Mozilla/5.0 (data-literacy-link-check)"}


def clean(url):
    url = url.rstrip(".,;:'")
    while url.endswith(")") and url.count("(") < url.count(")"):
        url = url[:-1]
    return url


def collect():
    found = {}
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "venv", "__pycache__")]
        for name in files:
            if not name.endswith((".md", ".html")):
                continue
            path = os.path.join(folder, name)
            with open(path, encoding="utf-8") as f:
                for raw in URL.findall(f.read()):
                    url = clean(raw)
                    if url.startswith(SKIP) or "{{" in url:
                        continue
                    found.setdefault(url, set()).add(os.path.relpath(path, ROOT))
    return found


def same_place(asked, got):
    a, g = urllib.parse.urlparse(asked), urllib.parse.urlparse(got)
    host = lambda u: u.netloc.lower().removeprefix("www.")
    path = lambda u: urllib.parse.unquote(u.path).rstrip("/")
    return host(a) == host(g) and path(a) == path(g)


def check(url):
    """Returns (result, detail)."""
    last_error = None
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                final = r.geturl()
                if same_place(url, final):
                    return "OK", str(r.status)
                return "MOVED", "now at " + final
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in (403, 429) and method == "GET":
                return "BLOCKED", "HTTP %d (open it in a browser)" % e.code
            if e.code in (403, 405, 429, 501) and method == "HEAD":
                continue  # some sites refuse HEAD, so try GET
            return "FAILED", "HTTP %d" % e.code
        except Exception as e:  # DNS, timeout, certificate, refused
            last_error = e
            if method == "HEAD":
                continue
            return "FAILED", str(e)[:80]
    return "FAILED", str(last_error)[:80]


def main():
    quiet = "--quiet" in sys.argv
    links = collect()
    print("Checking %d links...\n" % len(links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(zip(links, pool.map(check, links)))
    counts = {}
    for url in sorted(links):
        result, detail = results[url]
        counts[result] = counts.get(result, 0) + 1
        if quiet and result == "OK":
            continue
        print("%-8s %s\n         %s   (in %s)" % (result, url, detail, ", ".join(sorted(links[url]))))
    print("\nSummary: " + ", ".join("%d %s" % (n, k) for k, n in sorted(counts.items())))
    return 1 if counts.get("FAILED") or counts.get("MOVED") else 0


if __name__ == "__main__":
    sys.exit(main())
