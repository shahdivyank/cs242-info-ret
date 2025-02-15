import glob
import json

files = glob.glob("../job_listings_by_role*.json")

data = []

for file in files:
    with open(file, "r") as contents:
        jobs = json.load(contents)

        for job in jobs:
            data.append(job)
    
with open("data.json", "w") as file:
    json.dump(data, file, indent=4) 