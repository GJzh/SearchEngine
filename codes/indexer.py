from __future__ import division
from bs4 import BeautifulSoup, Comment
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from urlparse import urljoin
#import math
import numpy as np
import json
import time
import types
global DocumentNum
global df_max
global df_min
global df_max_term
global df_min_term
global tfidf_max
global tfidf_min

def get_json(indexFile):
	with open(indexFile) as handle:
		return json.load(handle)

def indexer():
    global df_max
    global df_min
    global df_max_term
    global df_min_term
    global tfidf_max
    global tfidf_min
    global DocumentNum
    global running_time
    df_max = 0
    df_min = 37500
    df_max_term = []
    df_min_term = []
    tfidf_max = 0
    tfidf_min = 10000
    DocumentNum=0
    print("Indexing!")
    filePathBase = "/Users/GJzh/Downloads/WEBPAGES_RAW/"
    Index = {}
    global res
    res=[]
    MapFile = "/Users/GJzh/Google Drive/CS221/Projects/Project3/WEBPAGES_RAW/bookkeeping.json"
    hash = get_json(MapFile)
    documentkey = {}
    for i in range(75):
        fileName1 = '%d' %i
        if i<=73:
            N=500
        else:
            N=497
        for j in range(N):
            fileName2 = '%d' %j
            document = fileName1 + '/' + fileName2
            filePath = filePathBase + fileName1 + '/' + fileName2
            print(filePath)
            res.append(filePath)
            # process web page content
            with open(filePath) as f:
                duplication = False
                soup = BeautifulSoup(f.read(),"lxml")
                if soup.head is not None:
                    text = soup.head.findAll(text=True)
                    visible_text = filter(visible, text)
                    visible_text = [term.string.encode('utf-8') for term in visible_text]
                    head_terms = termProcessing(visible_text)
                    headKey = ""
                    for term in head_terms:
                        headKey += (term + " ")
                    if len(headKey)>0 and headKey in documentkey:
                        duplication = True
                        continue
                    DocumentNum += 1
                    documentkey[headKey] = document
                    res.append(head_terms)
                    for k in range(len(head_terms)):
                        term = head_terms[k]
                        if term not in Index:
                            # a new term
                            Index[term] = {}
                            Index[term][document]={'tf': 0,'tf-idf': 0, 'head': [], 'body': [], 'link': [0,0]}
                        elif document not in Index[term]:
                            #an existing term but not the first occurance in the current document
                            Index[term][document]={'tf': 0,'tf-idf': 0, 'head': [], 'body': [], 'link': [0,0]}
                        Index[term][document]['tf']+=1
                        Index[term][document]['head'].append(k)
                if soup.body is not None and not duplication:
                    text = soup.body.findAll(text=True)
                    visible_text = filter(visible, text)
                    visible_text = [term.string.encode('utf-8') for term in visible_text]
                    body_terms = termProcessing(visible_text)
                    res.append(body_terms)
                    for k in range(len(body_terms)):
                        term = body_terms[k]
                        if term not in Index:
                            #a new term
                            Index[term]={}
                            Index[term][document]={'tf': 0,'tf-idf': 0, 'head': [], 'body': [], 'link': [0,0]}
                        elif document not in Index[term]:
                            #an existing term but not the first occurance in the current document
                            Index[term][document]={'tf': 0,'tf-idf': 0, 'head': [], 'body': [], 'link': [0,0]}
                        Index[term][document]['tf']+=1
                        Index[term][document]['body'].append(k)
                # process the urls
                if not duplication:
                    baseUrl = hash[document.decode('utf-8')].encode('utf-8')
                    urls = []
                    urls.append(baseUrl)
                    for link in soup.find_all('a'):
                        if 'href' in link.attrs:
                            newurl = link.attrs['href']
                            # relative url changes to absolution url
                            if newurl.startswith('/'):
                                newurl = urljoin(baseUrl, newurl)
                            urls.append(newurl.encode('utf-8'))
                    url_terms = termProcessing(urls)
                    res.append(url_terms)
                    for k in range(len(url_terms)):
                        term = url_terms[k]
                        if type(term) is not types.StringType:
                            z=input()
                        if term not in Index:
                            # a new term
                            Index[term] = {}
                            Index[term][document] = {'tf': 0, 'tf-idf': 0, 'head': [], 'body': [], 'link': [0,0]}
                        elif document not in Index[term]:
                            # an existing term but not the first occurance in the current document
                            Index[term][document] = {'tf': 0, 'tf-idf': 0, 'head': [], 'body': [], 'link': [0,0]}
                        if k==0:
                            Index[term][document]['link'][0] += 1
                        else:
                            Index[term][document]['link'][1] += 1
    for term in Index:
        df = len(Index[term])
        #update df_max, df_min, df_max_term, df_min_term
        if df>df_max:
            df_max=df
            df_max_term=[term]
        elif df==df_max:
            df_max_term.append(term)
        if df<df_min:
            df_min=df
            df_min_term=[term]
        elif df==df_min:
            df_min_term.append(term)
        for document in Index[term]:
            tf = Index[term][document]['tf']
            Index[term][document]['tf-idf']=calculate_Tfidf(tf,df)
            # update tfidf_max, tfidf_min
            tfidf_max = np.maximum(Index[term][document]['tf-idf'],tfidf_max)
            tfidf_min = np.minimum(Index[term][document]['tf-idf'], tfidf_min)
    #compression(Index)
    Index = sorted(Index.iteritems(), key=lambda d:d[0])
    return Index

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'meta']:
        return False
    elif isinstance(element, Comment):
        return False
    return True

