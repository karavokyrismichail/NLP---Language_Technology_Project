import sklearn
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.svm import LinearSVC
import nltk.stem
from scipy import spatial
from sklearn.metrics import jaccard_score
from nltk.corpus import stopwords
import numpy as np

#fetch the 20newsgroups with sklearn
E = fetch_20newsgroups(subset = 'train', remove = ('headers','footers','quotes'))
A = fetch_20newsgroups(subset = 'test', remove = ('headers','footers','quotes'))

#stemmer to steme the words of the train and test data
english_stemmer = SnowballStemmer('english', ignore_stopwords=True)
punctuations="?:!.,;/''-—``><#&@[]|"
#train data
X_train = E.data
y_train = E.target

#test data
X_test = A.data
y_test = A.target

#a function that gets a list of texts and stemms each word of the text. At the end it returns the same list but the texts have only the stemmed words
def stemm_data(data_list):
    stemmed_words_list = []
    final_list = []
    for text in data_list:
        #tokenize list to get every single word
        tokenized_text =  nltk.word_tokenize(text)
        for word in tokenized_text:
            #remove punctuations
            if word in punctuations:
                pass
            elif word not in punctuations:
                stemmed_word = english_stemmer.stem(word)
                stemmed_words_list.append(stemmed_word)
        final_text = ' '.join(map(str, stemmed_words_list))
        final_list.append(final_text)
        stemmed_words_list.clear()
    return final_list

#stem data
X_train_stemmed = stemm_data(X_train)
X_test_stemmed = stemm_data(X_test)

#print(X_train_stemmed)
#get TF-IDF weights of the stemmed data
tfidf_vect = TfidfVectorizer()
tfidf_vect.fit(X_train_stemmed)
X_train_tfidf_vect = tfidf_vect.transform(X_train_stemmed)
X_test_tfidf_vect = tfidf_vect.transform(X_test_stemmed)

#Text classification with Linear SVM
scv_classification = LinearSVC()
scv_classification.fit(X_train_tfidf_vect,y_train)
pred = scv_classification.predict(X_test_tfidf_vect)
print('Cosine Similarity : ', 1 - spatial.distance.cosine(pred, y_test))
print('jaccard Similarity : ', jaccard_score(pred, y_test, average='macro'))