import glob
import json

files = glob.glob("../job_listings_by_role*.json")

data = []

for file in files:
    with open(file, "r", encoding="utf-8", errors="ignore") as contents:
        try:
            jobs = json.load(contents)
            for job in jobs:
                data.append(job)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {file}: {e}")
    
with open("data.json", "w") as file:
    json.dump(data, file, indent=4) 