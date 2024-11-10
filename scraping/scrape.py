import requests

def get_cookie(cookie_str):
    command, cookies = cookie_str.split(':')

    c = cookies.split(';')
    cookies = {}
    for i in c:
        elem = i.split('=')

        cookies[elem[0].strip()]=elem[1]
    return command, cookies

# Reads the contents of the secret cookie.txt file, so the cookie isn't shared on github
cookie_str=""
with open('cookie.txt') as f: cookie_str = f.read()

if cookie_str == "":
    print("Err: Cookie string not found")
    exit(1)

url = "https://csstats.gg/match/219125581/watch/c1b586758c874d951f854565bb586976ba530ec283247baacd4cb07e984cbe5b"
referer_url = "https://csstats.gg/match/219125581"

# Create a session
session = requests.Session()

# Define headers (based on the request you posted)
session.headers.update({
    "Host": "csstats.gg",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": referer_url,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=1"
})

command, cookie_vals = get_cookie(cookie_str)

# Define cookies
session.cookies.update({
    "XSRF-TOKEN": cookie_vals["XSRF-TOKEN"],
    "laravel_session": cookie_vals["laravel_session"],
    "NotificationSeen": cookie_vals["NotificationSeen"],
    "DiscordSeen": cookie_vals["DiscordSeen"],
    "__cf_bm": cookie_vals["__cf_bm"],
    "cf_clearance": cookie_vals["cf_clearance"]
})



def get_steam_link(url):
    # Send the GET request
    response = session.get(url, allow_redirects=False)  # Disable redirects to capture original headers
    print(response)

    # Check for the Steam link in the response headers
    steam_link = response.headers.get('Location')

    if steam_link and steam_link.startswith("steam://"):
        print("Steam link found:", steam_link)
    else:
        print("No Steam link in headers or other issue encountered.")
    return steam_link

get_steam_link(url)


response = requests.get("https://csstats.gg/match")
#print(f"response.content       :       {response.content}")


#print(type(response.content))
response.encoding = "utf-8"
print(response.text)

