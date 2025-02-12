import json
import time
import random
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor, as_completed


from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent

def C_driver():
    ua = UserAgent()
    random_user_agent = ua.random
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    firefox_options.set_preference("general.useragent.override", random_user_agent)
    firefox_options.set_preference("intl.accept_languages", "en-US, en;q=0.9")
    firefox_options.set_preference("network.http.referer-XOriginPolicy", 0)
    firefox_options.set_preference("network.http.referer.spoofSource", True)
    firefox_options.set_preference("privacy.donottrackheader.enabled", True)
    firefox_options.set_preference("network.http.keep-alive", True)
    service = Service("C:\\Program Files\\geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver

def human_like_scroll(driver):
    """Simulates a human-like scroll behavior to prevent bot detection."""
    for _ in range(random.randint(3, 5)):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(1, 2))

def anti_bot_wait():
    """Randomized sleep time to reduce bot suspicion."""
    wait_time = random.uniform(1, 3)
    print(f"Waiting {wait_time:.2f} seconds to avoid detection...")
    time.sleep(wait_time)

def extract_section(text, start_marker, end_marker):
    try:
        start_index = text.find(start_marker)
        if start_index == -1:
            return "Section not found"
        start_index += len(start_marker)
        end_index = text.find(end_marker, start_index)
        if end_index == -1:
            return text[start_index:].strip()
        return text[start_index:end_index].strip()
    except Exception as e:
        return f"Error extracting section: {e}"

def scrape_job_details(driver, link_index = 0):
    try:
        time.sleep(random.uniform(2, 4))
        job_title_element = driver.find_element(By.CSS_SELECTOR, "h1.font-bold.text-primary.text-header-md")
        job_title = job_title_element.text
        job_description_element = driver.find_element(By.CSS_SELECTOR, "div.text-primary.whitespace-pre-line.break-words")
        job_description = job_description_element.text
        responsibilities = extract_section(job_description, "About the Role", "About You")
        qualifications = extract_section(job_description, "Minimum Qualifications", "Preferred Qualifications")
        preferred_qualifications = extract_section(job_description, "Preferred Qualifications", "What You’ll Get")
        full_qualifications = f"{qualifications}\n\n{preferred_qualifications}"
        try:
            location_element = driver.find_element(By.CSS_SELECTOR, "div.mb-24 p.text-primary.normal-case.text-body-md")
            location = location_element.text.strip()
        except Exception as e:
            location = "Location not found"
            print(f"Error extracting location: {str(e)}")
        print(location)
        try:
            job_link_element = driver.find_elements(By.CSS_SELECTOR, "h2.font-bold.text-primary.text-header-sm a")
            href = job_link_element[link_index].get_attribute("href")
            print(href)
        except Exception as e:
            href = "Application link not found"
            print(f"Error: {str(e)}")
        print(f"Application Link ID: {href}")
        job_data = {
            "Qualification": full_qualifications,
            "Description": job_description,
            "Title": job_title,
            "Responsibility": responsibilities,
            "Application Link": href,
            "Location" : location,
        }
        return job_data
    except Exception as e:
        print(f"Error scraping job details: {e}")
        return None

def click_and_scrape_jobs(driver):
    job_listings = []
    job_elements = driver.find_elements(By.CLASS_NAME, "job_result_two_pane")
    link_index = 0
    for job_element in job_elements:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", job_element)
            time.sleep(random.uniform(1, 2))
            job_title_link = job_element.find_element(By.CSS_SELECTOR, "h2.font-bold.text-primary.text-header-sm a")
            ActionChains(driver).move_to_element(job_title_link).click().perform()
            print(f"Clicked on job: {job_element.text[:50]}...")
            job_data = scrape_job_details(driver,link_index)
            if job_data:
                job_listings.append(job_data)
            link_index+=1
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Error clicking job: {e}")
            continue
    return job_listings

def scrape_ziprecruiter(role, location,max_pages=60):
    print("Starting Web Scraping...")
    driver = C_driver()
    role_url = f"https://www.ziprecruiter.com/jobs-search?search={role.replace(' ', '+')}&location={location.replace(' ', '+')}+%28USA%29"
    driver.get(role_url)
    job_listings = []
    anti_bot_wait()
    human_like_scroll(driver)
    for page in range(max_pages):
        print(f" Scraping Page {page + 1}...")
        time.sleep(random.uniform(2, 3))
        job_listings.extend(click_and_scrape_jobs(driver))

        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, "a[title='Next Page']")
            next_page_url = next_page_button.get_attribute("href")
            print(f"➡️ Moving to Next Page: {next_page_url}")
            driver.get(next_page_url)
            anti_bot_wait()
            human_like_scroll(driver)
        except Exception:
            print("No more pages found, stopping pagination.")
            break


    # json_filename = "job_listings.json"
    # with open(json_filename, "w", encoding="utf-8") as json_file:
    #     json.dump(job_listings, json_file, indent=4, ensure_ascii=False)
    # print(f" JSON file '{json_filename}' generated successfully!")
    driver.quit()
    return job_listings

def multi_threaded_JR(job_roles , locations, max_workers=4):
    job_listings = []
    with ThreadPoolExecutor(max_workers = max_workers) as executor:
        rbj = {
        executor.submit(scrape_ziprecruiter, role, location): (role,location)
        for role in job_roles for location in locations
        }
        for future in as_completed(rbj):
            role = rbj[future]
            try:
                jl = future.result()
                job_listings.extend(jl)
            except Exception as e:
                print(f"Job role '{role}' generated an exception: {e}")
    return job_listings






url = "https://www.ziprecruiter.com/jobs-search?search=software+engineer&location=CA+%28USA%29"
job_roles = ["software engineer","developer engineer","data analyst"]
locations = ["GA","PA"]
# job_listings = scrape_ziprecruiter(url)
job_listings = multi_threaded_JR(job_roles,locations, 3)
json_filename = "job_listings_by_role_v3.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(job_listings, json_file, indent=4, ensure_ascii=False)
print(f"JSON file '{json_filename}' generated successfully!")