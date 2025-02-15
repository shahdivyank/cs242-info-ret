@echo off


echo Installing packages
pip install selenium fake-useragent
pip install selenium webdriver-manager


echo Running new_script_jobs_save.py
python .\new_script_jobs_save.py

echo Done
pause