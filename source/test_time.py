import xml.dom.minidom
import mysql.connector
import collections, functools, operator
import time
import random

mydb = mysql.connector.connect(host='localhost', user='root', password='', database='news')
mycursor = mydb.cursor()

mycursor.execute("SELECT url FROM articles")
all_articles = mycursor.fetchall()

inverted_index = xml.dom.minidom.parse("inverted.xml")
lemmas = inverted_index.getElementsByTagName("lemma")

def Convert(string):
    li = list(string.split(" "))
    return li

words = []
for i in range(lemmas.length):
            words.append(lemmas[i].attributes['name'].value)

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
final_time = 0.0
search_words = []

#function that gets a list of words, uses the find_urls function and prints the urls in correct order
def test (searching_words):
    list_of_results = find_urls(searching_words)

    result = dict(functools.reduce(operator.add,
            map(collections.Counter, list_of_results)))

    d_view = [(v,k) for k,v in result.items()]
    d_view.sort(reverse=True) # natively sort tuples by first element
    for v,k in d_view:
        print ("%s: %f" % (k,v))


#TEST CASES
'''
for i in range (20):
    x = random.randint(0, lemmas.length - 1)
    search_words.append(words[x])

    start = time.time()

    test(search_words)

    end = time.time()
    final_time = final_time + (end - start)
'''
'''
for i in range (20):
    x = random.randint(0, lemmas.length - 1)
    y = random.randint(0, lemmas.length - 1)
    search_words.append(words[x])
    search_words.append(words[y])

    start = time.time()

    test(search_words)

    end = time.time()
    final_time = final_time + (end - start)
'''
'''
for i in range (30):
    x = random.randint(0, lemmas.length - 1)
    y = random.randint(0, lemmas.length - 1)
    z = random.randint(0, lemmas.length - 1)
    search_words.append(words[x])
    search_words.append(words[y])
    search_words.append(words[z])

    start = time.time()

    test(search_words)

    end = time.time()
    final_time = final_time + (end - start)
'''
'''
for i in range (30):
    x = random.randint(0, lemmas.length - 1)
    y = random.randint(0, lemmas.length - 1)
    z = random.randint(0, lemmas.length - 1)
    t = random.randint(0, lemmas.length - 1)
    search_words.append(words[x])
    search_words.append(words[y])
    search_words.append(words[z])
    search_words.append(words[t])

    start = time.time()

    test(search_words)

    end = time.time()
    final_time = final_time + (end - start)
'''

print(final_time)
