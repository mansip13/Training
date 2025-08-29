from bs4 import BeautifulSoup
import requests
import pandas as pd
import pendulum
import csv
import json

'''
#setting up url of the site to scrape 
url = "https://www.bbc.com/news"
response = requests.get(url)
#printing status code of the request
print(response.status_code)
#show first n specified(500 here) characters of the web page 
#text= BeautifulSoup(response.text[:1000])
#print(text.prettify())

soup=BeautifulSoup(response.content,"html.parser")
#print(soup.prettify())

#finding headlines 
headline= soup.find("h2")
#print(headline.get_text())

#getting all headlines 
headlines= soup.find_all("h2")
#print([h.get_text() for h in headlines[:10]])


#extracting news articles via href tag and storing the title and link to the article 
news_data =[]

for h in soup.find_all("h2"):
    a_tag = h.find("a")  # find the <a> inside <h2>
    if a_tag:
        text = a_tag.get_text(strip=True)
        link = a_tag.get("href")

        if text and link and ("/news/" in link or link.startswith("http")):
            if link.startswith("/"):
                link = "https://www.bbc.com" + link

            news_data.append({
                "title": text,
                "Link": link,
                "Scraped_At": pendulum.now().format("DD-MM-YYYY HH:mm:ss")
            })
        
        
print(news_data)

#structuring the data : clean data and create its dictionary, add timestamps, use pandas 
df=pandas.DataFrame(news_data)

pandas.set_option('display.max.rows',200)
print(df.head(150))

df.to_csv("bbc_headlines.csv",index=False,encoding="utf-8")
df.to_json("bbc_headlines.json",orient="records",indent=4)
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pendulum

url = "https://www.bbc.com/news"
response = requests.get(url)
print("Status code:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

news_data = []

# Find ALL links on page
for a_tag in soup.find_all("a", href=True):
    text = a_tag.get_text(strip=True)
    link = a_tag["href"]

    # Keep only real news articles
    if text and "/news/" in link:
        # Fix relative URLs
        if link.startswith("/"):
            link = "https://www.bbc.com" + link

        news_data.append({
            "title": text,
            "Link": link,
            "Scraped_At": pendulum.now().format("DD-MM-YYYY HH:mm:ss")
        })

# Remove duplicates
df = pd.DataFrame(news_data).drop_duplicates(subset=["Link"])

pd.set_option('display.max.rows', 200)
print(df.head(100))

# Save to CSV + JSON
#df.to_csv("bbc_headlines.csv", index=False, encoding="utf-8")
#df.to_json("bbc_headlines.json", orient="records", indent=4)
