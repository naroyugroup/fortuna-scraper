from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json
import time
import consts
 
service = Service(executable_path="chromedriver.exe")
browser = uc.Chrome(service=service)
browser.get("https://www.ifortuna.cz/")

time.sleep(2)

# Accept cookies
try:
    browser.find_element(By.XPATH, "//button[@id='cookie-consent-button-accept']").click()
except: pass

# Log In
logInModal = browser.find_element(By.XPATH, "//div[@id='login-mounted']")
logInModal.click()

emailInput = browser.find_element(By.XPATH, "//input[@id='login-dialog-input-name']")
emailInput.send_keys(consts.EMAIL)

passwordInput = browser.find_element(By.XPATH, "//input[@id='login-dialog-input-password']")
passwordInput.send_keys(consts.PASSWORD)

logInButton = browser.find_element(By.XPATH, "//button[@id='login-dialog-sign-in']")
logInButton.click()

time.sleep(2)

# Set filter to "Dnes"
browser.find_element(By.XPATH, '//*[@id="offer_filter_box"]/div[1]/div[2]/div[1]/div[2]').click()
browser.find_element(By.XPATH, '//*[@id="offer_filter_box"]/div[1]/div[2]/div[1]/div[3]/div/ul/li[6]').click()

time.sleep(2)

tables = browser.find_elements(By.XPATH, "//table[contains(@class, 'table') and contains(@class, 'events-table')]")

matchData = []

for table in tables:
    try:
        # Extract odds names
        tableHeadCol = table.find_elements(By.XPATH, ".//span[contains(@class, 'odds-name')]")
        tableBodyRows = table.find_elements(By.XPATH, ".//tbody/tr")
    
        for tableRow in tableBodyRows:
            try:
                # Extract match title
                title = tableRow.find_element(By.XPATH, ".//span[contains(@class, 'market-name')]")
                titleText = title.get_attribute("textContent").replace(" ", " ").strip()

                odds = {}
                # Extract odds values
                cols = tableRow.find_elements(By.XPATH, ".//span[contains(@class, 'odds-value')]")
                for colIndx, col in enumerate(cols):
                    odds[tableHeadCol[colIndx].get_attribute("textContent").replace(" ", " ").strip()] = col.get_attribute("textContent").replace(" ", " ").strip()
            
                # Append match data to the list
                matchData.append({
                    "title": titleText,
                    "date":  "Dnes",
                    "odds": odds
                })
            except: pass

    except: pass

# Create a dictionary with match data
data = {"matches": matchData}

# Write data to a JSON file
with open("fortuna-matches.json", "w") as jsonFile:
    json.dump(data, jsonFile, indent=4)

browser.quit()
