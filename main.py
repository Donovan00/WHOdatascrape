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
        disease = "Ebola"
        country = headline[headline.find('–') + 1:].strip()

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

url = 'https://www.who.int/emergencies/disease-outbreak-news/item/2022-DON377'
data = scrape_data(url)

# Add the data to the sheet
if data:
    sheet.append_row(data)
    print("Data added successfully.")
else:
    print("Failed to add data.")
