import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import datetime

# Define the URL of the page to scrape
url = "https://www.theverge.com/"

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the article headlines and their links
headlines = soup.find_all("h2", class_="c-entry-box--compact__title")

# Find all the article authors and dates
authors_and_dates = soup.find_all("div", class_="c-byline")

# Create an empty list to store the data
data = []

# Loop through the articles and extract the relevant data
for i, headline in enumerate(headlines):
    link = headline.find("a").get("href")
    title = headline.find("a").text.strip()
    author = authors_and_dates[i].find("a").text.strip()
    date = authors_and_dates[i].find("time").get("datetime")
    data.append((i+1, link, title, author, date))

# Convert the data list into a pandas DataFrame
df = pd.DataFrame(data, columns=["id", "URL", "headline", "author", "date"])

# Get the current date to use in the filename
today = datetime.date.today().strftime("%d%m%Y")

# Write the data to a CSV file
filename = today + "_verge.csv"
df.to_csv(filename, index=False)

