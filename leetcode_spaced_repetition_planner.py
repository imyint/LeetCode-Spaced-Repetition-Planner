import sys
import time
import schedule
import dateparser

from datetime import timedelta, date
from notion.client import NotionClient
from selenium import webdriver
from selenium.webdriver.common.by import By


# Replace with LeetCode username and password
NAME = ''
PASSWORD = ''

# This will hold accepted problems from the current day
ac_leetcode_problems = []

# Replace with the desired number of days between each spaced repetition 
spaced_rep_days = [1, 3, 7, 14]

# Install and import needed packages if using webdriver for Chrome, Firefox, etc.
driver = webdriver.Safari()



def login(name=None, pwd=None):

    login_url = 'https://leetcode.com/accounts/login/'
    if name is not None and pwd is not None:
        driver.get(login_url)
        
        usernameField = driver.find_element_by_id("id_login")
        usernameField.send_keys(NAME)
        time.sleep(1)

        passwordField = driver.find_element_by_id("id_password") 
        passwordField.send_keys(PASSWORD)
        time.sleep(1)

        signinBtn = driver.find_element_by_xpath("//*[@id='signin_btn']")
        driver.execute_script("arguments[0].click();", signinBtn)
        time.sleep(2)    
        return True
    else:
        return None 


     
def get_ac_problems():

    leetcode_submission_link = "https://leetcode.com/submissions/" 
    driver.get(leetcode_submission_link)
    time.sleep(3)

    try:
        if driver.find_element_by_id("submission-list-app"):
            print("Submissions loaded.")
            print()
    except Exception as e:  
        print("Submissions could not be loaded.")
        sys.exit()

    while(True):
        tbody = driver.find_element_by_id("submission-list-app").find_element(By.TAG_NAME, "tbody")
        tr = tbody.find_elements(By.TAG_NAME, "tr")
        for row in tr:
            time_submitted = row.find_elements(By.TAG_NAME, "td")[0].text
            question = row.find_elements(By.TAG_NAME, "td")[1].text
            status_val = row.find_elements(By.TAG_NAME, "td")[2]   
            status = status_val.find_elements(By.TAG_NAME, "strong")[0].text   # Extract status from status column

            # Only pulling newly solved problems (<24 hours)
            if dateparser.parse(time_submitted).date() == date.today() and status == "Accepted":
                ac_leetcode_problems.append(question)
                
        try:
            # Load next submission page
            next_page = driver.find_elements_by_class_name("next")[0].find_element(By.TAG_NAME, "a").get_attribute('href')
            driver.get(next_page)
            time.sleep(3)
        except Exception as e:
            break  



def send_to_notion():
     # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
    token = ''
    client = NotionClient(token_v2=token)
            
    # Replace with the URL of the Notion page that contains your calendar (must be full page)
    cal_url = ''
    cal = client.get_collection_view(cal_url)

    for problem in ac_leetcode_problems:
        for day in spaced_rep_days:
            notion_event = cal.collection.add_row()
            notion_event.name = problem
            notion_event.date = date.today() + timedelta(days=day)



def script():
    if login(NAME, PASSWORD):
        get_ac_problems()
        send_to_notion()
        driver.quit()



if __name__ == '__main__':
   # Replace with day/time you would like script to check for new problems
   schedule.every().day.at('').do(script)

   while True:  
       schedule.run_pending()
       time.sleep(1)
   


