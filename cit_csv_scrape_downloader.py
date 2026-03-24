from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import requests
import time
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv

# Logging into CiT Bank Account and downloading csv
def cit_login():

    # Getting username and password
    load_dotenv()
    username = os.getenv("CIT_USER")
    password = os.getenv("CIT_PASS")
    not_have_otp = True

    # Initiating driver
    driver = webdriver.Firefox()

    # Giving the driver the logon website
    driver.get("https://secure.citbank.com/CITConsumer/#/Login")

    # Waiting before checking if we are in or OTP
    time.sleep(4)

    # Finding User ID Label and grabbing the widget number for the textbox from there
    user_id_textbox_from_label = driver.find_element(By.XPATH, "//label[contains(text(), 'User ID')]").get_attribute("for")

    # Inputting User ID
    driver.find_element(
       "xpath", '//*[@id="'+user_id_textbox_from_label+'"]').send_keys(username)

    # Finding Password Label and grabbing the widget number for the textbox from there
    user_pass_textbox_from_label = driver.find_element(By.XPATH, "//label[contains(text(), 'Password')]").get_attribute("for")

    # Inputting password
    driver.find_element(
       "xpath", '//*[@id="'+user_pass_textbox_from_label+'"]').send_keys(password)

    # Clicking the Sign In Button
    # Finds the button specifically by its aria-label
    driver.find_element(By.CSS_SELECTOR, "button[aria-label='Sign in']").click()
    
    # Waiting before checking if we are in or OTP
    time.sleep(10)

    # Grabbing current url
    curr_url = driver.current_url

    # If it asks us for an OTP code
    if "OtpChoice" in curr_url:

        # Clicking the Send SMS Button
        driver.find_element(By.XPATH, "//label[contains(text(), 'Send SMS')]").click()

        # Waiting to get OPT code
        while not_have_otp:

            # Filepath for the MFA Token
            mfa_filename = "/home/tcaetano/Documents/Repos/bank-tracker-scraper/mfa.txt"
            file_path = Path(mfa_filename)

            # Waiting for the token file to be created and grabbing it
            if file_path.is_file():
                not_have_otp = False
                try:
                    with open(mfa_filename, 'r') as f:
                        mfa_code = f.readline()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return None
        
        # Deleting the mfa file
        os.remove(mfa_filename)
        
        # Inputting MFA Token
        driver.find_element(By.CSS_SELECTOR, "input[aria-label='first digit pin']").send_keys(mfa_code)

        # Clicking the Continue Button
        driver.find_element(
            "xpath", '/html/body/app-root/app-page-validateotpandpassword/div/main/div/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div[3]/div/form/div/div[2]/button').click()

        # Waiting to load into the account
        time.sleep(15)

        # Clicking into the Platinum Savings
        driver.find_element(By.XPATH, "//label[contains(text(), 'Platinum Savings')]").click()

        # Waiting to load into the savings account
        time.sleep(10)

        # Clicking the Download Button
        driver.find_element(By.CSS_SELECTOR, "button[aria-label='Download Transactions']").click()

        # Waiting for the download screen to appear
        time.sleep(2)

        # Clicking into the Export Button
        driver.find_element(By.CSS_SELECTOR, "button[aria-label='Export']").click()

        # Waiting for download to finish
        time.sleep(5)

    # Closing window
    driver.close()
   
cit_login()

