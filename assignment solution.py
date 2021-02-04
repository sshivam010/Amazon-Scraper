from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
def get_links(base_url):
    try:
        src_url = 'https://www.amazon.in'
        links = []
        for a in main_soup.find_all("a", attrs={'class':'a-link-normal a-text-normal'}):
            links.append(src_url + a['href'])
    except:
        links=[]
    return links

# Function to extract Product Title
def get_title(soup):
     
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'}).string.strip()
 
    except AttributeError:
        title = ""   
 
    return title
 
# Function to extract Product Price
def get_price(soup):
 
    try:
        price = soup.find("span", attrs={'class':'a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P'}).string.strip()
 
    except AttributeError:
        price = ""  
 
    return price[2:]
 
# Function to extract Product Rating
def get_rating(soup):
 
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
         
    except AttributeError:
         
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = "" 
 
    return rating
 
# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
         
    except AttributeError:
        review_count = ""   
 
    return review_count
 
# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
 
    except AttributeError:
        available = ""  
 
    return available

listofdicts = list()
base_url = 'https://www.amazon.in/s?k=books&ref=nb_sb_noss_2'
page = requests.get(base_url, headers=HEADERS)
main_soup = BeautifulSoup(page.content, 'html.parser')
links = get_links(base_url)
print("Creating Output file")
for entry in links:
    temp_page = requests.get(entry, headers=HEADERS)
    soup = BeautifulSoup(temp_page.content, 'html.parser')
    td = dict()
    td['Name'] = get_title(soup)
    td['Price'] = get_price(soup)
    td['Rating'] = get_rating(soup)
    td['Review_count'] = get_review_count(soup)
    td['Availabilty'] = get_availability(soup)
    td['Link'] = entry
    listofdicts.append(td)
    time.sleep(2) #we use time.sleep to avoid getting our IP blocked  
    
df = pd.DataFrame.from_records(listofdicts)
df.to_csv("output.csv", index=False, header=True)
print("Done.")
