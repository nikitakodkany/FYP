#libraries
import csv
import math
import numpy as np
import pandas as pd

#To open processed dataset (JDs)
with open('/home/nikita/Desktop/PGN/Dataset/pros_Dataset2.csv', newline='') as f1:
    JDVtext1 = f1.readlines() #6131

#To open KLSGIT syllabus
with open('/home/nikita/Desktop/PGN/Dataset/syllabuskeys.csv', newline='') as f2:
    SylVtext2 = f2.readlines() #981
    
#A list that has the entire corpus
EntireCorpus = JDVtext1 + SylVtext2

#To index every word in the corpus
class WordIdGenerator:
    word_map = {}
    word_id_counter = 0
    def word_id(self, words):
        for word in words:
            if word in self.word_map:
                return self.word_map
            else:
                self.word_map[word] = self.word_id_counter
                self.word_id_counter += 1
                return self.word_map

#To generate an index for words and their hash values
gen = WordIdGenerator()
for w in EntireCorpus:
    wordtoindex = gen.word_id(w.split())
    
#intialising JD-values and Syllabus-values to zeros
JDVhashed = np.zeros((6131,1400))
SylVhashed = np.zeros((1400,1))

#To have an encoded JD-Value vector where there are 6131 JDS and 1400 Word-To-Index Values 
for i,sentence in enumerate(JDVtext1):
    wordlist = sentence.split() 
    for word in wordlist:
        if word in wordtoindex:
            index = wordtoindex[word]
            JDVhashed[i][index] = 1

#To have an encoded Syl-Value vector
for sentence in SylVtext2: 
    wordlist = sentence.split() 
    for word in wordlist:
        if word in wordtoindex:
            index = wordtoindex[word]
            SylVhashed[index][0] = 1 

#Cosine Similarity Scores
from sklearn.metrics.pairwise import cosine_similarity
print("Similarity Score:", np.max((cosine_similarity(JDVhashed, SylVhashed.T))))
print("Average Similarity Score: ", np.mean((cosine_similarity(JDVhashed, SylVhashed.T))))
print("Dissimilarity Score:", 1-np.max((cosine_similarity(JDVhashed, SylVhashed.T))))
