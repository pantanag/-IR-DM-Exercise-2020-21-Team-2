import lib
import os
titles,desc,narr = lib.extract_info("topics.trec")
#Savign titles, descriptions and narratives in new files
currPath = os.getcwd()
if not os.path.exists(currPath + "/Topics, Desc, Narr"):
	os.mkdir("Topics, Desc, Narr")
os.chdir(currPath+"/Topics, Desc, Narr")
files = {"titles.txt":titles,"descriptions.txt":desc,"narratives.txt":narr}
for filename,values in files.items():
	with open(filename,"w") as f:
		for line in values:
			f.write(line)
f.close()
#Removing punctuation and formatting text
titles = lib.remove_pun(titles)
desc = lib.remove_pun(desc)
narr = lib.remove_pun(narr)
#Combine titles with descriptions and narratives
titles_and_desc = lib.combine_texts(titles,desc)
titles_and_desc_and_narr = lib.combine_texts(titles_and_desc,narr)
#Write queries parameters files for each part
os.chdir(currPath)
if not os.path.exists(currPath + "/Baseline Queries"):
	os.mkdir("Baseline Queries")
os.chdir(currPath+"/Baseline Queries")
lib.write_queries(titles,"titles-queries")
lib.write_queries(titles_and_desc,"titles-desc-queries")
lib.write_queries(titles_and_desc_and_narr,"titles-desc-narr-queries")
os.chdir(currPath) 
