import requests

def get_cookie(cookie_str):
    command, cookies = cookie_str.split(':')

    c = cookies.split(';')
    cookies = {}
    for i in c:
        elem = i.split('=')

        cookies[elem[0].strip()]=elem[1]
    return command, cookies


cookie_str="Cookie: NotificationSeen=true; DiscordSeen=true; XSRF-TOKEN=eyJpdiI6ImdQdVN2ckVwOGJDM0NMWDBIaDEvbWc9PSIsInZhbHVlIjoid01NdFFiRG1BdmR4bm9BQi9vS0dCOWdpU2lKNmYrOGRTWlNleDRYNk1jcnR4dUdjVTU5ZGZCVHhLR3VlSWhqb0RKU1hCM3I5UXdybm1vMERzcHp5N1NOYTNJdisrbmhIaTM4cjZ4d0J4UUlOMTl2YjRrZ3QvMVkrc21vQVF2MFciLCJtYWMiOiIyOTdlM2FlNGVkNWRhZTEwNTgxNmM3ZjgyZDQ5NDVmMjg0MjRkZjIyYTRiZTMwODg5YWZhMDljNjdhYzU2OWVjIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6ImhhVDdCUFhzNlZBU2Q2OTczRkdHVWc9PSIsInZhbHVlIjoid2pyMGxVMVFkYStROWxXTjhDV2ZsOEl0aUc0aHVLWnBVQU1OT0JqanNyWkt5UTJHZ3BmZENxLzIrM0JQS3VkK3pIMGdWZzRIYWRGTzhlT3lVOEwxNkk5UldsODd2YVBXcnpyRzRCSFFEazRKczBrR3hjL1g4TnBwMzFYR3hpemUiLCJtYWMiOiI3NWE1M2RmYjA5YmYzODg4ZjI1ZGVjMjYzM2IyZDg1YTg1YjY3MTc1ZWNhY2NhMTM1YzJkMDc0OTViMjBkYzE2IiwidGFnIjoiIn0%3D; __cf_bm=h5mhpsrpKCULuE.1cgqJ0ouCJzOrTkp4jNgcoS6Ausk-1731245891-1.0.1.1-ETjMBtEdJphrcaP8qzVT2sLsFdakhkC3r_k6M.5YUWoSE0xTcLFGXiSC0Ada18cl9C2Bg02Sy_knJtDQpUHxcA; cf_clearance=.4VCfme2rt_JO7OP6XXZrVcMWTPuX4t8I1szPIB_TQs-1731246421-1.2.1.1-xCf0wr4DwiL98Bje0KxZMzFpYm2WuR4Kj23GR_VX315tARVmxHNI0gbFHBwG5CYiqeAs5BHGnoJcwRLh2vOgTokiVCKRBgIY6AKWIPen1jWcA.gcFKlpdODWbRHpGC01Hi2lAvM6tWvOGei4WaAIpbAWOvMxMAZZWmwkTlgLB7yGekrDO4kg.sjf4mxwaCZ8z5jCfwoZOMmpxZ6jjK8QprrIbWhibAZg3BvX1dZ79GZZGc4zXQoBmRiDvSeb_G73UxBJvyq46PxO4XMtfOBYopdijG1kDewr46hdo5g6iyRCqxtCtTRKGzlOCfrly7DLXtRJ_1zt1WvsHsx6hUKjtBrNB10CdWRjRg4yrJPBf.9PNAHwKRKW1t5K8oSkRkyq"
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
