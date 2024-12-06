from csgo.sharecode import decode
import csv
import subprocess
import os
from .shell_colors import shell_colors as colors
import pandas as pd
from collections import Counter
from datetime import datetime

steamlink = "steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-38jZH-2shwO-Pj2A7-x5qsy-fqbNE"

class column_header:
    match_id = "match_id"
    steam_link = "steamlink"
    map = "map"
    server = "server"
    average_rank = "avg_rank"
    type = "type"
    team1_player_ids = "team1_string"
    team2_player_ids = "team2_string"
    cheater_names = "cheater_names_str"
    demo_file_name = "demo_file_name"
    
def steamlink_to_sharecode(url:str):
    return url.split("%20")[1]

def sharecode_to_outcomeid(share_code):
    return decode(share_code)["outcomeid"]

def steamlink_to_outcomeid(url:str):
    return sharecode_to_outcomeid(steamlink_to_sharecode(url))

def get_newest_file_name(folder):
    """
        Parameter:
            - The path for the folder that the data is in
        Returns:
            - Returns the newest scraper file
    """
    dir_list = os.listdir(folder)
    filtered_list = [k for k in dir_list if 'cs_scrape_' in k]
    if len(filtered_list) > 0:
        filtered_list.sort(reverse=True)
        return filtered_list[0]
    return None

def is_match_downloaded(url:str, path:str):
    """
        parameters: 
            - steam link with match sharing code. Ex: \"steam://rungame/730/76561202255233023/+csgo_download_match%20CSGO-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx\"
            - Download folder: path to the folder where the demofiles are stored.
        returns
            - bool: True if match corresponding to the steamlink was found in the download folder. False if not.
    """
    outcome_id = sharecode_to_outcomeid(url)
    #TODO

def check_duplicate_outcomeids(filepath):
    """
        Parameters: 
            - File path to a csv file that needs to be checked for duplicate outcomeid values
        Returns: 
            - A set of the duplicate outcome ids. If no duplicates were found the set is empty.
    """
    # Track seen IDs to filter duplicates
    seen_ids = set()
    duplicate_ids = set()

    with open(filepath, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        for row in reader:
            outcome_id = steamlink_to_outcomeid(row[1])

            #print(f"{outcome_id}")
            if outcome_id in seen_ids:
                print(f"Outcome ID duplicate: {outcome_id}")
                duplicate_ids.add(row[1])
                continue

            seen_ids.add(row[1])

    if len(duplicate_ids) != 0:
        print(f"{colors.FAIL}Duplicates found{colors.ENDC}")
    else:
        print("No duplicates have been seen")

    return duplicate_ids

def lookup_in_csv(search_term:str, column_header:str, csv_file_path:str) -> int:
    """
        Parameter:
            - The column_header that you want to look up. 
            [Ex: match_id,steamlink,map,server,avg_rank,type,team1_string,team2_string, cheater_names_str]
        Returns:
            - Returns the row number that the sharecode apears on in the csv. 
              Returns -1 if column_header given does not match any header in the file.
        Example:
            - lookup_in_csv("CSGO-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx", column_header.steam_link, get_newest_file_name())
        Warning
            - Note that when working with data representation from other modules, such as
              pandas the indexing might be off by one
    """
    with open(csv_file_path, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)

        column=-1

        # Finds the column that the column header refers to
        for i in range(0, len(header)):
            if header[i] == column_header:
                column = i
                break
            if i >=len(header):
                print(f"{colors.FAIL}No column header found with the name: \"{column_header}\"")
                print(f"Valid column headers include: {header}{colors.ENDC}")
                return column

        # i starts being one as the first row is the header row.
        i = 1

        for row in reader:
            if search_term in row[column]:
                return i
            i = i + 1
        print("search term not found in csv file")
        return -2

def add_filename_to_csv(sharecodes:list, demos_path:str, csvs_file_path:str):
    """
        parameters: 
            - list of match sharing code. Ex: [CSGO-xxxxx-xxxxx-xxxxx-xxxxx-xxxxx]
            - Download folder: path to the folder where the demofiles are stored.
        functionality:
            - gets the names of the newly downloaded demo files and adds them to the correct rows in the csv file
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H_%M_%S.%f")
    new_csv_file_name = f"cs_scrape_{timestamp}.csv"
    files_list = os.listdir(demos_path)
    latest_csv = get_newest_file_name(csvs_file_path)
    df = pd.read_csv(latest_csv)
    df['demo_file_name'] = df['demo_file_name'].astype(str)
    for s in sharecodes:
        outcome_id = str(sharecode_to_outcomeid(s))
        filtered_list = [item for item in files_list if outcome_id in item and ".info" not in item]
        if len(filtered_list) == 1:
            row_nr = lookup_in_csv(s, column_header.steam_link, latest_csv)
            # row_nr-1 is needed due to difference in pandas data row vs row nr in actual file, as 
            # lookup uses the row of the file
            df.loc[row_nr-1, column_header.demo_file_name] = filtered_list[0]
        else:
            print(f"{colors.FAIL}Duplicates found{colors.ENDC}")
            print(f"Filtered list: {filtered_list}")
            print(f"Sharecode: {s}")
    df.to_csv(csvs_file_path + "/" + new_csv_file_name, index=False)

def get_duplicate_ids(filepath):
    # Read the first column (IDs)
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        ids = [row[0] for row in reader]

    # Count occurrences of each ID
    id_counts = Counter(ids)

    # Find duplicates
    duplicates = [id for id, count in id_counts.items() if count > 1]

    if duplicates:
        print("Duplicate IDs found:", duplicates)
    else:
        print("No duplicate IDs found.")

def remove_duplicate_ids(in_filepath:str, out_filepath:str):

    # Track seen IDs to filter duplicates
    seen_ids = set()

    with open(in_filepath, 'r') as infile, open(out_filepath, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if row[0] not in seen_ids:
                writer.writerow(row)  # Write only unique rows
                seen_ids.add(row[0])

    print(f"Duplicates removed. Output saved to {out_filepath}")
