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
    sheet = client.open('WHODONdatabase2022-2024').sheet1
    print("Spreadsheet opened successfully.")
except gspread.SpreadsheetNotFound:
    print("Spreadsheet not found. Please check the name and sharing settings.")
    exit()

# URLs to scrape
urls = [
    'https://www.who.int/emergencies/disease-outbreak-news/item/2024-DON518',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2023-DON498',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2023-DON491',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2023-DON481',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2023-DON475',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2023-DON448',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON424',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON414',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON412',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON401',
    'https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON387',
    'https://www.who.int/emergencies/disease-outbreak-news/item/dengue---timor-leste'
]

for url in urls:
    data = scrape_data(url)
    if data:
        sheet.append_row(data)
        print(f"Data from {url} added successfully.")
    else:
        print(f"Failed to add data from {url}.")
