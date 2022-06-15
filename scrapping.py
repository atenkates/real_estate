## ENTER REDFIN LIST DETAILS HERE
ltp = ['https://www.redfin.com/OH/Cleveland/3266-W-125th-St-44111/home/70745671' ]


import requests
from bs4 import BeautifulSoup
import random
import time 
import undetected_chromedriver.v2 as uc

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_proxies():
    
    anonymity = { 'elite proxy' : {'ip' : True, 'proxy' : True},
                 'anonymous' : {'ip' : True, 'proxy' : False},
                 'transparent' : {'ip' : False, 'proxy' : False},
    }
    
    r = requests.get('https://www.us-proxy.org/')
    soup = BeautifulSoup(r.content, 'html.parser')

    tbl = soup.find('table')
    rows = tbl.find_all('tr')

    proxies = []

    for row in rows[1:201]:
        cells = row.find_all('td')
        ip = cells[0].text + ':' + cells[1].text
        https = cells[6].text
        is_ip_hidden = anonymity[cells[4].text]['ip']
        is_proxy_hidden = anonymity[cells[4].text]['proxy']
        last_checked = cells[7].text

        if https == 'yes':
            proxies.append({'ip_address' : ip,
                            'last_checked' : last_checked,
                            'is_proxy_hidden' : is_proxy_hidden,
                            'is_ip_hidden' : is_ip_hidden, 
                           })

    return proxies

def random_proxy():
    pick_one = random.randint(0, 0)
    proxy_server = proxies[pick_one]
    return proxy_server


def load_page(url, proxy='none'):
    waitTime = random.randint(3000,3100)
    driver = uc.Chrome()
    driver.get(url)
    driver.set_window_size(1920, 1080)
    #driver.FindElement(By.LinkText("See all property history")).Click()
    WebDriverWait(driver, waitTime)
    html = driver.page_source
    s_redfin = BeautifulSoup(html, 'html.parser')
    
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument('--proxy-server={}'.format(proxy['ip_address'])) 
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #chrome_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return s_redfin

def soupStart(soup, valv):
    scndClass = 'div' if valv!= 'abp-sqFt' else 'span'
    soupFind = soup.find('div', {'data-rf-test-id':valv}).find(scndClass, {'class':'statsValue'})
    if len(soupFind)==1:
        return soup.find('div', {'data-rf-test-id':valv}).find(scndClass, {'class':'statsValue'}).text
    else:
        return 'missing'


#TO -DO zipcode to area
comdic ={}
comdic['Lakewood'] = ['John F Ensighns','Lakewood Park','Genck',' Lakewood','Pleasant Hill Allotment']
comdic['Edgewater'] = ['Edgewater Land Co']
comdic['Rocky River'] = []
comdic['Detroit Shoreway'] = ['Brooklyn','Cleveland']
comdic['Kamms Corner'] = ['Cleveland']
comdic['Parma']  = []
comdic['Ohio City'] = ['Ohio City']

def comcodeMap(zipcode):
    return _
    
 # TO DO def extractPropertyDetails( listUrl) without breaking:
detailList = {}
for lp in ltp:
    redfin = load_page(lp)
    print('the page was downloaded')
    #Step 1: Main components of the listing
    listAdress = redfin.find('div', {'data-rf-test-id':'abp-streetLine'}).text.replace(',', '')
    detailList[listAdress] = {}  

    detailList[listAdress]['url'] = lp
    temp = 0
    detailList[listAdress]['listAdress'] = redfin.find('div', {'data-rf-test-id':'abp-streetLine'}).text.replace(',', '')
    detailList[listAdress]['listPrice'] = soupStart(redfin, 'abp-price')
    detailList[listAdress]['numBed'] = soupStart(redfin, 'abp-beds')
    detailList[listAdress]['numBath'] = soupStart(redfin, 'abp-baths')
    detailList[listAdress]['sqFt'] =  soupStart(redfin, 'abp-sqFt')
    detailList[listAdress]['zipCode'] = redfin.find('div', {'data-rf-test-id':'abp-cityStateZip'}).text[-5:]
    detailList[listAdress]['description'] = redfin.find('div', {'class':'remarks'}).text


    # Step 2 Details / Pricing history

    home_fact = redfin.find('div', {'class':'keyDetailsList'} ).text
    home_fact += 'endValue111'

    key_label = ['Year Built','Community','Lot Size','endValue111']
    prvWrd = 'Property Type'
    prvIdx = home_fact.find(prvWrd)+len(prvWrd)

    for wrd in  key_label:
        idx = home_fact.find(wrd)
        statVal = home_fact[prvIdx:idx]
        detailList[listAdress][prvWrd.replace(" ", "")] = statVal 
        prvIdx = idx + len(wrd)
        prvWrd = wrd


    relCharac = ['Date','Public Records','Price']
    detailList[listAdress]['SoldDate'] = '--'
    detailList[listAdress]['SoldPrice'] = '--'

    for stc in redfin.find_all('div', {'class':'property-history-content-container'} ):
        print(stc.text)
        soldIx= stc.text.find('Sold')
        if soldIx >0:
            for ix,strg in enumerate(relCharac):
                relIx = stc.text.find(strg)
                if strg=='Date':
                    detailList[listAdress]['SoldDate'] = stc.text[0:relIx][-12::]
                elif strg=='Price':
                    poundIx = stc.text[prevIx:relIx].find('$')
                    detailList[listAdress]['SoldPrice'] = stc.text[prevIx:relIx][poundIx::]
                prevIx = stc.text.find(strg)
            break
    del redfin
detailList  
