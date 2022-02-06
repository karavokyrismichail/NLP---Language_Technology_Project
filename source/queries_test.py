import xml.dom.minidom
import mysql.connector
import collections, functools, operator
import time

#connect to database
mydb = mysql.connector.connect(host='localhost', user='root', password='', database='news')
mycursor = mydb.cursor()

#get urls of the articles from database
mycursor.execute("SELECT url FROM articles")
all_articles = mycursor.fetchall()

#load xml file
inverted_index = xml.dom.minidom.parse("inverted.xml")
lemmas = inverted_index.getElementsByTagName("lemma")

#def that gets a string and splits the words. It returns a list with the words
def Convert(string):
    li = list(string.split(" "))
    return li

print("You can enter words separated by space:")
user_input  = input()

#get the list of the words from user_input
words = Convert(user_input)

#function that gets the list of the words and returns a list with dictionaries. 
#Each dictionary contains the urls of the articles that contein the lemma and the TF-IDF values
def find_urls (li):
    list_of_dicts = []
    for word in li:
        mydict = {}
        doc_ids = []
        doc_weights = []
        for i in range(lemmas.length):
            if lemmas[i].attributes['name'].value == word:
                docs = lemmas[i].getElementsByTagName("document")
                for doc in docs:
                    doc_id = int(doc.getAttribute("id"))
                    doc_ids.append(all_articles[doc_id])
                    doc_weight = float(doc.getAttribute("weight"))
                    doc_weights.append(doc_weight)
                mydict = dict(zip(doc_ids, doc_weights))
                list_of_dicts.append(mydict)
    return list_of_dicts

start = time.time()

list_of_results = find_urls(words)

#add the values of the duplicate urls and make one dictionary with all single urls and their values
result = dict(functools.reduce(operator.add,
         map(collections.Counter, list_of_results)))

#print urls sorted by value
d_view = [(v,k) for k,v in result.items()]
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    print ("%s: %f" % (k,v))

end = time.time()
print(end - start)





        