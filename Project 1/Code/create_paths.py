import os
import json
def extract_filenames(files):
	output_dict = {}
	for filename in files:
		f = open(filename,"r",encoding="latin-1")
		lines = f.readlines()
		temp = []
		for line in lines:
			if "<DOCNO>" in line:
				#title = line.split()[1]
				title = line.replace("<DOCNO>","").replace("</DOCNO>","").strip()				
				temp.append(title)
		output_dict[filename] = temp
	return output_dict
def merge_dicts(a,b):
	c = a.copy()
	c.update(b)
	return c
currPath = os.getcwd()
os.chdir(currPath +"/fbis")
fbis = os.listdir()
print("Extracting fbis titles...")
path_dict = extract_filenames(fbis)
print("Done")
os.chdir(currPath +"/latimes")
la = os.listdir()
print("Extracting latimes titles...")
path_dict = merge_dicts(path_dict,extract_filenames(la))
print("Done")
os.chdir(currPath + "/fr94")
fr = os.listdir()
print("Extracting fr94 titles...")
for folder in fr:
	os.chdir(currPath+"/fr94/"+folder)
	fr94 = os.listdir()
	path_dict = merge_dicts(path_dict,extract_filenames(fr94))
print("Done")
os.chdir(currPath + "/ft")
ft = os.listdir()
print("Extracting ft titles...")
for folder in ft:
	os.chdir(currPath+"/ft/"+folder)
	ftFiles = os.listdir()
	path_dict = merge_dicts(path_dict,extract_filenames(ftFiles))
print("Done")
os.chdir(currPath)
with open("paths.json","w") as json_file:
	json.dump(path_dict,json_file,indent = 4)
json_file.close() 

