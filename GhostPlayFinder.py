import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init()

print("Script starting...")  # Debug line to confirm execution

# Color definitions using colorama
class Colors:
    BLUE = Fore.BLUE
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    RED = Fore.RED
    LIGHTBLUE = Fore.LIGHTBLUE_EX  # Used for "Version" and now "Twitter"
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL

# User-Agent list to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1'
]

# Queries targeting specific cracked game and streaming sites
QUERIES = [
    "free cracked game sites like steamunlocked.net gog-games.to steamrip.com -torrent -signup -login",
    "download pre-installed cracked games like steamunlocked.net gog-games.to steamrip.com -torrent",
    "free pc games cracked direct download like steamunlocked.net gog-games.to steamrip.com -torrent",
    "pirate streaming sites like alphatron.tv mapple.tv hianime.to -torrent",
    "free movie streaming sites like alphatron.tv mapple.tv hianime.to -torrent",
    "best free cracked games and streaming sites like steamunlocked.net gog-games.to steamrip.com alphatron.tv mapple.tv hianime.to -torrent"
]

# Function to display colorful creator box with updated colors
def display_creator_box():
    box = [
        f"{Colors.BLUE}========================================{Colors.RESET}",
        f"{Colors.YELLOW}|       Pirate Search Tool             |{Colors.RESET}",
        f"{Colors.BLUE}|--------------------------------------|{Colors.RESET}",
        f"{Colors.MAGENTA}| Created by: YourAnonSp1r1t           |{Colors.RESET}",
        f"{Colors.LIGHTBLUE}| Twitter: x.com/YourAnonSp1r1t        |{Colors.RESET}",  # Now Light Blue
        f"{Colors.LIGHTBLUE}| Version: 1.0                         |{Colors.RESET}",
        f"{Colors.GREEN}| Made In 2025                         |{Colors.RESET}",
        f"{Colors.RED}| Purpose: Find cracked game &         |{Colors.RESET}",
        f"{Colors.RED}|          streaming sites             |{Colors.RESET}",
        f"{Colors.BLUE}========================================{Colors.RESET}"
    ]
    for line in box:
        print(line)
    print("\nPress Enter to start the search...")
    input()  # Waits for Enter key press

# Function to check if a URL is accessible
def is_url_accessible(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Function to extract a snippet
def get_page_snippet(url):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        snippet = soup.find('p') or soup.find('div')
        return snippet.text[:150] + "..." if snippet else "No snippet available."
    except Exception as e:
        return f"Error fetching snippet: {e}"

# Function to search using DuckDuckGo and Bing
def perform_search(query, num_pages=3):
    urls = set()
    headers = {'User-Agent': random.choice(USER_AGENTS)}

    # DuckDuckGo Search
    print(f"Searching DuckDuckGo for: {query}")
    for page in range(num_pages):
        ddgo_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}&p={page}"
        try:
            response = requests.get(ddgo_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"DuckDuckGo returned status: {response.status_code} on page {page + 1}")
                break
            soup = BeautifulSoup(response.text, 'html.parser')
            for result in soup.select('a.result__url'):
                href = result.get('href')
                if href:
                    full_url = urllib.parse.urljoin("https://", href.split('uddg=')[1]) if 'uddg=' in href else href
                    if full_url.startswith('http') and 'duckduckgo' not in full_url.lower():
                        urls.add(full_url)
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
            break

    # Bing Search
    if len(urls) < 10:
        print(f"Searching Bing for: {query}")
        for page in range(num_pages):
            bing_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&first={page * 10}"
            try:
                response = requests.get(bing_url, headers=headers, timeout=10)
                if response.status_code != 200:
                    print(f"Bing returned status: {response.status_code} on page {page + 1}")
                    break
                soup = BeautifulSoup(response.text, 'html.parser')
                for result in soup.select('li.b_algo h2 a'):
                    href = result.get('href')
                    if href and href.startswith('http') and 'bing' not in href.lower():
                        urls.add(href)
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"Bing search failed: {e}")
                break

    return list(urls)

# Main logic
display_creator_box()  # Show the colorful creator box first
results = []
print("Starting deep search for cracked game and pirate streaming sites...")
for query in QUERIES:
    found_urls = perform_search(query)
    print(f"Found {len(found_urls)} URLs for query: {query}")
    
    for url in found_urls:
        print(f"Checking: {url}")
        if is_url_accessible(url):
            snippet = get_page_snippet(url)
            results.append((url, snippet))
            print(f"Accessible: {url}")
            print(f"Snippet: {snippet}\n")
        else:
            print(f"Inaccessible, skipping: {url}")
        time.sleep(random.uniform(1, 3))

# Save results
with open("pirate_gaming_and_streaming_sites.txt", "w", encoding="utf-8") as file:
    file.write("Free Cracked Game and Pirate Streaming Sites Search Results\n")
    file.write(f"Generated on: {time.ctime()}\n\n")
    for url, snippet in results:
        file.write(f"URL: {url}\nSnippet: {snippet}\n\n")

print(f"\nSearch complete! Results saved to 'pirate_gaming_and_streaming_sites.txt'.")
print(f"Found {len(results)} accessible sites.")