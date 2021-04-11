import os
import codecs
import nltk
import string
import krovetz
import json
import re
from collections import Counter
nltk.download('wordnet')
nltk.download("punkt")
nltk.download('stopwords')
from nltk.corpus import wordnet as wn
#Function for exctracting info
def extract_info(topics_file):#Open topics file and reading lines
	f = open(topics_file)
	lines = f.readlines()
	#Initialize empty lists for title,descrption and narrative
	titles = []
	desc = []
	narr = []
	#Extracting info
	for i in range(0,len(lines)):
		line = lines[i]
		#Extracting title from line(where tag <title> is located)
		if "<title>" in line:
			line = line.replace("<title>","")
			titles.append(line)	
		#Extracting description from next line(-s) (where tag <desc> is located)
		elif "<desc>" in line:
			description = ""
			i = i+1
			while("<narr>" not in lines[i]):
				description = description + lines[i]
				i = i+1
			desc.append(description)	
		#Extracting narrative from next line(-s) (where tag <narr> is located)
		elif "<narr>" in line:
			narrative = ""
			i = i+1
			while("</top>" not in lines[i]):
				narrative = narrative + lines[i]
				i = i+1
			narr.append(narrative)		
	f.close()
	return titles,desc,narr
#Function to write queries parameters file
def write_queries(input_text,output_name,extra_input = [],weight = 1):
	with open(output_name+".trec","w") as f:
		f.write("<parameters>\n")
		#Change path here for index
		f.write("<index>/home/pantazis/Downloads/IR-2019-2020-Project-1/indices/example</index>\n")
		f.write("<rule>method:dirichlet,mu:1000</rule>\n")
		f.write("<count>1000</count>\n")
		f.write("<trecFormat>true</trecFormat>\n")
		size = len(input_text)
		for i in range(0,size):
			if weight < 1:
				extra_input[i] = extra_input[i].strip()
				f.write("<query> <type>indri</type> <number>"+str((301+i))+"</number> <text>"+"#weight("+str(weight)+" #combine("+ str(input_text[i]).rstrip("\n")+") " +  str(round(1-weight,1))+ " #combine("+str(extra_input[i]).rstrip("\n") + "))" + "</text> </query>\n")
			else:			
				f.write("<query> <type>indri</type> <number>"+str((301+i))+"</number> <text>"+str(input_text[i]).rstrip("\n")+"</text> </query>\n")
		f.write("</parameters>")
	f.close()
#Combine two arrays of text with a space bewteen them
def combine_texts(textA,textB):
	out = []	
	for i in range(0,len(textA)):
		out.append(textA[i] + " " + textB[i])
	return out	
#Function to remove punctuation and format text according to our need
def remove_pun(input_text):
	length = len(input_text)
	for i in range(0,length):
		item = input_text[i]
		#Replace some punctuations according to below patterns to avoid misunderstanding words in query
		item = item.replace("-"," ").replace("'s","").replace("&"," and ").replace("/"," ")
		#Remove any left punctuation
		out = item.translate(item.maketrans('','',string.punctuation))
		input_text[i] = out
		#Remove leading and trailing whitespaces
		input_text[i] = input_text[i].strip()
	return input_text
#Function to return best 15 related documents
def get_top15(filename):
	#Open file with results
	f = open(filename+".trec","r")
	lines = f.readlines()
	previous = ""
	num_queries = []	
	final ={}
	counter = 0
	#Read every line and check for a new number query
	for i in range(0,len(lines)):	
		line = lines[i]
		line_values = line.split()	
		if(line_values[0] != previous):
			num_queries.append(line_values[0])
			previous = line_values[0]
			#New query found so start keeping best 15
			start = True
		if(start):
			temp = []
			for k in range(0,15):
				temp.append(lines[i].split()[2])
				i = i+1
			start =  False
			final[num_queries[counter]] = temp
			counter = counter +1
	return final
#Function to write best 15 related documents in new files
def write_top15(dictionary):
	keys = dictionary.keys()
	keys = sorted(keys)
	with open("top15.txt","w") as top:
		for key in keys:
			valuesOfKey = dictionary[key]
			for item in valuesOfKey:
				top.write(item+"\n")
	top.close()
def choose_folder(asking_file):
	os.chdir("/home/pantazis/Downloads/IR-2019-2020-Project-1")
	currPath = os.getcwd()
	#Change current path according to the given name	
	if "FBIS" in asking_file:		
		os.chdir(currPath + "/fbis")
	elif "FR" in asking_file:
		os.chdir(currPath + "/fr94/"+asking_file[4:6])
	elif "LA" in asking_file:
		os.chdir(currPath + "/latimes")
	else:
		os.chdir(currPath + "/ft/"+asking_file[:5].lower())
def find_corresponding_file(asking_file):
	#Display files in current directory
	files = os.listdir()
	#Open every file and check if our given name is in there
	for filename in files:
		with codecs.open(filename,"r",encoding="latin-1") as data:
			wholeText = data.read()
			#Return corresponding file
			if asking_file in wholeText:
				return filename
