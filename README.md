# SearchEngine
UCI CS221 Project Search Engine
This is a Search Engine I designed with my teammate Zhen Chen in the winter quarter 2017. 
Goal: Implement a complete search engine for the ICS domain. At the end of this project, 
we have a web interface that provides the user with a text box to enter queries and returns relevant results.
Milestone #1: Build an index
Using the pages that we stored by crawling the ics.uci.edu domain in the previous project, construct an index that maps words to documents (pages). We store following information into the index: (1) keywords after tokenize (stemming, stopwords, wordlength control, Capital recongize and so on); (2) the documents the ketwords appear; (3) the term frequency (tf); (4) the document frequency (df); (5) keywords locations after compression (delta encoding); (6) head or body; (7) internal url; (8) outwords urls. Note that we only focus on the urls and visible content.
A three-tier file system is used to save the index. We divide the extreme index into a great number of small files in terms of keywords' first 3 characters. This smart storage strategy greatly reduce the running time.
A relevance scoring function is designed to calculate the relevance measure for the given query and documents.
Moreover, we develop an interface to search our index that retrieves documents according to the relevance score. The logo of our search engine is googal. Similar to Google’s search engine, we return not only top-k relevant urls but also corresponding heads and snippets. To evaluate the search engine’s performance, we also show the running time.
More details about this search engine can be found in the reports (Report1, Report2, Report3).
