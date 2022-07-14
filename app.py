from cgi import print_form
from doctest import master
import json
from ssl import AlertDescription
import string
import re
import bcrypt
from bson import ObjectId
from flask import (Flask, flash, redirect, render_template, request, session, url_for)
from pymongo import MongoClient
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from audioop import avg
import csv
from inspect import CO_COROUTINE
import math
import random
from tarfile import SYMTYPE
from xml.sax.handler import EntityResolver
import pandas as pd
from torch import int8
from tqdm import tqdm
import itertools
import numpy as np
from collections import Counter


app  = Flask(__name__)
app.secret_key = "super secret key"

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['organizationdata']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logindata', methods =["GET", "POST"])
def logindata():
    loginuser = db.orgdata.find_one({'email' : request.form['email']})

    if loginuser:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), loginuser['password']) == loginuser['password']:
            session['email'] = request.form['email']
            return redirect(url_for('dashboard'))

    return 'invalid username/password combination'




@app.route('/register', methods =["GET", "POST"])
def register():
    if request.method == 'POST':
        
        existing_user = db.orgdata.find_one({'email' : request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            db.orgdata.insert_one({'name' : request.form['name'], 'email' : request.form['email'] , 'password' : hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('dashboard'))
        else:
            return 'username exists'

    return render_template('register.html')    
        

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        username  = db.orgdata.find({'email': session['email']})
        syllabusdb = db.syllabusdata.find({'email': session['email']})
        return render_template('dashboard.html', sdata = syllabusdb, data = username)
    else:
        return redirect(url_for('index'))


@app.route('/syllabus')
def syllabus():
    if 'email' in session:
        return render_template('syllabus.html')
    else:
        return redirect(url_for('index'))       

@app.route('/syllabusdata', methods =["GET", "POST"])
def syllabusdata():
    db.syllabusdata.insert_one({'email' : session['email'],'syllabus' : request.form['syllabustext'], 'Subject' : request.form['option']})
    flash('syllabus uploaded successfully')
    return redirect(url_for('syllabus'))

@app.route('/addedsyllabus')
def addedsyllabus():
    username  = db.orgdata.find({'email': session['email']})
    syllabusdb = db.syllabusdata.find({'email': session['email']})
    return render_template('addedsyllabus.html', sdata = syllabusdb, data = username)

@app.route('/syllabusfile', methods = ['GET', 'POST'])
def syllabusfile(header=None):
    if request.method == 'POST': 
        file = request.files['syllabusfile']
        filename = secure_filename(file.filename)


        

        print(request.form['filetype'])
        if request.form['filetype'] == "Text":
            
            with open(filename) as f:
                filecontent = f.read()
                print(filecontent)
                db.syllabusdata.insert_one({'email' : session['email'] , 'syllabus' : filecontent, 'Subject' : request.form['option'] })
                return redirect(url_for('dashboard'))
        elif request.form['filetype'] == "Pdf":
            return " Available in future" 

@app.route("/perdata/<oid>")
def perdata(oid):
    sydata = db.syllabusdata.find_one({'_id': ObjectId(oid)})
    syllabus_subject = sydata['Subject']
    syllabus_data = sydata['syllabus']
    sd = syllabus_data.lower()
    
   

    #Open the appropriate dataset. This should change based on the subject.
    if syllabus_subject == 'Python':
        JDVtext1 = pd.read_excel('Dataset/dataset/Excel/processed_python_dataset.xlsx')
    elif syllabus_subject == 'Web Development':
        JDVtext1 = pd.read_excel('Dataset/dataset/Excel/processed_web_dataset.xlsx')

    #To open syllabus. Notice the format of the file as well. This is basically the file from the server
    # with open(syllabus_data, newline='') as f2:
    SylVtext2 = sd
   


    #Process the syllabus by removing punctuations and further remove the empty string formed
    SylVtext2 = [a.replace('\n' , '').replace('.','').replace(',' , '').replace('(' , '').replace(')' , '').replace(':' , '').replace('-','') for a in SylVtext2.split()]
 
    
    removed_digits = str.maketrans('','',string.digits)

    SylVtext2 = [a for a in SylVtext2 if a != '']
    SylVtext2 = [a.translate(removed_digits) for a in SylVtext2]
    SylVtext2 = [a.lower() for a in SylVtext2]
    SylVtext2.append('angular.js')
  

    #Create a corpus of all words that are present in the dataset+syallbus
    #EntireCorpus contains strings, which is basically every row incase of dataset and line in case of syllabus
    #Finally, corpus contains a list of every single word present in the dataset+syllabus
    # EntireCorpus = np.concatenate((JDVtext1.job_desc_processed.values, SylVtext2))
    
    corpus = set([word for line in JDVtext1.job_desc_processed.values for word in line.split()] + SylVtext2)
    

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
    syllabus_words = [word.lower() for word in SylVtext2]

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
    counters = [Counter() for _ in range(3)]

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
    
    
    print_data =str((common_words_count/30)*100)

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
    missing_words = (sorted(words_dict, key= lambda a : words_dict[a])[:len(words_dict)-len(SylVtext2)])
   

    #Repeat the same loop before
    counters_missing = [Counter() for _ in range(4)]
    for i in range(1,5):
        for sub_list in jds_decoded:
            r = i
            #BUT THE WORDS TO FIND COMBINATIONS FOR ARE ONLY THE WORDS THAT ARE COMMON BETWEEN A PARTICULAR JD AND THE MISSING WORDS DICT
            #The following list comprehension does exactly that
            w = [word for word in sub_list.split() if word in missing_words]
           
            #The rest of the loop is same as the previous loop

            a = itertools.combinations(np.unique(np.array(w)), r)
            counters_missing[i-1].update(a)

    techs = {'front-end':['html','xhtml ','boot strap','scss','ajax','dom','jquery','react.js','angular.js','vue.js','typescript','redux','flutter','css'],
             'databases':['mysql','mongodb','rdbms','redis','nosql'],
             'server-side programming': ['node.js','php','c++','java','python'],
             'backend framework':['express.js','codeigniter','laravel','cake','magento','meteor.js'],
             'server':['apache','iis','nginx'],
             'design':['xd','dreamweaver','illustrator','coreldraw','photoshop'],
             'cms': ['wordpress','joomla','drupal','plugins'],
             'project management':['github','mercurial','svn','git','jenkins','jira'],
            }
            # 'pwa':['ionic','polymer','lighthouse']

    expt_counter = {k:[Counter() for _ in range(5)] for k in techs.keys()}

    for i in range(1,6):

        r = i
        for sub_list in jds_decoded: 
            w = [word for word in np.unique(sub_list.split()) if word in missing_words]
            #x = [word for word in sub_list.split() if word not in missing_words]
            for tech_key,tech_value in techs.items():
                b = [word for word in w if word in tech_value]
               
                a = itertools.combinations(np.unique(np.array(b)) , r)
                expt_counter[tech_key][i-1].update(a)
    print('#######################################')
   
    
    # techStack = techs.keys()     
    # db.syllabusdata.update(
    # {"_id": ObjectId(oid)},
    # {"$set": {"Sug_syl":[list(techStack)]}}
    # )
    # for tech, occurences in expt_counter.items():
    #     for i in range(3):
    #             db.syllabusdata.update(
    #             {"_id": ObjectId(oid)},
    #             {"$push": {"Sug_syl":occurences[i].most_common(1)[0][0]}}
    #             )
    #             print(tech, occurences[i].most_common(1)[0][0])

    # techStack = techs.keys()
    # db.syllabusdata.update(
    # {"_id": ObjectId(oid)},
    # {"$set": {"Sug_syl":list(techStack)}}
    # )
    for tech, occurences in expt_counter.items():
        for i in range(3):
            if occurences[i]:
                db.syllabusdata.update(
                {"_id": ObjectId(oid)},
                {"$push": { f"Suggested.{tech}":occurences[i].most_common(1)[0][0]}}
                )
                print(tech, occurences[i].most_common(1)[0][0])
    
    # master_counter = {}
    # for counters in expt_counter:
    #     for counter in counters: 
    #         master_counter.update(counter)

    # a = itertools.combinations(master_counter.keys(),5)
    # num = 0
    # combis = []
    # for combi in a: 
    #     combi = list((itertools.chain(*combi)))

    #     if len(combi) == 5:
    #         combis.append(combi)
    #         num+=1
    
    # chosen = random.sample(combis , 20)
    # print(*chosen , sep = '\n')



    print("Most commonly co-occuring words missing from syllabus but present in JD are:-")
    for counter in counters_missing:
        print(counter.most_common(5) , end = '\n\n')
    print('----------------------------------------------------------')

    print("\n Most commonly occurring missing words are")
    #print(missing_words)

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

    return redirect("/results/" + oid)

@app.route("/results/<oid>")
def results(oid):
    sydata = db.syllabusdata.find({"_id": ObjectId(oid)})
    suggestedData = db.syllabusdata.find({"Suggested": ()})
    return render_template('results.html', sgd = suggestedData, syd = sydata)
    

   
if __name__ == '__main__':
    app.debug = True
    app.run()
