from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import TimeoutException

PATH='C:/Users/Acer/Desktop/Python/crawler_pratice/webdriver/chromedriver.exe'

email='你的帳號'
email_password='你的密碼'

options = webdriver.ChromeOptions()
options.add_argument("--headless")                 #不開啟實體瀏覽器背景執行
#options.add_argument("--start-maximized")         #最大化視窗
driver=webdriver.Chrome(PATH,options = options)
driver.get('https://database.coffeeinstitute.org/login')

username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
login=driver.find_element_by_class_name('submit')
username.clear()
password.clear()

username.send_keys(email)
password.send_keys(email_password)
login.click()
time.sleep(2)

coffees_button=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'coffees')))
coffees_button.click()
time.sleep(8)

robusta_button=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'robusta')))
robusta_button.click()
time.sleep(5)

page=0
coffeenum=0

"""
robusta
"""

for i in range(1,232,8):
    print('page: {}, coffee number: {}'.format(page,coffeenum))
    #time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/content/div/div[4]/table/tbody/tr[20]/td[2]/a')))
    
    coffee_data_page=driver.find_elements(By.XPATH,'//td')[i].click()
    #time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/content/div/div[2]/div[2]/div/table[4]/tbody/tr[4]/td')))
    
    print('rows: \n',len(driver.find_elements(By.XPATH,"//tr")))
    tables = driver.find_elements(By.TAG_NAME,"table")
    print('tables: \n',len(tables))

    j=0
    
    for table in tables:
        t = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
        #print(t)
        #print(type(t))
        coffee_df=pd.read_html(str(t))[0]
        #print(coffee_df)
        name='C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/robusta/coffee_data_robusta_{}_table_{}.csv'.format(coffeenum,j)
        coffee_df.to_csv(name)
        j+=1
    driver.back()
    #driver.get('https://database.coffeeinstitute.org/coffees/robusta')
    #time.sleep(2)
    coffeenum+=1

driver.get('https://database.coffeeinstitute.org/coffees/arabica')

"""
arabica
"""
while page<4:
    
    for i in range(1,400,8):
        #time.sleep(5)
        for p_num in range(page):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/content/div/div[4]/table/tbody/tr[50]/td[2]/a')))

            page_buttons=driver.find_elements(By.CLASS_NAME,'paginate_button')
            page_buttons[-1].click()
            time.sleep(2) 

        try:
            print('page: {}, coffee number: {}'.format(page,coffeenum))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/content/div/div[4]/table/tbody/tr[1]/td[2]/a')))
            coffee_data_page=driver.find_elements(By.XPATH,'//td')[i]
            coffee_data_page.click()
            print(coffee_data_page.text)
            #time.sleep(5)
        except IndexError:
            print("Crawler Complete")
            break

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/content/div/div[2]/div[2]/div/table[4]/tbody/tr[4]/td')))
            print('rows: \n',len(driver.find_elements(By.XPATH,"//tr")))
            tables = driver.find_elements(By.TAG_NAME,"table")
            print('tables: \n',len(tables))
        except TimeoutException:
            web='https://database.coffeeinstitute.org/coffee/{}'.format(coffee_data_page.text[1:])
            driver.get(web)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/content/div/div[2]/div[2]/div/table[4]/tbody/tr[4]/td')))
            print('rows: \n',len(driver.find_elements(By.XPATH,"//tr")))
            tables = driver.find_elements(By.TAG_NAME,"table")
            print('tables: \n',len(tables))

        j=0
        
        for table in tables:
            t = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
            #print(t)
            #print(type(t))
            coffee_df=pd.read_html(str(t))[0]
            #print(coffee_df)
            name='C:/Users/Acer/Desktop/Python/crawler_pratice/cqi/coffeedata/arabica/coffee_data_arabica_{}_table_{}.csv'.format(coffeenum,j)
            coffee_df.to_csv(name)
            j+=1
        #driver.back()
        driver.get('https://database.coffeeinstitute.org/coffees/arabica')
        #time.sleep(2)
        coffeenum+=1
    page+=1

# arabica_button=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'arabica')))
# arabica_button.click()

time.sleep(3)
driver.quit()