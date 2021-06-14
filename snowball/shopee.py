from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from time import sleep
import re
import pandas as pd
# create object for chrome options
chrome_options = Options()

# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('user-data-dir=C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

header = {
    'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
}

def get_url(search_term):
    """Generate an url from the search term"""
    template = "https://www.shopee.tw/search?keyword={}&order=asc&page=0&sortBy=price"
    # https://shopee.tw/search?keyword=%E5%8F%A3%E7%BD%A9&order=asc&page=0&sortBy=price
    search_term = search_term.replace(' ', '+')

    # add term query to url
    url = template.format(search_term)

    # add page query placeholder
    url += '&page={}'

    return url
    

def main(search_term):
    # invoke the webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    rows = []
    url = get_url(search_term)
    driver.get(url)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    for i, item in enumerate (soup.find_all('div', {'class': 'col-xs-2-4 shopee-search-item-result__item'}), start=5):
        if i == 10:
            break

        name = item.find('div', {'class': 'yQmmFK _1POlWt _36CEnF'})
        if name is not None:
            name = name.text.strip()
        else:
            name = ''

        item_price = []
        for item_p in item.find_all('span', {'class':'_29R_un'}):
            print(item_p.get_text())
            item_price.append(item_p.text)

      

        location = item.find('div', {'class': '_2CWevj'})
        if location is not None:
            location = location.text.strip() 
        else:
            location = ''

        

        freeShip = item.find('div', {'class': '_1HW7eF'})
        if freeShip is not None:
            freeShip = 'yes'
        else:
            freeShip = 'no'
        

        print([name, item_price[0], item_price[-1], location, freeShip])
        # temp_product = product(name, item_price[0], item_price[-1], location, freeShip)
        # product_list.append(temp_product)
        rows.append([name, item_price[0], item_price[-1], location, freeShip])

    # temp = []
    # product_list.sort(key=lambda x: x.min_price)

    # for ppp in product_list:
    #     print(ppp.min_price)

    # with open('shopee_item_list.csv', 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([search_term,'Name', 'Minimum Price', 'Maximum Price', 'Location', 'Free Shipping'])
    #     writer.writerows(rows)
    w_path = '{}_shopee_item_list.csv'.format(search_term)
    col_name = ['Name', 'Minimum Price','Maximum Price','Location','Free Shipping']
    result = pd.DataFrame(rows, columns=col_name)
    print(result)
    result.to_csv(w_path, index=False)

input_list = ['口罩','coffee']

for i in range(len(input_list)):
    main(input_list[i])

#할거 output 파일만 두개로 figure out 하기