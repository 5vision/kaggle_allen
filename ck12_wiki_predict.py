import argparse
import utils
import numpy as np
import pandas as pd

#urls  to get toppics
ck12_url_topic = ['https://www.ck12.org/earth-science/', 'http://www.ck12.org/life-science/', 
                  'http://www.ck12.org/physical-science/', 'http://www.ck12.org/biology/', 
                  'http://www.ck12.org/chemistry/', 'http://www.ck12.org/physics/']
wiki_docs_dir = 'data/wiki_data'


def get_wiki_docs():
    # get keywords 
    ck12_keywords = set()
    for url_topic in ck12_url_topic:
        keywords= utils.get_keyword_from_url_topic(url_topic)
        for kw in keywords:
            ck12_keywords.add(kw)
    
    #get and save wiki docs
    utils.get_save_wiki_docs(ck12_keywords, wiki_docs_dir)


def predict(data, docs_per_q):  
    #index docs
    docs_tf, words_idf = utils.get_docstf_idf(wiki_docs_dir)
    
    res = []

    for index, row in data.iterrows():
        #get answers words
        w_A = set(utils.tokenize(row['answerA']))
        w_B = set(utils.tokenize(row['answerB']))
        w_C = set(utils.tokenize(row['answerC']))
        w_D = set(utils.tokenize(row['answerD']))
    
        sc_A = 0
        sc_B = 0
        sc_C = 0
        sc_D = 0
    
        q = row['question']
        
        for d in zip(*utils.get_docs_importance_for_question(q, docs_tf, words_idf, docs_per_q))[0]:
            for w in w_A:
                if w in docs_tf[d]:
                    sc_A += 1. * docs_tf[d][w] * words_idf[w]
            for w in w_B:
                if w in docs_tf[d]:
                    sc_B += 1. * docs_tf[d][w] * words_idf[w]
            for w in w_C:
                if w in docs_tf[d]:
                    sc_C += 1. * docs_tf[d][w] * words_idf[w]
            for w in w_D:
                if w in docs_tf[d]:
                    sc_D += 1. * docs_tf[d][w] * words_idf[w]

        res.append(['A','B','C','D'][np.argmax([sc_A, sc_B, sc_C, sc_D])])
        
    return res

if __name__ == '__main__':
    #parsing input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--fname', type=str, default='validation_set.tsv', help='file name with data')
    parser.add_argument('--docs_per_q', type=int, default= 10, help='number of docs to consider when ranking quesitons')
    parser.add_argument('--get_data', type=int, default= 0, help='flag to get wiki data for IR')
    args = parser.parse_args()
    
    if args.get_data:
        get_wiki_docs()
    
    #read data
    data = pd.read_csv('data/' + args.fname, sep = '\t' )
    #predict
    res = main(data, args.docs_per_q)
    #save result
    pd.DataFrame({'id': list(data['id']), 'correctAnswer': res})[['id', 'correctAnswer']].to_csv("prediction.csv", index = False)
    


    
        
        
         
    
    
    
