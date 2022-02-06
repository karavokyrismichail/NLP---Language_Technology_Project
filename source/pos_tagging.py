import mysql.connector
import nltk
from nltk.tokenize import word_tokenize
import json

#connect to mysql database
mydb = mysql.connector.connect(host='localhost', user='root', password='', database='news')
mycursor = mydb.cursor()

#get the urls and the texts from all articles in database
mycursor.execute("SELECT url, article FROM articles")
all_articles = mycursor.fetchall()

dict = {}
#for loop for each article
for article in all_articles:
  #get the url and the text of the article
  url = article[0]
  text = article[1]
  #tokenize the article using nltk
  tokenized_article = nltk.word_tokenize(text)
  #pos-tag the tokenized article using nltk
  pos_tag_article = nltk.pos_tag(tokenized_article)
  #add the pos tags of the article in dictionary
  dict[url] = pos_tag_article

#save the pos-tagged articles in json file for later use
with open('json_pos_tags.json', 'w') as outfile:
    json.dump(dict, outfile)


