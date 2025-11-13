# Provide the GZip decompression utilities
import gzip
# HTTP client for fetching URLs
import requests
# XML parsing library
import xml.etree.ElementTree as ET 
# Safely construct absolute URLs from relative URLs
from urllib.parse import urljoin
# Multithreaded URL checks
from concurrent.futures import ThreadPoolExecutor, as_completed

# Sitemap URL to be crawled by the script
SITEMAP_URL = "https://www.frontify.com/sitemap.xml"

# Custom User Agency (UA) for requests
UA = {"User-Agent": "sitemap-url-checker/1.0 (+https://example.com)"}
# HTTP timeout for requests
TIMEOUT = 40
# Maximum concurrency for URL checks
MAX_WORKERS = 20

def fetch_text(url: str) -> str:
    # Download the sitemap or sitemap index
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    # Raise exceptions for any HTTP errors that could occur
    r.raise_for_status()
    # Decompress .gz files
    if url.endswith(".gz") or "gzip" in r.headers.get("Content-Type", ""):
        return gzip.decompress(r.content).decode("utf-8", errors="replace")
    # Return plain XML text
    return r.text

def parse_xml(xml_text: str):
    # Return (urls, child_sitemaps) from a sitemap XML string
    root = ET.fromstring(xml_text)
    # Extract <loc> URLs from the XML file
    urls = [el.text.strip() for el in root.findall(".//{*}url/{*}loc") if el.text]
    # Extract nested sitemaps
    children = [el.text.strip() for el in root.findall(".//{*}sitemap/{*}loc") if el.text]
    # Return a tuple of (URLs, nested sitemap URLs)
    return urls, children

def gather_urls(sitemap_url: str, seen=None):
    # Recursively collect URLs from sitemap indexes and urlsets
    if seen is None:
        # Track visited sitemaps to avoid loops
        seen = set()
    if sitemap_url in seen:
        # Skip reprocessing already seen sitemaps
        return set()
    # Mark the current sitemap as seen
    seen.add(sitemap_url)

    try:
        # Download sitemap contents
        xml_text = fetch_text(sitemap_url)
    except requests.RequestException as e:
        # Log any failures but continue execution of the script
        print(f"{sitemap_url} - {e}")
        return set()

    # Parse sitemap into: URLs and child sitemaps
    urls, children = parse_xml(xml_text)
    # Add discovered URLs to the output
    out = set(urls)
    # Iterate over nested sitemaps
    for child in children:
        # Resolve relative child sitemap URLs
        child_url = urljoin(sitemap_url, child)
        # Recursively collect URLs
        out |= gather_urls(child_url, seen)
    return out

def _head_then_get(url: str) -> int:
    # Try HEAD first, if the site disallows this (405/403), fallback to GET.
    # Returns the final status code (follows redirects)
    try:
        # Try HEAD request first
        r = requests.head(url, headers=UA, timeout=TIMEOUT, allow_redirects=True)
        # Some sites return 405 for HEAD; some return 403 but allow GET
        if r.status_code in (405, 403) or r.status_code == 404 and r.is_redirect:
            # Fallback to GET request if HEAD does not work
            r = requests.get(url, headers=UA, timeout=TIMEOUT, allow_redirects=True, stream=True)
            # If no Body is needed, close quickly
            r.close()
        # Return the final HTTP status code
        return r.status_code
    except requests.RequestException:
        # Treat network errors as 0 when returned
        return 0

def check_urls(urls):
    # Check all URLs concurrently and print the results. Returns dict of url->status
    results = {}
    print(f"Checking {len(urls)} URLs for HTTP status codes...\n")
    # Create thread pool
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        # Submit tasks
        fut_map = {ex.submit(_head_then_get, u): u for u in urls}
        # Process completed tasks
        for fut in as_completed(fut_map):
            # Lookup URL for this future
            u = fut_map[fut]
            # Get HTTP status code
            status = fut.result()
            # Save the result
            results[u] = status
            # Print live progress
            print(f"{status or 'ERR'} {u}")
    return results

if __name__ == "__main__":
    # Log which sitemap is being fetched
    print(f"Fetching sitemap: {SITEMAP_URL}\n")
    # Recursively gather all URLs
    all_urls = gather_urls(SITEMAP_URL)

    if not all_urls:
        # Handle empty sitemap case
        print("No URLs found.")
    else:
        # Report the number of URLs
        print(f"Found {len(all_urls)} URLs in the sitemap.\n")
        # Check URLs and capture results
        results = check_urls(sorted(all_urls))

        # Filter missing URLs
        bad = [u for u, s in results.items() if s in (404, 410)]
        if bad:
            # Print summary of bad URLs that return 404 or 410 HTTP status codes
            print(f"\n Not Found ({len(bad)}) URLs (404/410):\n")
            for u in bad:
                print(u)
        else:
            # Report success when no 404 or 410 HTTP status codes are returned
            print("No 404/410 URLs found.")