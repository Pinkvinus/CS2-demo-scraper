import cloudscraper
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
from .shell_colors import shell_colors as colors

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

def get_headers():
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
    return headers

def get_scraper():
    
    scraper = cloudscraper.create_scraper()
    scraper.headers.update(get_headers()) 

    return scraper

def get_html(url):
    scraper = get_scraper()
    return scraper.get(url).text


def url_2_file(url, filename):
    f = open("./tmp/"+filename+".html", "w")
    f.write(get_html(url))
    
def html_2_file(html, filename):
    f = open("./tmp/"+filename+".html", "w")
    f.write(html)

def get_steam_link(url):
    """
        arg: A match watch demo url
        return: the steam link and the scraper used
    """
    # Send the GET request
    scraper = get_scraper()
    response = scraper.get(url, allow_redirects=False)  # Disable redirects to capture original headers

    if response.status_code != 302:
        print(f"{colors.WARNING}response code: {response.status_code}")
        print("================================== cookie outdated ==================================")
        input("update cookie and press Enter to continue..." + colors.ENDC)

        return get_steam_link(url)


    # Check for the Steam link in the response headers
    steam_link = response.headers.get('Location')

    if steam_link and steam_link.startswith("steam://"):
        return steam_link, scraper

    print("No Steam link in headers or other issue encountered.")
    return "", scraper

def single_lookup_html(html:str, search_word:str):
    """"
        Takes an html string and a search word as an argument.

        returns the line of html with the first hit
    """
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

def get_players_from_match(html:str):
    """
        Takes the html string from a match site and returns a list of tuples. 
        
        the tuples describe the players id, username, and ban status. 
        The list is ordered in terms of teams. Splitting the list in half will
        reveal the two opposing teams.
    """
    soup = BeautifulSoup(html, 'html.parser')

    scoreboard = soup.find('table', class_="scoreboard", id="match-scoreboard")
    teams = scoreboard.find_all('tbody')
    teams = [teams[0], teams[2]]

    player_info = []

    for team in teams:

        players = team.find_all('tr')

        #players = list(team.children)
        for player in players:

            link = player.find('a')

            if link is None or len(link) == 0:
                continue

            #gets the url from the tag
            url = link.get('href')

            #gets the id from the url
            match = re.search(r"/(\d+)$", url)
            id = match.group(1)

            #gets the username from the span within the link
            username = link.find('span').text

            isBanned=False
            if player.get('class') == ['has-banned']:
                isBanned=True

            #print(f"id: {id}; username: {username}; isbanned: {isBanned}")

            player_info.append((id, username, isBanned))
    return player_info
        
def get_matches_from_all_matches(html:str):
    """
        Takes the html from the all matches page and returns a list of match hrefs.
        csstats.gg + one of these hrefs will go to match page.
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", class_="table table-striped")
    table_body = table.findChild("tbody")
    rows = table_body.find_all(['tr'])
    match_hrefs = []
    for row in rows:
        match = re.search(r"(/match/\d+)", row["onclick"])
        match_id = match.group(1).split("/")[2]
        match_hrefs.append(match_id)
    return match_hrefs

def get_matches_from_player(html:str):
    """
        Takes the html string from a player site
        
        Returns a list of strings.  of cs stats match ids, that have been played in the last 30 days.
    """
    soup = BeautifulSoup(html, 'html.parser')
    match_list = soup.find("div", id="match-list-outer")
    table = match_list.findChild("table", class_="table table-striped")
    table_body = table.findChild("tbody")
    rows = table_body.find_all(['tr'])
    results = 0
    for row in rows:
        vals = row.find_all(["td"])
        date_played = vals[0].get_text(strip=True).lower()
        if "hours ago" in date_played or "minutes ago" in date_played or "hour ago" in date_played or "minute ago" in date_played or "day ago" in date_played:
            results += 1
        else:
            date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_played)
            date_obj = datetime.strptime(date_str_cleaned, "%a %d %b %y")
            if date_obj <= datetime.now() - timedelta(days=30):
                break # More than 30 days ago
            else:
                results += 1
    match_hrefs = []
    for row in rows:
        if results == 0:
            break
        match = re.search(r"(/match/\d+)", row["onclick"])
        match_id = match.group(1).split("/")[2]
        match_hrefs.append(match_id)
        results -= 1
    return match_hrefs

def get_match_information(html:str):
    """
        parameters: Html from a match site
        returns: a dictionary with match information like: map, server, average rank, and match making type
    """

    soup = BeautifulSoup(html, 'html.parser')
    info_list = soup.find("div", id="match-info-inner")
    infos = info_list.find_all('div', class_="info")
    map = infos[2].get_text().strip()
    server = infos[3].get_text().strip()
    matchmaking_type = infos[1].get_text().strip()
    is_premier = infos[1].get_text().strip().lower().find("premier matchmaking") != -1
    rank = ""
    if is_premier:
        rank_spans = infos[4].find_all("span")
        rank = int(rank_spans[1].get_text().strip().replace(",",""))
    else:
        rank = infos[4].find("img").get("title")

    dict = {"map": map, "server": server, "rank": rank, "type": matchmaking_type}
    print(dict)
    return dict
