import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

email = input("Email : ")
password = input("Password : ")

if __name__ == '__main__':

    #parametres
    p = {"download.default_directory": "download_csv"}

    option = webdriver.ChromeOptions() 
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1920,1000")
    option.add_argument("--start-maximized")
    
    driver = uc.Chrome(options=option,headless=False,debug=False,keep_alive=True)
    #user_data_dir='/home/yassin/.config/BraveSoftware/Brave-Browser/Default'

    def set_url(url):
        try:
            driver.get(url)
        except:
            print("Couldn't load the URL.")

    #login_avec_compte
    def login(email,password):
        try :
            l = driver.find_element(By.ID,"loginform-email")
            psd = driver.find_element(By.ID,"loginform-password")
            l.send_keys(email)
            psd.send_keys(password)
            
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
        if driver.current_url == "https://members.helium10.com/black-box/phrases?accountId=1544313151":
            try:

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
        
    
    set_url('https://members.helium10.com/user/signin')
    login(email, password)
    time.sleep(5)
    set_url('https://members.helium10.com/black-box/phrases?accountId=1544313151')

    getparameters()
    setparameters()
    time.sleep(15)