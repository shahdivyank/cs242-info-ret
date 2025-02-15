@echo off

echo Installing packages
pip install selenium 
pip install selenium webdriver-manager
pip install requests
pip install beautifulsoup4

if not exist jobspressoLinks.json echo [] > jobspressoLinks.json
if not exist jobspressoJobs.json echo [] > jobspressoJobs.json

if not exist remoteokLinks.json echo [] > remoteokLinks.json
if not exist remoteokJobs.json echo [] > remoteokJobs.json

echo Running jobspressoScraper.py
python jobspressoScraper.py

echo Running remoteok.py
python remoteok.py

echo Done