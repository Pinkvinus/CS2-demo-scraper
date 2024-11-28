from utils import csv_utils


demos_path = "C:/Users/Gert/Desktop/demos"
csv_file_path = "C:/Users/Gert/repos/CS2-demo-scraper/scraping"
lines = []
with open('sharecodes.txt', 'r') as file:
    for line in file:
        lines.append(line.strip())
    file.close()

csv_utils.add_filename_to_csv(lines, demos_path, csv_file_path)