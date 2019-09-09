# ######################################################################### ###
# ############################ Test-Anatomy v1.1 ########################## ###
# ######################################################################### ###

# #############################################################################
# ################# License, Copyright, and References ########################
# #############################################################################

# License: _testAnatomy.py is GPLv3
# Sideload Module License: DO_NOT_DISTRIBUTE_WITHOUT_CONSENT (%company%)
# Test-Anatomy Code Copyright: Eric  (github.com/eagleEggs)
# Modified Kiosk Code Belongs To: %company% (only Sideload Module, Database 
# Module)
# Modified %APPNAME% Code Belongs To: %company% (only Sideload Module, 
# Database 
# Module)
# Contact: github.com/eagleEggs
# Tip: Don't eat yellow snow...

# Icons are MIT licensed from: github.com/primer/octicons/blob/master/LICENSE

# ######################################################################### ###
# ############################### Imports ################################# ###
# ######################################################################### ###

import sys

# #########################################
# ##           Test Anatomy              ##
# #########################################
import TestAnatomy_images  # base64 image db
import TA_Changelog
import TA_Report_Template
#import TA_Class_Sideload as app  # this is only used in build mode
#import TA_Local_Database

#######################
##   Web Automation  ##
#######################

# #####################
# ##    Selenium     ##
# #####################
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# #####################
# ##   Web Parsing   ##
# #####################
from urllib3 import connection_from_url

# #####################
# ## HTML Generation ##
# #####################
import glob
from glob import glob
import dominate
from dominate import document
from dominate.tags import *

# ######################
# ## Image Processing ##
# ######################
# import PIL
from PIL import Image
from PIL import ImageGrab
# from PIL import ImageFont
# from PIL import ImageDraw
import imageio
import win32gui

# #################
# ##  Database   ##
# #################
import shelve
import mysql.connector
import json

# ################
# ##  Graphing  ##
# ################
import matplotlib as mpl
from matplotlib.ticker import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import seaborn as sns
import tkinter
from tkinter import PhotoImage

# ####################
# ## PDF Generation ##
# ####################
import pdfkit

# #########
# ## GUI ##
# #########
import PySimpleGUI as Sg
import imwatchingyou as debug

# #########
# ## SYS ##
# #########
import operator
from operator import *
import _thread as thread
import shutil
import os
from os import makedirs, listdir, system
import uuid
from uuid import uuid4
from logging import basicConfig
import logging
import re
from re import sub
import random
from random import choice
import winsound
import importlib
from time import sleep
from time import clock
import copy
import datetime
from pathlib import Path
import webbrowser

# #############
# ## NETWORK ##
# #############
from socket import *
# import socketserver
# import ssl

# ###########
# ## Email ##
# ###########
import smtplib

#######################
##   GUI Automation  ##
#######################
import cv2
import numpy as np
import pyautogui
import keyboard
import random
import time
from win10toast import ToastNotifier
import argparse

####################
##   CLI SETUP    ##
####################

parser = argparse.ArgumentParser()

parser.add_argument('--cli', action = 'store_true',
                    default=False,
                    help='Bypass GUI')

parser.add_argument('--test', action='store_true', default=False,
                            help='Start TA In Test Mode')

parser.add_argument('--build', action='store_true', default=True,
                    help='Start TA in Build Mode')

parser.add_argument('--reports', action='store_true', default=False, help='Get '
                                                                       'a '
                                                                       'list of all Reports')



results = parser.parse_args()
if results.cli:
    print("Using CLI")
else:
    print("Using GUI")



# ######################################################################### ###
# ########################## Globals and Setup ############################ ###
# ######################################################################### ###
basicConfig(filename='TestAnatomy.log', level=logging.INFO)
logging.info("Launched TA")

toasty = ToastNotifier()

# Utilizes the JSON located at database/ta.config
class DataManager(object):
    def __init__(self):
        self.configs = ""
        logging.info("DatMan: Init")

        try:
            with open("database/ta.config") as config:
                self.configs = json.load(config)

        except:
            Sg.PopupOK("You are either missing or misconfigured\nthe config file ("
                                                    "database/ta.config)\n JSON "
                                                    "Format")

            logging.error("DatMan: Quitting due to issue with ta.config")
            quit()

    def save_configs(self):
        testername = configWindow.FindElement('testername')
        browsertype = configWindow.FindElement('browsertype')
        appuri = configWindow.FindElement('appuri')
        appname = configWindow.FindElement('appname')
        # emailfrom = configWindow.FindElement('emailfrom')
        # emailto = configWindow.FindElement('emailto')
        # emailusername = configWindow.FindElement('emailusername')
        # emailpassword = configWindow.FindElement('emailpassword')
        databasecheck = configWindow.FindElement('databasecheck')
        emailcheck = configWindow.FindElement('emailcheck')
        dbhost = configWindow.FindElement('dbhost')
        dbip = configWindow.FindElement('dbip')
        dbun = configWindow.FindElement('dbun')
        dbpw = configWindow.FindElement('dbpw')
        dbport = configWindow.FindElement('dbport')
        repositorypath = configWindow.FindElement('repositorypath')
        sideload = configWindow.FindElement('sideload')


        self.configs['platform'] = str(values3['browsertype'])
        self.configs['url'] = values3['appuri']
        self.configs['title'] = str(values3['appname'])
        self.configs['engineer'] = values3['testername']
        self.configs['repository'] = values3['repositorypath']

        # database
        self.configs['database_ip'] = values3['dbip']
        self.configs['database_port'] = values3['dbport']
        self.configs['database_name'] = values3['dbhost']
        self.configs['database_username'] = values3['dbun']
        self.configs['database_password'] = values3['dbpw']

        # email
        # self.configs['email_from'] = values3['emailfrom']
        # self.configs['email_to'] = values3['emailto']
        # self.configs['email_username'] = values3['emailusername']
        # self.configs['email_password'] = values3['emailpassword']

        # checkboxes
        self.configs['sql'] = values3['databasecheck']
        # SQL database
        self.configs['sl'] = values3['sideload']  # sideload mods
        # usage
        self.configs['email_check'] = values3['emailcheck']

        with open("database/ta.config", 'w') as config_file:
            json.dump(self.configs, config_file)
            # print(self.configs['title'], print(values3['appname']))
        with open("database/ta.config", 'r') as config_file:
            self.configs = json.load(config_file)
            # print(self.configs['title'], print(values3['appname']))

        logging.info("DatMan: Saved Configs Successfully")
        # return True


        # logging.warning("DatMan: Issue saving configs")
        # Sg.PopupOK("Issue saving configs")
        # return False

    def load_configs(self):
        logging.info("Config: Pressed Load")
        self.testername = configWindow.FindElement('testername')
        self.browsertype = configWindow.FindElement('browsertype')
        self.appuri = configWindow.FindElement('appuri')
        self.appname = configWindow.FindElement('appname')
        # self.emailfrom = configWindow.FindElement('emailfrom')
        # self.emailto = configWindow.FindElement('emailto')
        # .emailusername = configWindow.FindElement('emailusername')
        # self.emailpassword = configWindow.FindElement('emailpassword')
        self.databasecheck = configWindow.FindElement('databasecheck')
        self.emailcheck = configWindow.FindElement('emailcheck')
        self.dbhost = configWindow.FindElement('dbhost')
        self.dbip = configWindow.FindElement('dbip')
        self.dbun = configWindow.FindElement('dbun')
        self.dbpw = configWindow.FindElement('dbpw')
        self.dbport = configWindow.FindElement('dbport')
        self.repositorypath = configWindow.FindElement('repositorypath')
        self.sideload = configWindow.FindElement('sideload')


        # MAIN SETTINGS
        self.browsertype.Update(self.configs['platform'])
        self.appuri.Update(self.configs['url'])
        self.appname.Update(self.configs['title'])
        self.testername.Update(self.configs['engineer'])

        # EMAIL SETTINGS
        # self.emailto.Update(self.configs['email_to'])
        # self.emailfrom.Update(self.configs['email_from'])
        # self.emailusername.Update(self.configs['email_username'])

        # CHECKBOX SETTINGS
        self.databasecheck.Update(self.configs['sql'])
        self.sideload.Update(self.configs['sl'])
        self.emailcheck.Update(self.configs['email_check'])

        # DATABASE SETTINGS
        self.dbhost.Update(self.configs['database_name'])
        self.dbip.Update(self.configs['database_ip'])
        self.dbun.Update(self.configs['database_username'])
        self.dbport.Update(self.configs['database_port'])

        # REPOSITORY SETTINGS
        self.repositorypath.Update(self.configs['repository'])

        # Passwords can optionally be enabled (Insecure):
        # emailpassword.Update(configs['email_password'])
        # dbpw.Update(configs['database_password'])

        # Now make available to the rest of the app:

        self.browsertype = self.configs['platform']
        self.appuri = self.configs['url']
        self.appname = self.configs['title']
        self.testername = self.configs['engineer']

        # EMAIL SETTINGS
        # self.emailto = self.configs['email_to']
        # self.emailfrom = self.configs['email_from']
        # self.emailusername = self.configs['email_username']

        # CHECKBOX SETTINGS
        self.databasecheck = self.configs['sql']
        self.sideload = self.configs['sl']
        self.emailcheck = self.configs['email_check']

        # DATABASE SETTINGS
        self.dbhost = self.configs['database_name']
        self.dbip = self.configs['database_ip']
        self.dbun = self.configs['database_username']
        self.dbport = self.configs['database_port']

        # REPOSITORY SETTINGS
        self.repositorypath = self.configs['repository']

        logging.info("DatMan: Updated Configs Successfully")
        # return True


        # logging.warning("DatMan: Issue loading from Config")
        # Sg.PopupOK("Issue loading from Config")
        # return False


data_man = DataManager()


# ########################################
# ## Build Window Dictionaries and Vars ##
# ########################################
ddURLS = []
ddVals = ["GUI Application", "Internet Explorer", "Firefox", "Chrome"]
ddElements = ["Select Element Type", "CSS Selector", "XPATH", "ID",
              "Link Text", "Partial Link Text", "Tag Name", "Class"]
ddCols = ["Select Color", "Red", "Green", "Orchid", "Aqua", "Aquamarine",
          "Orange", "Tomato", "Salmon", "Yellow", "Blue", "Plum", "PeachPuff",
          "AntiqueWhite", "AliceBlue", "BlanchedAlmond", "Black", "DeepPink",
          "Gold", "MediumSpringGreen", "Wheat", "RebeccaPurple", "PapayaWhip",
          "PaleVioletRed", "PaleGoldenRod", "Olive", "MintCream", "Lavender",
          "LavenderBlush", "Ivory", "HotPink", "Indigo", "GhostWhite",
          "ForestGreen", "FireBrick", "DeepSkyBlue", "Cornsilk", "Crimson",
          "Coral", "Chocolate"]
dd_plottypes = ['line', 'bar', 'heat']
dd_plotstyles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
dd_database = ["id", "iddate", "iduuid", "idpassfail"]
ddbuildactions = ["Select Command", "", "Web Automation:"," - Open Site",
                  " - Click Element",
                  " - Hover Over Element", " - Verify Element Text",
                  " - Type Text", " - Wait", " - Wait for Element",
                  " - Hold Element",
                  " - Release Element", " - Highlight Element(s)",
                  " - Go Back", " - Go Forward", " - Refresh Page",
                  " - Take Screenshot", " - Clear Text Input",
                  "",
                  "GUI Automation:",
                  " - Click Image",
                  " - Type With Keyboard",
                  " - Type Hotkey With Keyboard",
                  " - Click Cancel",
                  " - Click OK",
                  " - Click Red X",
                  " - Press Escape",
                  " - Press Enter",
                  " - Press Tab",
                  " - Screenshot Window Handle",
                  " - Screenshot Fullscreen",
                  " - Screenshot Window and Highlight Image(s)",
                  " - Screenshot Fullscreen and Highlight Image(s)",
                  "",
                  "Sideload Commands:",
                  " - Load Sideload (SL) Module",
                  " - Kiosk: Add Script Header",
                  " - Kiosk: Enter SSN (Req. SL)",
                  " - Kiosk: Click Pain Level (Req. SL)",
                  " - Kiosk: Fill Patient Admission Page (Req. SL)",
                  " - Kiosk: Login (Req. SL)",
                  " - Kiosk: Admin Logon (Req. SL)",
                  " - Kiosk: Admin Database Settings (Req. SL)",
                  " - Kiosk: Admin General Settings (Req. SL)",
                  " - Kiosk: Admin Clinic Settings (Req. SL)",
                  " - Insert Random Encoding String (Req. SL)",
                  " - Insert Random SQL Injection String (Req. SL)",
                  " - Insert Random XSS String",
                  "",
                  "Reporting Commands:",
                  " - Reporting: Generate HTML",
                  " - Reporting: Generate PDF",
                  " - Reporting: Send Email"]

# #########################
# ## MATPLOTLIB SETTINGS ##
# #########################
mpl.rcParams['font.size'] = 9
mpl.rcParams['legend.fontsize'] = 'small'
mpl.rcParams['figure.titlesize'] = 'small'
mpl.rcParams['figure.figsize'] = [8.0, 6.0]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 100

# ##########################
# ##    PDF SETTINGS     ### # TODO need to fix this...
# ##########################
# This module requires installing
# https://wkhtmltopdf.org/downloads.html to work correctly
htmlToPDFpath = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# change this to where you have wkhtmltopdf
try:
    htmlToPDFconfig = pdfkit.configuration(wkhtmltopdf=htmlToPDFpath)
    logging.info("PDF Tool WKHTMLTOPDF Loaded")
except:
    logging.info("PDF Tool WKHTMLTOPDF Not Found")

# ######################################################################### ###
# ###########          Engine: Master Controller Class          ########### ###
# ######################################################################### ###

global uid  # TODO need to clean this global up
uid = str(uuid4())


