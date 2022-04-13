# FYP - Final Year Project
**Problem Statement:** University-Curriculum Analysis based on entry level based job description.
## Directories iPython notebooks for Exploratory Data Analysis
### 1. Legacy
1. DataPreparation [directory]:
* EDA [directory]: Directory for Exploratory Data Analysis
 >EDA.ipynb | EDA_updated.ipynb
* ProcessedData [directory]: Directory for Processed Dataset
> pros_Dataset.csv | pros_Dataset2.csv
2. Scripts:
* Scrape.py : Python script to scrape the data
* SimilarityScore.py : Python script to find the similarity score between syllabus and JD

### 2. Dataset
1. csv_files [directory]: Contains the scraped JD dataset from naukri.com
2. dataset.csv: Final JD Dataset
3. ScriptToMergeDataset.ipynb.ipynb: Notebook file to merge all the scraped data from naukri.com
4. Syllabus_Dataset.csv: Contains syllabus key words and description
5. uselessWords [directory]: Contains the list of useless words
    * uselessWordsRemoval.ipyb : Notebook to remove useless words 
    * useless_words.txt : Combined list of all useless words
6. word_removal_helper.py : A script to assist in adding useless words to the file. Documentation can be found in the file itself
7. dataset_excel.xlsx : JD Dataset in excel format for better readability



### 3. Others
1. Phase 0 powerpoint presentation pdf

## Dependencies
1. Pandas
2. Selenium
3. Python
4. iPython

## Authors
1. Nikita Kodkany
2. Nischal Kanishk
3. Prathamesh Koranne
4. Prithvi Gudodagi
