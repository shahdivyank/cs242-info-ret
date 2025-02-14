import requests
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://remoteok.com/?compact=true&order_by=date"


HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def getJobLinks():
    jobLinks = set()

    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless") 
    # # options.add_argument("--no-sandbox")
    # # options.add_argument("--disable-dev-shm-usage")

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 5)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#jobsboard tr.job")))

    previous_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust if needed

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == previous_height:
            print("No more jobs to load.")
            break
        previous_height = new_height

    jobListings = driver.find_elements(By.CSS_SELECTOR, "table#jobsboard tr.job a.preventLink")
    for job in jobListings:
        jobUrl = job.get_attribute("href")
        if jobUrl:
            jobLinks.add(jobUrl)

    print(f"Found {len(jobLinks)} job links.")

    with open("remoteokLinks.json", "r+", encoding="utf-8") as file:
        try:
            existingLinks = json.load(file)
        except json.JSONDecodeError:
            existingLinks = []
        
        allLinks = list(set(existingLinks + list(jobLinks)))

        file.seek(0)
        json.dump(allLinks, file, indent=4, ensure_ascii=False)

    driver.quit()
    return jobLinks


def getJobDetails(jobUrl):

    driver.get(jobUrl)

    time.sleep(1)

    

    print("Parsing: ", jobUrl)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = soup.find("h2", itemprop = "title").get_text(strip=True) if soup.find("h2", itemprop = "title") else "N/A"

    company_element = soup.find("div", class_="company_profile")
    if company_element:
        company = company_element.find("h2").get_text(strip=True) if company_element.find("h2") else "N/A"
    else:
        company = "N/A"

    location = soup.find("div", class_="location").get_text(strip=True) if soup.find("div", class_="location") else "N/A"
    date = soup.find("li", class_="date-posted").get_text(strip=True) if soup.find("li", class_="date-pposted") else "N/A"
    job_description = soup.find("div", class_="markdown").get_text("\n", strip=True) if soup.find("div", class_="markdown") else "N/A"
    appUrl = "N/A"

    if soup.find("li", class_="job_listing-company-social company-social"):
        socialLinks = soup.find("ul", class_="job_listing-company-social company-social") 
        socialLinks = {a["class"][0].replace("job_listing-", ""): a["href"] for a in socialLinks.find_all("a")}
    else:
        socialLinks = "N/A"
    

    job = {
        "title": title,
        "company": company,
        "location": location,
        "date posted" : date,
        "description": job_description,
        "Application": appUrl,
        "url": jobUrl,
        "socials" : socialLinks
    }
    
    with open("remoteokJobs.json", "r+", encoding="utf-8") as file:
        try:
            jobs = json.load(file)
        except json.JSONDecodeError:
            jobs = []
        
        jobs.append(job)
        file.seek(0)
        json.dump(jobs, file, indent=4, ensure_ascii=False)

    return job


# jobsFound = getJobLinks()
# print(jobsFound)

with open("remoteokLinks.json", "r", encoding="utf-8") as file:
    jobsFound = json.load(file)

for link in jobsFound:
    getJobDetails(link)

# getJobDetails("https://remoteok.com/remote-jobs/remote-fx-artist-ingenuity-studios-696327")