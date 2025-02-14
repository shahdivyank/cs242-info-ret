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

BASE_URL = "https://jobspresso.co/remote-work/"


HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }


def getJobLinks(tries):
    jobLinks = set()

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    if tries == "infinite":
        while True:
            try:
                loadMore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "load_more_jobs")))
                driver.execute_script("arguments[0].click();", loadMore)
                time.sleep(3)
            except Exception:
                print("No more jobs to load.")
                break 
    else:
        for i in range(tries):
            try:
                loadMore = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "load_more_jobs")))
                driver.execute_script("arguments[0].click();", loadMore)
                time.sleep(3)
            except Exception:
                print("No more jobs to load.")
                break 


    jobListings = driver.find_elements(By.CSS_SELECTOR, "ul.job_listings li.job_listing")
    for job in jobListings:
        jobUrl = job.get_attribute("data-href")
        if jobUrl:
            jobLinks.add(jobUrl)
    
    print(f"{len(jobLinks)} job links.")
    
    with open("jobspressoLinks.json", "r+", encoding="utf-8") as file:
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
    response = requests.get(jobUrl, headers=HEADERS)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", class_="page-title").get_text(strip=True) if soup.find("h1", class_="page-title") else "N/A"
        company = soup.find("li", class_="job-company").get_text(strip=True) if soup.find("li", class_="job-company") else "N/A"
        location = soup.find("li", class_="location").get_text(strip=True) if soup.find("li", class_="location") else "N/A"
        date = soup.find("li", class_="date-posted").get_text(strip=True) if soup.find("li", class_="date-pposted") else "N/A"
        job_description = soup.find("div", class_="job-overview-content row").get_text("\n", strip=True) if soup.find("div", class_="job-overview-content row") else "N/A"
        appUrl = soup.find("a", class_="application_button_link")
        appUrl = appUrl["href"] if appUrl else "N/A"

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
        
        with open("jobspressoJobs.json", "r+", encoding="utf-8") as file:
            try:
                jobs = json.load(file)
            except json.JSONDecodeError:
                jobs = []
            
            jobs.append(job)
            file.seek(0)
            json.dump(jobs, file, indent=4, ensure_ascii=False)

        return job
    
    return None

jobsFound = getJobLinks(1)
print(jobsFound)

with open("jobspressoLinks.json", "r", encoding="utf-8") as file:
    jobsFound = json.load(file)

for link in jobsFound:
    getJobDetails(link)


# getJobDetails("https://jobspresso.co/job/technical-customer-support-advocate/")