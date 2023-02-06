# change input data file name in line 32, text must be in column 3 (last column)
# output file is called limit_post.csv on line 100. Change this name before you run the script each time.
# obtain words surrounding an attribute like performance, use brand = bmw, attribute = performance, limit of words = 2
# To just extract posts containing a brand like bmw, use brand = bmw, attribute = bmw, limit of words = 5 or 10
# The output will be partial sentences with words around "bmw"
import re
import nltknltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import pandas as pd
import csv

def isNum(passedString):
    return any(i.isdigit() for i in passedString)

posts_found_with_brand = []
limited_post = []
limited_post2 = []
final_list = []
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
newStopWords = ["n't","'s","'m","also","'d","'ve","could","would","ca"]
removeStopWords = ['above','below','up','down']
stopwords.extend(newStopWords)
for word in removeStopWords:
    stopwords.remove(word)
inter1 = []
completeComment_list = []

with open('edmunds_new_output.csv') as f:
    rows = csv.reader(f,  delimiter=str(','), quotechar=str('"'))
    for row in rows:
        inter1.append(row[2])
for f in inter1:
    stop_words = set(stopwords)
    sentence_list = sent_tokenize(f)
    temp_list = []
    for sentence in sentence_list:
        word_tokens = word_tokenize(sentence)
        wordLower_tokens = []
        wordLower_tokens = [g.lower() for g in word_tokens]
        firstF_list = [h for h in wordLower_tokens if not h in stop_words]
        firstF_list = []
        secondF_list = []
        for i in wordLower_tokens:
            if i not in stop_words:
                firstF_list.append(i)
        for j in firstF_list:
            if(isNum(j) == False):
                wordNoPunctuation = re.sub('[\W_]+', '', j)
                secondF_list.append(wordNoPunctuation)
            else:
                secondF_list.append(j)
        temp_list.append(secondF_list)
    completeComment_list.append(temp_list)

nb = input('Choose a Brand: ')
nb2 = input('Choose an Attribute: ')
nb3 = input('Limit of the words in the sentence: ');

for post in completeComment_list:
    for sentence in post:
        x = 0
        for i in sentence:
            if(i == nb):
                x = 1
                posts_found_with_brand.append(post)
                break

        if(x == 1):
            break

limit = int(nb3) + 1

for post in posts_found_with_brand:
    sentence_with_attribute = []
    position_in_sentences = []
    for sentence in post:
        position  = 0
        for i in sentence:
            if(i == nb2):
                position_in_sentences.append(position)
                sentence_with_attribute.append(sentence)
            position = position + 1
    j = 0
    for sentence in sentence_with_attribute:
        limited_sentence = []
        for i in range(len(sentence)):
            if(abs(i - position_in_sentences[j]) < limit):
                limited_sentence.append(sentence[i])
        j = j + 1
        limited_post.append(limited_sentence)

for sent in limited_post:
    limited_post2.append(' '.join(sent))

df = pd.DataFrame()
writer = 'limit_post.csv'

df['Sentences']  = limited_post2
df.to_csv(writer, index = False)

print("written limit_post.csv")