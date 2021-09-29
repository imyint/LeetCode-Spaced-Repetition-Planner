# LeetCode-Spaced-Repetition-Planner
This program utilizes Selenium and the unofficial [Notion API](https://github.com/jamalex/notion-py) to pull completed problems from LeetCode and insert them into a Notion calendar on a spaced repetition schedule. 

# How To Use
Clone the repo and open up `Leetcode_spaced_repetition_planner.py`. Inside, you will find variables that you'll need to provide values for: your LeetCode username and password, number of desired days between each spaced repetition, your Notion token and calendar URL, and desired schedule for the program to run. To obtain your Notion token, sign into the Notion workspace containing your calendar. Open the developer console and navigate to Cookies. Your token is the value under 'token_v2'.

# Install Dependencies
`pip install -r requirements.txt`

# Other Notes
- The Notion URL you provide must link to a full page, not inline, calendar for this program to run.
- This program only pulls problems that have been completed on the current day so you can schedule your repetitions as you work through problems, but this can be adjusted as needed.
