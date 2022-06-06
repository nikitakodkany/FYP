#Imports

from audioop import avg
import csv
from inspect import CO_COROUTINE
import math
import random
from tarfile import SYMTYPE
from xml.sax.handler import EntityResolver
import numpy as np
import pandas as pd
from torch import int8
from tqdm import tqdm
import itertools
import numpy as np
from collections import Counter


#Open the appropriate dataset. This should change based on the subject.
JDVtext1 = pd.read_excel('../../Dataset/dataset/Excel/processed_web_dataset.xlsx')

#To open syllabus. Notice the format of the file as well. This is basically the file from the server
with open('./../../Dataset/dataset/CSV/web.csv', newline='') as f2:
    SylVtext2 = f2.readlines()


#Process the syllabus by removing punctuations and further remove the empty string formed
SylVtext2 = [a.replace('\n' , '').replace('.','').replace(',' , '').replace('(' , '').replace(')' , '').replace(':' , '') for a in SylVtext2]
SylVtext2 = [a for a in SylVtext2 if a != '']



#Create a corpus of all words that are present in the dataset+syallbus
#EntireCorpus contains strings, which is basically every row incase of dataset and line in case of syllabus
#Finally, corpus contains a list of every single word present in the dataset+syllabus
EntireCorpus = np.concatenate((JDVtext1.job_desc_processed.values, SylVtext2))
corpus = [word for line in EntireCorpus for word in line.split()]



class WordIdGenerator:
    """
    Helper Class to generate unique id for every word present in the corpus
    This word,unique_id pair is stored in the form of a dict
    """
    word_map = {}
    word_id_counter = 0
    def word_id(self, words):
        #Iterate over the list of words
        #if it is present in the mapping, then do nothing and continue
        for word in words:
            if word in self.word_map:
                continue
        #if word is missing, add the word to the mapping and add the counter value as its unique id
            else:
                self.word_map[word] = self.word_id_counter
                self.word_id_counter += 1
        return self.word_map


#List of words present only in the syllabus
syllabus_words = [word for line in SylVtext2 for word in line.split()]


# Create an instance of the class
gen = WordIdGenerator()

#wordtoindex is a dict that contains the mapping of all words present in the corpus
wordtoindex = gen.word_id(corpus)

#indextoword is a dict that contains the reverse mapping, that is unique_id to word
indextoword = {v:k for k,v in wordtoindex.items()}

#Create a vector to represent both the Job descriptions and Syllabus
JDVhashed = np.zeros((len(JDVtext1) , len(wordtoindex)))
SylVhashed = np.zeros((len(wordtoindex) , 1))

#Create the bag of words representation of the syllabus
#Iterate over every line of the syllabus
for sentence in SylVtext2:
    #Split the line into a list of words
    wordlist = sentence.split()
    #iterate over the list of words
    for word in wordlist:
        #find the unique id and set the unique_id-th index as 1 (i.e Bag of words representation)
        index = wordtoindex[word]
        SylVhashed[index] = 1


#Iterate over every JD in the dataset
for i,sentence in enumerate(JDVtext1.job_desc_processed):

    #split the JD into a list of words
    wordlist = sentence.split()

    #iterate over the list of words
    for word in wordlist:
     #find the unique id and set the unique_id-th index as 1 (i.e Bag of words representation)

        if word in wordtoindex:
            index = wordtoindex[word]
            JDVhashed[i][index] = 1

from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# score = ((cosine_similarity(JDVhashed, SylVhashed.T)))
# print(f'\nAverage comparision value  {np.mean(score)*100}%')
# print(f'\nMax similarity {np.max(score)*100} %')
# print('----------------------------------------------------------')

#Contains all the JDs in string format itself in a numpy array
jds_decoded = JDVtext1.job_desc_processed.to_numpy()

#init 3 counters for uni-grams, bi-grams and trigrams
counters = [Counter() , Counter(),Counter()]

#iterate over n where n is used to form the n-gram. This loop runs for 1 to 3 inclusive.
#A number higher than 3 may result in the process being killed by the kernel
for i in range(1,4):
    #Iterate over every JD in the dataset
    for sub_list in jds_decoded:

        #Set the number of elements to be considered at a time (r). This is equivalent to r in nCr formula in combinations

        r = i
        #Calculate every single combination for the words present in the particular JD
        a = itertools.combinations(np.unique(np.array(sub_list.split())), r)
        #Update the corresponding counter (for uni-gram , bi-gram and tri-gram)
        #a gives a dict that contain all combinations of a word. For every iteration of the for-loop (sublist in jd_decoded),
        #a generates all combinations of words. The words that are repeated across JDs are then counted whenever the update happens in the next line.
        counters[i-1].update(a)


print("\nMost commonly occuring words in the JD are :-")
#Iterate over the counters and print out the most common uni-grams , bi-grams and tri-grams.
for counter in counters:
    print(counter.most_common(5) , end = '\n\n')

#most_common_words contains the n most common words present across JDs
most_common_words = [a[0][0] for a in counters[0].most_common(30)]

#init the variable for counting number of common words
common_words_count = 0

#iterate over the most common words and check if they are in the Syallbus
#If present, increment the common_words_count variable
for word in most_common_words:
    if word in syllabus_words:
        common_words_count+=1

print(f"Similarity of Syllabus wrt Job descriptions is :- {(common_words_count/30)*100} %")

print('Most common words present in job descriptions are:-')
print(most_common_words)

print('----------------------------------------------------------')

#Syllabus hashed(i.e bag of words encoded) gets vectorised in this operation
#the difference will yield in positive values for words present in the JD but not in the Syl
#Hence we sum these up to get the total count

diff = SylVhashed - JDVhashed.T
diff = (np.sum(diff , axis = 1))

#This is a list of all unique words
words = [indextoword[num] for num in range(len(wordtoindex))]
    #position = JDVtext1.loc[top_jd_indices]['position']

#This dict contains the word:frequency for every word (The frequency here is the number of times a word was present in JD but not in syllabus)
#Frequency is obtained from the diff vector
words_dict = {word:num for word,num in zip(words , diff)}

#Sort the words to find out the 20 most commonly occuring words missing from the Syllabus but present in the JD
missing_words = (sorted(words_dict, key= lambda a : words_dict[a])[:20])


#Repeat the same loop before
counters_missing = [Counter() , Counter(),Counter()]
for i in range(1,4):
    for sub_list in jds_decoded:
        r = i
        #BUT THE WORDS TO FIND COMBINATIONS FOR ARE ONLY THE WORDS THAT ARE COMMON BETWEEN A PARTICULAR JD AND THE MISSING WORDS DICT
        #The following list comprehension does exactly that
        w = [word for word in sub_list.split() if word in missing_words]

        #The rest of the loop is same as the previous loop

        a = itertools.combinations(np.unique(np.array(w)), r)
        counters_missing[i-1].update(a)


print("Most commonly co-occuring words missing from syllabus but present in JD are:-")
for counter in counters_missing:
    print(counter.most_common(5) , end = '\n\n')
print('----------------------------------------------------------')

print("\n Most commonly occurring missing words are")
print(missing_words)

print('----------------------------------------------------------')

print("Suggested Syllabus (Each module of 8 hours):-  \n ")

#Print syllabus by grouping the list of missing words into groups of 5

idx = 0
for i in range(4):
    print(missing_words[idx:idx+5])
    idx +=5


#Alternate way of finding missing words:-
#Print if required , and replace this array with the other missing_word_array
missing_words_alt = [word for word in most_common_words if word not in syllabus_words]
# print(missing_words_alt)
