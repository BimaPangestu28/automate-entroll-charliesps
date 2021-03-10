from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, presence_of_all_elements_located
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from datetime import datetime
import platform
import traceback
import xlsxwriter
import time
import os
import pandas as pd
import random
from faker import Faker

fake = Faker()


class CharlieBot():
    def __init__(self, email):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--start-maximized")
        # chromeOptions.add_argument("--headless")
        chromeOptions.add_experimental_option(
            "prefs", {"intl.accept_languages": "en,en_US"})

        self.browser = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=chromeOptions)
        self.browserWait = WebDriverWait(self.browser, 10)
        self.email = email
        self.link_courses = []

    def signIn(self):
        self.browser.get("https://charliesps.co.id/my-account/")

        input = self.browserWait.until(
            presence_of_all_elements_located((By.CLASS_NAME, "woocommerce-Input--text")))

        emailInput = input[2]
        emailInput.send_keys(self.email)
        emailInput.send_keys(Keys.ENTER)

        time.sleep(2)

        return True

    def getListCourses(self):
        self.browser.get("https://charliesps.co.id/courses/")

        list_courses = self.browserWait.until(
            presence_of_all_elements_located((By.CLASS_NAME, "course-permalink")))

        for link in list_courses:
            self.link_courses.append(link.get_attribute('href'))

    def enrollCourse(self):
        for link in self.link_courses:
            self.browser.get(link)

            button = self.browserWait.until(presence_of_all_elements_located(
                (By.CLASS_NAME, "button-enroll-course")))

            button[0].click()

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


if __name__ == "__main__":
    print("Halo! Ini adalah instagram bot untuk auto follow dan unfollow, gunakan dengan bijak. \nApabila kamu dibanned oleh pihak instagram saya selaku kreator dari bot ini tidak bertanggung jawab")

    # username = input("Masukkan username mu : ")
    total_loop = 20

    for i in range(total_loop):
        bot = CharlieBot(fake.email())

        try:
            bot.signIn()

            bot.getListCourses()

            bot.enrollCourse()

            bot.closeBrowser()
        except Exception:
            bot.closeBrowser()

    # print("Tunggu beberapa saat, sedang proses login")

    # if (bot.signIn()):
    #     print("=======================")
    #     print("Login telah berhasil...")
    #     print("=======================")

    #     bot.askOptions()
    # else:
    #     print("Ada yang salah dengan username dan password yang dimasukkan")
    #     bot.closeBrowser()