class Engine(object):
    def __init__(self, browsername, siteaddress,
                 appName, folder=None):

        logging.info("Starting Engine...")

        self.browsername = browsername
        self.siteaddress = siteaddress
        self.repositoryroot = str(data_man.repositorypath)
        self.appName = appName.lower()
        self.address = address
        self.elementStore = ""
        self.elementtype = None
        self.tagvalue = None
        self.time = None
        self.words = None
        self.gif_array = []

        print(self.browsername)
        print(self.siteaddress)
        print(self.appName)

        if self.browsername == "Firefox":
            logging.info("Launching Firefox")
            self.engine = webdriver.Firefox(executable_path=
                                            "drivers/geckodriver.exe")
            # self.engine.set_window_position(-10000, 0)
        if self.browsername == "Internet Explorer":
            logging.info("Launching IE")
            self.engine = webdriver.Ie(executable_path=
                                       "drivers/IEDriverServer.exe")
            # self.engine.set_window_position(-10000, 0)
        if self.browsername == "Chrome":
            logging.info("Launching Chrome")
            self.engine = webdriver.Chrome(executable_path=
                                           "drivers/chromedriver.exe")
            # self.engine.set_window_position(-10000, 0)
        if self.browsername == "GUI Application":
            logging.info("Using GUI Application Engine")
            self.engine = pyautogui

        self.folder = str(data_man.repositorypath)
        self.UUID = uid
        self.functionality = None
        self.xystore = []

        try:
            os.mkdir("{}\{}_{}".format(self.repositoryroot, self.appName,
                                       self.UUID))
            os.mkdir("{}\{}_{}\Screenshots".format(self.repositoryroot,
                                                  self.appName, self.UUID))
            os.mkdir("{}\{}_{}\Report".format(self.repositoryroot,
                                                self.appName,
                                                self.UUID))
            self.report_folder = "{}\{}_{}\Report".format(self.repositoryroot,
                                                          self.appName,
                                    self.UUID)
            self.screenshot_folder = "{}\{}_{}\Screenshots".format(
                                                self.repositoryroot,
                                                 self.appName, self.UUID)
            print(self.screenshot_folder)
            self.project_folder = "{}\{}_{}".format(self.repositoryroot,
                                                  self.appName, self.UUID)
            logging.info("UUID generated")
        except:
            self.report_folder = "{}\{}_{}\Report".format(self.repositoryroot,
                                                          self.appName,
                                                          self.UUID)
            self.screenshot_folder = "{}\{}_{}\Screenshots".format(
                self.repositoryroot,
                self.appName, self.UUID)
            print(self.screenshot_folder)
            self.project_folder = "{}\{}_{}".format(self.repositoryroot,
                                                    self.appName, self.UUID)
            logging.info("UUID being reused")

        logging.info("Initiated TA Engine")

    def screenshot(self, functionality, scroll=True, gui=False):
        self.functionality = functionality

        if not gui:
            try:
                try:

                    full_screen = driver.engine.find_element_by_tag_name('body')
                    full_screen.screenshot("{}/{}.png".format(
                                    self.screenshot_folder, self.functionality))
                    self.gif_array.append("{}/{}.png".format(
                                    self.screenshot_folder, self.functionality))
                    logging.info("Fullscreen Screenshot Successful "
                                 "for project: {}".format(
                            self.folder))

                except:
                # if scroll:
                #    self.engine.execute_script(
                #        "window.scrollTo(0, document.body.scrollHeight);")
                    self.engine.save_screenshot("{}/{}.png".format(
                                    self.screenshot_folder, self.functionality))
                    self.gif_array.append("{}/{}.png".format(
                            self.folder, self.functionality))

                    logging.info("Screenshot Successful for project: {}".format(
                                                                self.folder))

            except:
                logging.warning("Issue creating full and normal "
                                "screenshot for project: {}".format(self.folder))

            # the following is a hack to get this moving along

            try:
                report_hook.add_screenshot("{}/{}.png".format(
                                self.screenshot_folder, self.functionality),
                                            self.functionality)  # REPORT HOOK
                logging.info("Added screenshot to Report")
            except:
                logging.warning("Cannot save screenshot to Report")

        else:
            # TODO: implement GUI screenshot here
            pass

    def screenshot_element(self, css):
        image = driver.engine.find_element_by_css_selector(css)
        driver.engine.save_screenshot("{}/temp_screenshot_element.png".format(
                driver.folder))
        loc = image.location
        size = image.size
        x = loc['x']
        y = loc['y']
        w = loc['x'] + size['width']
        h = loc['y'] + size['height']
        open_image = Image.open("{}/temp_screenshot_element.png".format(
                driver.folder))
        open_image.crop((int(x), int(y), int(w), int(h)))
        open_image.save("{}/temp_screenshot_element_saved.png".format(
                driver.folder))

    def get_element_loc(self, image):
        album = []
        loc = image.location
        size = image.size
        album.append(loc['x'])
        album.append(loc['y'])
        album.append(loc['x'] + size['width'])
        album.append(loc['y'] + size['height'])
        return album

    def htmlgen(self):
        try:
            screenshots = glob('{}/*.png'.format(self.folder))
        except:
            logging.info("Issue parsing screenshots within project: {}".format(
                    self.folder))
            return
        try:
            with document(
                    title='{} Automation Report'.format(
                            self.appName)) as report:
                h1('{} Automation Report'.format(self.appName))
                for listings in screenshots:
                    h3(listings)
                    div(img(src=listings), _class='photo')
        except:
            logging.warning("Issue Generating "
                            "HTML for Screenshots from Project Folder")
        with open('{}/{} Automation Report.html'.format(self.folder,
                                                        self.appName),
                                                        'w') as resultshtml:
            resultshtml.write(report.render())

    def pdfgen(self): # TODO: bring in PDFKIT here
        pass

    def email(self, totals): # TODO: verify email functionality
        self.totals = totals

        if not data_man.emailcheck:
            return

        from email.mime.text import MIMEText
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.starttls()
        mailServer.login(data_man.emailusername, data_man.emailpassword)

        body = MIMEText(self.totals)
        mailServer.sendmail(data_man.emailfrom,
                            data_man.emailto, body.as_string())

    def zip(self): # TODO: send zip to project folder
        shutil.make_archive("{}".format(self.folder), 'zip',
                            self.folder)

    def gif(self):
        for image in listdir(self.screenshot_folder):
            if image.endswith(".png"):
                self.gif_array.append(imageio.imread(image))
        kargs = {'duration': 3}
        try:
            imageio.mimsave('{}\Lazy Automation Report.gif'.format(
                    self.report_folder), self.gif_array, **kargs)
        except:
            logging.warning("Could not create Lazy Report")

    def getwebelement(self, elementtype, tagvalue, text=None):
        self.elementtype = elementtype.lower()
        self.tagvalue = tagvalue

        if self.elementtype == "css" or self.elementtype == "css selector":
            element = self.engine.find_element_by_css_selector(self.tagvalue)
            if text:
                assert element.text == text
                logging.info("Asserted Text: {} on Element: {}".format(
                        text, tagvalue))
                return
            return element

        if self.elementtype == "xpath":
            element = self.engine.find_element_by_xpath(self.tagvalue)
            if text:
                assert element.text == text
            return element

    def typewords(self, elementtype, tagvalue, words, special_key=None):
        self.elementtype = elementtype.lower()
        self.tagvalue = tagvalue
        self.words = words

        wordinput = self.getwebelement(self.elementtype, self.tagvalue)
        wordinput.send_keys(self.words)
        if special_key is "TAB":
            try:
                wordinput.send_keys(Keys.TAB)
            except:
                logging.error("Could not send special key to input box")
        if special_key is "ENTER":
            try:
                wordinput.send_keys(Keys.ENTER)
            except:
                logging.error("Could not send special key to input box")

    def clearinput(self, elementtype, tagvalue):
        inputbox = self.getwebelement(elementtype, tagvalue)
        inputbox.clear()

    def waiter(self, time):
        self.time = time
        sleep(self.time)

    def hold_element(self, elementtype, tagvalue):
        element = self.getwebelement(elementtype, tagvalue)
        action = ActionChains(self.engine).click_and_hold(element)
        action.perform()

    def release_element(self, elementtype, tagvalue):
        element = self.getwebelement(elementtype, tagvalue)
        action = ActionChains(self.engine).release(element)
        action.perform()

    def hoverelement(self, elementtype, tagvalue):
        element = self.getwebelement(elementtype, tagvalue)
        action = ActionChains(self.engine).move_to_element(element)
        action.perform()

    def highlighter(self, type, tagvalue, multi=False):
            element = self.getwebelement(type, tagvalue)
            self.ehx_highlight(element, multi)

    def box_highlighter(self, type, tagvalue, multi=False):
            element = self.getwebelement(type, tagvalue)
            self.ehx_highlight(element, multi, box=True)

    def waitforelement(self, elementtype, tagvalue, time):
        self.elementtype = elementtype.lower()
        self.tagvalue = tagvalue
        self.time = time

        if elementtype == "css selector":
            element = WebDriverWait(self.engine, time).until(
                    ec.presence_of_element_located((
                        By.CSS_SELECTOR, self.tagvalue)))
        if elementtype == "xpath":
            WebDriverWait(self.engine, time).until(
                    ec.presence_of_element_located((
                        By.XPATH, self.tagvalue)))
        if elementtype == "id":
            WebDriverWait(self.engine, time).until(
                    ec.presence_of_element_located((
                        By.ID, self.tagvalue)))

    def clickwebelement(self, elementtype, tagvalue):
        self.elementtype = elementtype.lower()
        self.tagvalue = tagvalue

        if eq(self.elementtype, "css") or eq(self.elementtype, "css selector"):
            logging.info("Clicking CSS Web Element: {}, {}".format(
                    elementtype, tagvalue))
            self.engine.find_element_by_css_selector(self.tagvalue).click()

        if eq(self.elementtype, "xpath"):
            logging.info("Clicking Web Element XPATH: {}, {}".format(
                    elementtype, tagvalue))
            self.engine.find_element_by_xpath(self.tagvalue).click()

    def entertext(self, elementtype, text, element):
            input_loc = self.getwebelement(elementtype, element)
            input_loc.send_keys(text)

    def special_keys(self, key):
        pass

    def alert_accept(self):
        alert = self.engine.switch_to.alert.accept()

    def kill_drivers(self): # TODO: make kill_drivers work
        try:
            os.system("taskkill /im geckodriver.exe /F")
            logging.info("FF Driver(s) killed")
        except:
            logging.error("Some Drivers could not be killed or do not exist")

    def maximize(self):
        self.engine.maximize_window() # TODO make sure this works

    def minimize(self):
        self.engine.minimize_window() # TODO make sure this works

    def full_screen(self):
        self.engine.fullscreen_window() # TODO make sure this works

# ######################################################################### ###
# ###########                EHX HIGHLIGHTING                   ########### ###
# ######################################################################### ###

    def ehx_highlight(self, element, multi, box=None):
        try:
            if self.elementStore is not "" and multi is False:
                logging.info("Highlight: Removing Previous Element from Store")
                self.ehx_highlight_remove(self.elementStore)
        except:
            logging.error("Highlight: Issue with Element Store")
        try:
            self.elementStore = element
            parent = element._parent
            if box is not None:
                self.ehx_stylize(parent, element, "border: "
                                                  "3px solid {};".format(
                                                    values2["colortype"]))
            else:
                self.ehx_stylize(parent, element, "background: {}; border: "
                                                  "3px solid {};".format(
                                                    values2["colortype"],
                                                    values2["colortype"]))
        except:
            logging.error("Could not Highlight Element")
            Sg.PopupError("Highlight: There was an issue Highlighting, "
                          "Check Element")

    def ehx_stylize(self, parent, element, style):
        try:
            self.engine.execute_script("arguments[0].setAttribute('style', "
                                       "arguments[1]);", element, style)
            # reference: https://gist.Instance.com/dariodiaz/3104601
        except:
            logging.error("Could not Stylize Element")

    def ehx_highlight_remove(self, element):
        try:
            parent = element._parent
            self.ehx_stylize_remove(parent, element, " ;")
        except:
            logging.error("Could not Remove Element Highlight")

    def ehx_stylize_remove(self, parent, element, style):
        self.engine.execute_script("arguments[0].setAttribute("
                                   "'style', arguments[1])", element, style)

    # References for Style Override Function:
    # https://gist.github.com/dariodiaz/3104601
    # https://gist.github.com/marciomazza/3086536

    ##########################################
    #            GUI Automation              #
    ##########################################
    # Used for GUI Applications
    # Reference: https://github.com/drov0/python-imagesearch

    def screenshot_xy(self, region):
        x1 = region[0]
        y1 = region[1]
        width = region[2] - x1
        height = region[3] - y1

        return self.engine.screenshot(region=(x1, y1, width, height))

    def get_element_from_xy(self, image, x1, y1, x2, y2, precision=0.8,
                            im=None):
        if im is None:
            im = self.screenshot_xy(region=(x1, y1, x2, y2))

        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc

    def click_element(self, image, pos, action, timestamp, offset=0,
                      precision=0.8):
        img = cv2.imread(image)
        height, width, channels = img.shape
        self.engine.moveTo(pos[0] + self.r(width / 2, offset),
                         pos[1] + self.r(height / 2, offset),
                         timestamp)
        self.engine.click(button=action)

    def search_for_element(self, image, precision=0.8):
        im = self.engine.screenshot()
        img_rgb = np.array(im)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return [-1, -1]
        return max_loc

    def wait_for_element(self, image, timesample, precision=0.8):
        pos = self.search_for_element(image, precision)
        while pos[0] == -1:
            print(image + " not found, waiting")
            time.sleep(timesample)
            pos = self.search_for_element(image, precision)
        return pos

    def search_for_element_iterate(self, image, timesample, maxSamples,
                                   precision=0.8):
        pos = self.search_for_element(image, precision)
        count = 0
        while pos[0] == -1:
            print(image + " not found, waiting")
            time.sleep(timesample)
            pos = self.search_for_element(image, precision)
            count = count + 1
            if count > maxSamples:
                break
        return pos

    def wait_for_element_xy_loop(self, image, timesample, x1, y1, x2, y2,
                                precision=0.8):
        pos = self.get_element_from_xy(image, x1, y1, x2, y2, precision)

        while pos[0] == -1:
            time.sleep(timesample)
            pos = self.get_element_from_xy(image, x1, y1, x2, y2, precision)
        return pos

    def count_element(self, image, precision=0.9):
        img_rgb = self.engine.screenshot()
        img_rgb = np.array(img_rgb)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        count = 0
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
            # 2) // Uncomment to draw boxes around found occurances
            count = count + 1
        # cv2.imwrite('result.png', img_rgb) // Uncomment to write output
        # image with boxes drawn around occurances
        return count

    def r(self, num, rand):
        return num + rand * random.random()

    # compare_images takes two required images as inputs
    def compare_images(self, image_one, image_two):
        first_image = cv2.imread(image_one)
        second_image = cv2.imread(image_two)

        try:
            x1 = cv2.cvtColor(first_image, cv2.COLOR_BGR2GRAY)
            x2 = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

            absdiff = cv2.absdiff(first_image, second_image)
            cv2.imwrite("images/absdiff.png", absdiff)

            diff = cv2.subtract(first_image, second_image)

            b, g, r = cv2.split(diff)

            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and \
                    cv2.countNonZero(r) == 0:

                return True
            else:
                return False

        except:
            logging.warning("Issue parsing images for diff")

    def edge_detect_save(self, image):
        pass

    def screenshot_window(self, func, title): # TODO Needs testing
        handle_name = win32gui.FindWindow(None, title)
        rect = win32gui.GetWindowRect(handle_name)

        screenshot_window = ImageGrab.grab(rect)
        screenshot_window.save("{}/{}.png".format(self.screenshot_folder,
                                                   func))

    def input_text(self, text, interval=None, press_enter=None):
        if not interval: # interval is INT
            interval = 0.1

        if not press_enter:
            self.engine.typewrite(text, interval)

        else:
            text = str(text + "\n")
            self.engine.typewrite(text, interval)


