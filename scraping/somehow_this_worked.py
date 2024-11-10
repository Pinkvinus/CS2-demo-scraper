import requests

# URL of the csstats.gg page
url = "https://csstats.gg/match/219078981/watch/93c9a69d8dde12cb512c35eb211d6229b22b07cf359e8520eac0de5a72ec88fa"

# Create a session object
session = requests.Session()

# Set headers exactly as seen in the browser
session.headers.update({
    "Host": "csstats.gg",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://csstats.gg/match/219078981",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=1",
    "TE": "trailers"
})

# Set cookies as they appear in the request headers
session.cookies.update({
    "XSRF-TOKEN": "eyJpdiI6Imtlc1pGSC90L21vRENmWG96cFJBMlE9PSIsInZhbHVlIjoiTmVrTjZwVXdiOFF1RHhxVjlETnZnd3NpVkZjWE53eVgyTjY5eGV5QVhyNlEweXFiSW81dzR1aFlBeXhCVkxZcThLbmgyZVE0d2VVZlJFdlZCRWdNbGcvcUtYOUx1L0xrNHpqZ3RZdlg3VWxQbFZaZUxWa2YrSm5zWTVxaXRZTWkiLCJtYWMiOiIyNDJjYzIzNDkwYjAwYjA5NjIzMzBiZTkxMjdhNjA3YWJlMDJjNGVlNTlhNTM3OTAwM2ZlMmJjOTI2NTdiYjJkIiwidGFnIjoiIn0%3D",
    "laravel_session": "eyJpdiI6IitXN1ljMGExaXJWZXozODJrbEd1UVE9PSIsInZhbHVlIjoiK3dzQ2NhMHpVWkpxNzZVWDVFb2dPR21DNFhOMDB5WGxJWG1rR1FLajZHQisyRFhFSXU0YzhyaGtOS2t1Kzd4Z1dzWTdadmRzdUhESVBvaWY5dTFXSWxyQ0ZCazZKVHhwR1VGMkgxeUZVbTg3ZjFwVmZoWEtnMG5NSjN1bkwxSFciLCJtYWMiOiI0MjYzOTZjMDFiZWM0ZGEzZDFiNzJiNWZmYWE0OWI3MmIxYjk3OGMyYjgyNDRjYThkODEwYzdiOGNkNmJjMmIyIiwidGFnIjoiIn0%3D",
    "__cf_bm": "6ug84bbGIirsxyvkyO7lL4UkbkLKdQbyGLyVEzjEtY8-1730559605-1.0.1.1-EI0VYR4YdBwWJ1e9mfsMO4.F0nlhgQlVghxq9ADTEe7WhB_QIgKKqoViCijg175tKSKl5OKlFHGFZjzzm3nUEA",
    "cf_clearance": "H4NIjtUoSaOVVNu6NRp6XkobRyzDSVPUOsTVF3c5_XA-1730558370-1.2.1.1-KKNMcpwm1O9ToHTKeKBWn9LbZ2P1TRX6zlMTj0ArGNi5p.PmrQEqteicSHimXt9WX.wHI8lJbyC7RmzGxnEKKaYdOXxa.KWgJQcuwGNB3KDhdQMgTEqfMLkKphplSA9Lf8.K.xJnGwpSIaI9.4Z9sOzrtw5xFMHZJw3U1Xey08nhzG5ZLPaAbTFv6bGC.z5RPcaKdOlDUgnnpj0XlhN90lEhmAqTGNIOPKKSOaWoypjg1XaOmfcgJMR.wvhLxX9Pt7EZoFDILct5b_F_DXjcXUtS7I1Cu5vHByeId2OsSYB.Vsdi5iEXlEa05b6S6XeIIkQ8Nhv_XmkEDMiZoP8cfJK_XtQ3FupJ5AAtsEoSUeNnfNi_0KrJY0t6Ov0IIgYF",
    "NotificationSeen": "true",
    "DiscordSeen": "true"
})

# Send the GET request
response = session.get(url, allow_redirects=False)  # Disable redirects to capture original headers
print(response)
# Check if we get the Steam link in headers
steam_link = response.headers.get('location')

if steam_link and steam_link.startswith("steam://"):
    print("Steam link found:", steam_link)
else:
    print("No Steam link in headers or encountered other issues.")
