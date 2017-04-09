from __future__ import division
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup, Comment
import time, re
import numpy as np
import json
import webbrowser
import Tkinter as tk


def calculate_Tfidf(tf,df):
    N=13645
    return (1+np.log10(tf))*(np.log10(N/df))


def get_json(indexFile):
	with open(indexFile) as handle:
		return json.load(handle)

def callback(url):
    webbrowser.open_new(url)

def interface():
	root = tk.Tk()
	root.geometry('1000x800')
	root.title("Googol")

	logo = tk.Label(root, text = 'Googol', fg = "blue", font = "Helvetica 64 bold italic")
	var = tk.StringVar()
	query_ety = tk.Entry(root, textvariable = var)
	results_output0 = tk.Message(root, text = '', width = 500)
	results_output1 = tk.Label(root, text="", fg='dark blue', cursor="hand2", font = 'Times 20 bold')
	results_output2 = tk.Label(root, text="", fg='dark green', cursor="hand2")
	results_output3 = tk.Label(root, text="", fg='black', cursor="hand2")
	results_output4 = tk.Label(root, text="", fg='dark blue', cursor="hand2", font = 'Times 20 bold')
	results_output5 = tk.Label(root, text="", fg='dark green', cursor="hand2")
	results_output6 = tk.Label(root, text="", fg='black', cursor="hand2")
	results_output7 = tk.Label(root, text="", fg='dark blue', cursor="hand2", font = 'Times 20 bold')
	results_output8 = tk.Label(root, text="", fg='dark green', cursor="hand2")
	results_output9 = tk.Label(root, text="", fg='black', cursor="hand2")
	results_output10 = tk.Label(root, text="", fg='dark blue', cursor="hand2", font = 'Times 20 bold')
	results_output11 = tk.Label(root, text="", fg='dark green', cursor="hand2")
	results_output12 = tk.Label(root, text="", fg='black', cursor="hand2")
	results_output13 = tk.Label(root, text="", fg='dark blue', cursor="hand2", font = 'Times 20 bold')
	results_output14 = tk.Label(root, text="", fg='dark green', cursor="hand2")
	results_output15 = tk.Label(root, text="", fg='black', cursor="hand2")

	search_btn = tk.Button(root, text = 'Go', command = lambda: print_result(var, results_output0, results_output1, results_output2, results_output3, results_output4, results_output5, results_output6, results_output7, results_output8, results_output9, results_output10, results_output11, results_output12, results_output13, results_output14, results_output15))
	root.bind('<Return>', lambda event : print_result(var, results_output0, results_output1, results_output2, results_output3, results_output4, results_output5, results_output6, results_output7, results_output8, results_output9, results_output10, results_output11, results_output12, results_output13, results_output14, results_output15))

	logo.pack(pady = 50)
	query_ety.pack(ipadx = 200, ipady = 8)
	search_btn.pack(ipadx = 20, ipady = 8)
	results_output0.pack()
	results_pady = 0
	results_output1.pack()
	results_output2.pack()
	results_output3.pack()

	results_output4.pack()
	results_output5.pack()
	results_output6.pack()

	results_output7.pack()
	results_output8.pack()
	results_output9.pack()

	results_output10.pack()
	results_output11.pack()
	results_output12.pack()

	results_output13.pack()
	results_output14.pack()
	results_output15.pack()

	root.mainloop()

def get_stem(content):
    stemmer = SnowballStemmer('english')
    for k in range(len(content)):
        content[k] = stemmer.stem(content[k]).encode('utf-8')

def isstopwords(word):
    sw = set(stopwords.words('english'))
    if word in sw:
        return True
    else:
        return False

def getCapitals(content):
    terms = []
    word = ""
    for i in range(len(content)):
        if len(word) >= 2 and len(word) <= 15 and not isstopwords(word.lower()) and word.isupper():
            terms.append(word)
        word = ""
        for j in range(len(content[i])):
            # if content[i][j].isalpha() or content[i][j].isdigit() or (content[i][j]=='-' and len(word)>0):
            if content[i][j].isalpha():
                word += content[i][j]
            else:
                if len(word) >= 3 and len(word) <= 15 and not isstopwords(word.lower()) and word.isupper():
                    terms.append(word)
                word = ""
    if len(word) >= 2 and len(word) <= 15 and not isstopwords(word.lower()) and word.isupper():
        terms.append(word)
    #get_stem(terms)
    return terms

def termProcessing(content):
    terms = []
    word=""
    for i in range(len(content)):
        if len(word)>=3 and len(word)<=15 and not isstopwords(word):
            terms.append(word.lower())
        word = ""
        for j in range(len(content[i])):
            if content[i][j].isalpha() or content[i][j].isdigit():
                word += content[i][j]
            else:
                if len(word)>=3 and len(word)<=15 and not isstopwords(word):
                    terms.append(word.lower())
                word=""
    if len(word)>=3 and len(word)<=15 and not isstopwords(word):
        terms.append(word.lower())
    get_stem(terms)
    return terms