class Database(Engine):  # TODO: insert error when hopping GUI during test
    def __init__(self, username, dbhost, database, password, databaseport):
        self.username = username
        self.database = database
        self.password = password
        self.dbhost = dbhost
        self.databaseport = databaseport
        print(self.username,self.database,self.password,self.databaseport,
               self.dbhost)
        self.database = mysql.connector.connect(user=str(self.username),
                                                database=str(self.database),
                                                passwd=str(self.password),
                                                port=str(self.databaseport),
                                                host=str(self.dbhost))

        self.myCursor = self.database.cursor(buffered=True)
        logging.info("Instantiating DB")
        self.app = data_man.appname
        self.UUID = sub('-', '', driver.UUID)

    def plot_all(self):

        # this
        global figure_w, figure_h, fig
        fig = plt.figure()
        query = """SELECT   id,
                            iddate,
                           iduuid,
                           idtest,
                           idpassfail from {}""".format(self.app)

        querymod = self.myCursor.execute(query, [self.app, self.UUID])

        # this
        df = pd.read_sql(query, driverDB.database)
        result = df.pivot(index='id', columns='iduuid', values='idpassfail')
        sns.set(style="darkgrid")

        # sns.load_dataset(df) # for URL datasets
        # sns.pairplot(df, hue="id")
        # sns.barplot(x="iduuid", y = "idpassfail", data = result)

        # this
        sns.heatmap(result) # nice cool

        # sns.countplot(x="iduuid", hue="idpassfail", data=df)
        # df["idpassfail"] = df["idtest"].astype('category')
        # df.loc[['iduuid'] == '94378e063b124a4787c46acb44d59885']
        # scatter_matrix(TM, alpha=0, figsize=(5, 5), diagonal='kde')

        # this
        fig.tight_layout()
        plt.plot()

        # plt.subplots_adjust(right = 2, left = 1, top = 1, bottom = 0.5)

        # this
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        # reference: Tony Crewe https://Instance.com/MikeTheWatchGuy/
        # PySimpleGUI/blob/master/ProgrammingClassExamples/
        # 10e%20PSG%20(Same%20Window).py

    # index is for heatmap, axisx,y, style for design output
    def set_plot_heat(self, plot_index, axis_x, axis_y,
                      plot_style=None):
        if plot_index is not None:
            self.plot_index = plot_index
        else:
            self.plot_index = "id"
        self.index = index
        self.x = axis_x
        self.y = axis_y
        if plot_style is not None:
            self.plot_style = plot_style
        else:
            self.plot_style = "darkgrid"
        # this
        global figure_w, figure_h, fig
        fig = plt.figure()
        fig, f1_axes = plt.subplots(ncols=2, nrows=2, constrained_layout=True)
        query = """SELECT   {}, {},
                            {} from {}""".format(self.plot_index, self.x,
                                                         self.y,
                                                         self.app)

        querymod = self.myCursor.execute(query)

        # this
        print(querymod)
        df = pd.read_sql(query, driverDB.database)
        print(df)
        result = df.pivot(index=self.plot_index, columns=self.x, values=self.y)
        sns.set(style=self.plot_style)

        # sns.load_dataset(df) # for URL datasets
        # sns.pairplot(df, hue="id")
        # sns.barplot(x=self.x, y=self.y, data = result)

        # this
        sns.heatmap(result) # nice cool

        # sns.countplot(x="iduuid", hue="idpassfail", data=df)
        # df["idpassfail"] = df["idtest"].astype('category')
        # df.loc[['iduuid'] == '94378e063b124a4787c46acb44d59885']
        # scatter_matrix(TM, alpha=0, figsize=(5, 5), diagonal='kde')

        # this
        fig.tight_layout()
        plt.plot()

        # plt.subplots_adjust(right = 2, left = 1, top = 1, bottom = 0.5)

        # this
        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        # reference: Tony Crewe https://Instance.com/MikeTheWatchGuy/
        # PySimpleGUI/blob/master/ProgrammingClassExamples/
        # 10e%20PSG%20(Same%20Window).py

    def set_plot_bar(self, hue, data, axis_x, axis_y,
                     start_date, end_date, plot_style=None):
        self.x = axis_x
        self.y = axis_y
        self.hue = hue
        self.data = data
        self.start_date = start_date
        self.end_date = end_date

        global figure_w, figure_h, fig
        fig = plt.figure()
        query = """SELECT   id, iddate, {}, {} from {}
                                    where iddate >= '{}' 
                                    and iddate < '{}'""".format(self.x,
                                                            self.y,
                                                            self.app,
                                                            str(self.start_date),
                                                            str(self.end_date))
        querymod = self.myCursor.execute(query)

        print(querymod)
        df = pd.read_sql(query, driverDB.database)
        print(df)
        # result = df.pivot(index="id", columns=self.x, values=self.y)
        sns.set(style="darkgrid")
        sns.barplot(x=self.x, y=self.y, data=df)

        # sns.load_dataset(df) # for URL datasets
        # sns.pairplot(df, hue="id")
        # sns.barplot(x=self.x, y=self.y, data = result)

        # this
        # sns.heatmap(result) # nice cool

        # sns.countplot(x="iduuid", hue="idpassfail", data=df)
        # df["idpassfail"] = df["idtest"].astype('category')
        # df.loc[['iduuid'] == '94378e063b124a4787c46acb44d59885']
        # scatter_matrix(TM, alpha=0, figsize=(5, 5), diagonal='kde')
        # ax = plt.gca()
        # ax.yaxis.set_major_locator(MultipleLocator(0.1))

        # set the labels of y axis and text orientation
        # ax.xaxis.set_major_locator(MultipleLocator(10))
        # ax.set_xticklabels(labels, rotation=90)

        fig.tight_layout()
        plt.plot()

        # plt.subplots_adjust(right = 2, left = 1, top = 1, bottom = 0.5)

        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        # reference: Tony Crewe https://Instance.com/MikeTheWatchGuy/
        # PySimpleGUI/blob/master/ProgrammingClassExamples/
        # 10e%20PSG%20(Same%20Window).py

    def set_plot_line(self, hue, data, axis_x, axis_y,
                     start_date, end_date, plot_style=None):
        self.x = axis_x
        self.y = axis_y
        self.hue = hue
        self.data = data
        self.start_date = start_date
        self.end_date = end_date

        global figure_w, figure_h, fig
        fig = plt.figure()
        query = """SELECT   id, iddate, {}, {} from {}
                                    where iddate >= '{}' 
                                    and iddate < '{}'""".format(self.x,
                                                            self.y,
                                                            self.app,
                                                            str(self.start_date),
                                                            str(self.end_date))
        querymod = self.myCursor.execute(query)

        print(querymod)
        df = pd.read_sql(query, driverDB.database)
        print(df)
        # result = df.pivot(index="id", columns=self.x, values=self.y)
        sns.set(style="darkgrid")
        sns.lineplot(x=self.x, y=self.y, data=df)

        # sns.load_dataset(df) # for URL datasets
        # sns.pairplot(df, hue="id")
        # sns.barplot(x=self.x, y=self.y, data = result)

        # this
        # sns.heatmap(result) # nice cool

        # sns.countplot(x="iduuid", hue="idpassfail", data=df)
        # df["idpassfail"] = df["idtest"].astype('category')
        # df.loc[['iduuid'] == '94378e063b124a4787c46acb44d59885']
        # scatter_matrix(TM, alpha=0, figsize=(5, 5), diagonal='kde')

        fig.tight_layout()
        plt.show()

        # plt.subplots_adjust(right = 2, left = 1, top = 1, bottom = 0.5)

        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

        # reference: Tony Crewe https://Instance.com/MikeTheWatchGuy/
        # PySimpleGUI/blob/master/ProgrammingClassExamples/
        # 10e%20PSG%20(Same%20Window).py

    def PlotDraw(self, canvas, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)
        canvas.create_image(
               loc[0] + figure_w / 2, loc[1] + figure_h / 2, image=photo)
        tkagg.blit(
               photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        return photo

    def insert(self, module, line, passfail):
        self.module = module
        self.line = line
        self.passfail = passfail

        sql = """
            INSERT INTO 
            {} (id, iddate, idtest, idline, idpassfail, iduuid,
            idresult, idengineer, idbranch, idbuild, idversion) 
            VALUES 
            (id, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(self.app)

        self.Pool(sql, (self.module, self.line, self.passfail, self.UUID))

    def insert_gui(self, action, user, url, app):
        self.action = action
        self.user = user
        self.url = url
        self.app = app
        self.db_name = "gui"

        sql = """
            INSERT INTO 
            {} (id, iddate, idaction, iduser, idurl, idapp) 
            VALUES 
            (id, NOW(), %s, %s, %s, %s)""".format(self.db_name)

        self.Pool(sql, (self.action, self.user, self.url, self.app))

    def Pool(self, sql, cmds):
        # pool = mysql.connector.connect(
        # user=self.username, database=self.database, passwd=self.password,
        # port=self.databaseport)
        cursor = self.myCursor
        cursor.execute("SET AUTOCOMMIT=1")

        try:
            cursor.execute(sql, cmds)
            # cursor.close()
        except:
            logging.error(" - Database Insert Error - Cannot Commit")

        # pool.close()

    def disconnect(self):
        self.database.close()

    def case_status(self, status, case):
        pass


def save_to_file(filename, content=[]):  # send filename and content
    with open('{}_{}'.format(driver.folder, filename), 'w') as savefile:
        for results in content:
            savefile.write(results)


# ######################################################################### ###
# ###########           Test Rail Controller Class              ########### ###
# ############              Inherits: Engine                   ############ ###
# ######################################################################### ###

class TestRail(object):
    pass


# ######################################################################### ###
# ###########            Browser Controller Class               ########### ###
# ############              Inherits: Engine                   ############ ###
# ######################################################################### ###


class Instance(Engine):
    def __init__(self, *args):
        logging.info("Initiating Instance")
        super(Instance, self).__init__(*args)

    # no args = use inherited param > else use hard param
    def open_site(self, site=None):
        if site is None:
            logging.info("Opening Browser Session")
            self.engine.get(self.siteaddress)
        else:
            logging.info("Opening Custom Browser Session")
            self.engine.get(site)


# ######################################################################### ###
# ###########            Test Cycle Controller Class            ########### ###
# ############           Inherits: Instance > Engine           ############ ###
# ######################################################################### ###

class TestCycle(Instance):
    def __init__(self, order, thread_max, cycles, brake, instance, scripts,
                 *args):
        logging.info("Initiating Test Cycle")
        super(Instance, self).__init__(*args)
        self.order = order
        self.instance = instance
        self.scripts = scripts
        self.time = "1"
        self.successes = 0
        self.failures = 0
        if self.order == "repository":
            self.script_total = os.listdir(self.scripts)
        self.thread_total = 0
        self.thread_max = thread_max
        self.script_max = len(self.script_total)
        self.running = True
        self.running_thread = True
        self.cycles = cycles
        self.brake = brake
        global report_hook
        self.UUID = uuid
        report_hook = TA_Report_Template.Report(self.UUID, self.appName)

        logging.info("Test Cycle Starting")
        logging.info("Order: {}".format(self.order))
        logging.info("Max Cycles: {}".format(self.thread_max))
        logging.info("Test Cycle: Scripts: {}".format(self.scripts))

        if self.order == "single":
            logging.info("Running Single Test")
            Sg.Print("\nRunning Single Test:\n{}".format(self.scripts))
            thread.start_new_thread(
                    self.runonce, (self.instance, self.scripts))
        if self.order == "repository" and thread_max > 0:
            logging.info("Running Repository Cycles")
            Sg.Print("\nTotal: {} Tests:\n{}"
                     .format(self.script_total, self.scripts))
            # self.run_repository(self.instance, self.scripts)
            thread.start_new_thread(
                     self.run_repository, (self.instance, self.scripts,
                                           report_hook))
            while self.thread_total <= self.thread_max and \
                    self.script_max != 0:
                pass

        if self.order == "repository" and thread_max == 0:
            thread.start_new_thread(self.run_repository_inc, (self.instance,
                                                              self.scripts,
                                                              report_hook))

    def run_repository_inc(self, driver, scripts, _report_hook):
        for cycle_count in range(int(self.cycles)):
            for module in listdir(self.scripts):
                if module.endswith(".py"):

                    _report_hook.add_script(module)  # REPORT HOOK

                    repscriptopen = open(self.scripts + "/" + module, 'r')
                    repscript = repscriptopen.readlines()
                    self.running_thread = True
                    thread.start_new_thread(self.run_repository_inc_thread,
                                            (repscript, module))
                    while self.running_thread is True:
                        sleep(1)

            logging.info("Test Cycle: Run Repository Completed: "
                        "Successes: {} | Failures: {}".format(
                    self.successes, self.failures))
            Sg.Print("\nRepository Test Cycle Complete\n"
                    "Successes: {}\nFailures: {}".format(
                    self.successes, self.failures))

            try:
                driverDB.insert("Run Repository Completed",
                                "Successes: {} , Failures: {}".format(
                    self.successes, self.failures), 3)
            except:
                logging.warning("Cannot Commit Report to Database")

            _report_hook.finalize_html(driver)  # REPORT HOOK
            try:
                self.gif()
            except:
                logging.warning("Could not generate lazy GIF report")

            if data_man.emailcheck == True:
                try:
                    body = "Test Cycle: Run Once Completed | " \
                       "Successes: {} | Failures: {}".format(self.successes,
                                                             self.failures)
                    self.email(body)
                except:
                    logging.error("Could not send email report")

            self.htmlgen()
            self.successes = 0
            self.failures = 0

            # added to test swapping UUID on 02/12/19

            uid = str(uuid4())
            self.UUID = uid

            report_hook = TA_Report_Template.Report(self.UUID, self.appName)

            os.mkdir("{}/{}_{}".format(self.repositoryroot, self.appName,
                                       self.UUID))
            os.mkdir(
                "{}/{}_{}/Screenshots".format(self.repositoryroot,
                                              self.appName, self.UUID))
            os.mkdir("{}/{}_{}/Report".format(self.repositoryroot,
                                              self.appName, self.UUID))
            self.report_folder = "{}/{}_{}/Report".format(self.repositoryroot,
                                              self.appName, self.UUID)
            self.screenshot_folder = "{}/{}_{}/Screenshots".format(
                    self.repositoryroot, self.appName, self.UUID)
            self.project_folder = "{}/{}_{}".format(self.repositoryroot,
                                                    self.appName, self.UUID)

    def run_repository_inc_thread(self, script, module):
        for repscriptline in script:
            try:
                if int(self.brake) != 0:
                    logging.info("Sleeping for {}".format(self.brake))
                    sleep(int(self.brake))
                exec(repscriptline)
            except:
                self.failures = self.failures + 1
                driver.screenshot("Screenshot at Failure")

                report_hook.add_status("Failure Script Location: ",
                                       repscriptline)
                # Removed 021419 TODO: add containers to add to above ss

                logging.error(
                        "Exec Line Failed: {}_{}".format(module,
                                                         repscriptline))
                # if shelfdb['ta'][7] == True:

                driverDB.insert(module, repscriptline, 1)

                self.running_thread = False
                self.script_max = self.script_max - 1
                return

        self.successes = self.successes + 1
        self.running_thread = False
        self.script_max = self.script_max - 1

        report_hook.add_status("PASS")  # REPORT HOOK
        # TODO: add containers to add to above ss

        try:
            driverDB.insert(module, "All Passed", 0)
        except:
            pass

    # TODO fix Shelve to JSON if going to use this chunk of code
    def run_repository(self, driver, scripts): # TODO make threads work better
        logging.info("Test Cycle: Run Repository Starting")
        duplicated_driver = 0
        for module in listdir(self.scripts):
            if module.endswith(".py"):
                logging.info("Loading module: {}".format(module))
                self.thread_total = self.thread_total + 1
                self.driver_change = "driver{}".format(duplicated_driver)
                logging.info("Opening Thread for: {}".format(module))

                driver = Instance(shelfdb['ta'][19], shelfdb['ta'][0],
                                         shelfdb['ta'][1],
                                         shelfdb['ta'][2])
                #driver.open_site()
                logging.info("Loaded Engine Mirror: {}".format(
                        self.driver_change))

                if str(shelfdb['ta'][0]) == "Firefox":
                    shutil.copy("drivers/geckodriver.exe",
                                "drivers/geckodriver{}.exe".format(
                                        duplicated_driver))

                    driver.engine = webdriver.Firefox(executable_path=
                    "drivers/geckodriver{}.exe".format(
                            duplicated_driver))
                    driver.engine.set_window_position(-10000, 0)
                    driver.minimize()

                if str(shelfdb['ta'][0]) == "Internet Explorer":
                    shutil.copy("drivers/IEDriverServer.exe",
                            "drivers/IEDriverServer{}.exe".format(
                                    duplicated_driver))
                    driver.engine = webdriver.Ie(executable_path=
                                               "drivers/IEDriverServer{}."
                                               "exe".format(
                                                    duplicated_driver))
                    driver.engine.set_window_position(-10000, 0)

                if str(shelfdb['ta'][0]) == "Chrome":
                    logging.info("Launching Chrome")
                    driver.engine = webdriver.Chrome(executable_path=
                                                   "drivers/chromedriver.exe")
                    driver.engine.set_window_position(-10000, 0)
                logging.info("Changed Engine Mirror Copy: {}".format(
                        self.driver_change))

                # driver_change.folder = shelfdb['ta'][17
                # instance.engine.minimize_window()
                duplicated_driver = duplicated_driver + 1
                thread.start_new_thread(
                        self.run_repository_threads, (scripts, module,
                                                      driver))

                # self.run_repository_threads(scripts, module, driver)

        while self.thread_total != 0:
            pass  # this helps push things through
        logging.info("Test Cycle: Run Repository Completed: "
                     "Successes: {} | Failures: {}".format(
                self.successes, self.failures))
        Sg.Print("\nRepository Test Cycle Complete\n"
                 "Successes: {}\nFailures: {}".format(
                self.successes, self.failures))
        if shelfdb['ta'][11] == True:
            try:
                body = "Test Cycle: Run Once Completed | " \
                       "Successes: {} | Failures: {}".format(self.successes,
                                                             self.failures)
                self.email(body)
            except:
                logging.error("Could not send email report")
        if shelfdb['ta'][9] == True:
            self.htmlgen()

    # def site_pool(self, site):
    #    dive = connection_from_url(site, timeout=9, maxsize=33, block=True)

    def run_repository_threads(self, scripts, module, driver):
        logging.info("Running Engine Mirror Thread: {}".format(driver))
        logging.info("Parsing: {}".format(module))
        repscriptopen = open(self.scripts + "/" + module, 'r')
        repscript = repscriptopen.readlines()

        for repscriptline in repscript:
            try:
                exec(repscriptline)
            except:
                self.failures = self.failures + 1
                driver.screenshot("{}_{}".format(repscriptopen.name,
                                                   repscriptline))
                logging.error("Exec Line Failed: {}".format(repscriptline))
                if shelfdb['ta'][7] == True:
                    driverDB.insert(module, repscriptline, 1)
                repscriptopen.close()
                self.thread_total = self.thread_total - 1
                self.script_max = self.script_max - 1
                self.running = self.running - 1
                driver.engine.quit()
                thread.exit()
                return

        self.successes = self.successes + 1
        self.thread_total = self.thread_total - 1
        self.script_max = self.script_max - 1
        self.running = self.running - 1
        repscriptopen.close()
        driver.engine.quit()
        thread.exit()

    def runonce(self, instance, scripts=[]):
        logging.info("Test Cycle: Run Once Starting")
        singlescript = open(self.scripts, 'r')
        script = singlescript.readlines()
        total = [0]
        count = 1
        for count in total:
            try:
                for line in script:
                    logging.info("Test Cycle: Run Once |"
                                 " Exec Line: {}, {}".format(singlescript.name,
                                                             line))
                    exec(line)
                    logging.info(" - Test Cycle: Run Once |"
                                 "Exec Line Success: {}, {}"
                                 .format(singlescript.name, line))
            except:
                self.failures = self.failures + 1
                logging.error("! Test Cycle: Run Once |"
                              " Exec Line Failed: {}, {}"
                              .format(singlescript.name, line))
                Sg.Print("\n! Test Cycle: Run Once\nExec Line Failed: {}, {}"
                         .format(singlescript.name, line))

                if shelfdb['ta'][7] == True:
                    driverDB.insert(singlescript.name, line, 1)
                singlescript.close()
                continue
            self.successes = self.successes + 1

        logging.info(
                " - Test Cycle: Run Once Completed | {} | Successes: {} |"
                " Failures: {}".format("1", self.successes, self.failures))
        Sg.Print("\nRun Once Test Complete\nSuccesses: {} \n"
                 "Failures: {}".format(self.successes, self.failures))

        if shelfdb['ta'][11] == True:
            body = "Test Cycle: Run Once Completed | " \
                   "Successes: {} | Failures: {}".format(self.successes,
                                                         self.failures)
            self.email(body)

class Mirror(object):
    def __init__(self, instance):
        self.instance = instance
        if str(shelfdb['ta'][0]) == "Firefox":
            logging.info("Mirroring Engine Driver")
            self.engine = webdriver.Firefox(executable_path=
                                            "drivers/geckodriver{}.exe")

    def destroy(self):
        del self.instance.engine

    def close(self):
        self.instance.engine.quit()

    # b = Instance()
    # a = Mirror(b)


# ######################################################################### ###
# ###########                 AUDIO CONTROLLER                  ########### ###
# ######################################################################### ###


platform = 'Windows'


class Audio(object):
    def __init__(self):
        event = ''
        audio_platform = {
            'Windows': 'c:\\Windows\\media\\',
            'Linux': '/usr/share/sounds/gnome/default/alerts'

        }

        self.audio_path = audio_platform.get(platform)

    def play_sound(self, event, platform):
        audio_dict = {
            'launchapp': 'ir_inter',
            'addbutt': 'Speech Off',
            'buildlaunch': 'Speech On',
            'launch': 'Windows Proximity Notification',
            'quit': '',
            'highlight': 'Windows Print complete',
            'save': '',
            'load': '',
            'testcomplete': 'Alarm04'

        }

        audio_generator = {
            'Windows': 'winsound.PlaySound(\'{}\{}.wav\', '
                       'winsound.SND_FILENAME)'
                .format(self.audio_path, audio_dict.get(event))
        }

        try:
            play_it = audio_generator.get(platform)
            exec(play_it)
        except:
            logging.warning("Cannot Process Sound Files for Audio")


sound = Audio()
sound.play_sound('launchapp', platform)


# ######################################################################### ###
# ###########                 NETWORK CONTROLLER                ########### ###
# ######################################################################### ###

class Networking(object):
    def __init__(self, server_ip, server_port, server_password,
                 server_data, object_pass):
        self.server_ip = server_ip
        self.server_password = server_password
        self.server_port = server_port
        self.sock_obj = socket(AF_INET, SOCK_STREAM)
        # self.sock_obj.settimeout(30) no timeout
        self.server_send_data = server_data
        self.object_pass = object_pass

    # ########################
    # ##   NETWORK LISTEN   ##
    # ########################

    def open_connection_listener(self):
        self.sock_obj.bind((self.server_ip, self.server_port))
        self.sock_obj.listen(99)
        while True:
            # print("Starting Server")
            connection, address = self.sock_obj.accept()
            # print("Accepted Connection")
            thread.start_new_thread(
                    self.open_connection_thread_listener,
                    (connection, address))

    def open_connection_thread_listener(self, connection, address):
        while True:
            received_data = connection.recv(1024)
            # print("Data: {}, Address: {}").format(received_data, address)
            if received_data == "task":
                Scheduler("do", self.object_pass)
            else:
                pass


# ########################
# ##    NETWORK SEND    ##
# ########################

    def open_connection_sender(self):
        thread.start_new_thread(
                self.open_connection_thread_sender,
                (self.server_ip, self.server_port, self.server_send_data))

    def open_connection_thread_sender(self, server_ip, server_port,
                                      server_send_data):
        self.sock_obj.connect((self.server_ip, self.server_port))
        self.sock_obj.send(str.encode(self.server_send_data))


# ######################################################################### ###
# ###########                 SCHEDULE CONTROLLER               ########### ###
# ######################################################################### ###

class Scheduler(object):
    def __init__(self, task, object_pass):
        self.task = task
        self.repository = "repository"
        self.object_pass = object_pass

    def run_repository(self):
        TestCycle("repository", self.object_pass.driver,
                  self.object_pass.driver.repositoryroot,
                  self.object_pass.driver.browsername,
                  self.object_pass.driver.siteaddress,
                  self.object_pass.driver.appName)

    def run_single(self):
        TestCycle("single", self.object_pass.driver,
                  self.object_pass.driver.repositoryroot,
                  self.object_pass.driver.browsername,
                  self.object_pass.driver.siteaddress,
                  self.object_pass.driver.appName)


# ######################################################################### ###
# ###########       PROXY: Process Traffic Through Burp         ########### ###
# ######################################################################### ###

class Burp(object):
    pass

# ######################################################################### ###
# ###########         GUI: Layouts and Declarations             ########### ###
# ######################################################################### ###

# ########################
# ## MATPLOT PREP (GUI) ##
# ########################


def draw_graph(canvas, figure, loc=(0, 0)):
   figure_canvas_agg = FigureCanvasAgg(figure)
   figure_canvas_agg.draw()
   figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
   figure_w, figure_h = int(figure_w), int(figure_h)
   photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)
   canvas.create_image(
           loc[0] + figure_w / 2, loc[1] + figure_h / 2, image=photo)
   tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
   return photo


def set_graph():
   global figure_w, figure_h, fig
   fig = plt.figure()
   ax = fig.add_subplot(111)
   x = 1
   y = 2
   plt.plot(x, y)
   plt.subplots_adjust(right = 2, left = 1, top = 1, bottom = 0.5)#

   figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
   fig.tight_layout()


set_graph()

# ########################
# ## Main Window (GUI)  ##
# ########################

# ########################
# ## IMAGES (Base 64)   ##
# ########################

maindisplay = [  #[Sg.T("")],
               [Sg.Button(image_data=TestAnatomy_images.main_config,
                          key="config", tooltip="Open Config Window"),
                Sg.Button(image_data=TestAnatomy_images.main_build,
                          key="build", tooltip="Open Build Window"),
                Sg.Button(image_data=TestAnatomy_images.main_test,
                          key="test", tooltip="Open Test Window")],

               [Sg.ReadButton('', image_data=TestAnatomy_images.license,
                              key="license", tooltip="View Legal / License"),
                Sg.T("", size=(9, 1)),
                Sg.ReadButton("", image_data=TestAnatomy_images.report,
                              key="report", tooltip="Reporting Configuration"),
                Sg.ReadButton("", image_data=TestAnatomy_images.log,
                              key="log", tooltip="Open Log"),
                Sg.ReadButton('', image_data=TestAnatomy_images.main_track,
                              key="track", tooltip="Open Graphing"),
                Sg.ReadButton('', image_data=TestAnatomy_images.github_small,
                              key="github", tooltip="Open Github Repository"),
                Sg.ReadButton('', image_data=TestAnatomy_images.exit,
                              key="exit", tooltip="Quit TA")]]

layout = [[Sg.Column(maindisplay)]]

icon = TestAnatomy_images.icon

debug.initialize()

mainWindow = Sg.Window("Test Anatomy (v1.1) - Main Menu",
                       auto_size_text=False, icon=TestAnatomy_images.icon,
                       border_depth=0).Layout(
        maindisplay).Finalize()


# ######################################################################### ###
# ###########               GUI: Main Loop                      ########### ###
# ######################################################################### ###

configWindow_active = False
buildWindow_active = False
testWindow_active = False # TODO: Review button changes to 'Single'
trackWindow_active = False
reportWindow_active = False
screenshotWindow_active = False

# buildWindow_sl = False
buildWindow_sl_active = False

testTypeSingle = False
testTypeMulti = False

verified = False
loadsingle = False
loadrepository = False
savebuildcontents = False

ss_window_x = 70
ss_window_y = 70

def config_manage(action, configs): # action (save/load), global configs)
    logging.info("Window 2: Pressed Save")

    testername = configWindow.FindElement('testername')
    browsertype = configWindow.FindElement('browsertype')
    appuri = configWindow.FindElement('appuri')
    appname = configWindow.FindElement('appname')
    emailfrom = configWindow.FindElement('emailfrom')
    emailto = configWindow.FindElement('emailto')
    emailusername = configWindow.FindElement('emailusername')
    emailpassword = configWindow.FindElement('emailpassword')
    databasecheck = configWindow.FindElement('databasecheck')
    emailcheck = configWindow.FindElement('emailcheck')
    dbhost = configWindow.FindElement('dbhost')
    dbip = configWindow.FindElement('dbip')
    dbun = configWindow.FindElement('dbun')
    dbpw = configWindow.FindElement('dbpw')
    dbport = configWindow.FindElement('dbport')
    repositorypath = configWindow.FindElement('repositorypath')
    sideload = configWindow.FindElement('sideload')

    if action == "save":
        try:
            configs['platform'] = str(values3['browsertype'])
            configs['url'] = values3['appuri']
            configs['title'] = str(values3['appname'])
            data_man.testername = values3['testername']
            configs['repository'] = values3['repositorypath']

            # database
            configs['database_ip'] = values3['dbip']
            configs['database_port'] = values3['dbport']
            configs['database_name'] = values3['dbhost']
            configs['database_username'] = values3['dbun']
            configs['database_password'] = values3['dbpw']

            # email
            configs['email_from'] = values3['emailfrom']
            configs['email_to'] = values3['emailto']
            configs['email_username'] = values3['emailusername']
            configs['email_password'] = values3['emailpassword']

            # checkboxes
            configs['sql'] = values3['databasecheck']
            # SQL database
            configs['sl'] = values3['sideload']  # sideload mods
            # usage
            configs['email_check'] = values3['emailcheck']

            with open("database/ta.config", 'w') as config_file:
                json.dump(configs, config_file)
                print(configs['title'], print(values3['appname']))
            with open("database/ta.config", 'r') as config_file:
                configs = json.load(config_file)
                print(configs['title'], print(values3['appname']))

            logging.info("Saved Configs Successfully")

        except:
            logging.error("Issue saving configs")
            Sg.PopupOK("Issue saving configs")

    if action == "load":
        logging.info("Config: Pressed Load")
        testername = configWindow.FindElement('testername')
        browsertype = configWindow.FindElement('browsertype')
        appuri = configWindow.FindElement('appuri')
        appname = configWindow.FindElement('appname')
        emailfrom = configWindow.FindElement('emailfrom')
        emailto = configWindow.FindElement('emailto')
        emailusername = configWindow.FindElement('emailusername')
        emailpassword = configWindow.FindElement('emailpassword')
        databasecheck = configWindow.FindElement('databasecheck')
        emailcheck = configWindow.FindElement('emailcheck')
        dbhost = configWindow.FindElement('dbhost')
        dbip = configWindow.FindElement('dbip')
        dbun = configWindow.FindElement('dbun')
        dbpw = configWindow.FindElement('dbpw')
        dbport = configWindow.FindElement('dbport')
        repositorypath = configWindow.FindElement('repositorypath')
        sideload = configWindow.FindElement('sideload')

        try:
            # MAIN SETTINGS
            browsertype.Update(configs['platform'])
            appuri.Update(configs['url'])
            appname.Update(configs['title'])
            testername.Update(data_man.testername)

            # EMAIL SETTINGS
            emailto.Update(configs['email_to'])
            emailfrom.Update(configs['email_from'])
            emailusername.Update(configs['email_username'])

            # CHECKBOX SETTINGS
            databasecheck.Update(configs['sql'])
            sideload.Update(configs['sl'])
            emailcheck.Update(configs['email_check'])

            # DATABASE SETTINGS
            dbhost.Update(configs['database_name'])
            dbip.Update(configs['database_ip'])
            dbun.Update(configs['database_username'])
            dbport.Update(configs['database_port'])

            # REPOSITORY SETTINGS
            repositorypath.Update(configs['repository'])

            # Passwords can optionally be enabled (Insecure):
            # emailpassword.Update(configs['email_password'])
            # dbpw.Update(configs['database_password'])

            logging.info("Updated Configs Successfully")

        except:
            logging.info("Issue loading from Config")
            Sg.PopupOK("Issue loading from Config")


while True:

    b, values = mainWindow.Read(timeout=100)

    debug.refresh(locals(), globals())  # call the debugger to

    if b != Sg.TIMEOUT_KEY:
        pass
    if b == "license":
        Sg.PopupOK("Test-Anatomy (TA) Version: 1.1\n"
                   "Base TA Code Copyright: Eric  \n"
                   "Kiosk Modifications Belong to %company%\n"
                   "License: DO_NOT_DISTRIBUTE_WITHOUT_CONSENT",
                   title="License Details")

        logging.info("Window 1: Pressed License")

    if b == "github":
        webbrowser.open("https://www.github.com/eagleEggs")

    if b == "report":
        reportWindow_active = True

        report_layout = [[Sg.T("Application Name:         ", size=(15,0)), Sg.InputText(
                '')],
                         [Sg.T("Company Name:", size=(15,0)), Sg.InputText(
                                 '')],
                         [Sg.T("Contract ID:", size=(15,0)), Sg.InputText('')],
                         [Sg.T("Company Logo:   ", size=(15,0)), Sg.Button("",
                                        image_data=TestAnatomy_images.imgload,
                                                         key="report_image1"),
                          Sg.InputText("", size=(39, 1))],
                         # [Sg.T("Image 2:   ", ), Sg.Button("Load Image",
                         #                                disabled=True,
                         #
                         # key="report_image2")],
                         # [Sg.T("Footer 1:  "), Sg.InputText('')],
                         # [Sg.T("Footer 2:  "), Sg.InputText('')],
                         [Sg.T("", size=(52,0)), Sg.Button("",
                                               key="reload_report_template",
                                                     image_data=
                                           TestAnatomy_images.reload_small,
                                                     tooltip="Reload Report "
                                                             "Template")],
                         [Sg.T("", size=(36,0)), Sg.Button("",
                                    tooltip="Save and open Report Preview",
                                    image_data=TestAnatomy_images.preview,
                                    key="report_preview"),
                          Sg.Button('', tooltip="Save Preview to Project "
                                                "Folder",
                                    image_data=TestAnatomy_images.save,
                                                        key="report_save")]]

        reportWindow = Sg.Window(
                'Test Anatomy - Reporting',
                grab_anywhere=False,
                no_titlebar=False,
                auto_size_text=False,
                icon=icon).Layout(report_layout).Finalize()


    if reportWindow_active:
        b_report, v_report = reportWindow.Read(timeout=0)

        if b_report == 'Exit':
            trackWindow_active = False
            # logging.info("Report Window Inactive, Clicked Exit or None")
            reportWindow.Close()

        if not b_report:
            pass

        if b_report == "reload_report_template":
            try:
                sys.path.append('../')
                sys.path.append(os.path.dirname(sys.executable))
                import TA_Report_Template
                importlib.reload(TA_Report_Template)
                logging.info("Reloaded Report Template")
                Sg.PopupOK("Report Template Reloaded")
            except (ImportError, ImportWarning, IndentationError,
                    SyntaxError, NoSuchElementException, NameError,
                    NoSuchWindowException,
                    ModuleNotFoundError) as report_import_error:
                logging.error(report_import_error)
                Sg.PopupOK("Issue Reloading Report Template"
                           "\n{}".format(report_import_error))

        if b_report == "report_preview":
            logging.info("Beginning Report Preview...")
            pre_report = TA_Report_Template.Report("0000-0000-0000-0000",
                                        "Test_App_Name",
                                                   "C:\\Users\\Administrator\\Documents\\GitHub\\_testAnatomy\\TA\\demo_logo.png",
                                                   "Test Company",
                                                   "Contract: ABCYEAYOUGNOME"
                                                   ).finalize_html(
                    driver)
            system('start {}'.format(driver.folder))
            logging.info("Report Saved and Available for Preview within "
                         "Report Folder: {}".format(driver.report_folder))

        if b_report == "report_save":
            pre_report = TA_Report_Template.Report("0000-0000-0000-0000",
                                        "Test_App_Name").finalize_html(driver)
            logging.info("Report Saved and Available for Preview within "
                         "Report Folder: {}".format(driver.report_folder))


    if b == "exit":
        logging.info("Window 1: Pressed Exit")
        # shelfdb.close()
        try:
            driver.engine.close()
            logging.info("Closing Browser Session...")
        except (NameError, NoSuchWindowException, WebDriverException):
            logging.info("No Browser Session to Close.")
        logging.info("Closed Test Anatomy")
        logging.shutdown()
        break

    if b == "log":
        try:
            system('start etc/cmtrace.exe TestAnatomy.log')

        except:
            logging.warning("Issue opening cmtrace")
            Sg.PopupOK("Issue opening log in cmtrace")

    # #########################
    # ## Graph Window (GUI)  ##
    # #########################

    if b == "track":

        BAR_WIDTH = 100
        BAR_SPACING = 150
        EDGE_OFFSET = 3
        GRAPH_SIZE = (500, 500)
        DATA_SIZE = (500, 500)

        graph = Sg.Graph(GRAPH_SIZE, (0, 0), DATA_SIZE)

        trackWindow_active = True
        logging.info("Tracking Window Active: Pressed Track")
        trackWindow = Sg.Window(
                'Test Anatomy - Tracking',
                grab_anywhere=True,
                no_titlebar=False,
                icon=icon).Layout(
                [[Sg.Canvas(size=(figure_w, figure_h), key='canvas_graph'),
                    #graph,
                    Sg.ReadButton('', border_width=0,
                                  image_data=TestAnatomy_images.track_refresh,
                                  key="Refresh")],
                 [Sg.T("Plot Type:"), Sg.Combo(dd_plottypes, key="plottypes")],
                 [Sg.T("Style:"),Sg.Combo(dd_plotstyles, key="plotstyles")],
                 [Sg.T("Index:"), Sg.Combo(dd_database, key="db_index")],
                 [Sg.T("Hue:"), Sg.Combo(dd_database, key="db_hue")],
                 [Sg.T("Start Date:"), Sg.T("D:"), Sg.InputText(
                         "", size=(3, 0), key="sday"),
                  Sg.T("M:"), Sg.InputText("", size=(3, 0), key="smonth"),
                  Sg.T("Y:"),
                  Sg.InputText("", size=(4, 0), key="syear")],
                 [Sg.T("End Date:"), Sg.T("D:"), Sg.InputText(
                         "", size=(3, 0), key="eday"),
                  Sg.T("M:"), Sg.InputText("", size=(3, 0), key="emonth"),
                  Sg.T("Y:"),
                  Sg.InputText("", size=(4, 0), key="eyear")],
                 [Sg.T("x:"), Sg.Combo(dd_database, key="track_x"),
                  Sg.T("=="), Sg.InputText("")],
                 [Sg.T("y:"), Sg.Combo(dd_database, key="track_y"),
                  Sg.T("=="), Sg.InputText(""), Sg.Button("Today Pass/Fail")
                 ]]).Finalize()

        fig_photo = draw_graph(
               trackWindow.FindElement('canvas_graph').TKCanvas, fig)

    if trackWindow_active:
        b5, values5 = trackWindow.Read(timeout=0)
        if b5 != Sg.TIMEOUT_KEY:
            pass
        if b5 == 'Exit' or b5 is None:
            trackWindow_active = False
            logging.info("Tracking Window Set Inactive, Clicked Track")
            trackWindow.Close()
        if b5 == "Refresh":
            if values5['plottypes'] == "heat":
                try:
                    driverDB.set_plot_heat(
                            values5['db_index'], values5['track_x'], values5[
                        'track_y'], values5['plotstyles'])
                    fig_photo = driverDB.PlotDraw(
                            trackWindow.FindElement('canvas_graph').TKCanvas, fig)
                    logging.info("Tracking Window - Updated Graph")
                except:
                    logging.warning("Issue updating Heat Graph")

            if values5['plottypes'] == "bar":
                try:
                    syear = int(values5['syear'])
                    sday = int(values5['sday'])
                    smonth = int(values5['smonth'])
                    eyear = int(values5['eyear'])
                    eday = int(values5['eday'])
                    emonth = int(values5['emonth'])

                    # convert time for mySQL:
                    start_time = datetime.datetime(syear, smonth,
                                                   sday).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.datetime(eyear, emonth, eday).strftime(
                            '%Y-%m-%d %H:%M:%S')

                    driverDB.set_plot_bar(values5['db_index'],
                                                values5['db_hue'],
                                                values5['track_x'],
                                                values5['track_y'],
                                                start_time, end_time,
                                                values5['plotstyles'])
                    fig_photo = driverDB.PlotDraw(
                            trackWindow.FindElement('canvas_graph').TKCanvas, fig)
                    logging.info("Tracking Window - Updated Graph")
                except:
                    logging.warning("Issue updating Bar Graph")

            else:
                logging.info("No Chart Type Selected")
                pass

            if values5['plottypes'] == "line":
                try:
                    syear = int(values5['syear'])
                    sday = int(values5['sday'])
                    smonth = int(values5['smonth'])
                    eyear = int(values5['eyear'])
                    eday = int(values5['eday'])
                    emonth = int(values5['emonth'])

                    # convert time for mySQL:
                    start_time = datetime.datetime(syear, smonth,
                                                   sday).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.datetime(eyear, emonth, eday).strftime(
                            '%Y-%m-%d %H:%M:%S')

                    driverDB.set_plot_line(values5['db_index'],
                                          values5['db_hue'],
                                          values5['track_x'],
                                          values5['track_y'],
                                          start_time, end_time,
                                          values5['plotstyles'])
                    fig_photo = driverDB.PlotDraw(
                            trackWindow.FindElement('canvas_graph').TKCanvas, fig)
                    logging.info("Tracking Window - Updated Graph")
                except:
                    logging.warning("Issue updating Line Graph")

            else:
                logging.info("No Chart Type Selected")
                pass

        if b5 == "home":
            trackWindow_active = False
            logging.info("Tracking Window Set Inactive: Pressed Main Menu")
            trackWindow.Close()

    # ##########################
    # ## Config Window (GUI)  ##
    # ##########################
    if b == "config":  # main menu config button press
        configWindow_active = True
        logging.info("Window 2 Active: Pressed Config")

        configlayoutloop_general = [[Sg.Frame("Quick Launch",
                                              [[Sg.Text('Platform:',
                                                        size=(20, 0)),
                                                Sg.InputCombo(
                                                        ddVals, default_value=
                                                        "",
                                                        key="browsertype",
                                                        size=(42, 10))],
                                               [Sg.Text('URL:', size=(20, 0)),
                                                Sg.Input(
                                                        "",
                                                        key='appuri',
                                                              size=(42, 10))],
                                               [Sg.Text('Application Title:',
                                                        size=(20, 0)),
                                                Sg.InputText(
                                                        "",
                                                             key='appname',
                                                             do_not_clear=
                                                             True)],
                                               [Sg.Text(
                                                   'Repository Root Path:',
                                                   size=(20, 0)),
                                                Sg.InputText(
                                                        "",
                                                        key='repositorypath',
                                                        do_not_clear=True,
                                                             size=(40, 1)),
                                            Sg.Button("", key="root_search",
                                     image_data=TestAnatomy_images.search)],
                                               [Sg.Text('Automation Engineer:',
                                                        size=(20, 0)),
                                                Sg.InputText(
                                                        "",
                                                        key='testername',
                                                        do_not_clear=
                                                        True)]])]]

        configlayoutloop_appdetails = [[Sg.Frame("Application "
                                              "Details:", [[
                                        Sg.Text('Build:',
                                                 size=(20, 0)),
                                         Sg.InputText(
                                                 "",
                                                 key='appbuild',
                                                 do_not_clear=
                                                 True)],
                                        [Sg.Text('Release:',
                                                 size=(20, 0)),
                                         Sg.InputText(
                                                 "",
                                                 key='apprelease',
                                                 do_not_clear=
                                                 True)],
                                        [Sg.Text('Version:',
                                                 size=(20, 0)),
                                         Sg.InputText(
                                                 "",
                                                 key='appversion',
                                                 do_not_clear=
                                                 True)],
                                        [Sg.Text('Branch:',
                                                 size=(20, 0)),
                                         Sg.InputText(
                                                 "",
                                                 key='appbranch',
                                                 do_not_clear=
                                                 True)],
                                        [Sg.Text('Event Title:',
                                                 size=(20, 0)),
                                         Sg.InputText(
                                                 "",
                                                 key='appevent',
                                                 do_not_clear=
                                                 True)]])]]

        configlayoutloop_email = [[Sg.Frame("Email",
                                            [[Sg.Text('From:', size=(20, 0)),
                                              Sg.InputText(str(
                                                      ""),
                                                           key='emailfrom',
                                                           size=(45, 10),
                                                           do_not_clear=True)],
                                             [Sg.Text('To:', size=(20, 0)),
                                              Sg.InputText(str(
                                                      ""),
                                                           key='emailto',
                                                           size=(45, 10),
                                                           do_not_clear=True)],
                                             [Sg.Text('Username:',
                                                      size=(20, 0)),
                                              Sg.InputText("",
                                                           key='emailusername',
                                                           size=(45, 10),
                                                           do_not_clear=True)],
                                             [Sg.Text('Password:',
                                                      size=(20, 0)),
                                              Sg.InputText("",
                                                           key='emailpassword',
                                                           password_char="*",
                                                           size=(45, 10),
                                                           do_not_clear=True)],
                                             [Sg.Text('Server:', size=(20, 0)),
                                              Sg.InputText('',
                                                           key='emailserver',
                                                           size=(45, 10),
                                                           do_not_clear=True)],
                                             [Sg.Text('Existing Project UUID:',
                                                      key="projectUUIDID",
                                                      visible=False,
                                                      size=(20, 0))]])]]

        configlayoutloop_reporting = [[Sg.Frame("Reporting",
                                                [[Sg.Checkbox('HTML',
                                                              size=(10, 0),
                                                              key='htmlcheck',
                                                              default=
                                                              1),
                                                  Sg.Checkbox('Email',
                                                              size=(10, 0),
                                                              key='emailcheck',
                                                              default=
                                                              0,
                                                              disabled=True),

                                                  Sg.Checkbox('PDF',
                                                              size=(10, 0),
                                                              key='pdfcheck',
                                                              default=
                                                              1),
                                                  Sg.Checkbox('Create Graphs',
                                                              size=(14, 0),
                                                              key='graphcheck',
                                                              default=
                                                              0)]])]]

        configlayoutloop_testing = Sg.Column([[Sg.Frame("Test Server",
                                                        [[Sg.Text("Server: "),
                                                          Sg.InputText(
                                                              "Server IP",
                                                                size=(45, 10),
                                                            key="server_ip")],
                                                         [Sg.ReadButton(
                                                                 "Launch")]])]]
                                             )

        configlayoutloop_db = [[Sg.Frame("Database",
                                         [[Sg.Text('DB Name / Port / IP:',
                                                   size=(20, 1)),
                                           Sg.InputText("",
                                                        key='dbhost',
                                                        size=(15, 10),
                                                        do_not_clear=True,
                                                        change_submits=True),
                                           Sg.InputText("",
                                                        key='dbport',
                                                        size=(11, 1),
                                                        do_not_clear=True),

                                           Sg.InputText("",
                                                        key='dbip',
                                                        size=(15, 1),
                                                        do_not_clear=True,
                                                        change_submits=True)],
                                          [Sg.Text('Username / '
                                                   'Password:', size=(20,
                                                                        1)),
                                           Sg.InputText("",
                                                        key='dbun',
                                                        size=(15, 10),
                                                        do_not_clear=True),

                                           Sg.InputText('', key='dbpw',
                                                        size=(28, 10),
                                                        password_char="*",
                                                        do_not_clear=True)],
                                          [Sg.Checkbox('SQL Database',
                                                       size=(17, 0),
                                                       key='databasecheck',
                                                       default=1),
                                          Sg.Checkbox("Local Mods",
                                                        size=(15, 0),
                                                        default=1,
                                                        key="sideload"),
                                           Sg.Checkbox("Network Mods",
                                                       size=(12, 0),
                                                       default=1,
                                                       key="sideload"),
                                           # Sg.T("", size=(3, 0)),
                                           Sg.Button("", key="reload_mods",
                                                     image_data=
                                           TestAnatomy_images.reload_small,
                                                     tooltip="Reload Mods")
                                            ]])]]

        configlayoutloop_cycles = [[Sg.Frame("Test Cycle Throttling",
                                             [[Sg.Slider([0,60], size=(45, 10),
                                                         key='throttle',
                                                         default_value=0,
                                                         disabled = True,
                                                         enable_events=True,
                                                         orientation='h')]],
                                             size=(35, 55))]]

        configlayoutloop_launch = [[Sg.ReadButton(
                "",
                tooltip='Start Testing Environment',
                key="Launch2",
                image_data=TestAnatomy_images.HLlaunch),
            Sg.ReadButton(
                    "",
                    image_data=TestAnatomy_images.save,
                    key="config_save",
                    tooltip='Save'),
            Sg.ReadButton(
                    "",
                    image_data=TestAnatomy_images.load,
                    key="config_load",
                    tooltip='Load'),
            Sg.ReadButton(
                    "",
                    image_data=TestAnatomy_images.home,
                    key="home",
                    tooltip='Main Menu')]]

        configlayoutlooppane = [[
            Sg.Column(configlayoutloop_general)],
            [Sg.Column(configlayoutloop_appdetails)],
            [Sg.Column(configlayoutloop_db)],
            [Sg.Column(configlayoutloop_reporting)],
            # [Sg.Column(configlayoutloop_email)], # REMOVED 042519
            [Sg.Column(configlayoutloop_launch)]]

        configWindow = Sg.Window(
                'Test Anatomy - Configuration',
                grab_anywhere=False,
                no_titlebar=False,
                auto_size_text=True,
                icon=icon).Layout(configlayoutlooppane)

        data_man.load_configs()

        # Sg.PopupOK("There is an issue with the config file "
        #          "(/database/ta.config")

    # ########################
    # ## Test Window (GUI)  ##
    # ########################

    if b == "test":  # main menu test button press
        testWindow_active = True
        logging.info("Window 4 Active: Pressed Test")

        testsingleimg = TestAnatomy_images.tsingle
        testmultiimg = TestAnatomy_images.tmulti

        testlayoutloop_local = [[  # Sg.Column(
                # [[Sg.Frame("Local Testing",
                   Sg.ReadButton(
                      image_data=TestAnatomy_images.tsingle,
                      button_text='', key="loadsingle"),
                    Sg.Image(data=TestAnatomy_images.or_image),
                    Sg.ReadButton(image_data=TestAnatomy_images.tmulti,
                                  button_text='', key="loadrep"),
                    Sg.Image(data=TestAnatomy_images.arrowright),
                    Sg.ReadButton(image_data=TestAnatomy_images.treview,
                                  button_text='', key="testreview"),
                    Sg.Image(data=TestAnatomy_images.arrowright),
                    Sg.ReadButton(image_data=TestAnatomy_images.tgo,
                                  button_text='', key="go")],
            [Sg.T("Cycles:      ", tooltip="Total number of times to "
                                                "run the test event"),
                    Sg.Slider([1, 1000], size=(72, 10),
                       key='cycles',
                       default_value=0, tooltip="Total number of times to "
                                                "run the test event",
                       enable_events=True,
                       orientation='h')],
            [Sg.T("Throttle:     ", tooltip="Number of scripts to "
                                                "thread concurrently"),
                        Sg.Slider([0, 100], size=(72, 10),
                       key='throttle', disabled= True,
                       default_value=0, tooltip="Number of scripts to "
                                                "thread concurrently",
                       enable_events=True,
                       orientation='h')],
            [Sg.T("Step Break:", tooltip="Seconds in between each "
                                                    "step in a test script"),
                                        Sg.Slider([0, 180], size=(72, 10),
                                       key='brake',
                                       default_value=0,
                                            tooltip="Seconds in between each "
                                                    "step in a test script",
                                       enable_events=True,
                                       orientation='h')],
            [Sg.T("GIF Break: ", tooltip="Seconds in between "
                                                "images of the GIF report"),
                                    Sg.Slider([0, 60], size=(72, 10),
                                       key='gif',
                                       default_value=0,
                                            tooltip="Seconds in between "
                                                    "images of the GIF report",
                                       enable_events=True,
                                       orientation='h')],
            [Sg.Frame("Reporting",
                                                [[Sg.Checkbox('HTML',
                                                              size=(15, 0),
                                                              key='htmlcheck',
                                                              default=
                                                              0),
                                                  Sg.Checkbox('Email',
                                                              size=(15, 0),
                                                              key='emailcheck',
                                                              default=
                                                              0),

                                                  Sg.Checkbox('PDF',
                                                              size=(15, 0),
                                                              key='pdfcheck',
                                                              default=
                                                              0),
                                                  Sg.Checkbox('Graphs',
                                                              size=(15, 0),
                                                              key='graphcheck',
                                                              default=
                                                              0),
                                                  Sg.Checkbox('GIF',
                                                              size=(23, 0),
                                                              key='GIF')

                                                  ]])
        ],

            [Sg.Frame("Proxy",
                      [[Sg.Radio('None', group_id="proxy",
                                    size=(15, 0),
                                    key='proxy_log_all'),

                          Sg.Radio('Basic', group_id="proxy",
                                    size=(15, 0),
                                    key='proxy_log_all'),

                        Sg.Radio('Advanced (Req. BurpSuitePro)',
                                 group_id="proxy",
                                    key='proxy_log_burp')

                        ]])
             ]
        ]

        testlayoutloop_remote = Sg.Column(
                [[Sg.Frame("Remote Testing", [[Sg.ReadButton(
                        image_data=TestAnatomy_images.tsingle,
                        button_text='', key="loadsingle"),
                    Sg.Image(data=TestAnatomy_images.or_image),
                    Sg.ReadButton(image_data=TestAnatomy_images.tmulti,
                                  button_text='', key="loadrep"),
                    Sg.Image(data=TestAnatomy_images.arrowright),
                    Sg.ReadButton(image_data=TestAnatomy_images.treview,
                                  button_text='', key="testreview")]])]])

        testlayoutlooppane = [[
            Sg.Pane([testlayoutloop_local, Sg.Column([[
                Sg.Pane([testlayoutloop_remote], handle_size=25)]])],
                    handle_size=25)]]

        testWindow = Sg.Window('Test Anatomy - Test',
                               grab_anywhere=False,
                               no_titlebar=False, icon=icon).Layout(
                testlayoutloop_local)

    if testWindow_active:
        b4, values4 = testWindow.Read(timeout=0)

       # PySimpleGUIdebugger.refresh(locals(),
        #                            globals())  # call the debugger to
        # refresh the items being shown

        if b4 != Sg.TIMEOUT_KEY:
            pass
        if b4 == 'Exit' or b4 is None:
            testWindow_active = False
            logging.info("Window 4 Set Inactive, Clicked Exit")
            testWindow.Close()
        if b4 == "Main Menu":
            testWindow_active = False
            logging.info("Window 4 Set Inactive, Clicked Main Menu")
            testWindow.Close()
        if b4 == "loadsingle":
            logging.info("Window 4 Active: Pressed Load Single Test")
            try:
                singlefile = Sg.PopupGetFile("Select the Test Script",
                                             initial_folder=
                                             driver.repositoryroot,
                                             default_path=
                                             driver.repositoryroot)
                testWindow.FindElement('loadsingle').Update(
                        image_data=TestAnatomy_images.tsinglesel)
                testWindow.FindElement('loadrep').Update(
                        image_data=TestAnatomy_images.tmulti)
                loadrepository = False
                testTypeSingle = True
                testTypeMulti = False
                if singlefile is not None:
                    testWindow.FindElement('loadsingle').Update(
                            image_data=TestAnatomy_images.tsingleselfin)
                    loadsingle = True
            except:
                Sg.PopupOK("No session active, launch from config")
        if b4 == "loadrep":
            try:
                Sg.PopupOKCancel("Verify Settings:\n{}".format(
                        driver.repositoryroot))

                loadsingle = False
                logging.info("Window 4 Active: Pressed Load Repository")
                testTypeMulti = True
                testTypeSingle = False
                testWindow.FindElement('loadsingle').Update(
                        image_data=TestAnatomy_images.tsingle)
                testWindow.FindElement('loadrep').Update(
                        image_data=TestAnatomy_images.tmultisel)
                testWindow.FindElement('loadrep').Update(
                        image_data=TestAnatomy_images.tmultiselfin)
                loadrepository = True
            except:
                Sg.PopupOK("No session active, launch from config")

        if b4 == "testreview":
            if testTypeMulti or testTypeSingle:
                testWindow.FindElement('testreview').Update(
                        image_data=TestAnatomy_images.treviewsel)
                review = Sg.PopupYesNo("Hmm you should be fine...")
                if review == "Yes":
                    testWindow.FindElement('testreview').Update(
                            image_data=TestAnatomy_images.treviewselfin)
                    verified = True
                else:
                    testWindow.FindElement('testreview').Update(
                            image_data=TestAnatomy_images.treview)
                    verified = False

        if b4 == "go":
            cycles = values4['cycles']
            brake = values4['brake']
            throttle = values4['throttle']
            if verified and loadsingle:
                TestCycle("single", driver, singlefile,
                          driver.browsername, driver.siteaddress,
                          driver.appName, cycles)
            if loadrepository: # REMOVED VERIFIED TEMPORARILY
                TestCycle("repository", throttle, cycles, brake,
                          driver, driver.repositoryroot,
                          driver.browsername,
                          driver.siteaddress, driver.appName)

    # #########################
    # ## Build Window (GUI)  ##
    # #########################

    if b == "build":  # main menu build button press
        logging.info("Window 3 Active: Pressed Build")

        EHX_column = [[Sg.Image(data=TestAnatomy_images.econfig)],
                      [Sg.Multiline("Enter Element Tag", size=(35, 1),
                                    enter_submits=True, key='enterElement',
                                    do_not_clear=True)],
                      [Sg.InputCombo(ddElements, key="elementtype",
                                     size=(35, 1))],
                      [Sg.InputCombo(ddCols, key="colortype", size=(35, 1))],
                      [Sg.T("", size=(1,1))],
                      [Sg.ReadButton('', key="highlight", border_width=0,
                                     size=(33, 5),
                                     image_data=TestAnatomy_images.HLimg,
                                     tooltip="Highlight Element")]]

        buildcolumn = [[Sg.Image(data=TestAnatomy_images.scriptoptionsconfig)],
                       [Sg.InputCombo(ddbuildactions, key="buildactions",
                                      size=(35, 1))],
                       [Sg.InputText("Add Arguments to Command",
                                     key="enterText", size=(33, 1)),
                        Sg.ReadButton('', key="imgload", border_width=0,
                                      size=(33, 5),
                                      image_data=TestAnatomy_images.imgload,
                                      tooltip="Load Image from Repository")],
                       [Sg.T("")],
                       [Sg.T("")],
                       [Sg.T("")],
                       [Sg.ReadButton('',
                               key="addButt",
                                pad = (0, 11),
                               image_data=TestAnatomy_images.addButt,
                               border_width=0,
                               tooltip="Add the command to your script")]]

        BuildModeColBox = [[Sg.Image(data=TestAnatomy_images.sbuilder)],
                           [Sg.Multiline(size=(81, 22), enter_submits=True,
                                         key='buildscriptbox',
                                         do_not_clear=True,
                                         background_color="white",
                                         auto_size_text=True)],
                           [Sg.Image(data=TestAnatomy_images.boptions)],
                           [Sg.T("Save Script:"),
                            Sg.InputText('',
                                         key='testName', do_not_clear=True,
                                         size=(25, 0)),
                           Sg.Button("", key="api",
                                      image_data=
                                      TestAnatomy_images.api_small,
                                      tooltip="View Scripting API Reference"),
                            Sg.ReadButton("",
                                          image_data=TestAnatomy_images.log,
                                          key="log", tooltip="Open Log"),
                           Sg.ReadButton("",
                                         image_data=TestAnatomy_images.camera,
                                         key="grab_image", tooltip=
                                         "Open Screenshot Tool")],
                           [Sg.ReadButton(
                                   "",
                                   border_width=0,
                                   tooltip='Test This Case',
                                   image_data=TestAnatomy_images.test_code,
                                   key="testbuildcase"),
                               Sg.ReadButton("",
                                             border_width=0,
                                             tooltip='Load a Case',
                                             image_data=
                                             TestAnatomy_images.loadcase,
                                             key="loadcase"),
                               Sg.ReadButton("",
                                             border_width=0,
                                             tooltip='Save This Case',
                                             image_data=
                                             TestAnatomy_images.savecase,
                                             key="savecase"),
                               Sg.ReadButton("",
                                             image_data=
                                             TestAnatomy_images.folder,
                                             border_width=0, key="folder",
                                             tooltip="Open Project Folder"),
                               Sg.ReadButton("",
                                             image_data=
                                             TestAnatomy_images.bnotes,
                                             border_width=0, key="notes",
                                             tooltip="Open Notepad"),
                               Sg.ReadButton("",
                                             image_data=
                                             TestAnatomy_images.sl,
                                             border_width=0, key="sl",
                                             tooltip="Open Sideload Editor"),
                               Sg.ReadButton("",
                                             image_data=
                                             TestAnatomy_images.home,
                                             border_width=0, key="Main Menu",
                                             tooltip="Main Menu")]]

        BuildModeCol = [[Sg.Column(buildcolumn, size=(1, 1), pad=(0,0)),
                         Sg.Column(BuildModeColBox, size=(1, 1), pad=(0,0))]]

        buildWindow = Sg.Window('Test Anatomy - Build', grab_anywhere=False,
                                no_titlebar=False, resizable= True,
                                auto_size_text=True, icon=icon).Layout(
                [[Sg.Column([[Sg.Column(EHX_column), Sg.Column(buildcolumn)],
                 [Sg.Column(BuildModeColBox)]], pad=(0,0))]])

        #PySimpleGUIdebugger.refresh(locals(),
        #                            globals())  # call the debugger to
        # refresh the items being shown

        buildscriptbox = buildWindow.FindElement('buildscriptbox')
        entertext = buildWindow.FindElement('enterText')
        colortype = buildWindow.FindElement('colortype')
        enterelement = buildWindow.FindElement('enterElement')
        testname = buildWindow.FindElement('testName')

        if savebuildcontents:
            buildscriptbox.Update(buildscriptbox_contents)
            entertext.Update(entertext_contents)
            colortype.Update(colortype_contents)
            enterelement.Update(enterelement_contents)
            testname.Update(testname_contents)

        buildWindow_active = True

    if buildWindow_active or buildWindow_sl_active:
        if buildWindow_active:
            buildWindow_sl_active = False
            buildWindow_active = True
            # # print("bw", buildWindow_active)
            b2, values2 = buildWindow.Read(timeout=0)

        if buildWindow_sl_active:
            buildWindow = buildWindow_sl
            buildWindow_active = False
            buildWindow_sl_active = True
            # # print("bw_sl", buildWindow_sl_active)

            b2, values2 = buildWindow_sl.Read(timeout=0)

        if b2 != Sg.TIMEOUT_KEY:
            pass
        if b2 == 'Exit' or b2 is None:
            buildWindow_active = False
            logging.info("Window 3 Set Inactive")
            buildWindow.Close()

        if b2 == "sl" and buildWindow_sl_active:
            savebuildcontents = True
            buildscriptbox_contents = values2['buildscriptbox']
            entertext_contents = values2['enterText']
            colortype_contents = values2['colortype']
            enterelement_contents = values2['enterElement']
            testname_contents = values2['testName']
            sideloadbox_contents = values2['sideloadbox']

            buildscriptbox = buildWindow.FindElement('buildscriptbox')
            sideloadbox = buildWindow.FindElement('sideloadbox')
            entertext = buildWindow.FindElement('enterText')
            colortype = buildWindow.FindElement('colortype')
            enterelement = buildWindow.FindElement('enterElement')
            testname = buildWindow.FindElement('testName')

            buildscriptbox_sl = buildWindow_sl.FindElement(
                    'buildscriptbox')
            sideloadbox_sl = buildWindow_sl.FindElement('sideloadbox')
            entertext_sl = buildWindow_sl.FindElement('enterText')
            colortype_sl = buildWindow_sl.FindElement('colortype')
            enterelement_sl = buildWindow_sl.FindElement('enterElement')
            testname_sl = buildWindow_sl.FindElement('testName')

            buildWindow_sl.Close()

            buildWindow_sl_active = False
            buildWindow_active = True
            buildWindow.Read(timeout=0)

            #PySimpleGUIdebugger.refresh(locals(),
            #                            globals())  # call the debugger to
            # refresh the items being shown

            if savebuildcontents:
                buildscriptbox_sl.Update(buildscriptbox_contents)
                entertext.Update(entertext_contents)
                colortype.Update(colortype_contents)
                enterelement.Update(enterelement_contents)
                testname.Update(testname_contents)
                sideloadbox_sl.Update(sideloadbox_sl)

        if b2 == "sl" and not buildWindow_sl_active:
            savebuildcontents = True
            buildWindow_sl_active = True
            buildWindow_active = False
            logging.info("Build Window (No SL) Active: Pressed Build")

            EHX_column_sl = [[Sg.Image(data=TestAnatomy_images.econfig)],
                          [Sg.Multiline("Enter Element Tag", size=(35, 1),
                                        enter_submits=True, key='enterElement',
                                        do_not_clear=True)],
                          [Sg.InputCombo(ddElements, key="elementtype",
                                         size=(35, 1))],
                          [Sg.InputCombo(ddCols, key="colortype",
                                         size=(35, 1))],
                          [Sg.T("", size=(1, 1))],
                          [Sg.ReadButton('', key="highlight", border_width=0,
                                         size=(33, 5),
                                         image_data=TestAnatomy_images.HLimg,
                                         tooltip="Highlight Element")]]

            buildcolumn_sl = [
                [Sg.Image(data=TestAnatomy_images.scriptoptionsconfig)],
                [Sg.InputCombo(ddbuildactions, key="buildactions",
                               size=(35, 1))],
                [Sg.InputText("Add Arguments to Command",
                              key="enterText", size=(33, 1)),
                 Sg.ReadButton('', key="imgload", border_width=0,
                               size=(33, 5),
                               image_data=TestAnatomy_images.imgload,
                               tooltip="Load Image from Repository")],
                [Sg.ReadButton('',
                               key="addButt",
                               image_data=TestAnatomy_images.addButt,
                               border_width=0,
                               tooltip="Add the command to your script")],
                [Sg.ReadButton('',
                               key="addButtSL",
                               image_data=TestAnatomy_images.addButtSL,
                               border_width=0,
                               tooltip="Add the command to SL")]]

            BuildModeColBox_sl = [[Sg.Image(data=TestAnatomy_images.sbuilder)],
                               [Sg.Multiline(size=(81, 22), enter_submits=True,
                                             key='buildscriptbox',
                                             do_not_clear=True,
                                             # background_color="white",
                                             auto_size_text=True)],
                               [Sg.Image(data=TestAnatomy_images.boptions)],
                               [Sg.T("Save Script:"),
                                Sg.InputText('',
                                             key='testName', do_not_clear=True,
                                             size=(25, 0)),
                                # Sg.Button("", key="reload_mods",
                                #          image_data=
                                #          TestAnatomy_images.reload_small,
                                #          tooltip="Reload Mods"),
                                Sg.Button("", key="api",
                                          image_data=
                                          TestAnatomy_images.api_small,
                                          tooltip="View Scripting API "
                                                  "Reference"),
                                Sg.ReadButton("",
                                              image_data=
                                              TestAnatomy_images.log,
                                              key="log", tooltip="Open Log"),
                                Sg.ReadButton("",
                                              image_data=
                                              TestAnatomy_images.camera,
                                              key="grab_image", tooltip=
                                              "Open Screenshot Tool")],
                               [Sg.ReadButton(
                                       "",
                                       border_width=0,
                                       tooltip='Test This Case',
                                       image_data=TestAnatomy_images.test_code,
                                       key="testbuildcase"),
                                   Sg.ReadButton("",
                                                 border_width=0,
                                                 tooltip='Load a Case',
                                                 image_data=
                                                 TestAnatomy_images.loadcase,
                                                 key="loadcase"),
                                   Sg.ReadButton("",
                                                 border_width=0,
                                                 tooltip='Save This Case',
                                                 image_data=
                                                 TestAnatomy_images.savecase,
                                                 key="savecase"),
                                   Sg.ReadButton("",
                                                 image_data=
                                                 TestAnatomy_images.folder,
                                                 border_width=0, key="folder",
                                                 tooltip="Open Project "
                                                         "Folder"),
                                   Sg.ReadButton("",
                                                 image_data=
                                                 TestAnatomy_images.bnotes,
                                                 border_width=0, key="notes",
                                                 tooltip="Open Notepad"),
                                   Sg.ReadButton("",
                                                 image_data=
                                                 TestAnatomy_images.sl,
                                                 border_width=0, key="sl",
                                                 tooltip="Open Sideload "
                                                         "Editor"),
                                   Sg.ReadButton("",
                                                 image_data=
                                                 TestAnatomy_images.home,
                                                 border_width=0,
                                                 key="Main Menu",
                                                 tooltip="Main Menu")]]

            BuildModeColBoxSL = [[Sg.Image(data=TestAnatomy_images.slbuilder)],
                                 [Sg.Multiline(size=(81, 37),
                                               enter_submits=True,
                                               key='sideloadbox',
                                               do_not_clear=True,
                                               # background_color="white",
                                               auto_size_text=True)],
                                 [Sg.Image(data=TestAnatomy_images.boptions)],
                                 [Sg.Button("", key="reload_mods",
                                            pad=(0, 7),
                                            image_data=
                                            TestAnatomy_images.reload_small,
                                            tooltip="Reload SL")],
                                 [Sg.ReadButton("",
                                                border_width=0,
                                                tooltip='Load Core SL Module',
                                                image_data=
                                                TestAnatomy_images.loadcase,
                                                key="loadsideload"),
                                  Sg.ReadButton("",
                                                border_width=0,
                                                tooltip='Save SL Module',
                                                image_data=
                                                TestAnatomy_images.savecase,
                                                key="savesideload")]]

            BuildModeCol_sl = [[Sg.Column(buildcolumn_sl, size=(1, 1),
                                          pad=(0, 0)),
                             Sg.Column(BuildModeColBox_sl, size=(1, 1),
                                       pad=(0, 0))]]

            BuildModeColSL = [[Sg.Multiline(size=(81, 40), enter_submits=True,
                                            key='buildscriptbox',
                                            do_not_clear=True, pad=(0, 0),
                                            # background_color="white",
                                            auto_size_text=True)]]

            buildWindow_sl = Sg.Window('Test Anatomy - Build + SL',
                                    grab_anywhere=False,
                                    no_titlebar=False, resizable=True,
                                    auto_size_text=True, icon=icon).Layout(
                    [[Sg.Column(
                            [[Sg.Column(EHX_column_sl),
                              Sg.Column(buildcolumn_sl)],
                             [Sg.Column(BuildModeColBox_sl)]], pad=(0, 0)),
                      Sg.Column([[Sg.Column(BuildModeColBoxSL)]],
                                pad=(0, 0))]])

            buildscriptbox_contents = values2['buildscriptbox']
            entertext_contents = values2['enterText']
            colortype_contents = values2['colortype']
            enterelement_contents = values2['enterElement']
            testname_contents = values2['testName']
            try:
                sideloadbox_contents = values2['sideloadbox']
            except:
                logging.error("Could not get SL contents")

            buildscriptbox = buildWindow.FindElement('buildscriptbox')
            entertext = buildWindow.FindElement('enterText')
            colortype = buildWindow.FindElement('colortype')
            enterelement = buildWindow.FindElement('enterElement')
            testname = buildWindow.FindElement('testName')
            try:
                sideloadbox_sl.Update(sideloadbox_contents)
            except:
                logging.info("Could not load SL as it hasn't been opened yet")

            buildWindow.Close()

            buildscriptbox_sl = buildWindow_sl.FindElement('buildscriptbox')
            sideloadbox_sl = buildWindow_sl.FindElement('sideloadbox')
            entertext_sl = buildWindow_sl.FindElement('enterText')
            colortype_sl = buildWindow_sl.FindElement('colortype')
            enterelement_sl = buildWindow_sl.FindElement('enterElement')
            testname_sl = buildWindow_sl.FindElement('testName')

            if savebuildcontents:
                buildscriptbox_sl.Update(buildscriptbox_contents)
                entertext_sl.Update(entertext_contents)
                colortype_sl.Update(colortype_contents)
                enterelement_sl.Update(enterelement_contents)
                testname_sl.Update(testname_contents)
                try:
                    sideloadbox_sl.Update(sideloadbox_contents)
                except:
                    logging.info("Could not load SL as it hasn't been opened yet")

            buildWindow_sl_active = True

            b2, values2 = buildWindow_sl.Read(timeout=0)

            #PySimpleGUIdebugger.refresh(locals(),
            #                            globals())  # call the debugger to
            # refresh the items being shown


            if b2 != Sg.TIMEOUT_KEY:
                if data_man.databasecheck:
                    try:
                        driverDB.insert_gui("{}_{}".format(b, values),
                                            data_man.testername,
                                            data_man.appuri,
                                            data_man.appname)
                    except:
                        pass

        if b2 == "reload_mods":
            try:
                sys.path.append('../')
                sys.path.append(os.path.dirname(sys.executable))
                import TA_Class_Sideload as app
                importlib.reload(app)
                logging.info("Reloaded Mods")
                Sg.PopupOK("Mods Reloaded")
            except (ImportError, ImportWarning, IndentationError,
                    SyntaxError, NoSuchElementException, NameError,
                    NoSuchWindowException,
                    ModuleNotFoundError) as import_error:
                logging.error(import_error)
                Sg.PopupOK("Issue Reloading Mods\n{}".format(import_error))

        if b2 == 'Exit' or b2 is None:
            buildWindow_active = False
            logging.info("Window 3 Set Inactive")
            buildWindow.Close()

        if b2 == "Main Menu":
            savebuildcontents = True
            buildscriptbox_contents = values2['buildscriptbox']
            entertext_contents = values2['enterText']
            colortype_contents = values2['colortype']
            enterelement_contents = values2['enterElement']
            testname_contents = values2['testName']
            try:
                sideloadbox_contents = values2['sideloadbox']
            except:
                pass

            logging.info("Build Window: Set to Inactive")
            if buildWindow_active:
                buildWindow.Close()
                buildWindow_active = False
            else:
                buildWindow_sl.Close()
                buildWindow_sl_active = False

        if b2 == "loadsideload":
            try:
                sideloadbox = buildWindow.FindElement('sideloadbox')
                slfile = Sg.PopupGetFile("Select Sideload Module")
                if slfile is not None:
                    f = open(slfile, 'r')
                    sideloadbox.Update(f.read())
                else:
                    logging.warning("No SL module chosen to load")
            except:
                logging.warning("Issue opening SL module")
                Sg.PopupError("Issue opening SL module")

        if b2 == "imgload":
            try:
                imgfile_get = Sg.PopupGetFile("Select Image: ",
                                              default_path=driver.folder)
                imgfile_parsed = Path("{}".format(imgfile_get)).name
                entertext.Update(imgfile_get)
            except:
                logging.warning("Could not load image file")
                Sg.PopupError("You should start a session first")

        if b2 == "savesideload":
            try:
                f = open(slfile, 'w')
                f.write(values2['sideloadbox'])
                Sg.PopupOK("SL Saved")
            except:
                logging.warning("Cannot save SL Code")
                Sg.PopupError("Cannot save SL Code")

        if b2 == "grab_image":

            screenshot_layout = [[#Sg.ReadButton("",
                                  #       image_data=TestAnatomy_images.camera,
                                  #       key="grab_image_in")],
                                  Sg.Graph(canvas_size=(50, 50), key ="ss",
                                           drag_submits=True,
                                           # background_color="blue",
                                           graph_top_right=(ss_window_x,
                                                            ss_window_y),
                                           graph_bottom_left=(0, 0))
                                    ]]

            screenshotWindow = Sg.Window('Test Anatomy - Build',
                                         # background_color="blue",
                                no_titlebar=False, grab_anywhere=True,
                                         resizable=True,
                                         right_click_menu=['&Right',
                                                         ['Take Screenshot',
                                                          'E&xit']],
                                auto_size_text=True, alpha_channel=0.1,
                                         return_keyboard_events=True,
                                         size=(ss_window_x, ss_window_y),
                                         keep_on_top=True).Layout(
                                            screenshot_layout).Finalize()

            grapho = screenshotWindow.FindElement("ss")

            screenshotWindow_active = True

        if screenshotWindow_active:
            b_screenshot_window, values_screenshot_window = \
                screenshotWindow.Read(timeout=0)

            if b_screenshot_window == 'Exit' or b_screenshot_window is None:
                screenshotWindow_active = False
                screenshotWindow.Close()

            if b_screenshot_window != Sg.TIMEOUT_KEY and \
                    screenshotWindow_active:
                saveXY = values_screenshot_window
                ss_win_loc = screenshotWindow.CurrentLocation()

            if b_screenshot_window == "Take Screenshot" or \
                    b_screenshot_window == 's':
                try:
                    ss_name = Sg.PopupGetText("Name your screenshot element: ")
                    screenshotWindow.Hide()
                    ss_take = pyautogui.screenshot("{}/{}.png".format(
                            driver.repositoryroot, ss_name),
                            region=(ss_win_loc[0], ss_win_loc[1],
                                    screenshotWindow.Size[0] + 5,
                                    screenshotWindow.Size[1] + 5))
                    screenshotWindow.Close()
                    screenshotWindow_active = False

                except:
                    logging.warning("Issue taking Screenshot")
                    Sg.PopupError("Issue taking screenshot\nCheck Special Characters")



        if b2 == "log":
            try:
                system('start etc/cmtrace.exe TestAnatomy.log')

            except:
                logging.warning("Issue opening cmtrace")
                Sg.PopupOK("Issue opening log in cmtrace")

        if b2 == "api":
            try:
                api_file = os.path.relpath("documents/API.txt")
                system('start notepad.exe {}'.format(api_file))
                logging.info("Opened API file")
            except:
                logging.error("Couldn't open API file")

        if b2 == "highlight":
            try:
                if values2['elementtype'] == "CSS Selector":
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver.engine."
                         "find_element_by_css_selector(\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    sound.play_sound('highlight', platform)
                    logging.info("Scratchbox: Executed Command Successfully")
            except (AttributeError, WebDriverException,
                    NoSuchElementException, NoSuchWindowException,
                    StaleElementReferenceException) as highlighterror:
                logging.info("Scratchbox: Failed Executing Command")
                Sg.PopupError("There was an issue Highlighting:, {}"
                              .format(highlighterror))

            if values2['elementtype'] == "XPATH":
                try:
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver."
                         "engine.find_element_by_xpath(\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    logging.info("Scratchbox: Executed Command Successfully")
                except:
                    logging.info("Scratchbox: Failed Executing Command")
                    Sg.PopupError("There was an issue Highlighting, "
                                  "Check Element")

            if values2['elementtype'] == "ID":
                try:
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver."
                         "engine.find_element_by_id(\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    logging.info("Scratchbox: Executed Command Successfully")
                except:
                    logging.info("Scratchbox: Failed Executing Command")
                    Sg.PopupError("There was an issue Highlighting, "
                                  "Check Element")

            if values2['elementtype'] == "Link Text":
                try:
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver."
                         "engine.find_element_by_link_text(\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    logging.info("Scratchbox: Executed Command Successfully: "
                                 "Link Text")
                except:
                    logging.info("Scratchbox: Failed Executing Command")
                    Sg.PopupError("There was an issue Highlighting, "
                                  "Check Element")

            if values2['elementtype'] == "Partial Link Text":
                try:
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver."
                         "engine.find_element_by_partial_link_text("
                         "\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    logging.info("Scratchbox: Executed Command Successfully: "
                                 "Partial Link Text")
                except:
                    logging.info("Scratchbox: Failed Executing Command")
                    Sg.PopupError("There was an issue Highlighting, "
                                  "Check Element")

            if values2['elementtype'] == "Tag Name":
                try:
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver."
                         "engine.find_element_by_tag_name(\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    logging.info("Scratchbox: Executed Command Successfully:"
                                 "Tag Name")
                except:
                    logging.info("Scratchbox: Failed Executing Command")
                    Sg.PopupError("There was an issue Highlighting, "
                                  "Check Element")

            if values2['elementtype'] == "Class":
                try:
                    scriptvar = str.strip(values2['enterElement'])
                    exec("lite = driver."
                         "engine.find_element_by_class_name(\"{}\")\ndriver."
                         "ehx_highlight(lite, False)".format(scriptvar))
                    logging.info("Scratchbox: Executed Command Successfully:"
                                 "Class Name")
                except:
                    logging.info("Scratchbox: Failed Executing Command")
                    Sg.PopupError("There was an issue Highlighting, "
                                  "Check Element")

        if b2 == "addButt":
            try:
                if values2['buildactions'] == " - Click Element" or values2[
                                            'buildactions'] == "Click Input":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver."
                                          "clickwebelement(""{}"",""{}"")\n".
                        format(repr(str.strip(
                            values2['elementtype'])),
                            repr(str.strip(
                                    values2['enterElement']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Click Button")

                if values2['buildactions'] == " - Verify Element":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver."
                                          "getwebelement(""{}"",""{}"",""{}"")"
                                          "\n".
                        format(repr(str.strip(
                            values2['elementtype'])),
                            repr(str.strip(
                                    values2['enterElement'])),
                            repr(str.strip(values2['enterText']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Verify Button")

                if values2['buildactions'] == " - Hold Element":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver."
                                          "hold_element(""{}"",""{}"")"
                                          "\n".
                        format(repr(str.strip(
                            values2['elementtype'])),
                            repr(str.strip(
                                    values2['enterElement']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Hold Element")

                if values2['buildactions'] == " - Release Element":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver."
                                          "release_element(""{}"",""{}"")"
                                          "\n".
                        format(repr(str.strip(
                            values2['elementtype'])),
                            repr(str.strip(
                                    values2['enterElement']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Hold Element")

                if values2['buildactions'] == " - Highlight Element(s)":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver."
                                          "highlighter(""{}"", ""{}"", {})"
                                          "\n".
                                format(repr(str.strip(values2['elementtype'])),
                                       repr(str.strip(
                                               values2['enterElement'])),
                                       str.strip(values2['enterText'])),
                            append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: "
                            "Highlight Element")

                if values2['buildactions'] == " - Open Site":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver.open_site()\n", append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Open Site")

                if values2['buildactions'] == " - Type Text":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.typewords(""{}"", ""{}"", ""{}"")\n".
                                format(repr(str.strip(values2['elementtype'])),
                                       repr(str.strip(
                                               values2['enterElement'])),
                                       repr(str.strip(values2['enterText']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Type Words")

                if values2['buildactions'] == " - Wait":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver.waiter({})\n".format(
                            (values2['enterText'])),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Wait")

                if values2['buildactions'] == " - Wait for Element":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.waitforelement(""{}"", ""{}"", ""{}"")\n".
                                format(repr(str.strip(values2['elementtype'])),
                                       repr(str.strip(
                                               values2['enterElement'])),
                                       repr(str.strip(values2['enterText']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Wait for Element")

                if values2['buildactions'] == " - Verify Element Text":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.getwebelement(""{}"", ""{}"", ""{}"")\n".
                                format(repr(str.strip(values2['elementtype'])),
                                       repr(str.strip(
                                               values2['enterElement'])),
                                       repr(str.strip(values2['enterText']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Wait for Element")

                if values2['buildactions'] == " - Hover Over Element":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.hoverelement(""{}"", ""{}"")\n".
                                format(repr(str.strip(values2['elementtype'])),
                                       repr(str.strip(
                                               values2['enterElement']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Hover Element")

                if values2['buildactions'] == " - Go Back":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver.back()\n", append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Back")

                if values2['buildactions'] == " - Go Forward":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver.forward()\n", append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Back")

                if values2['buildactions'] == " - Refresh Page":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("driver.refresh()\n", append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Back")

                if values2['buildactions'] == " - Take Screenshot":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.screenshot({})"
                                .format(repr(str.strip(values2['enterText']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Screenshot")

                if values2['buildactions'] == " - Clear Text Input":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.clearinput(""{}"", ""{}"")\n".
                                format(repr(str.strip(values2['elementtype'])),
                                       repr(str.strip(
                                               values2['enterElement']))),
                            append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: "
                            "Clear Text Input")

                if values2['buildactions'] == " - Reporting: Send Email":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.email()\n", append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: Email")

                if values2['buildactions'] == " - Reporting: Generate PDF":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.pdfgen()\n", append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: PDF Generation")

                if values2['buildactions'] == \
                        " - Kiosk: Fill Patient Admission Page (Req. SL)":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            """app.admission_page(driver, "Scheduled")\n""",
                            append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: Kiosk Admission")

                if values2['buildactions'] == " - Kiosk: Login (Req. SL)":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "app.login(driver)\n",
                            append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: Kiosk Login")

                if values2['buildactions'] == " - Reporting: Generate HTML":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "driver.htmlgen()\n", append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: HTML Generation")

                if values2['buildactions'] == " - Load Sideload (SL) Module":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "app.localdb(driver)\n", append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: Local DB")

                if values2['buildactions'] == " - Kiosk: Add Script Header":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    backup_script = values2['buildscriptbox']
                    appended_header = """# ###################################
# ####  Test-Anatomy (TA) Test Case  ####
# ###################################
# #####  TA Copyright: Eric     #####
# ###################################
# Test Case Author: 
# Creation Date: DAY/MONTH/YEAR
# Target Application: APP NAME
# Test Rail ID: 
# Jira ID: 
# Test Description: 
# Notes: 
# Modification Date: 
# Modification Notes: 
# #################################\n\n"""
                    new_script = appended_header + backup_script
                    buildscriptbox.Update(new_script)

                if values2['buildactions'] == " - Kiosk: Enter SSN (Req. SL)":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("""app.enter_ssn(driver, "auto", 
                    "SSN")\n""", append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Kiosk: Enter_SSN")

                if values2[
                    'buildactions'] == " - Kiosk: Click Pain Level (Req. SL)":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update("app.click_pain_level(driver)\n",
                                          append=True)
                    logging.info(
                            "BUILDMODE: Using Object: Updated Script with: "
                            "Kiosk: Click Pain Level")

                if values2[
                    'buildactions'] == " - Insert Random Encoding String " \
                                       "(Req. SL)":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            "app.BadStrings().get_bad_string()\n",
                            append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: "
                            "Insert Malicious Stringy")

                if values2["buildactions"] == " - Click Image":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(

                            """img = driver.wait_for_element({}, 0)
driver.click_element({}, img, "left", 0, offset=5)\n""".format(
                                    repr(str.strip(values2['enterText'])),
                                    repr(str.strip(values2['enterText']))),
                                    append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: "
                            "(GUI) Click Image {}".format(
                                    repr(str.strip(values2['enterText']))))

                    """
                    "GUI Automation:",
                  " - Click Image",
                  " - Type With Keyboard",
                  " - Click Cancel",
                  " - Click OK",
                  " - Click Red X",
                  " - Press Escape",
                  " - Press Enter",
                  " - Press Tab",
                  " - Screenshot Window Handle",
                  " - Screenshot Fullscreen",
                  " - Screenshot Window and Highlight Image(s)",
                  " - Screenshot Fullscreen and Highlight Image(s)",
                    """

                if values2["buildactions"] == " - Type With Keyboard":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            """keyboard.write({})\n""".format(
                                    repr(str.strip(values2['enterText']))),
                                    append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: "
                            "(GUI) Input Text")

                    if values2["buildactions"] == " - Press Tab":
                        buildscriptbox = buildWindow.FindElement(
                            'buildscriptbox')
                        buildscriptbox.Update(
                                """keyboard.write({})\n""".format(
                                        repr(str.strip(values2['enterText']))),
                                append=True)
                        logging.info(
                                "BUILDMODE: Updated Script with: "
                                "(GUI) Input Text")

                if values2["buildactions"] == " - Type Hotkey With Keyboard":
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    buildscriptbox.Update(
                            """keyboard.send({})\n""".format(
                                    repr(str.strip(values2['enterText']))),
                                    append=True)
                    logging.info(
                            "BUILDMODE: Updated Script with: "
                            "(GUI) Input Text")

            except NameError:
                Sg.PopupOK("Requires an open session launched from Config "
                           "Window")


        if b2 == "testbuildcase":
            try:
                cmd = exec(values2['buildscriptbox'])
                logging.info("Build Mode - Testing Case: Executed Command "
                             "Successfully: {}".format(
                        values2['buildscriptbox']))
                Sg.PopupOK("Case Ran Successfully")
            except (NameError, SyntaxError, NoSuchWindowException,
                    AttributeError, TypeError, InvalidSelectorException,
                    NoSuchElementException, WebDriverException, IOError,
                    StaleElementReferenceException, FileNotFoundError,
                    AssertionError, OSError) as testbuilderrordebug:
                logging.error("Error Importing Test Case Module: {}"
                              .format(testbuilderrordebug))
                testbuilderror = Sg.PopupOK("There is an error within "
                                            "your script:\n\n{}"
                                            .format(testbuilderrordebug))
        if b2 == "savecase":
            try:
                f = open('{}\{}.py'.format(driver.repositoryroot,
                                           values2['testName']),
                         'w')
                f.write(values2['buildscriptbox'])
                Sg.PopupOK("Case Saved")
            except:
                logging.warning("Cannot save Build Code")
                Sg.PopupError("Launch a session from config prior to using "
                              "Build Mode")

        if b2 == "loadcase":

            try:
                loadfile = Sg.PopupGetFile(message="Select a Test Case to "
                                                   "Import",
                                           default_path=driver.repositoryroot)
                if loadfile is not None:
                    buildscriptbox = buildWindow.FindElement('buildscriptbox')
                    f = open(loadfile, 'r')
                    buildscriptbox.Update(f.read())
            except:
                logging.warning("Cannot load Test Script")
                Sg.PopupOK("Launch a session from config first")

        if b2 == "notes":
            try:
                system('start notepad.exe')
            except:
                logging.warning("Cannot write to notes file. Must launch from "
                                "config first")

        if b2 == "folder":

            try:
                system('start {}'.format(driver.folder))
            except:
                logging.warning("Launch a session from config prior to using "
                                "Build Mode")
                Sg.PopupOK("Launch a session from config prior to using "
                           "Build Mode")

    # #################################
    # ## Config Window, Cont. (GUI)  ##
    # #################################

    if configWindow_active:
        b3, values3 = configWindow.Read(timeout=0)

        #PySimpleGUIdebugger.refresh(locals(),
        #                            globals())  # call the debugger to
        # refresh the items being shown

        if b3 != Sg.TIMEOUT_KEY:
            pass
        if b3 == 'Exit' or b3 is None:
            configWindow_active = False
            logging.info("Window 2 Set Inactive: Pressed Exit")
            configWindow.Close()

        if b3 == "home":
            configWindow_active = False
            logging.info("Window 2 Set Inactive: Pressed Main Menu")
            b3 = "config_save" # jump to save data before closing
            configWindow.Close()

        if b3 == "Launch2":

            if data_man.sideload:
                try:
                    sys.path.append(os.path.dirname(sys.executable))
                    import TA_Class_Sideload
                    logging.info("Loaded SL Module")
                except:
                    logging.warning("Issue Loading SL Module")

            try:  # auto save incase new values haven't been saved yet
                logging.info("Config Window: Launch - Autosaving")
                #config_manage("save", configs)
                data_man.save_configs()
            except:
                logging.error("Couldn't Autosave...")
                pass

            try:
                driver = Instance(str(data_man.browsertype),
                                  str(data_man.appuri),
                                  str(data_man.appname))
                logging.info("Instantiating Application")

                if data_man.databasecheck:
                    try: # username, dbhost, database, password, databaseport
                        driverDB = Database(str(data_man.dbun),
                                            str(data_man.dbip),
                                            str(data_man.dbhost),
                                            str(values3['dbpw']),
                                            str(data_man.dbport))

                        logging.info("Connected Database")
                        toasty.show_toast("Database",
                                           "Database Connected",
                                           icon_path=None,
                                           duration=5,
                                           threaded=True)
                        while toasty.notification_active():
                            time.sleep(0.1)
                        # driverDB.insert_gui("Launched Session, {}, {}, "
                        #                     "{}".format(
                        #             data_man.testername,
                        #             data_man.appuri,
                        #             data_man.appname))

                    except:
                        logging.error("Could not connect Database")
                        Sg.PopupError("Could not Connect Database")
                else:
                    logging.info("Not using Database")
                sound.play_sound('launch', platform)
            except:
                logging.warning("Issue Instantiating Application")
                Sg.PopupError("Make sure all values are completed")

        if b3 == "config_save":
            # config_manage("save", configs) # Moved to DM
            data_man.save_configs()

        if b3 == "config_load": # JSON LOAD COMPLETE
            data_man.load_configs()
            # config_manage("load", configs)

        if b3 == "reload_mods":
            try:
                sys.path.append('../')
                sys.path.append(os.path.dirname(sys.executable))
                import TA_Class_Sideload as app
                importlib.reload(app)
                logging.info("Reloaded Mods")
                Sg.PopupOK("Mods Reloaded")
            except (ImportError, ImportWarning, IndentationError,
                    SyntaxError, NoSuchElementException,
                    NoSuchWindowException,
                    ModuleNotFoundError) as import_error:
                logging.error(import_error)
                Sg.PopupOK("Issue Reloading Mods")

        if b3 == "root_search":
            try:
                root_folder = Sg.PopupGetFolder("")
                repositorypath = configWindow.FindElement('repositorypath')
                repositorypath.Update(root_folder)
            except:
                logging.error("Could Not Search for Root Folder")

    if b is None: # TODO quitting while in GUI MODE throws driver error
        logging.info("Used X to Exit Application")
        break

    else:
        pass
