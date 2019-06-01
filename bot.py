from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import datetime
import os
import sys
import csv
import json
import Tkinter

actionChains = None
browser = None
Contact = None
message = None
messages = None
conn = None
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None
media = None

send_config = [
    {
        "type": "message",
        "data": "Bot Message",
    },
    {
        "type": "message",
        "data": "Bot Message 1"
    },
    {
        "type": "image",
        "data": "instagram.png"
    },
    {
        "type": "message",
        "data": "Bot messages 2"
    },
    {
        "type": "message",
        "data": "Bot Messages 3"
    },
]

def whatsappLogin():
    global wait,browser,Link
    browser = webdriver.Chrome()
    actionChains = ActionChains(browser)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR scanned")

def selectContact(number):
    global wait, browser, actionChains
    # x_arg = '//span[contains(@title,' + contact + ')]'
    search_box = browser.find_element_by_xpath('//input[contains(@class, "_2zCfw")]')
    search_box.click()
    search_box.clear()
    
    for ch in str(number):
        search_box.send_keys(ch)

    time.sleep(2)
    
    options = browser.find_elements_by_xpath('//div[contains(@class, "X7YrQ")]')
    option = options[-1]
    option.click()

    try:
        input_box = browser.find_element_by_class_name("_13mgZ")
    except NoSuchElementException:
        o = options[2]
        o.click()

def sendMessage(message):
    global wait, browser
    try:
        input_box = browser.find_element_by_class_name("_13mgZ")

        for ch in message:
            if ch == "\n":
                btnSend = browser.find_element_by_class_name("_3M-N-")
                btnSend.click()
            else:
                input_box.send_keys(ch)

        input_box.send_keys(Keys.ENTER)
        print("Message sent")
        # time.sleep(5)
    except NoSuchElementException as err:
        print("No such element exception" + str(err))
        return

def sendImage(img): # img - name of image along with ext
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    mediaButtonInput = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input')
    
    image_path = os.getcwd() + '/Media/' + img

    mediaButtonInput.send_keys(image_path)

    time.sleep(3)
    whatsapp_send_button = browser.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()
    # Controlling windows dialog
    
def sendFile(filename):
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send a Document(PDF, Word file, PPT)
    docButton = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button')
    docButton.click()
    time.sleep(1)

    docPath = os.getcwd() + "\\Documents\\" + filename

    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", (docPath))
    autoit.control_click("Open", "Button1")

    time.sleep(3)
    whatsapp_send_button = browser.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    whatsapp_send_button.click()
    print('Sent Image')

def main():
    global browser
    messageConfig = json.loads(json.dumps(send_config))
    whatsappLogin()
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "_2zCfw")]')))
    with open('test.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        
        for row in reader:
            try:
                selectContact(row[0])
                obj = json.loads(json.dumps(send_config))
                for msg in obj:
                    if msg['type'] == 'message':
                        sendMessage(msg['data'])
                        time.sleep(2)
                    elif msg['type'] == 'image':
                        sendImage(msg['data'])
                        time.sleep(2)
            except Exception as e:
                print(e)
                pass

        browser.quit()

if __name__ == '__main__':
    main()