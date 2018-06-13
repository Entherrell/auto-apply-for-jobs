## auto-apply-for-jobs-Indeed.py automates applying for 'Easy Apply' jobs on Indeed.com 
## except for Google's reCaptcha image puzzle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from time import sleep
from random import randrange

print('REMINDER: MAKE SURE YOUR LOGIN IS NOT PUBLIC ON GITHUB')

qqaa_txt_input = {"How many years of SQL experience do you have?": "1",
                  "Address": "314159 Fake St.",
                  "City": "Los Angeles",
                  "State": "CA",
                  "ZIP": "90012",
                  "Postal Code": "90012",
                  "LinkedIn": "https://www.linkedin.com/in/vivian-duong-314159/",
                  "Portfolio": "https://github.com/vduong314159",
                  "How many years of SQL database experience do you have?": "0",
                  "How many years of Insurance experience do you have? *": "0",
                  "How many years of SAS experience do you have?": "0",
                  "What are your salary expectations?": "a bagillion dollars per second"
                 }

qqaa_txt_area = {"Desired Pay": "$65-80,000 per year depending on other factors",
                 "What are your salary expectations?": "a bagillion dollars per second"}

qqaa_fieldset = {"Have you completed the following level of education: Bachelor's?": "Yes",
                 "Have you completed the following level of education: High school or equivalent?": "Yes",
                 "Are you willing to undergo a background check, in accordance with local law/regulations?": "Yes",
                 "Are you authorized to work in the following country: United States?": "Yes",
                 "Work Authorization": "United States Citizen or Permanent Resident",
                 "Are you legally authorized to work": "Yes",
                 "Will you now or in the future require sponsorship for employment visa status": "No",
                 "Primary Contact Method": "Primary Phone",
                 "gender": "Female",
                 "Do you speak English fluently?": "Yes"
                 }

qqaa_file = {"Resume": "absolute\\path\\to\\your\\resume"}

qqaa_dropdown = {"Country": "United States"}  

def sleep_(n_seconds):
    print('will execute in...')
    for i in range(n_seconds):
        print(n_seconds - i)
        sleep(1)

# <a> stands for anchor tag. The tag defines a hyperlink, which is used to link from one page to another.
def open_in_new_tab(elem_anchor):
    elem_anchor.send_keys(Keys.CONTROL + Keys.RETURN)   

## TODO: lookup abstract classes in Python, should Job be an abstract class?    
class Job(object):
    # not really necessary at the moment b/c it only has one child class, 
    # but if I want to go on other job boards, it will have more child classes 
    def __init__(self, title = '', employer = ''):
        self.title = title
        self.employer = employer
        

class IndeedJob(Job):
    def __init__(self, listing, employer = ''):
        title = listing.find_element_by_xpath(".//a[@data-tn-element='jobTitle']").text
        Job.__init__(self, title, employer)
        self.listing = listing
        
    def is_entry_level(self):
        jt_lowercase = self.title.lower()
        if ('principal' in jt_lowercase or
            'director' in jt_lowercase or
            'senior' in jt_lowercase or
            'sr' in jt_lowercase or
            'ii' in jt_lowercase or
            'lead' in jt_lowercase):
            is_entry_level = False
        else:
            is_entry_level = True
        return is_entry_level
    
    def is_ez_apply(self):
        if 'Apply with your Indeed Resume' in self.listing.text:
            is_eza = True
        else:
            is_eza = False
        return is_eza
    
    def is_sponsored_by_indeed_prime(self):
        if 'Indeed Prime' in self.listing.text:
            is_sponsored = True
        else:
            is_sponsored = False
        return is_sponsored
           
        

