from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'
    RED = '\033[31m'

def loginSeedr(driver, SeedrUsername, SeedrPassword):
    driver.get("https://seedr.cc")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, 'Login'))) #on attend que la page soit chargée

    login=driver.find_element_by_partial_link_text("Login")  #on ouvre la fenetre de login
    login.click()

    mail=driver.find_element_by_name("username")
    mail.send_keys(SeedrUsername)                               #on rempli le champ mail

    password=driver.find_elements_by_name("password")[2]        #on rempli le champ mdp
    password.send_keys(SeedrPassword)

    trucChiant = driver.find_element_by_class_name("reveal-modal-bg")   #on enleve un element qui bloque
    driver.execute_script("arguments[0].style.visibility='hidden'", trucChiant)

    loginButton = driver.find_elements_by_name("sign-in-submit")[1]
    loginButton.click()         #finalement, click sur le bouton login

def addToSeedrDownload(driver, link):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'link'))) #on attend que la page soit chargée

    linkInput = driver.find_element_by_name("link")         #on rempli le champ lien
    linkInput.send_keys(link)

    sendButton = driver.find_element_by_id("upload-button") #on envoi le lien, le dl commence
    sendButton.click()

def downloadFromSeed(driver):
    #addToSeedrDownload(downloadLink)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'folder'))) #on attend que la page soit chargée
    folder = driver.find_elements_by_class_name("folder")[0]
    hover = ActionChains(driver).move_to_element(folder)
    hover.perform()
    downloadButton = folder.find_element_by_class_name("fa-download")
    downloadButton.click()

def getProgress(driver):
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'torrent'))) #on attend que la page soit chargée
        folder = driver.find_elements_by_class_name("torrent")[0]
        progress = folder.find_element_by_class_name("progress-label")
        return (bcolors.OKBLUE + progress.text + bcolors.ENDC)
    except (TimeoutException, StaleElementReferenceException):
        return (bcolors.OKGREEN + "Complete !" + bcolors.ENDC)

def waitToComplete(driver):
    p=""
    pp=""
    while p.find("Complete") == -1:
        pp=p
        p = getProgress(driver)
        if p!=pp:
            print(p)
        time.sleep(0.1)

def deleteLast(driver):
    #addToSeedrDownload(downloadLink)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'folder'))) #on attend que la page soit chargée
    folder = driver.find_elements_by_class_name("folder")[0]
    hover = ActionChains(driver).move_to_element(folder)
    hover.perform()
    downloadButton = folder.find_element_by_class_name("fa-times")
    downloadButton.click()
    alert = driver.switch_to_alert()
    alert.accept()
    print("Fichier supprimé sur seedr.cc")

def getNameOfLast(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'folder'))) #on attend que la page soit chargée
    folder = driver.find_elements_by_class_name("folder")[0]
    name = folder.find_element_by_class_name("file-link-container")
    return name.text

def getSizeOfLast(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'folder'))) #on attend que la page soit chargée
    folder = driver.find_elements_by_class_name("folder")[0]
    sizeLabel = folder.find_element_by_class_name("content-item-size")
    size = sizeLabel.text
    if size.find("MB") != -1:
        return float(size.replace("MB", ""))*1.024
    elif size.find("GB") != -1:
        return float(size.replace("GB", ""))*1024