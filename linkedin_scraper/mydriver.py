import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import logging as log
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# This class opens the browser windows necessary to open the LinkedIn connection without CAPTCHA. 

class mydriver(): 
    # Start selenium webdriver
    def __init__(self): 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.cookies = self.driver.get_cookies()
        self.driver_wait = WebDriverWait(self.driver, 120)
        self.driver_wait_small = WebDriverWait(self.driver, 10)

    # main execution
    def login_and_verify_account(self, email, pwd_linkedin, pwd_email): 
        self.login_linkedin(email, pwd_linkedin)
        time.sleep(5) #wait for email?

        if self.driver.title == "Security Verification | LinkedIn":

            # 1. Email 
            # 2. Temp restricted -> not implemented yet
            # 3. Something isn't quite right
            try:
                checkbox = self.driver_wait_small.until(
                    EC.presence_of_element_located((By.ID, "tosAgreementAccepted"))
                )
                checkbox.click()
                submit_button = self.driver_wait.until(
                    EC.element_to_be_clickable((By.ID, 'content__button--primary--muted'))
                )
                submit_button.click()
                return True

            except: 

                self.login_email(email, pwd_email)
                code = self.get_code()

                self.insert_code(code)
                time.sleep(5)
                return False
            
            
        if self.driver.title == "Restriction | LinkedIn": 
            return True
        

    # auxiliary methods
    def login_linkedin(self, email, password):
        log.info("Attempting Linkedin Login.")
        url='https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
        self.driver.get(url)
        
        usr_input = self.driver_wait.until(
            EC.element_to_be_clickable((By.ID, 'username'))
        )
        pwd_input = self.driver_wait.until(
            EC.element_to_be_clickable((By.ID, 'password'))
        )

        usr_input.send_keys(email)
        pwd_input.send_keys(password)

        log.info("Logging in Linkedin.")

        submit_button = self.driver_wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))
        )
        submit_button.click()

    def login_email(self, email, password):

        log.info("Attempting email login.")
        url='https://mail.rediff.com/cgi-bin/login.cgi'

        self.driver.execute_script(f"window.open('{url}', 'new_window')")
        self.driver.switch_to.window(self.driver.window_handles[1]) 
        
        usr_input = self.driver_wait.until(
            EC.element_to_be_clickable((By.ID, 'login1'))
        )

        pwd_input = self.driver_wait.until(
            EC.element_to_be_clickable((By.ID, 'password'))
        )
        
        email_usr = email.split("@")[0]

        usr_input.send_keys(email_usr)
        pwd_input.send_keys(password)

        log.info("Logging in Email.")

        submit_button = self.driver_wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'signinbtn'))
        )
        submit_button.click()

    #open last email and get code
    def get_code(self):
        log.info("Getting the email.")
        emails = self.driver_wait.until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'li_mail_item'))
        )
        email = emails[0]
        email.click()

        log.info("Getting the paragraph.")
        parag = self.driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="mail_main_box_cont"]/div[2]/div[3]/div/div/div/div[3]/table/tbody/tr/td/center/table/tbody/tr[2]/td/table[1]/tbody/tr/td/table/tbody/tr[3]/td/p[2]'))
        )

        log.info("Getting the code.")
        text = parag.get_attribute("innerHTML")
        text_list = text.split("strong>")
        code = text_list[1][0:6]
        return code
   
    def insert_code(self, code): 
        # close tab, back to Linkedin.
        self.driver.close() # switch to the main windo
        self.driver.switch_to.window(self.driver.window_handles[0]) 
        
        code_box = self.driver_wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="input__email_verification_pin"]'))
        )
        code_box.send_keys(code)

        log.info("Inserting code.")

        button = self.driver_wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="email-pin-submit-button"]'))
        )
        button.click()
    
    # Get session cookies
    def get_cookies_dict(self):
        cookie_dict = {}
        for cookie in self.cookies:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict

    # When finished: Quit 
    def quit(self): 
        self.driver.quit()