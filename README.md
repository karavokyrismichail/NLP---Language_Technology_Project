# NLP --- Language_Technology_Project

Project for Language Technology Course of the Department of Computer Engineering & Informatics.

## Description 

Python Scripts that crawl news from online newspapers, clear and vectorize the texts in order to create an inverted xml file for searching articles using key words.

## Scripts

#### crawler
- Crawls news that appear in frontpage of online newspapers (nbc, ifls) and save the articles in database.

#### pos_tagging

- Tokenizes each article from database and then finds pos-tag for every token. 
- Saves the pos-tagged articles in json file.

#### create_inverted_index
- Reads the json file with the pos-tags.
- Removes closed_class_category tags.
- Lemmatizes open_class_category tags.
- Joins the lemmatized words of each article and removes punctuation.
- Vectorizes the articles and calculates the TF-IDF value of each word.
- Creates an inverted xml file for future article searching.

#### queries_test

- Given one or more words returns in right order the URLs of most relative articles.

#### test_time

- Does queries automatically to calculate response time.

## Tech stack

- Python, VSC, XAMPP, MySQL, NLTK, scikit-learn, Beautiful Soup
