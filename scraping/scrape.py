import requests

def get_cookie(cookie_str):
    command, cookies = cookie_str.split(':')

    c = cookies.split(';')
    cookies = {}
    for i in c:
        elem = i.split('=')

        cookies[elem[0].strip()]=elem[1]
    return command, cookies


cookie_str="Cookie: XSRF-TOKEN=eyJpdiI6Ik55anRNRFh0cVB5eStBbEF1ZzF0L2c9PSIsInZhbHVlIjoieVdqdlUydmRXNTRqRUpEbFFaTTFaV2M5eWVxU0p2K0x3MU5heDNrUTdvVEdCdU1IU1Q2K24xK0NvYy9xZnc4ckZ6aWhMZWVybnBZdVMwZXVzMmZka21IUFRIS1plY3A3NmpkWlRxWEs5NC8zMWNyYU53a05IYWR1cnFBRFhZNVciLCJtYWMiOiJmMWQyMmRmZDAxZmJhOGJlOTUxMWE1OGNjNmI0MTAwOGQwN2U1NjA4YjA5YjdjODBhMjNmZjQzMzFhNmVlMTBhIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6InhUZDR6bVMvU3ovS0lTQzBucjJFVGc9PSIsInZhbHVlIjoiK1RYbW10aWlVT1dnOXBXK0dKUWFrZ3lyTGxZOTFySVo2N3NLR1l4TnJ2M2M3bnZqSVVVSEkzV1ltTGJORzMwcEJycEd3UjA2WWFkekREdzZtaXgzLzdkcTlzTVZFMnpOK3hqdEljWUZHV3JsN3hxSVIzYU5qK2ZFL2ZISmlvZW8iLCJtYWMiOiIwNjEyMGUyODM4ZGU4MjI1YWZmZjk0NjA2ZTc0ZGFhMTdjMTQ3N2NiOGNiZDA5NmVmNGIyMTczZDgyOWNhNzJiIiwidGFnIjoiIn0%3D; NotificationSeen=true; DiscordSeen=true; __cf_bm=v1Mw_JGWQiHMGZbXzw3p.esbUAlyrYMu0VmMQ3U56tA-1730571948-1.0.1.1-Ux6oST.qgEOLaZTUeC7EjMM.5dSzBC3adz6vW1FNfmNw74BqXXwrfG.DipmpwbN.3nZ2bTsPASot6olwe9TTAw; cf_clearance=0wdYFl2xuSr58RnZJcpe5Pqy2CBrXUYoNQJ8pski8IY-1730571945-1.2.1.1-w3fOVv4.sIk4eYLVw4_9OJVU2VAYp4XhydkYp57jVhz1br1FHgrJrjZE6asv6FLX2MaAFLEcgkQYqioP22BXx7NYUZGLeW8di5SNdDkZreJ3EGyr5L7HNB_gGgveloGmokR5R9dbTixMsLClrg.fn.gzhYKGrsx0x9yEqWvFi5v8A2knZRZFrvstfuK04elniKgQiuo08.WkDcRdOosb_GySziGc5ok.SApq03cnaHiyhXtlu52FMT7MoR0URVlWqcHu9FZdktqVuj46vGoI75OgmnSns5Hv6dAERFABcGDf50FnKGCOkuHht2fP71jqVhYi3iaLusa1ByzibHOUVCkjanwv9BbZnzqhdlFLMkuW96gNT3O13fvl5jmdy_Nh"
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

# Send the GET request
response = session.get(url, allow_redirects=False)  # Disable redirects to capture original headers
print(response)

# Check for the Steam link in the response headers
steam_link = response.headers.get('Location')

if steam_link and steam_link.startswith("steam://"):
    print("Steam link found:", steam_link)
else:
    print("No Steam link in headers or other issue encountered.")