def openCorrectFile(asking_file):
	previousPath = os.getcwd()
	os.chdir("/home/pantazis/Downloads/IR-2019-2020-Project-1")
	currPath = os.getcwd()
	filename = ""
	if os.path.exists(currPath + "/paths.json"):
		f = open("paths.json","r")
		data = json.load(f)
		f.close()
		for key in data.keys():
			if asking_file in data[key]:
				filename = key
	else:
		os.chdir(previousPath)
		print("paths.json file not found")
		filename = find_corresponding_file(asking_file)
	os.chdir(previousPath)
	return filename			 

#Function to retrieve text from the file obtained before
def retrieve_text(filename,title):
	text = ""
	#Pattern for html and etc tags
	cleanTags = re.compile('<.*?>')
	#Open and read file
	with codecs.open(filename,"r",encoding="latin-1") as data:
		lines = data.readlines()
		for i in range(0,len(lines)):
			line = lines[i]
			#Find the right section of our file and gather only the <TEXT> part
			if title in line:
				i = i +1
				while("<TEXT>" not in lines[i]):
					i=i+1
				i = i+1
				while("</TEXT>" not in lines[i]):
					#Remove html tags and dont add empty or newlines
					tempLine = re.sub(cleanTags,"",lines[i])
					if tempLine not in ["","\n"]:					
						text = text + tempLine
					i=i+1
	#Remove punctuation
	out = text.translate(text.maketrans('','',string.punctuation))	
	return out
#Create dictionary of tokenized words and their frequency
def make_dict(text):
	ks = krovetz.PyKrovetzStemmer()
	#Use nltk tokenizer to get every word in the text
	lista = nltk.word_tokenize(text)
	lista = [ks.stem(word) for word in lista]
	counter = Counter(lista)
	#Create stopwords array to dismiss them later	
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords.extend(list(string.ascii_lowercase))
	stopwords.extend([word.capitalize() for word in stopwords])
	pops = set(stopwords).intersection(counter.keys())
	for i in pops:
		counter.pop(i)	
	#Return only first 50 words	
	return counter.most_common(50)
#Function to create json file for 20 most common terms
def make_common20_file(filename,output_name):
	dictionary = get_top15(filename)
	num_queries = sorted(dictionary.keys())
	common20 = {}	
	for num in num_queries: 
		initList = []
		print("Query: " + num)
		tempString = ""
		for  name in dictionary[num]:						
			choose_folder(name)
			print("Name: " + name)
			collection = openCorrectFile(name)
			print("Collection: " +collection)
			tempString = tempString + retrieve_text(collection,name)
		tempDict = make_dict(tempString)
		common20[num] = tempDict
	os.chdir("/home/pantazis/Downloads/IR-2019-2020-Project-1")
	with open(output_name+".json", 'w') as json_file:
		json.dump(common20,json_file,indent=4)
	json_file.close()
def create_improved_queries(json_file,originalQueries,output,weight):
	#Data extraction from json file
	f = open(json_file+".json",'r')
	data = json.load(f)
	f.close()
	keys = sorted(data.keys())
	currPath  = os.getcwd()
	if not os.path.exists("Improved Queries"):
		os.mkdir("Improved Queries")
	os.chdir(currPath + "/Improved Queries")
	#Create dictionary for current (old) queries
	count = 301
	queries = {}
	originalQueries = remove_pun(originalQueries)
	for q in originalQueries:
		queries[str(count)] = q
		count+=1
	#Create improved queries
	improvedQueries = []
	for key in keys:
		temp = ""
		items = data[key]
		#Count to keep track of number of iterations (we want top 20 only)
		tempCount = 0
		for item in items:
			#Check for duplicates
			if item[0].lower() not in queries[key].lower() and tempCount < 20:
				temp = temp + " " + item[0]
				tempCount +=1
		#Build new improved query
		improvedQueries.append(temp)			
	write_queries(originalQueries,output+"extra-20-queries",improvedQueries,weight)
	queries_extra = combine_texts(originalQueries,improvedQueries)
	tempCount = 0
	#Create synonyms queries
	synQueries =[]
	ks = krovetz.PyKrovetzStemmer()
	for query in queries_extra:
		temp = ""
		tokenized = nltk.word_tokenize(query)
		words = [ks.stem(token).lower() for token in tokenized]
		for word in query.split():
			synsets = wn.synsets(word)
			count = 0
			for syn in synsets:		
				for l in syn.lemmas():
					if l.name().lower() not in temp.lower() and count !=2 and "_" not in l.name() and l.name().lower() not in words:
						temp = temp + " " + l.name()
						count += 1
		synQueries.append(temp)
	synQueries = remove_pun(synQueries)
	synQueries = combine_texts(improvedQueries,synQueries)
	write_queries(originalQueries,output+"extra-20-syn-queries",synQueries,weight)
	os.chdir(currPath)

