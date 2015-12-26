import os
import utils
import re
from bs4 import BeautifulSoup

def get_h1_text(doc):
    ''' get text between h1 tags, except:
        practice', 'questions', 'review', 'explore more', 'references '''
    doc = BeautifulSoup(doc, 'html.parser')
    doc_name = doc.find_all('title')[0].text.strip().replace("?", "")

    topics = {}
    for topic in doc.find_all('h1')[1:-1]: #ignore introduction and references
        topic_name = topic.text.strip().replace("?", "")
        content = [topic_name]
        #read all topics in doc
        for p in topic.find_next_siblings():
            #ignore all text below Summary
            if p.text.strip().lower() in ['practice', 'questions', 'review', 'explore more', 'references']:
                break
            #add
            content += p.text.split()
        topics[topic_name] = ' '.join(content)
        
    return topics

def get_h_all_text(doc):
    ''' get text between h tags, except:
        practice', 'questions', 'review', 'explore more', 'references '''
    start = []
    names = []
    regex = re.compile(r"<h[1-6].+\n.*")
    for match in regex.finditer(doc):
        h_name = re.findall(r">\n.*", match.group())[0][2:].strip()
        names.append(h_name)
        start.append(match.start())

    s = start[2] #put 2 to skip first two h
    paragraphs = {}
    for i in range(3,len(start)): #put 3 to skip first two h
        e = start[i] -1
        if names[i-1] not in ['Practice', 'Questions', 'Review', 'Explore More',
                              'Explore More I','Explore More II','Explore More III' 'References']:
            paragraphs[names[0] + "_" + str(i)] = (BeautifulSoup(doc[s:e], 'html.parser').get_text())
            
        s = e + 1
    
    return paragraphs
            
            
            
            
            
            
            