def queryProcess(query):
	token = query.lower()
	token = token.split(' ')
	# typo chcek
	# stop words
	for i in range(len(token)):
		if isstopwords(token[i]): del token[i]
	# stem
	get_stem(token)

	return token

def print_result(var, results_output0, results_output1, results_output2, results_output3, results_output4, results_output5, results_output6, results_output7, results_output8, results_output9, results_output10, results_output11, results_output12, results_output13, results_output14, results_output15):
	global N
	query = var.get()
	result_url = []
	result_visiable = []
	
	try:
		starttime = time.time()
		posting = search(query) # [url, title, snippet]
		runtime = time.time() - starttime
		results0 = "Run time is " + str(runtime) + "s."
		for i in range(N):
			result_url.append('http://' + posting[i][0])
			# result_visiable.append(posting[i][1]+'\n'+posting[i][0]+'\n'+posting[i][2]+'\n')
			result_visiable.append(posting[i][1])
			if len(posting[i][0]) > 50:
				result_visiable.append(posting[i][0][0:50])
			else:
				result_visiable.append(posting[i][0])
			result_visiable.append(posting[i][2]+'...')

	except:
		results0 =  'No search results for ' + query + '!'
		for i in range(N):
			result_url.append('')
			result_visiable.append('')

	results_output0.config(text = results0)

	results_output1.config(text = result_visiable[0])
	results_output2.config(text = result_visiable[1])
	results_output3.config(text = result_visiable[2])
	results_output4.config(text = result_visiable[3])
	results_output5.config(text = result_visiable[4])
	results_output6.config(text = result_visiable[5])
	results_output7.config(text = result_visiable[6])
	results_output8.config(text = result_visiable[7])
	results_output9.config(text = result_visiable[8])
	results_output10.config(text = result_visiable[9])
	results_output11.config(text = result_visiable[10])
	results_output12.config(text = result_visiable[11])
	results_output13.config(text = result_visiable[12])
	results_output14.config(text = result_visiable[13])
	results_output15.config(text = result_visiable[14])

	results_output1.bind("<Button-1>", lambda event: callback(result_url[0]))
	results_output4.bind("<Button-1>", lambda event: callback(result_url[1]))
	results_output7.bind("<Button-1>", lambda event: callback(result_url[2]))
	results_output10.bind("<Button-1>", lambda event: callback(result_url[3]))
	results_output13.bind("<Button-1>", lambda event: callback(result_url[4]))

	# var.set('')

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'meta', 'head', 'title']:
        return False
    elif isinstance(element, Comment):
        return False
    return True


