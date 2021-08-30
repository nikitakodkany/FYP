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
There are a few known errors (which are handled in the code, dont worry much about the log messages.) that occur due to Naukri.com's servers. The pages that could not be scraped because of that, will be added to a new file and saved.After one is done with their chunk, they should go back to those numbers and rescrape them.

You may have to play around with the numbers in driver.implicit_wait() based on your network connection. Incase your network is slow , increase it.
To confirm whether it is a network issue or if it is a script issue , comment out line 19 and see the it in action.

Contact Prathamesh incase of any errors in the script Scrape.py.
