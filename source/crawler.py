import urllib.request 
from bs4 import BeautifulSoup
import mysql.connector

#connect to mysql database
mydb = mysql.connector.connect(host='localhost', user='root', password='', database='news')
mycursor = mydb.cursor()

#function for inserting articles into database with their url and their title
def insert_into_database(url, title, text):
    sql = "INSERT IGNORE INTO articles (url, title, article) VALUES (%s, %s, %s)"
    val = (url, title, text)
    mycursor.execute(sql, val)
    mydb.commit()

#function for getting the urls of the articles from the nbc online newspaper
def nbc_get_urls(url):
    list = []
    html = urllib.request.urlopen(url)
    htmlParse = BeautifulSoup(html, 'html.parser')
    for href in htmlParse.find_all("a", class_="wide-tease-item__image-wrapper flex-none relative dn dt-m"):
        list.append((href['href']))
    return list

#function for getting the urls of the articles from the ifls online scientific newspaper
def ifls_get_urls(url):
    list = []
    html = urllib.request.urlopen(url)
    htmlParse = BeautifulSoup(html, 'html.parser')
    for href in htmlParse.find_all("a", class_="article-link"):
        if len(list) <= 10:
            list.append((href['href']))
    return list

#get the nbc urls for the articles
urls1 = nbc_get_urls("https://www.nbcnews.com/world")

#list that we will use later to append every paragraph of each article
text1 = []

#for every url from nbc articles, get the text and the title. Then store url, title and text into database
for url in urls1:
    html = urllib.request.urlopen(url)
    htmlParse = BeautifulSoup(html, 'html.parser')
    #get the paragraphs of the article
    for para in htmlParse.find_all("div", class_="article-body__content"):
        #insert paragraph into the list
        text1.append(para.get_text())
    #get the title of the article
    for title in htmlParse.find_all("div", class_="article-hero-headline layout-grid-item grid-col-10-l"):
        title1 = (title.get_text())
    
    #add the paragraphs of the list to make text
    listToStr1 = ' '.join(map(str, text1))
    #clear list
    text1.clear()
    #insert into database
    insert_into_database(url, title1, listToStr1)


#get the ifls urls for the articles
urls2 = ifls_get_urls("https://www.iflscience.com/")

#for every url from ifls articles, get the text and the title. Then store url, title and text into database
for url in urls2:
    html = urllib.request.urlopen(url)
    htmlParse = BeautifulSoup(html, 'html.parser')
    #get the text of the article
    for para in htmlParse.find_all("div", class_ = "article-content"):
        text2 = (para.get_text()).strip()
    #get the title of the article
    for title in htmlParse.find_all("h1", class_ = "title"):
        title2 = (title.get_text())
    #insert into database
    insert_into_database(url, title2, text2)




'''
text1 = []
url = "https://www.bbc.com/news/world-asia-60007119"

html = urllib.request.urlopen(url)
htmlParse = BeautifulSoup(html, 'html.parser')

for para in htmlParse.find_all("div", class_="ssrcss-uf6wea-RichTextComponentWrapper e1xue1i85"):
    text1.append(para.get_text())
listToStr = ' '.join(map(str, text1))
print(listToStr)
'''

'''
text1 = []
url = "https://www.bbc.com/news"

html = urllib.request.urlopen(url)
htmlParse = BeautifulSoup(html, 'html.parser')

for href in htmlParse.find_all("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"):
    url = href['href']
    print(url)
'''