def search(query):
	global indexPathBase, filePathBase
	global standard, GoogleResults, hash
	global parameter, N, N2
	global urlPR_dict
	if query == '':
		results = []
		return []
	else:
		# the set of related index files
		index = {}
		CapitalDocuments = {}

		query_list = getCapitals([query])
		for item in query_list:
			if item.isupper() and len(item) > 1:
				# deal with all-capital
				CapitalIndex = get_json(indexPathBase + 'CapitalIndexer/' + item[0] + '/' + item[1] + '.json')
				for k in range(len(CapitalIndex)):
					if CapitalIndex[k][0] == item:
						search_pool = CapitalIndex[k][1]
						for (key, value) in search_pool.items():
							documentName = key.encode('utf-8')
							CapitalDocuments[documentName] = value['tf'.decode('utf-8')]
						# print(documentName,CapitalDocuments[documentName])
		query_tokens = termProcessing([query])
		# document parameters (tfidf, ishead, pos)
		Documents = {}
		# the index of the token
		count = 0
		# the number of query tokens
		M = len(query_tokens)
		# initialize queue's tf-idf
		queryTfidf = np.zeros(M)
		for token in query_tokens:
			# read index
			if len(token) < 3:
				subpath = token + '.json'
				InitialName = token
			else:
				subpath = token[0] + '/' + token[1] + '/' + token[2] + '.json'
				InitialName = token[0] + token[1] + token[2]
			if InitialName not in index:
				index[InitialName] = get_json(indexPathBase + subpath)
			# search the current token in the corresponding index file
			for k in range(len(index[InitialName])):
				if index[InitialName][k][0] == token:
					search_pool = index[InitialName][k][1]
					# get df
					df = len(search_pool)
					# calculate query's tf-idf
					queryTfidf[count] = calculate_Tfidf(1, df)
					for (key, value) in search_pool.items():
						documentName = key.encode('utf-8')
						tf = value['tf'.decode('utf-8')]
						tfidf = value['tf-idf'.decode('utf-8')]
						head = value['head'.decode('utf-8')]
						body = value['body'.decode('utf-8')]
						baselink = value['link'.decode('utf-8')][0]
						outlink = value['link'.decode('utf-8')][1]
						if count == 0:
							Documents[documentName] = {}
							Documents[documentName]['tf-idf'] = np.zeros(M)
							Documents[documentName]['ishead'] = np.zeros(M)
							Documents[documentName]['pos'] = [[] for i in range(len(query_tokens))]
							Documents[documentName]['baselink'] = [0 for i in range(len(query_tokens))]
							Documents[documentName]['outlink'] = [0 for i in range(len(query_tokens))]
							Documents[documentName]['num'] = 0
						if documentName in Documents:
							if len(head) > 0:
								Documents[documentName]['ishead'][count] = 1
							Documents[documentName]['pos'][count] = body
							Documents[documentName]['baselink'][count] = baselink
							Documents[documentName]['outlink'][count] = outlink
							Documents[documentName]['tf-idf'][count] = tfidf
							Documents[documentName]['num'] += 1
					break
			count += 1
		scores = {}
		for documment in Documents:
			if Documents[documment]['num'] == M or sum(Documents[documment]['baselink']) > 0 or sum(
					Documents[documment]['outlink']) > 0:
				# calculate the score for (document, query)
				# calculate cosin
				if sum(Documents[documment]['tf-idf']) > 0:
					cosin = sum(np.multiply(queryTfidf, Documents[documment]['tf-idf'])) / np.sqrt(
						sum(Documents[documment]['tf-idf'] ** 2))
				else:
					cosin = 0
				# calculate link score
				linkScore1 = sum(Documents[documment]['baselink'])
				linkScore2 = sum(Documents[documment]['outlink'])
				# calculate headWeight
				headWeight = sum(Documents[documment]['ishead'])
				# calculate pagerank
				if documment in urlPR_dict:
					pagerank = urlPR_dict[documment]
				else:
					pagerank = 0
				# initializa posWeight
				posWeight = 0
				scores[documment] = parameter[0] * cosin + parameter[1] * headWeight + parameter[2] * linkScore1 + parameter[3] * np.log10(
					1 + linkScore2) + parameter[6] * pagerank

		for documment in CapitalDocuments:
			if documment not in scores:
				scores[documment] = 0
			scores[documment] += parameter[4] * CapitalDocuments[documment]
		# select the top N documents
		results_raw = sorted(scores.iteritems(), key=lambda d: -d[1])
		if M >= 2:
			for i in range(N2):
				posWeight = 0
				documentName = results_raw[i][0]
				position0 = Documents[documentName]['pos'][0]
				position1 = Documents[documentName]['pos'][1]
				curPos = 0
				posHash = {}
				for j in range(len(position1)):
					curPos += position1[j]
					posHash[curPos] = True
				curPos = 0
				for j in range(len(position0)):
					curPos += position0[j]
					if (curPos + 1) in posHash or (curPos + 2) in posHash:
						posWeight += 1
				if posWeight > 0:
					scores[documentName] += parameter[5] * np.log10(1 + posWeight)
			results_raw = sorted(scores.iteritems(), key=lambda d: -d[1])
		for i in range(5):
			print(results_raw[i][0], results_raw[i][1])
		'''
		# calculate DCG@5
		#x = [0, 0, 0, 0, 0]
		#for i in range(5):
				fileRes = results_raw[i][0]
			if fileRes in GoogleResults[query]:
				if i == 0:
					x[i] = GoogleResults[query][fileRes]
				else:
					x[i] = GoogleResults[query][fileRes] / np.log2(i + 1)
		for i in range(1, 5):
			x[i] += x[i - 1]
		for i in range(5):
			x[i] = x[i] / standard[i]
		print(x)
		'''
		results = []
		results_list = []
		for k in range(len(results_raw)):
			results_list.append([results_raw[k][0], hash[results_raw[k][0]]])
		#with open('score_' + query + '.json', 'w') as outfile:
		#	outfile.write(json.dumps(results_list))
		for k in range(N):
			url_list = []  # [url, title, snippet]
			url_list.append(hash[results_raw[k][0].decode('utf-8')])
			filePath = filePathBase + results_raw[k][0].decode('utf-8')
			with open(filePath, 'r') as file:
				soup = BeautifulSoup(file.read(), "lxml")

			if (soup.title is None) or (soup.title.string is None):
				url_list.append('')
			else:
				if len(soup.title.string) >= 50:
					title = soup.title.string[0:50]
				else:
					title = soup.title.string
				if not isinstance(title, unicode):
					url_list.append(title.decode('utf-8', 'ignore'))
				else:
					url_list.append(title)
			# print(k,url_list)
			snippet = ''
			if soup.body is not None:
				text = soup.body.findAll(text=True)
				visible_text = filter(visible, text)
				visible_text = [term.string.encode('utf-8') for term in visible_text]
				for term in visible_text:
					if term.find(query_tokens[0]) != -1:
						if len(term) >= 100:
							query_index = term.find(query_tokens[0])
							if 50 <= query_index <= len(term) - 50:
								term = term[query_index - 50:query_index + 50]
							elif query_index < 50 and query_index <= len(term) - 50:
								term = term[0:query_index + 50]
							elif query_index < 50 and query_index > len(term) - 50:
								term = term
							elif query_index >= len(term) - 50 and query_index < 50:
								term = term
							else:
								term = term[query_index - 50:len(term)]
						snippet = term
						break
			if not isinstance(snippet, unicode):
				url_list.append(snippet.decode('utf-8', 'ignore'))
			else:
				url_list.append(snippet)
			results.append(url_list)

	return results

