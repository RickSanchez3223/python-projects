from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import time


def get_drvier():
    # Set options to make browsing easier
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.get("http://automated.pythonanywhere.com/login")
    return driver


def formatt(data):
    return data.split(': ')[1]


def fun(driver):
    time.sleep(3)
    element = driver.find_element(by="xpath", value="/html/body/div[1]/div/h1[2]")
    value = formatt(element.text)
    with open('R ' + datetime.utcnow().strftime("%H:%M:%S") + '.txt', 'w') as file:
        file.write(value)


""" To print a txt from a webpage """
# def main():
#   driver = get_drvier()
#   time.sleep(2)
#   element = driver.find_element(by="xpath", value="/html/body/div[1]/div/h1[2]")
#   return format(element.text)


def main():
    driver = get_drvier()
    driver.find_element(by="id", value="id_username").send_keys("automated")
    time.sleep(2)
    driver.find_element(by="id", value="id_password").send_keys("automatedautomated" + Keys.RETURN)
    time.sleep(2)
    driver.find_element(by="xpath", value="/html/body/nav/div/a").click()

    for _ in range(10):
        fun(driver)
    return 'Completed'


print(main())
