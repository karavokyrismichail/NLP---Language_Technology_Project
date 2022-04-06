# NLP --- Language_Technology_Project

Project for the Language Technology Course of the [Department of Computer Engineering & Informatics](https://www.ceid.upatras.gr/en).

## Description 

Python Scripts that crawl news from online newspapers, clear and vectorize the texts in order to create an inverted xml file for searching articles using key words.

## Scripts

#### crawler
- Crawls news that appear in frontpage of online newspapers ([NBC News](https://www.nbcnews.com/), [IFLS](https://www.iflscience.com/)) and save the articles in database.

#### pos_tagging

- [Tokenizes](https://www.nltk.org/api/nltk.tokenize.html) each article from database and then finds [POS-Tag](http://www.infogistics.com/tagset.html) for every token. 
- Saves the POS-Tagged articles in [json](https://fileinfo.com/extension/json) file.

#### create_inverted_index
- Reads the json file with the pos-tags.
- Removes closed_class_category tags.
- [Lemmatizes](https://www.nltk.org/_modules/nltk/stem/wordnet.html) open_class_category tags.
- Joins the lemmatized words of each article and removes punctuation.
- [Vectorizes](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) the articles and calculates the [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) value of each word.
- Creates an inverted xml file for future article searching.

#### queries_test

- Given one or more words returns in right order the URLs of most relative articles.

#### test_time

- Does queries automatically to calculate response time.

## Tech stack

- Python, VSC, XAMPP, MySQL, NLTK, scikit-learn, Beautiful Soup
