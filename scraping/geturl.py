import requests
from bs4 import BeautifulSoup

# URL of the csstats.gg match page
url = "https://csstats.gg/match/219078981"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://csstats.gg/"
}

# Send a GET request to load the page
response = requests.get(url, headers=headers)
if response.status_code == 200:
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the button or link with the "watch demo" text
    # This example assumes the link contains 'watch' in its href attribute
    watch_demo_link = soup.find('a', href=lambda href: href and 'watch' in href)
    
    if watch_demo_link:
        # Extract the href attribute to get the link
        link = watch_demo_link['href']
        print("Found watch demo link:", link)
        
        # If the link is relative, you may need to concatenate the base URL
        full_link = requests.compat.urljoin(url, link)
        print("Full URL:", full_link)
    else:
        print("Watch demo link not found.")
else:
    print("Failed to load page. Status code:", response.status_code)
