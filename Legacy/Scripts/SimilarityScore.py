#libraries
import csv
import math
import numpy as np
import pandas as pd
from torch import int8
from tqdm import tqdm 

#To open processed dataset (JDs)
JDVtext1 = pd.read_excel('/home/pinto/Desktop/PGN/Dataset/dataset/Excel/dataset_lemmatized.xlsx')

#To open KLSGIT syllabus
# with open('./../../Dataset/dataset/CSV/web.csv', newline='') as f2:
#     SylVtext2 = f2.readlines() #981

SylVtext2 = pd.read_excel('./../../Dataset/dataset/Excel/syllabus_dataset_lemmatized.xlsx')


#A list that has the entire corpus
EntireCorpus = np.concatenate((JDVtext1.job_desc.values, SylVtext2.Description.values))

print(EntireCorpus.shape , len(EntireCorpus))

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


indextoword = {v:k for k,v in wordtoindex.items()}


#intialising JD-values and Syllabus-values to zeros
JDVhashed = np.zeros((len(JDVtext1) , len(wordtoindex)))
SylVhashed = np.zeros((len(SylVtext2) , len(wordtoindex))) 

#To have an encoded JD-Value vector where there are 6131 JDS and 1400 Word-To-Index Values
for i,sentence in enumerate(JDVtext1.job_desc):
    wordlist = sentence.split()
    for word in wordlist:
        if word in wordtoindex:
            index = wordtoindex[word]
            JDVhashed[i][index] = 1

#To have an encoded Syl-Value vector

for i,sentence in enumerate(SylVtext2.Description):
    wordlist = sentence.split()
    for word in wordlist:
        if word in wordtoindex:
            index = wordtoindex[word]
            SylVhashed[i][index] = 1

#Cosine Similarity Scores
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

score = ((cosine_similarity(JDVhashed, SylVhashed)))

print(score.shape)

# For finding out index of most common word omitted from JD 
missing_words_array = []
job_positions = []
for i,sub in tqdm(enumerate(SylVhashed)): 
   
    top_jd_indices = np.argpartition(score[:,i] , -100)[-100:]
    print(len(top_jd_indices))
    top_jds = JDVhashed[top_jd_indices]
    diff = sub - top_jds
    diff = (np.sum(diff , axis = 0))
    
    words = [indextoword[num] for num in range(3123)]
    position = JDVtext1.loc[top_jd_indices]['position']

    words_dict = {word:num for word,num in zip(words , diff)}
    missing_words = (sorted(words_dict , key= lambda a : words_dict[a])[:20])
    missing_words_array.append(missing_words)
    job_positions.append(position.values)
    
    
SylVtext2['missing words'] = missing_words_array
SylVtext2['job positions'] = job_positions
print(SylVtext2['job positions'])

SylVtext2.to_csv('./Syllabus_with_missing_words.csv' , sep = '|')

print((score.shape) , (JDVhashed.shape) , (SylVhashed.shape))



avg_score = np.mean(score , axis = 0)
max_score = np.max(score , axis = 0)

fig , (ax1 , ax2) = plt.subplots(1,2)

ax1.bar(SylVtext2.Subject, avg_score*100)
ax1.tick_params(labelrotation = 90)
ax1.title.set_text('Average Similarity')

ax2.bar(SylVtext2.Subject , max_score*100)
ax2.tick_params(labelrotation = 90 )
ax2.title.set_text('Maximum Similarity')

plt.show()

score = np.max(score)
print("Similarity Score: {}" .format(score))
print("Average Similarity Percentage: {}%" .format((np.mean(score))*100))
print("Dissimilarity Percentage: {}%" .format((1-np.max(score))*100))

print("The syllabus is {}% closer to the industry." .format(score*100))
