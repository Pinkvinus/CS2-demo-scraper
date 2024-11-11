import cloudscraper
import re
import time

# https://pypi.org/project/cloudscraper/
# The cloud scraper scrape object is identical to the session object in Requests

url = "https://csstats.gg"

def get_cookie():
    cookie_str=""
    with open('cookie.txt') as f: cookie_str = f.read()
    if cookie_str == "":
        print("Err: Cookie string not found")
        exit(1)


    command, cookies = cookie_str.split(':')

    c = cookies.split(';')
    cookies = {}
    for i in c:
        elem = i.split('=')

        cookies[elem[0].strip()]=elem[1]
    
    return command, cookies

# Reads the contents of the secret cookie.txt file, so the cookie isn't shared on github

_ , cookies = get_cookie()

headers = {
    "Host": "csstats.gg",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=1",
    "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])  # Convert cookies dictionary to a string
}

def get_scraper():
    scraper = cloudscraper.create_scraper()
    scraper.headers.update(headers) 

    return scraper

def get_html(url):
    scraper = get_scraper()
    return scraper.get(url).text


def url_2_file(url, filename):
    f = open("./tmp/"+filename+".html", "w")
    f.write(get_html(url))

def get_steam_link(url):
    # Send the GET request
    scraper = get_scraper()
    response = scraper.get(url, allow_redirects=False)  # Disable redirects to capture original headers
    print(response)

    # Check for the Steam link in the response headers
    steam_link = response.headers.get('Location')

    if steam_link and steam_link.startswith("steam://"):
        return steam_link, scraper

    print("No Steam link in headers or other issue encountered.")
    exit(1)

def single_lookup_html(html:str, search_word:str):
    for line in html.splitlines():
         if search_word in line:
            match = re.search(r'href="([^"]+)"', line)
            if match:
                link = match.group(1)
                return url+link
    return ""

def get_watch_demo_url(arg:str):
    """
        As argument it can either take a match link or html. If match link is given then
    """

    if not "\n" in arg and not "\r\n" in arg:
        arg = get_html(arg)

    return single_lookup_html(arg, "/watch/")

class Player:
    def __init__(self, username, link, isBanned):
        ...


def get_players():
    ...

match_url = "https://csstats.gg/match/221226336"

html = get_html(match_url)
print(get_steam_link(get_watch_demo_url(match_url))[0])









