import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_gtfs_table(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    feed_urls = ["https://gtfs.pro" + header.find('a').get('href') for header in soup.find_all('td') if header.find('a')]

    df['feed_url'] = feed_urls
    df['expired'] = df['Feed Name'].apply(lambda x: x.endswith('*'))
    df['Feed Name'] = df['Feed Name'].str.replace('*', '').str.strip()

    return df

def get_download_url(row: pd.Series):
    response = requests.get(row['feed_url'])
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.select('div.block-download-links--highlighted a')
    for l in link:
        href = l.get('href')
        if 's3.gtfs.pro' in href:
            return href
    return None

df = get_gtfs_table('https://gtfs.pro/en/spain')
df['download_url'] = df.apply(get_download_url, axis=1)

df.to_csv("sources.csv", index=False)

# for url in df['feed_url']:
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # link = soup.find('div', _class="block-download-links--highlighted")
#     # print(url, link)
#     link = soup.select('div.block-download-links--highlighted a')
#     for l in link:
#         href = l.get('href')
#         if 's3.gtfs.pro' in href:
#             link = href
#             break
#     else:
#         link = None
#     print(url, link)