if __name__ == '__main__':
	global indexPathBase
	global parameter, N, N2
	#parameter = [1, 0.75, 0, 0, 0, 0, 0]
	parameter = [1, 0.75, 0.25, 1, 0.5, 0.75, 0.5]
	N = 5
	N2 = 100
	global GoogleResults
	GoogleResults = {}
	GoogleResults["mondego"] = {'19/404': 5, '20/58': 4, '29/73': 3, '69/263': 2, '13/378': 1, '17/330': 1, '27/284': 1,
								'49/191': 1, '54/264': 1, '73/462': 1}
	GoogleResults["machine learning"] = {'0/17': 5, '35/271': 4, '14/218': 3, '57/319': 2, '39/49': 1}
	GoogleResults["software engineering"] = {'62/355': 5, '3/440': 4, '16/242': 3, '59/465': 2, '30/330': 1}
	GoogleResults["security"] = {'49/98': 5, '44/249': 4, '21/166': 3, '54/498': 2, '28/427': 1}
	GoogleResults["student affairs"] = {'0/45': 5, '55/8': 4, '64/345': 3, '49/260': 2, '22/134': 1}
	GoogleResults["graduate courses"] = {'13/428': 5, '41/161': 4, '31/138': 3, '69/328': 2, '17/150': 1}
	GoogleResults["Crista Lopes"] = {'20/58': 5, '51/46': 4, '56/422': 3, '72/168': 2, '2/415': 1}
	GoogleResults["REST"] = {'16/141': 5, '10/406': 4, '23/129': 3, '54/237': 2, '14/434': 1}
	GoogleResults["computer games"] = {'39/108': 5, '5/454': 4, '40/361': 3, '56/191': 2, '70/69': 1}
	GoogleResults["information retrieval"] = {'5/451': 5, '19/21': 4, '61/433': 3, '60/155': 3, '51/465': 3,
											  '51/231': 3, '47/439': 3, '43/299': 3, '35/52': 3, '34/193': 3,
											  '31/385': 3, '23/237': 3, '20/181': 3, '16/440': 3, '10/32': 2,
											  '20/58': 1}
	indexPathBase = "/Users/GJzh/Desktop/JunGuo/results/"
	filePathBase = "/Users/GJzh/Downloads/WEBPAGES_RAW/"
	# calculate the standard used to normalize NDCG@5
	global standard, hash, urlPR_dict
	x = [5, 4, 3, 2, 1]
	y = [0, 0, 0, 0, 0]
	for i in range(5):
		if i == 0:
			y[i] = x[i]
		else:
			y[i] = x[i] / (np.log2(i + 1))
	for i in range(1, 5):
		y[i] += y[i - 1]
	standard = y
	urlPR_dict = get_json('/Users/GJzh/Desktop/JunGuo/results/sorted_fullurl_PR_dict.json')
	hash = get_json(indexPathBase + 'bookkeeping.json')
	interface()
	'''''
	Querys=["mondego","machine learning","software engineering","security","student affairs","graduate courses","Crista Lopes","REST","computer games","computer games"]
	optParameter = parameter
	optScore=0

	for a in range(2):
		parameter[0]=0.5+0.25*(a+1)
		for b in range(2):
			parameter[1] = 0.5+0.25 * (b + 1)
			for c in range(4):
				parameter[2] = 0.25 * (c + 1)
				for d in range(2):
					parameter[3] = 0.5+0.25 * (d + 1)
					for e in range(4):
						parameter[4] = 0.25 * (e + 1)
						for f in range(4):
							parameter[5] = 0.25 * (f + 1)
							for g in range(4):
								parameter[6] = 0.25 * (g + 1)

	score = [0,0,0,0,0]
	for query in Querys:
		res=search(query)
		for i in range(5):
			score[i] += res[i]
	for i in range(5):
		score[i] /= 10
	print(parameter,score)
	'''''
