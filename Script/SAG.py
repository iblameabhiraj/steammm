# 01.03.2023
# Version 1.3 - tested only on windows 10
# Author: Lilkajt
# discord: lilkajt#6121
import time
from discord import SyncWebhook
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import string
import random
import keyboard as BasicBoard
import pandas as pd
import os
from win10toast import ToastNotifier
toast = ToastNotifier()

token = '' # Put here your discord webhook to receive successfuly created accounts details.
webhook = SyncWebhook.from_url(token)
url = "https://store.steampowered.com/join"
region = "ARS" # region where you create accounts
Limit = 1 #How many accounts you want to generate

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email():
    username = random_string(8)
    domain = "your-domain" #change to your domain
    return f"{username}@{domain}"

def random_password(length):
    return random_string(length)

def Notification(Type = "reCaptcha" or "email" or "name"):
    while True:
        if Type == "email":
            key = "m"
        elif Type == "reCaptcha":
            key = "c"
        else:
            key = "n"
        toast.show_toast(
            f"Check {Type} Steam",
            f"Press \"{key}\" to continue!",
            duration = 10,
            threaded = True,
        )
        if (toast.notification_active()):
            if (BasicBoard.is_pressed(key)):
                break

def Name_check(driver, basic = None):
    if (driver.find_element(By.ID, 'accountname_availability').text == "Not Available"):
        Notification("name")
        username = driver.find_element(By.XPATH, '//*[@id="accountname"]').text
        return str(username)
    else:
        return str(basic)

def ExcelFile(email, username,password):
    data = {"Email": email, "Username": username, "Password": password}
    df = pd.DataFrame(data, index=[0])
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}\\{region}_accounts.xlsx"

    if not os.path.exists(file_path):
        df.to_excel(file_path,sheet_name="Accounts",index=False)
    else:
        with pd.ExcelWriter(file_path,mode='a',engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer,sheet_name="Accounts",startrow=writer.sheets["Accounts"].max_row,index=False, header=False)

def Create_steam_account():
    email = random_email()
    username = email.split("@")[0]
    password = random_password(16)
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_email"]').click()
    for x in email: driver.find_element(By.XPATH, '//*[@id="reenter_email"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="i_agree_check"]').click()
    Notification("reCaptcha")
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    print("Creating Account - confirm mail")
    Notification("email")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="accountname"]').click()
    for x in username: driver.find_element(By.XPATH, '//*[@id="accountname"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="reenter_password"]').click()
    for x in password: driver.find_element(By.XPATH, '//*[@id="reenter_password"]').send_keys(x), time.sleep(np.random.uniform(0,0.1))
    username = Name_check(driver, basic=username)
    time.sleep(0.5)
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    time.sleep(4)
    print("Account succesfuly created")
    ExcelFile(email,username,password)
    webhook.send(f"Steam account created\nEmail: {email}\nUsername: {username}\nPassword: {password}")
    driver.close()

try:
    Count = 0
    while (Count < Limit):
        Create_steam_account()
        time.sleep(1)
        Count +=1
        print(f"Accounts generated: {Count}")
except Exception as err:
    print(err)