import cloudscraper

# https://pypi.org/project/cloudscraper/
# The cloud scraper scrape object is identical to the session object in Requests

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


def url_2_file(url, filename):
    scraper = cloudscraper.create_scraper()
    f = open("./tmp/"+filename+".html", "w")
    scraper.headers.update(headers)
    f.write(scraper.get(url).text)

def get_steam_link(url):
    # Send the GET request
    scraper = get_scraper()
    response = scraper.get(url, allow_redirects=False)  # Disable redirects to capture original headers
    print(response)

    # Check for the Steam link in the response headers
    steam_link = response.headers.get('Location')

    if steam_link and steam_link.startswith("steam://"):
        print("Steam link found:", steam_link)
    else:
        print("No Steam link in headers or other issue encountered.")
    return steam_link

#url_2_file("https://csstats.gg/match/221017699", "match1")

url = "https://csstats.gg"
match_url = "/match/221017699/watch/4adf23a35296450a0b5eef369c0c9d9133be1966abaadda8cba82491e0b2f631"


#url_2_file(url+match_url, "response")
get_steam_link(url+match_url)
