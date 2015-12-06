import os
import re
import wikipedia as wiki
from urllib2 import urlopen
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from math import log


def tokenize(review, remove_stopwords = True ):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    # 1. Remove non-letters
    review_text = re.sub("[^a-zA-Z]"," ", review)
    # 2. Convert words to lower case and split them
    words = review_text.lower().split()
    # 3. Optionally remove stop words (true by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    # 5. Return a list of words
    return words

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_keyword_from_url_topic(url_topic):
    # Topic includes: Earth Science, Life Science, Physical Science, Biology, Chemestry and Physics
    lst_url = []
    html = urlopen(url_topic).read()
    soup = BeautifulSoup(html, 'html.parser')
    for tag_h3 in soup.find_all('h3'):
        url_res =  ' '.join(tag_h3.li.a.get('href').strip('/').split('/')[-1].split('-'))
        lst_url.append(url_res)
    return lst_url


def get_save_wiki_docs(keywords, save_folder = 'data/wiki_data/'):
    
    ensure_dir(save_folder)
    
    n_total = len(keywords)
    for i, kw in enumerate(keywords):
        kw = kw.lower()
        print i, n_total, i * 1.0 / n_total, kw
        try:
            content = wiki.page(kw).content.encode('ascii', 'ignore')
        except wiki.exceptions.DisambiguationError as e:
            print 'DisambiguationError', kw
        except:
            print 'Error', kw
        if not content:
            continue
        with open(os.path.join(save_folder, '_'.join(kw.split()) + '.txt'), 'w') as f:
                f.write(content)

        
        
def get_docstf_idf(dir_data):
    """ indexing wiki pages:
    returns {document1:{word1:tf, word2:tf ...}, ....},
            {word1: idf, word2:idf, ...}"""
    docs_tf = {}
    idf = {}
    vocab = set()

    for fname in os.listdir(dir_data):
        dd = {}
        total_w = 0
        path = os.path.join(dir_data, fname)
        for index, line in enumerate(open(path)):
            lst = tokenize(line)
            for word in lst:
                vocab.add(word)
                dd.setdefault(word, 0)
                dd[word] += 1
                total_w += 1 
        
        for k, v in dd.iteritems(): 
            dd[k] = 1.* v / total_w
        
        docs_tf[fname] = dd
    
    for w in list(vocab):
        docs_with_w = 0
        for path, doc_tf in docs_tf.iteritems():
            if w in doc_tf:
                docs_with_w += 1
        idf[w] = log(len(docs_tf)/docs_with_w)

    return docs_tf, idf


def get_docs_importance_for_question(question, dosc_tf, word_idf, max_docs = None):
    question_words = set(tokenize(question))
    #go through each article
    doc_importance = []

    for doc, doc_tf in dosc_tf.iteritems():
        doc_imp = 0
        for w in question_words:
            if w in doc_tf:
                doc_imp += doc_tf[w]  * word_idf[w]
        doc_importance.append((doc, doc_imp))
    
    #sort doc importance    
    doc_importance = sorted(doc_importance, key=lambda x: x[1], reverse = True)
    if max_docs:
        return doc_importance[:max_docs]
    else:
        return doc_importance