def get_stem(content):
    stemmer = SnowballStemmer('english')
    for k in range(len(content)):
        content[k] = stemmer.stem(content[k]).encode('utf-8')
    #return [stemmer.stem(term).encode('utf-8') for term in content]

def isstopwords(word):
    sw = set(stopwords.words('english'))
    if word in sw:
        return True
    else:
        return False

def termProcessing(content):
    terms = []
    word=""
    for i in range(len(content)):
        if len(word)>=3 and len(word)<=15 and not isstopwords(word):
            terms.append(word.lower())
        word = ""
        for j in range(len(content[i])):
            #if content[i][j].isalpha() or content[i][j].isdigit() or (content[i][j]=='-' and len(word)>0):
            if content[i][j].isalpha() or content[i][j].isdigit():
                word += content[i][j]
            else:
                if len(word)>=3 and len(word)<=15 and not isstopwords(word):
                    terms.append(word.lower())
                word=""
    if len(word) >= 3 and len(word) <= 15 and not isstopwords(word):
        terms.append(word.lower())
    get_stem(terms)
    return terms
def calculate_Tfidf(tf,df):
    #N=500*75-3
    N=DocumentNum
    if tf==0 or df==0:
        return 0
    else:
        return (1+np.log10(tf))*(np.log10(N/df))

def compression(Index):
    for term in Index:
        for document in Index[term]:
            l1=len(Index[term][document]['head'])
            l2=len(Index[term][document]['body'])
            if l1>1:
                for i in range(l1-1,0,-1):
                    Index[term][document]['head'][i]-=Index[term][document]['head'][i-1]
            if l2>1:
                for j in range(l2-1,0,-1):
                    Index[term][document]['body'][j]-=Index[term][document]['body'][j-1]

def save_data(indexdict):
    global df_max
    global df_min
    global df_max_term
    global df_min_term
    global tfidf_max
    global tfidf_min
    global DocumentNum
    global running_time
    #with open('/Users/GJzh/Desktop/JunGuo/indexer.json', 'w') as outfile:
    #    outfile.write(json.dumps(indexdict))
    initial = '---'
    cur=[]
    for term in indexdict:
        if len(term[0])>2:
            if (term[0][0]+term[0][1]+term[0][2])!=initial:
                if len(cur)>0:
                    with open('/Users/GJzh/Desktop/JunGuo/results/'+initial[0]+'/'+initial[1]+'/'+initial[2]+'.json', 'w') as outfile:
                        outfile.write(json.dumps(cur))
                initial=term[0][0]+term[0][1]+term[0][2]
                cur=[]
            cur.append(term)
        else:
            if not (term[0][0].isalpha() or term[0][0].isdigit()):
                print('problem')
                z = input()
            with open('/Users/GJzh/Desktop/JunGuo/results/' + term[0] + '.json', 'w') as outfile:
                outfile.write(json.dumps([term]))
    if len(cur) > 0:
        with open('/Users/GJzh/Desktop/JunGuo/results/' + initial[0] + '/' + initial[1] + '/' + initial[2] + '.json', 'w') as outfile:
            outfile.write(json.dumps(cur))
    with open('StatisticData', 'w') as test:
        print>> test, "df_max:", df_max, "\n"
        print>> test, "df_min:", df_min, "\n"
        print>> test, "df_max_term:", df_max_term, "\n"
        print>> test, "df_min_term:", df_min_term, "\n"
        print>> test, "tfidf_max:", tfidf_max, "\n"
        print>> test, "tfidf_min:", tfidf_min, "\n"
        print>> test, "DocumentNum:", DocumentNum, "\n"
        print>> test, "running time:", running_time, "\n"

global res
global running_time
start_time = time.time()
Index=indexer()
end_time = time.time()
running_time = end_time-start_time
print "Indexing ended after %.2f seconds." %(running_time)
print("The number of unique words (after tokenizing) is %d" %(len(Index)))
print("Saving results...")
save_data(Index)
with open('filetext','w') as test:
    for i in range(len(res)):
        print>>test, res[i]

