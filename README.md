# PGN - Pointer Generator Networks

## Roadmap
![alt text](https://github.com/nikitakodkany/PGN/blob/main/DOCUMENTATION/RoadMap.png)

## Data Scrapping Instructions
There are 18,333 pages to be scraped. 
Following are the numbers that you have to enter in your 'for loop'.
- 1-2600: Sumedha 
- 2601-5200: Rashmi
- 5201-7800: Varun
- 7801-10400: Sahil
- 10401-13000: Nikita
- 13001-15000: Prathamesh
- 15001-18333: Prathamesh

### Installation Details for Scrape.py
Install Geckodriver and Firefox. Add Geckodriver to the path.

**Dependencies** 
1. Pandas
2. Selenium

**Usage**
Line No. 20 contains the range from which each person will have to scrape as alloted above. The script is recommended to be run in chunks as it would be easier to manage.

Everytime a chunk is run, change the name of the CSV file in the last line, else, the file will be overwritten. Remove the break at the end and please test it before running the script for a longer chunk of the data.

Contact Prathamesh incase of any errors in the script Scrape.py.
