import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        DONid = "DON-" + url.split('/')[-1]
        headline = soup.find('h1', class_='don-title').text.strip()
        date = soup.find('span', class_='timestamp').text.strip()

        parts = None
        if ' - ' in headline:
            parts = headline.split(' - ')
        elif ' – ' in headline:
            parts = headline.split(' – ')

        if parts:
            disease = parts[0].strip()
            country = parts[1].strip()
        else:
            disease = headline.strip()
            country = headline.strip()



        print(disease)

        return [DONid, headline, date, url, disease, country]
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')
        return None

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds_path = '/Users/donovandooley/Downloads/who-disease-outbreak-data-1b884301c981.json'

creds = Credentials.from_service_account_file(creds_path, scopes=scope)
client = gspread.authorize(creds)


# Open the Google Sheet
try:
    sheet = client.open("WHODONdatabase2022-2024").sheet1
    print("Spreadsheet opened successfully.")
except gspread.SpreadsheetNotFound:
    print("Spreadsheet not found. Please check the name and sharing settings.")
    exit()

# URLs to scrape
urls = [
    'https://www.who.int/emergencies/disease-outbreak-news/item/04-january-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/04-January-2019-hantavirus-panama-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/08-january-2019-poliovirus-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/09-january-2019-yellow-fever-nigeria-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/10-january-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/16-january-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/17-january-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/17-january-2019-measles-madagascar-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/23-January-2019-hantavirus-argentina-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/23-January-2019-hantavirus-argentina-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/24-january-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/25-january-2019-polio-mozambique-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/30-january-2019-gonococcal-infection-uk-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/31-january-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/4-february-2019-dengue-jamaica-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-february-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/11-february-2019-mers-oman-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/11-february-2019-yellow-fever-brazil-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/14-february-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/14-february-2019-lassa-fever-nigeria-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/15-february-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/20-February-2019-polio-png-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/21-february-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/26-february-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/27-february-2019-polio-indonesia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/28-february-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/04-march-2019-mers-oman-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/5-march-2019-carbapenem-resistant-p-aeruginosa-mex-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/5-march-2019-carbapenem-resistant-p-aeruginosa-mex-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/7-march-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/14-march-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/21-march-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/28-march-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/29-march-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/04-april-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/11-april-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/18-april-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/18-april-2019-yellow-fever-brazil-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/24-April-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/25-april-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/01-may-2019-chikungunya-congo-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/02-may-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/06-may-2019-measles-euro-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/07-may-2019-measles-western-pacific-region-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/09-may-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/09-may-2019-measles-tunisia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/09-may-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/13-may-2019-rift-valley-fever-mayotte-france-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/16-may-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/16-may-2019-monkeypox-singapore-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/17-may-2019-mers-saudi-arabia-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/20-may-2019-dengue-reunion-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/23-may-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/24-may-2019-wild-polio-virus-islamic-republic-of-iran-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/30-may-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/06-june-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/06-june-2019-polio-cameroon-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/13-june-2019-ebola-drc-en/',
    'https://www.who.int/emergencies/disease-outbreak-news/item/13-june-2019-ebola-uganda-en/'
]

for url in urls:
    data = scrape_data(url)
    if data:
        sheet.append_row(data)
        print(f"Data from {url} added successfully.")
    else:
        print(f"Failed to add data from {url}.")

