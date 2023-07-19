#!/usr/bin/env python
"""
This script downloads article information of one URL. The results are stored in 
JSON-files in a sub-folder.
You need to adapt the variables url and basepath in order to use the script.
"""
import os
import json

from newsplease import NewsPlease

URL = "https://www.rt.com/news/203203-ukraine-russia-troops-border/"
BASE_PATH = "/tmp/news-please/articles/"
os.makedirs(BASE_PATH, exist_ok=True)
article = NewsPlease.from_url(URL).get_serializable_dict()
print(article)
with open(BASE_PATH + article["filename"] + ".json", "w", encoding="utf-8") as outfile:
    json.dump(article, outfile, indent=4, sort_keys=True)
