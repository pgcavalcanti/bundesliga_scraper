from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep


URL = "https://www.bundesliga.com/en/bundesliga/stats/players/distance"

#selenium configuration
chrome_options = Options()
driver = webdriver.Chrome(options = chrome_options)

#open the URL
driver.get(URL)
#waits few seconds so page is ready
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "stats-player-card"))) 

#create a pandas to Dataframe to be saved in a csv file later
df = pd.DataFrame([], columns=['First Name', 'Last Name', 'Club', 'Value'])

#the first 3 players (those with pictures) should be found first, with an specific logic
players = driver.find_elements_by_css_selector('stats-player-card')
for i, elem in enumerate(players):
    fname = elem.find_element_by_css_selector('span.first')
    lname = elem.find_element_by_css_selector('span.last.font-weight-bold')
    club_logo = elem.find_element_by_css_selector('img.logo.ng-star-inserted')
    club_logo = club_logo.get_attribute('src')
    club = club_logo.split('/')[-1].split('-')[0]
    value = elem.find_element_by_css_selector('span.value')
    df.loc[i,'First Name'] = fname.text
    df.loc[i,'Last Name'] = lname.text
    df.loc[i,'Club'] = club
    df.loc[i,'Value'] = float(value.text)

#click the "Load more" button 20 times
#TODO: improve this
for c in range(20):
    bt = driver.find_element_by_css_selector('button.playerRow.view-more.linkActive.ng-star-inserted')
    try:
#        bt.click() #doesnt work
        webdriver.ActionChains(driver).move_to_element(bt).click(bt).perform()
#        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.playerRow.view-more.linkActive.ng-star-inserted'))) 
        sleep(3) #needs this because implicit wait doesnt work (why?)
        print(c)
    except:
        print(c + ' error')
    
#from the 4th to the bottom, the same logic can be used
players = driver.find_elements_by_css_selector("a.playerRow.container-fluid.linkActive.ng-star-inserted")
i = 3
for elem in players:
    fname = elem.find_element_by_class_name('first')
    lname = elem.find_element_by_class_name('last.font-weight-bold')
    try:
        #the following line selects the club name
        #however, since the club name is not available for the first 3 players
        #I chose to use the logo names as well
        
        #club = elem.find_element_by_class_name('clubName.d-none.d-lg-inline-block').text
        
        club_logo = elem.find_element_by_css_selector('img.logo.ng-star-inserted')
        club_logo = club_logo.get_attribute('src')
        club = club_logo.split('/')[-1].split('-')[0]
        
        
        value = elem.find_element_by_class_name('value.fixed.fixed-large')
        df.loc[i,'First Name'] = fname.text
        df.loc[i,'Last Name'] = lname.text
        df.loc[i,'Club'] = club
        df.loc[i,'Value'] = float(value.text)
        print(fname.text + ' ' + lname.text + ' ok')
        i += 1
    except:
        print(fname.text + ' ' + lname.text + ' wrong stat')

df.to_csv('distances.csv')