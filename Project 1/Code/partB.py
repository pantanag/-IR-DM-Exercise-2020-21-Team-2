import lib

#Creat json files for 20 most common words for each occasion
lib.make_common20_file("results-titles","common20_titles")
lib.make_common20_file("results-titles-desc","common20_titles_and_desc")

titles,desc,narr = lib.extract_info("topics.trec")
titles_and_desc = lib.combine_texts(titles,desc)
#Read json files
lib.create_improved_queries("common20_titles",titles,"titles-",0.4)
lib.create_improved_queries("common20_titles_and_desc",titles_and_desc,"titles-and-desc-",0.4)
