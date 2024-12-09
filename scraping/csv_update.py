from utils import csv_utils
import pandas as pd


demos_path = "C:/Users/Gert/Desktop/demos"
csv_file_path = "C:/Users/Gert/repos/CS2-demo-scraper/scraping"
lines = []

newest_file = csv_utils.get_newest_file_name(csv_file_path)

df = pd.read_csv(newest_file)
cheater_games_links = df[~df["cheater_names_str"].isna() & df["demo_file_name"].isna()]
links_only = cheater_games_links["steamlink"].to_list()
for i in links_only:
    lines.append(i.replace("steam://rungame/730/76561202255233023/+csgo_download_match%20", ""))

csv_utils.add_filename_to_csv(lines, demos_path, csv_file_path)