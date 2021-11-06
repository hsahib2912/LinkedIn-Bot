import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


driver = webdriver.Chrome(executable_path='/Users/harkishansingh/Desktop/chromedriver')
ta = 0
td = 0
print('Applied','Discarded')
def login():
    driver.get('https://www.linkedin.com/')
    #Enter your linkedin email below
    email = 'abc@xyz.com'
    try:
        driver.find_element_by_id('session_key').send_keys(email)
    except:
        driver.find_element_by_id('email-or-phone').send_keys(email)
    #Enter your linkedin password below
    password = 'ac611sdaAD'
    try:
        driver.find_element_by_id('session_password').send_keys(password)
    except:
        driver.find_element_by_id('password').send_keys(password)    
    try:
        driver.find_element_by_class_name('join-form__form-body-submit-button').click()
    except:
        driver.find_element_by_class_name('sign-in-form__submit-button').click()

def click(r):
    for k in r:
        id = k.get('id')
        try:
            driver.find_element_by_id(id).click()
            break
        except:
            continue

def open_jobs_portal():
    driver.get('https://www.linkedin.com/jobs')
    bp = BeautifulSoup(driver.page_source,'lxml')
    job_id = bp.find('input',class_ = 'jobs-search-box__text-input jobs-search-box__keyboard-text-input').get('id')
    #Enter your job profile below
    driver.find_element_by_id(job_id).send_keys('Software Engineer')
    loc_id = bp.find_all('input',class_ = 'jobs-search-box__text-input')
    for l in loc_id:
        id = l.get('id')
        if(id == job_id):
            continue
        else:
            try:
                #Enter your job location below
                driver.find_element_by_id(id).send_keys('India')
                break
            except:
                continue

    driver.find_element_by_xpath('//button[text()="Search"]').click()
    time.sleep(5)

    driver.find_element_by_xpath('//button[text()="On-site/Remote"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//label[@for="workplaceType-2"]').click()
    time.sleep(1)
    bp = BeautifulSoup(driver.page_source,'lxml')
    r = bp.find_all('button',class_ = 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml2')
    click(r)
    time.sleep(3)
    driver.find_element_by_xpath('//button[text()="Easy Apply"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//button[text()="Experience Level"]').click()
    driver.find_element_by_xpath('//label[@for="experience-2"]').click()
    time.sleep(1)
    bp = BeautifulSoup(driver.page_source,'lxml')
    r = bp.find_all('button',class_ = 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml2')
    click(r)

def scroll_to_the_bottom():
    last_id = ''
    while(True):
        bp = BeautifulSoup(driver.page_source,'lxml')
        res = bp.find_all('li',class_ = 'jobs-search-results__list-item occludable-update p0 relative ember-view')
        last_ele = res[len(res)-1]

        k = last_ele.find('div',class_ = 'full-width artdeco-entity-lockup__title ember-view')
        new_id = k.get('id')
        if(new_id == last_id):
            break
        driver_ele = driver.find_element_by_id(new_id)
        driver.execute_script("arguments[0].scrollIntoView();",driver_ele)
        last_id = new_id
        time.sleep(1)

def discard():
    driver.find_element_by_class_name('artdeco-button__icon').click()
    try:
        bp = BeautifulSoup(driver.page_source,'lxml')
        time.sleep(1)
        r = bp.find_all('button',class_ = 'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--primary ember-view')
        time.sleep(1)
        click(r)
    except:
        print('Not required')
    bp = BeautifulSoup(driver.page_source,'lxml')
    r = bp.find('button',class_ = 'artdeco-modal__confirm-dialog-btn artdeco-button artdeco-button--2 artdeco-button--secondary ember-view')
    id = r.get('id')
    driver.find_element_by_id(id).click()

def apply_to_job():
    bp = BeautifulSoup(driver.page_source,'lxml')
    r = bp.find('button',class_ = 'jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view')
    id = r.get('id')
    driver.find_element_by_id(id).click()
    cnt = 0
    for i in range(10):
        try:
            bp = BeautifulSoup(driver.page_source,'lxml')
            try:
                driver.find_element_by_xpath('//label[@for="follow-company-checkbox"]').click()
            except:
                pass
            r = bp.find('button',class_ = 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view')
            id = r.get('id')
            driver.find_element_by_id(id).click()
            cnt+=1
        except:
            break
    time.sleep(2)
    if(cnt == 10):
        discard()
        td+=1
    else:
        ta+=1
        try:
            driver.find_element_by_class_name('artdeco-button__icon').click()
        except:
            print('No notif')
    

def go_inside_job():
    scroll_to_the_bottom()
    page_number = 1
    while(True):
        s = '//button[@aria-label="Page '+str(page_number)+'"]'
        driver.find_element_by_xpath(s).click()
        bp = BeautifulSoup(driver.page_source,'lxml')
        res = bp.find_all('div',class_ = 'full-width artdeco-entity-lockup__title ember-view')
        if(page_number!=1):
            scroll_to_the_bottom()
        for r in res:
            time.sleep(1)
            try:
                id = r.get('id')
                time.sleep(1)
                driver.find_element_by_id(id).click()
            except:
                continue
            time.sleep(1)
            try:
                apply_to_job()
            except:
                continue
            time.sleep(2)
        page_number+=1

login()
open_jobs_portal()
time.sleep(5)
go_inside_job()
