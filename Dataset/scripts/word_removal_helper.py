"""
    This is a helper function to aid in the removal of useless words. Run the file and keep typing the words as you encounter them. 
    press Ctrl+C to exit. The words you have typed will automatically get saved into a list
"""



import signal 
import sys 

file = open('./words_list.txt' , 'r+')
existing_words = file.read().splitlines()
words = set(existing_words)


def signal_handler(sig,frame):
    with open('./words_list.txt', 'w') as file:
        file.write('\n'.join(words) + '\n')
  
    sys.exit()
signal.signal(signal.SIGINT , signal_handler)


while True:
    word = str(input("Enter the word:- ")).strip(' ')
    words.add(word)
    


