from bs4 import BeautifulSoup
import requests
''' 
with open("index.html","r") as file:
    doc =BeautifulSoup(file,"html.parser")
   
#Print whole html in formatted way     
print(doc.prettify())

#search content by tag
tag=doc.title 
print(tag)

#search content by tag and get just the content, not the tag
tag=doc.title 
print(tag.string)

#replacing the tag content
tag.string="hello"
print(tag)

#finding the first instance of the searched tag 
tags1=doc.find("p")
print(tags1)

#finding all instances of the tag
tags1=doc.find_all("p")
print(tags1)


#requests

url ="https://webscraper.io/test-sites/e-commerce/scroll/product/82"
result = requests.get(url)
doc = BeautifulSoup(result.text)
print(doc.prettify())
'''
#searching and filetering 

with open("index2.html","r") as f:
    doc = BeautifulSoup(f,"html.parser")

tag = doc.find("option")
tag['value']='new value'
tags= doc.find_all(["p","div","li"])
print(tags)