class IndeedApplier(webdriver.Chrome):

    def __init__(self, cover_letter = '', 
                 qqaa_txt_input = qqaa_txt_input,
                 qqaa_txt_area = qqaa_txt_area,
                 qqaa_fieldset = qqaa_fieldset,
                 qqaa_file = qqaa_file,
                 qqaa_dropdown = qqaa_dropdown,
                 chrome_driver = '../src/chromedriver.exe'):
        self.cover_letter = cover_letter
        self.qqaa_txt_input = qqaa_txt_input
        self.qqaa_txt_area = qqaa_txt_area
        self.qqaa_fieldset = qqaa_fieldset
        self.qqaa_file = qqaa_file
        self.qqaa_dropdown = qqaa_dropdown
        
        print('launching browser...', '\n')
        webdriver.Chrome.__init__(self, chrome_driver)
        
        print('going to Indeed login page...', '\n')
        signin_url = 'https://secure.indeed.com/account/login?service=my&hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F'
        webdriver.Chrome.get(self, signin_url)
        
    
    def login(self, username = 'throwAway6021023@gmail.com', pw = 'my-password'):
        # TODO: ask why wait isn't working..
        print('logging in...', '\n')
        wait = WebDriverWait(self, 15)
        login_eml = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#signin_email')))
        login_eml.send_keys(username)
        login_pw = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#signin_password')))
        login_pw.send_keys(pw)
        login_pw.submit()        
               
    def close_popover(self):
        # if there is a popover, close popover
        print('Checking for popover for Indeed Prime...')
        if len(self.find_elements_by_xpath(".//button[@id='prime-popover-close-button']")) > 0:
            print('Closing popover... \n')
            popover_x_button = self.find_elements_by_xpath(".//button[@id='prime-popover-close-button']")[0]
            popover_x_button.click()
        else:
            print('There is no popover. \n')
        print()
        
    ## TODO add params to search so you can specify search terms or w/e        
    def search(self):
        print('searching for jobs...', '\n')
        base_search_DA = 'https://www.indeed.com/jobs?q=data+analyst'
        near_me = '&l=90035&radius=25'
        most_recent = '&sort=date'
        my_DA_search = base_search_DA + near_me + most_recent
        self.get(my_DA_search)
    
    def get_listings(self):
        listings_column = browser.find_element_by_xpath(".//td[@id='resultsCol']")
        listings_elements = listings_column.find_elements_by_xpath(".//div[@data-jk]")
        return listings_elements
    
    ## TODO: lookup private methods in Py, it appears this should be a private method
    def switch_to_application_form(self):
        wait = WebDriverWait(self, timeout=10)
        print('switching driver to apply form...')
        outer_frame = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
        browser.switch_to.frame(outer_frame)
        inner_frame = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
        browser.switch_to.frame(inner_frame)
  

    def typing_cover_letter(self):
        if len(self.cover_letter) > 0:
            print('check if we need to click "Add cover letter"')
        
            if len(browser.find_elements_by_css_selector('button.icl-Button--transparent.icl-Button--sm.ia-AddCoverLetter-button')) > 0:
                add_cover_letter_btn = browser.find_elements_by_css_selector('button.ia-AddCoverLetter-button')
                add_cover_letter_btn.click()
                print("clicking 'Add cover letter' button...")
            else:
                print('No need to click "Add cover letter"')
            print()
            print("typing in cover letter...")
            cover_letter_box = wait.until(EC.presence_of_element_located((By.NAME, 'applicant.applicationMessage')))
            cover_letter_box.send_keys(self.cover_letter)
        else:
            print('Not typing in cover letter b/c there is no cover letter...')
    
    def check_not_robot(self):
        print('checking reCaptcha checkbox... \n')
        wait = WebDriverWait(self, 15)
        captcha_frame = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'iframe')))
        self.switch_to.frame(captcha_frame)
        captcha_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, ".//span[@role='checkbox']")))
        sleep_(randrange(5))
        captcha_checkbox.click
        print("Sadly, I cannot solve the image puzzle so you need to do it...")
    
    def go_to_next_page(self):
        wait = WebDriverWait(self, 1)
        
        cont_btn = self.find_elements_by_id('form-action-continue')
        if cont_btn:
            cont_btn[0].click()
        else:
            print("there is no 'Continue' button... \n")
    
    def clear_text(self, input_box):
        input_box.send_keys(Keys.CONTROL + 'a')
        input_box.send_keys(Keys.BACKSPACE)
    
    def answer_qs(self):
        print('answering questions...', '\n')
        txt_inputs = self.find_elements_by_xpath(".//div[@class='icl-TextInput']")
        txt_inputs_vis = [t for t in txt_inputs if t.size["width"] > 1]
        
        txt_areas = self.find_elements_by_xpath(".//div[@class='icl-Textarea']")
        txt_areas_vis = [t for t in txt_areas if t.size["width"] > 1]
        
        fields = self.find_elements_by_css_selector('fieldset')
        fields_vis = [f for f in fields if f.size["width"] > 1]
        
        file_inputs = self.find_elements_by_xpath(".//div[@class='ia-MultipleFileInput']")
        file_inputs_vis = [f for f in file_inputs if f.size["width"] > 1]
        
        dropdowns = self.find_elements_by_xpath(".//div[@class='icl-Select']")
        dropdowns_vis = [dd for dd in dropdowns if dd.size["width"] > 1]
        
        ## TODO: define function so you don't have to copy and paste these loops
        for ti in txt_inputs_vis:
            for q, a in qqaa_txt_input.items():
                if q in ti.text:
                    input_box = ti.find_element_by_xpath(".//input[@type='text']")
                    self.clear_text(input_box)
                    input_box.send_keys(a)
                    
        for ta in txt_areas_vis:
            for q, a in qqaa_txt_area.items():
                if q in ta.text:
                    input_box = ta.find_element_by_xpath(".//textarea")
                    clear_text(input_box)
                    input_box.send_keys(a)
                    
        for fi in file_inputs_vis:
            for q, a in qqaa_file.items():
                if q in fi.text:
                    upload_btn = fi.find_element_by_xpath(".//input[@type='file']")
                    upload_btn.send_keys(a)
        
        for dd in dropdowns_vis:
            for q, a in qqaa_dropdown.items():
                if q in dd.text:
                    dd_list = Select(dd.find_element_by_xpath(".//select"))
                    dd_list.select_by_visible_text(a)

        for f in fields_vis:
            for q, a in qqaa_fieldset.items():
                if q.lower() in f.text.lower():
                    radios = f.find_elements_by_xpath(".//div[@class='icl-Radio-item']")
                    for r in radios:
                        if a in r.text:
                            r.click()
    

    def apply(self, indeed_job):
        print("starting application for", indeed_job.title, "/n")
        anchor = indeed_job.listing.find_element_by_xpath(".//a[@data-tn-element='jobTitle']")
        open_in_new_tab(anchor)
        posting_tab = self.window_handles[-1]
        self.switch_to_window(posting_tab)
        
        wait = WebDriverWait(self, 10)
        
        # apply button is not in <button> tags for some reason so clicking doesn't always work,
        # better to press enter
        apply_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Apply Now")))
        apply_btn.send_keys(Keys.ENTER)
        
        self.switch_to_application_form()
        
        self.typing_cover_letter()
        self.go_to_next_page()
        
        is_unanswerable_q = False
        is_on_apply_page = False
        you_already_applied = False
        
        while not(is_unanswerable_q or is_on_apply_page or you_already_applied):
            self.answer_qs()
            self.go_to_next_page()
            if "This question is required." in self.find_element_by_xpath(".//html").text:
                is_unanswerable_q = True
                print("I can't answer this question. Check it out.", "\n")
            if not self.find_elements_by_id('form-action-continue') and self.find_elements_by_css_selector('button#form-action-submit'):
                print('on apply page...', '\n')
                is_on_apply_page = True
                self.check_not_robot()
            if "You have applied to this job" in self.find_element_by_xpath(".//html").text:
                you_already_applied = True
            
            
        search_results_tab = self.window_handles[0]
        self.switch_to_window(search_results_tab)
                

browser = IndeedApplier()
browser.login()
browser.search()
browser.close_popover()
listings = browser.get_listings()
jobs = [IndeedJob(listg) for listg in listings]


## set because we want to use set operator & =intersection
jobs_entry_level = {j for j in jobs if j.is_entry_level()}
jobs_eza = {j for j in jobs if j.is_ez_apply()}
jobs_not_prime = {j for j in jobs if not j.is_sponsored_by_indeed_prime()}

# set operator '&' = intersection 
jobs_to_auto = jobs_entry_level & jobs_eza & jobs_not_prime


jobs_to_auto = list(jobs_to_auto)
for j in jobs_to_auto:
    browser.apply(j)
print("My work is done. Your turn to do the rest.")
