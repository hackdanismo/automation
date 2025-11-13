import gzip
import requests
import xml.etree.ElementTree as ET 
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

SITEMAP_URL = "https://www.frontify.com/sitemap.xml"

UA = {"User-Agent": "sitemap-url-checker/1.0 (+https://example.com)"}
TIMEOUT = 20
# Adjust for the network/site
MAX_WORKERS = 20

def fetch_text(url: str) -> str:
    # Fetch the text (handles .gz compressed sitemaps)
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    if url.endswith(".gz") or "gzip" in r.headers.get("Content-Type", ""):
        return gzip.decompress(r.content).decode("utf-8", errors="replace")
    return r.text

def parse_xml(xml_text: str):
    # Return (urls, child_sitemaps) from a sitemap XML string
    root = ET.fromstring(xml_text)
    urls = [el.text.strip() for el in root.findall(".//{*}url/{*}loc") if el.text]
    children = [el.text.strip() for el in root.findall(".//{*}sitemap/{*}loc") if el.text]
    return urls, children

def gather_urls(sitemap_url: str, seen=None):
    # Recursively collect URLs from sitemap indexes and urlsets
    if seen is None:
        seen = set()
    if sitemap_url in seen:
        return set()
    seen.add(sitemap_url)

    try:
        xml_text = fetch_text(sitemap_url)
    except requests.RequestException as e:
        print(f"{sitemap_url} - {e}")
        return set()

    urls, children = parse_xml(xml_text)
    out = set(urls)
    for child in children:
        child_url = urljoin(sitemap_url, child)
        out |= gather_urls(child_url, seen)
    return out

def _head_then_get(url: str) -> int:
    # Try HEAD first, if the site disallows this (405/403), fallback to GET.
    # Returns the final status code (follows redirects)
    try:
        r = requests.head(url, headers=UA, timeout=TIMEOUT, allow_redirects=True)
        # Some sites return 405 for HEAD; some return 403 but allow GET
        if r.status_code in (405, 403) or r.status_code == 404 and r.is_redirect:
            r = requests.get(url, headers=UA, timeout=TIMEOUT, allow_redirects=True, stream=True)
            # If no Body is needed, close quickly
            r.close()
        return r.status_code
    except requests.RequestException:
        # Treat network errors as 000
        return 0

def check_urls(urls):
    # Check all URLs concurrently and print the results. Returns dict of url->status
    results = {}
    print(f"Checking {len(urls)} URLs for HTTP status codes...\n")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        fut_map = {ex.submit(_head_then_get, u): u for u in urls}
        for fut in as_completed(fut_map):
            u = fut_map[fut]
            status = fut.result()
            results[u] = status
            print(f"{status or 'ERR'} {u}")
    return results

if __name__ == "__main__":
    print(f"Fetching sitemap: {SITEMAP_URL}\n")
    all_urls = gather_urls(SITEMAP_URL)

    if not all_urls:
        print("No URLs found.")
    else:
        print(f"Found {len(all_urls)} URLs in the sitemap.\n")
        results = check_urls(sorted(all_urls))

        # Report 4xx not-found types promonently (404/410)
        bad = [u for u, s in results.items() if s in (404, 410)]
        if bad:
            print(f"\n Not Found ({len(bad)}) URLs (404/410):\n")
            for u in bad:
                print(u)
        else:
            print("No 404/410 URLs found.")