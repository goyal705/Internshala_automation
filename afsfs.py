from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os

op=webdriver.ChromeOptions()
op.binary_location=os.environ.get('GOOGLE_CHROME_BIN')
op.add_argument('--headless')
op.add_argument('--no-sandbox')
op.add_argument('--disable-dev-shmcd -usage')
driver=webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),options=op)

telegram_auth_token='5485600475:AAGZZZee14pCFfiCDnTiGR0dce1txRN5E0Y'
telegram_grp_id='internship_intershala'

urls=['https://internshala.com/internships/accounts-internship/','https://internshala.com/internships/analytics-internship/','https://internshala.com/internships/android-app-development-internship/','https://internshala.com/internships/angular.js-development-internship/','https://internshala.com/internships/backend-development-internship/','https://internshala.com/jobs/accounts-jobs/','https://internshala.com/jobs/analytics-jobs/','https://internshala.com/jobs/android-app-development-jobs/','https://internshala.com/jobs/angular.js-development-jobs/','https://internshala.com/jobs/backend-development-jobs/']

while True:
    for url in urls:
        try:
            driver.get(url)
            soup=BeautifulSoup(driver.page_source,'html5lib')
            lists=soup.find('div',attrs={'id':'internship_list_container_1'})
            if lists!=None:
                i=1
                for content in lists.find_all('div',attrs={'class':'container-fluid individual_internship visibilityTrackerItem'}):
                    result={}
                    result['Link']='https://www.internshala.com'+ content.find('a',attrs={'class':'view_detail_button'})['href']
                    result['Title']=content.find('a',attrs={'class':'view_detail_button'}).text.strip()
                    result['Location']=content.find('a',attrs={'class':'location_link view_detail_button'}).text.strip()
                    result['Company']=content.find('a',attrs={'class':'link_display_like_text view_detail_button'}).text.strip()
                    result['Start Date']=content.find('div',attrs={'class':'item_body'}).text.strip().replace('\xa0immediately',' ')

                    message=''
                    if 'jobs' in url:
                        result['CTC']=content.find('div',attrs={'class':'other_detail_item'}).find_next_sibling().find('div',attrs={'class':'item_body'}).text.strip()
                        keys=list(result.values())
                        n=keys[3].replace('&','')
                        message=f'\nTitle: {keys[1]}'+'\n'+f'Location: {keys[2]}'+'\n'+f'Company: {n}'+'\n'+f'Start Date: {keys[4]}'+ '\n'+f'CTC: {keys[5]}'+'\n'+f'Link: {keys[0]}'
                    else:
                        result['Stipend']=content.find('span',attrs={'class':'stipend'}).text.strip()
                        result['Duration']=content.find('div',attrs={'class':'other_detail_item'}).find_next_sibling().find('div',attrs={'class':'item_body'}).text.strip()
                        keys=list(result.values())
                        n=keys[3].replace('&','')
                        message=f'\nTitle: {keys[1]}'+'\n'+f'Location: {keys[2]}'+'\n'+f'Company: {n}'+'\n'+f'Duration: {keys[4]}'+ '\n'+f'Stipend: {keys[5]}'+'\n'+f'Duration: {keys[6]}'+'\n'+f'Link: {keys[0]}'
                    
                    if i<=5:
                        telegram_api_url=f"https://api.telegram.org/bot{telegram_auth_token}/sendMessage?chat_id=@{telegram_grp_id}&text={message}"
                        tel_resp=requests.get(telegram_api_url)
                        time.sleep(60)
                    i+=1    
        except Exception as e:
            continue
