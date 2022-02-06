import mysql.connector
import nltk
import sklearn
import json
import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from xml.dom import minidom

#connect to database
mydb = mysql.connector.connect(host='localhost', user='root', password='', database='news')
mycursor = mydb.cursor()

mycursor.execute("SELECT url, article FROM articles")
all_articles = mycursor.fetchall()

#read json file 
with open('json_pos_tags.json') as json_file:
    postaged_articles = json.load(json_file)

tfidf_transformer=TfidfTransformer()
count_vector = CountVectorizer()
lemmatizer = WordNetLemmatizer()
#list with closed class categories tags
closed_class_categories = ['CD', 'CC', 'DT', 'EX', 'IN', 'LS', 'MD', 'PDT', 'POS', 'PRP', 'PRP$', 'RP', 'TO', 'UH', 'WDT', 'WP', 'WP$', 'WRB']
text = []
all_clear_articles = []
#, ',', "''", '.', '``', ':', '-', '—', '/'

#for loop for all the articles of the database
for article in all_articles:

  #get the pos-tagged words from the json file by url 
  pos_tagged_words = postaged_articles[article[0]]

  #for every cell in pos_tagged_words check the pos tag
  for word in pos_tagged_words:

    #if tag is not in closed class categories then lemmatize the word and then add it to a list
    if word[1] not in closed_class_categories:
        open_class_word = lemmatizer.lemmatize(word[0])
        text.append(open_class_word)

  #from the list with the lemmatized words, create the text
  semi_final_text = ' '.join(map(str, text))

  #a final removal of punc
  final_text = (re.sub(r'[^\w\s]', '', semi_final_text)).replace("  ", " ").replace(" s ", " ").replace(" A ", " ").replace(" t ", " ")

  #add the clear text of the article in a list
  all_clear_articles.append(final_text)
  
  #clear the list with the lemmatized words
  text.clear()

#count vector and TF-IDF
c_vect = count_vector.fit_transform(all_clear_articles)
tfidf = tfidf_transformer.fit_transform(c_vect)
doc_vectors = tfidf.toarray()

#PARSE TO XML
root = minidom.Document()

#root object
xml = root.createElement('inverted_index') 
root.appendChild(xml)


for index, bla in enumerate(doc_vectors.T):
  #insert lemma to xml as child to inverted_index
  lemma = root.createElement('lemma')
  lemma.setAttribute('name', count_vector.get_feature_names()[index])
  
  xml.appendChild(lemma)
  for docId, weight in enumerate(bla):
    #insert document to xml as child to lemma
    if weight>0:
      documentchild = root.createElement('document')
      documentchild.setAttribute('id', str(docId))
      documentchild.setAttribute('weight', str(weight))
      
      lemma.appendChild(documentchild)


#save xml file
xml_str = root.toprettyxml() 

save_path_file = "inverted.xml"
  
with open(save_path_file, "w", encoding="utf-8") as f:
    f.write(xml_str) 

