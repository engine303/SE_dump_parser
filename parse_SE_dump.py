# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import pandas as pd
from unidecode import unidecode
import re
import codecs
import string
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument("-f",  "--filename", type=str,
                    help="filename of stackexchange dump")

args = parser.parse_args()

if args.filename:
    filename = args.filename
else:
    raise Exception('There is no filename to parse dump as an argument for script')

logging.info('Parsing xml to tree')
tree = ET.parse(filename)
root = tree.getroot()

logging.info ('Xml tree processing')
l = []
for child in root:
    body_text = re.sub("</?[^>]+>", "", child.attrib["Body"])
    tup = (int(child.attrib["Id"]), int(child.attrib.get("ParentId", child.attrib["Id"])), 
           int(child.attrib["PostTypeId"]), body_text)
    l.append(tup)

df = pd.DataFrame(l, columns=["Id", "ParentId", "PostTypeId", "Body"])
df = df.sort_values(by=["ParentId", "PostTypeId"])

logging.info('There is %s rows in original dataset' % df.shape[0])

logging.info('Pandas dataframe constructing')
l = []

for i, (j, row) in enumerate(df.iterrows()):
    pid = row["ParentId"] 
    if row["PostTypeId"] == 1:
        q = row["Body"]
    if row["PostTypeId"] == 2:
        a = row["Body"]
        l.append((q, a))
    
    if i % 10000 == 0:
        logging.info("Process %s rows" % str(i))

data = pd.DataFrame(l, columns=["question", "answer"])

logging.info('Preprocessing text fields')
data.question = data.question.apply(lambda x: unidecode(x).lower() 
                                    if not re.search(u"[А-я]", x) else x.lower())
data.question = data.question.apply(lambda x: re.sub("\n{1,}", " ", x).strip())
data.question = data.question.apply(lambda x: re.sub('([%s])' % string.punctuation, r' \1 ', x))
data.question = data.question.apply(lambda x: re.sub('\s{2,}', ' ', x).strip())
                                    
data.answer = data.answer.apply(lambda x: unidecode(x).lower() 
                                    if not re.search(u"[А-я]", x) else x.lower())
data.answer = data.answer.apply(lambda x: re.sub("\n{1,}", " ", x).strip())
data.answer = data.answer.apply(lambda x: re.sub('([%s])' % string.punctuation, r' \1 ', x))
data.answer = data.answer.apply(lambda x: re.sub('\s{2,}', ' ', x).strip())

logging.info('Successfully parsed %s pairs of questions-answers' % data.shape[0])

logging.info('Storing to csv')
data.to_csv('%s.csv' % filename.split(".")[0], index=False, encoding="utf8")

