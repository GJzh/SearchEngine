from bs4 import BeautifulSoup
import json
from urlparse import urljoin
import requests
import copy
import numpy as np

def get_json(inFile):
	with open(inFile) as handle:
		return json.load(handle)

def save_json(filename, content):
	with open(filename, 'w') as outfile:
		outfile.write(json.dumps(content))

def buildURLgraph():
	filePathBase = "/Users/zhenchen/Documents/Courses/Information retrieval/project/project 3/WEBPAGES_RAW/"
	urlhash_old = get_json(filePathBase+'bookkeeping.json');
	urlhash_new = dict() # key: url string  value: number
	urlhash_value = 0
	url_graph = dict() # key: url node  value: list of urls which key url points to
	for i in range(75):
		fileName1 = '%d' %i
		if i <= 73: N = 500
		else: N = 497
		for j in range(N):
			fileNmae2 = '%d' %j
			filePath = filePathBase + fileName1 + '/' + fileNmae2
			url = urlhash_old[fileName1 + '/' + fileNmae2]
			if url.startswith('ftp'):
				url = 'ftp://' + url
			else:
				url = 'http://' + url
			if url not in urlhash_new:
				urlhash_new[url] = urlhash_value
				urlhash_value += 1

			urlgraph_key = urlhash_new[url]
			if urlgraph_key not in url_graph:
				urlgraph_key = urlhash_new[url]
				url_graph[urlgraph_key] = list()

			# build the URL graph
			with open(filePath) as infile:
				baseurl = url
				soup = BeautifulSoup(infile.read(), 'lxml')
				for link in soup.find_all('a'):
					if 'href' in link.attrs:
						pointurl = link.attrs['href']
						# relative url changes to absolution url
						# if pointurl.startswith('/'):
						pointurl = urljoin(baseurl, pointurl)
						# ignore the url which not starts with http ands https
						# if pointurl.startswith('http'):
						if pointurl not in urlhash_new:
							urlhash_new[pointurl] = urlhash_value
							urlhash_value += 1

						if urlhash_new[pointurl] not in url_graph[urlgraph_key]:
							url_graph[urlgraph_key].append(urlhash_new[pointurl])

	save_json('url_hash.json', urlhash_new)
	save_json('url_graph.json', url_graph)
	return urlhash_value

def PageRank(graphfile, damping, n_iterations, totallink):
	url_graph = get_json(graphfile)
	# initialize the PR, all the links' PR are 1
	PR_current = list()
	PR_previous	= list()
	for link in xrange(totallink):
		PR_current.append(1.0)
		PR_previous.append(1.0)

	for i in range(n_iterations):
		# print i, PR_current
		isbig = 0
		for link in xrange(totallink):
			pr = 0.0
			for key in url_graph:
				if link in url_graph[key]:
					pr += PR_previous[int(key)] / len(url_graph[key])

			PR_current[link] = (1 - damping) + damping * pr
			if PR_current[link] > 1000:
				isbig = 1
		if isbig:
			for link in xrange(totallink):
				PR_current[link] = PR_current[link] / 1000
		PR_previous = copy.copy(PR_current)

	
	save_json('url_PR.json', PR_current)

def assignPR(urlhashname, urlPRname, dictname):
	url_hash = get_json(urlhashname)
	url_PR = get_json(urlPRname)
	url_dict = get_json(dictname)
	reverse_url_dict = {v:k for k,v in url_dict.items()}
	fullurl_PR = dict()
	for key in url_hash:
		fullurl_PR[key] = url_PR[url_hash[key]]
	save_json('fullurl_PR.json', fullurl_PR)
	sorted_fullurlPR_tuple = sorted(fullurl_PR.items(), key = lambda d:d[1], reverse = True)
	# save_json('sorted_fullurl_PR.json', sorted_fullurlPR)
	sorted_fullurlPR_dict = dict()
	rank = 0
	count = 0
	for term in sorted_fullurlPR_tuple:
		if term[0].startswith('ftp://'):
			url = term[0][6:]
		elif term[0].startswith('http://'):
			url = term[0][7:]
		elif term[0].startswith('https://'):
			url = term[0][8:]
		else:
			url = term[0]
		if url in reverse_url_dict and reverse_url_dict[url] not in sorted_fullurlPR_dict:
			sorted_fullurlPR_dict[reverse_url_dict[url]] = 1.0 / (1+np.log(1+rank))
			count += 1
		elif url not in reverse_url_dict:
			sorted_fullurlPR_dict[url] = 1.0 / (1+np.log(1+rank))
		rank += 1
	save_json('sorted_fullurl_PR_dict.json', sorted_fullurlPR_dict)
	print count

if __name__ == '__main__':
	damping = 0.85
	n_iterations = 5
	filePathBase = "/Users/zhenchen/Documents/Courses/Information retrieval/project/project 3/WEBPAGES_RAW/"
	# totallink = buildURLgraph()
	# print "Build graph finished!"
	# PageRank('url_graph.json', damping, n_iterations, totallink)
	# print "PageRank finished!"
	assignPR('url_hash.json', 'url_PR.json', filePathBase+'bookkeeping.json')
	print "All finished!"





  
