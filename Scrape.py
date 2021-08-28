from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import sys 
import pandas as pd 

df = pd.DataFrame()


url_head = "https://www.naukri.com/it-jobs-"
url_tail = "?k=it"

options = Options()
options.add_argument('--headless') 

driver = webdriver.Firefox(options=options)

x = 1
for i in range(1,18333):
    url = url_head+str(i)+url_tail

    driver.get(url)
    driver.implicitly_wait(5)
    elems = driver.find_elements_by_xpath('//*[@class="title fw500 ellipsis"]')

    job_urls = [x.get_attribute('href') for x in elems ]
    
    for j in range(20):
        try:
            driver.get(job_urls[j])

            position = driver.find_element_by_xpath('//header/h1[@class = "jd-header-title"]').text
            position = {'position' : position}

            salary = driver.find_element_by_xpath('//div[@class = "salary"]/span').text
            experience = driver.find_element_by_xpath('//div[@class = "exp"]/span').text
            job_desc = driver.find_element_by_xpath('//section[@class = "job-desc"]').text
            labels = driver.find_elements_by_xpath('//span[@class = "stat"]/label')
            label_contents = driver.find_elements_by_xpath('//span[@class = "stat"]/span')

            education_degree = driver.find_elements_by_xpath('//div[@class = "education"]/div[@class = "details"]/label')
            education_requirement = driver.find_elements_by_xpath('//div[@class = "education"]/div[@class = "details"]/span')

            education = {k.text:v.text for k,v in zip(education_degree,education_requirement)}

            key_skills = driver.find_elements_by_xpath('//a[@class = "chip clickable"]/span')
            key_skills = [x.text for x in key_skills]
            key_skills = {'key_skills': key_skills}
            stats = {k.text:v.text for k,v in zip(labels, label_contents)}

            salary = {'salary' :salary}
            experience = {'experience': experience}
            job_desc = {'job_desc' : job_desc}

            row = {**position , **salary , **experience , **job_desc , **stats , **key_skills , **education }
            
            df = df.append(row , ignore_index=True)
            sys.stdout.write("\r Added {0} rows to the record".format(x))
            sys.stdout.flush()
            x +=1
            
        except Exception as e:
            print(e)
           
        driver.implicitly_wait(3)
        

    break
df.to_csv('data.csv')
