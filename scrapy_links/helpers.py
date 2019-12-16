''' Helper functions and Calsses'''
import csv
import os
from pathlib import Path

# default path - cwd and file name is urls.csv
path = os.path.dirname(os.path.abspath(__file__))
csv_file_name='urls.csv'
ful_path = Path(path, csv_file_name)

# Import urls from csv file
def get_urls_fm_csv(ful_path=ful_path):
    '''Get Url list from csv file. Return list'''
    url_list = []
    if os.path.exists(ful_path):
        with open(ful_path, 'r') as f:
            for line in f.readlines():
                url_list.append(line.strip())
        return url_list
    else: 
        return None


if __name__ == "__main__":
    urls = get_urls_fm_csv()
    print(urls)