from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os

CHROMEDRIVER_PATH = "/home/maxmin2127/Documents/projects/data-science-network-analysis/chromedriver.exe"

def get_driver(url):
    try:
        # access chrome driver
        service = Service(executable_path = CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service = service)
        driver.get(url)
    except Exception as e:
        print("Error: ", e)
    return driver

def get_job_site(job_title):
    try:
        job_title = job_title.replace(" ", "-").lower()
        url = f"https://ph.jobstreet.com/career-advice/role/{job_title}"

        # use webdriver to run site
        driver = get_driver(url)
        return driver
        
    except Exception as e:
        print("Error: ", e)

### List of Job Titles related to Data Science ###

JOB_TITLE_LIST = ["Business Analyst", 
                  "Machine Learning Engineer", 
                  "Data Scientist", 
                  "Data Analyst", 
                  "Automation Engineer"  
                ]

def main():
    jobs = []

    for job_title in JOB_TITLE_LIST:
        # scrape jobstreet for skills required for each job
        driver = get_job_site(job_title)
        src = driver.page_source
        soup = BeautifulSoup(src, features = "html.parser")

        try:
            # collect skills needed for the job title
            skills = soup.select('.mwre990.u0b8ch59.u0b8chh9.u0b8chgh.u0b8ch6t.u0b8chhp.o1zlst0')[3]
            for skill in skills:
                # append as a row in the table
                jobs.append([job_title, skill.get_text().strip()])

        except Exception as e:
            print("Error: ", e)

        driver.quit()

    
    # convert to dataframe
    df = pd.DataFrame(jobs, columns=["Job Title", "Skill"])

    # save to csv
    os.makedirs("data", exist_ok=True)

    df.to_csv("data/job_titles.csv", index=False)
    print("Jobs successfully saved in data/job_titles.csv!")
    
if __name__ == "__main__":
    main()