import undetected_chromedriver as webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil
import json
import tempfile
import configparser
from functools import reduce

class ChromeWithPrefs(webdriver.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        # remove the user_data_dir when quitting
        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):
            # turn a (dotted key, value) into a proper nested dict
            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            # undot prefs dict keys
            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},  # merge dicts
                (undot_key(key, value) for key, value in prefs.items()),
            )

            # create an user_data_dir and add its path to the options
            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            # create the preferences json file in its default directory
            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            # pylint: disable=protected-access
            # remove the experimental_options to avoid an error
            del options._experimental_options["prefs"]
    
def set_url(url):
    try:
        driver.get(url)
    except:
        print("Couldn't load the URL.")

#login_avec_compte
def login(email_credential,password_credential):
    set_url('https://members.helium10.com/user/signin')

    try :
        l = driver.find_element(By.ID,"loginform-email")
        psd = driver.find_element(By.ID,"loginform-password")
        l.send_keys(email_credential)
        psd.send_keys(password_credential)
        
        button_input = "#login-form > button"
        input = driver.find_element(By.CSS_SELECTOR,button_input).click()

        #validity check
    except:
        print('Something went wrong. Did the site write ask for a CAPTCHA ?')

#mise_en_place_des_filtres
def getparameters():
    try:
        if driver.find_element(By.CSS_SELECTOR,"#marketplace-select > span.selected-domain") != "www.amazon.fr":
                flg = driver.find_element(By.CSS_SELECTOR,'#marketplace-select')
                flg.click()

                correct_flg = driver.find_element(By.CSS_SELECTOR,"#marketplace-A13V1IB3VIYZZH > span.select-domain")
                correct_flg.click()
        else:            
            print('Current url for degguging: '+ driver.current_url)
            print('GetParameters went wrong.')
            pass
    except:
        print('Something went wrong in GetParameters func.')

def setparameters():
    
    if driver.current_url == "https://members.helium10.com/black-box/phrases?accountId=1544313151" and driver.find_element(By.CSS_SELECTOR,"#marketplace-select > span.selected-domain") == "www.amazon.fr":
        pass
    else: 
        getparameters()

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID,"filter-bsr-min")))
        bsr_min = driver.find_element(By.ID,"filter-bsr-min")
        bsr_max = driver.find_element(By.ID,"filter-bsr-max")
        
        tpl = tuple((i for i in range(0,50400,400)))
        for j in tpl:
            
            print("preparing values for the bsr")
            value_min = str(j)
            value_max = str(j+200)
            bsr_min.send_keys(value_min)
            bsr_max.send_keys(value_max)
            
            try :
                search_button_slt = "#wrapper > div.content.pb-0 > div > div > div > div > div.card-body > div.action-buttons.mb-3 > div > div > button.btn.btn-info.action-search-phrase"
                search_button = driver.find_element(By.CSS_SELECTOR,search_button_slt)
                search_button.click()

            except:
                print("Couldn't find the search button, did you wait enough time ? " )

            try: 
                #click on button to search
                download_to_csv_button = "#wrapper > div.content.pt-2 > div > div > div > div > div > div.row.mb-3 > div.col-lg-8.col-xl-9.d-flex.flex-column.flex-lg-row.align-items-start.align-items-lg-center.justify-content-end > div.show-with-data.my-2 > div:nth-child(4)"
                
                #wait and click on download the csv
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,download_to_csv_button)))
                driver.find_element(By.CSS_SELECTOR,download_to_csv_button).click()

                
            except:
                print("SetParameters couldn't download the file. ")
            time.sleep(15)
            bsr_min.clear()
            bsr_max.clear()
    except:
        print('Current url for degguging: '+ driver.current_url)
        print('Set parameters went wrong.')

def config_set(download_folder='download_folder'):
        config = configparser.ConfigParser()
        
        if not config.has_section("INFO") or not config.has_section("PREFS"):
            config.add_section("INFO")
            config.set("INFO", "login", "")
            config.set("INFO", "password", "")
            config.set("INFO", "version", "0.1")
            config.add_section("PREFS")
            config.set("PREFS", "download.default_directory", download_folder)
            config.set("PREFS", "proxies", "")
            config.set("PREFS","plugins.always_open_pdf_externally","True")
            config.set("PREFS", "download.directory_upgrade", "True")
            config.set("PREFS", "download.prompt_for_download", "False")
            config.set("PREFS", "safebrowsing.enabled", "True")


        with open("config_a.ini", 'w') as configfile:
            config.write(configfile)

def config_read():

    config = configparser.ConfigParser()		
    config.read("config_a.ini")
    infos_section = config['INFO']
    prefs_section = config['PREFS']
    login = infos_section["login"]
    password = infos_section["password"]
    prefs = {"download.default_directory":prefs_section["download.default_directory"],
    "plugins.always_open_pdf_externally":prefs_section["download.default_directory"]}

    return login, password, prefs

def create_download_folder(dirc):
    if not os.path.isdir(dirc):
         os.makedirs(dirc)


if __name__ == '__main__':
    
    login_email, password_email, prefs = config_read()
    
    options = webdriver.ChromeOptions()
    create_download_folder("download_folder")
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--start-maximized')
    options.add_argument('--single-process')
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")

    # use the derived Chrome class that handles prefs
    driver = ChromeWithPrefs(options=options)
    
    login(login_email,password_email)
    set_url('https://members.helium10.com/black-box/phrases?accountId=1544313151')
    time.sleep(5)
    getparameters()
    time.sleep(5)
    setparameters()