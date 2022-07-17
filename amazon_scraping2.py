#importing libraries
from selenium import webdriver 
import requests
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import bs4 as bs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image 
import PIL 
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless") #running in headless mode
options.add_argument('--log-level=1')

# options.add_experimental_option("detach", True)

driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.maximize_window()
driver.get("https://www.amazon.in/")
parent_window= driver.current_window_handle
driver.implicitly_wait(5)

current_dir= "C:\\Users\\Vidip\\OneDrive\\Documents\\DhiOmic analytics internship"
item_name= "phone" #item you want to search
col0= "image"
col1= "name"
col2= "price"
col3= "stars"
col4= "about_item"
field_names = [col0,col1, col2, col3,col4] #fields you want to scrape
data= [] #storing list of dictionaries

driver.find_element(By.XPATH,"//input[contains(@id,'search')]").send_keys(item_name)
driver.find_element(By.XPATH,"//input[contains(@id,'nav-search-submit-button')]").click() #seaching item name

pages= driver.find_element(By.XPATH,"//span[contains(@class,'s-pagination-item s-pagination-disabled')]").text.strip()
pages=int(pages) #number of pages
count=0
page=1
# imgs=[]

while count<=30 and page<20:
    driver.implicitly_wait(5)
    try:
        element_present = EC.presence_of_element_located((By.ID, 'element_id')) #waiting to load all items in page
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    items_in_page= driver.find_elements(By.XPATH,"//span[contains(@class,'a-size-medium a-color-base a-text-normal')]") #list of all items in page
    print("phones in page: ",len(items_in_page))
    for item in items_in_page:
        count+=1
        driver.implicitly_wait(10)
        item.click() #opening product view 
        driver.implicitly_wait(5)
        windows=driver.window_handles
        for child in windows:
            if child!= parent_window:
                driver.switch_to.window(child)
                driver.implicitly_wait(5)
                # driver.find_element(By.XPATH,"//a[contains(@class,'a-declarative')]").click()
                try:
                    driver.find_element(By.XPATH,"//div[contains(@id,'poToggleButton')]").click()
                except:
                    pass
                d=dict() # column name:value for each item
                image=driver.find_element(By.XPATH,"//img[contains(@id,'landingImage')]").get_attribute('src')
                image_name=f"{item_name}_{count}"
                image_name=f"{current_dir}\\{item_name} images\\{image_name}.png"
                # image_name="C:\\Users\\Vidip\\OneDrive\\Documents\\DiAnomic analytics internship\\"+item_name+"images\\"+image_name+".png"
                d["image"]=image_name
                # im1.save(image_name)
                with open(image_name, 'wb') as f:
                    im = requests.get(image)
                    f.write(im.content)
                    # print('Writing: ', name)
                    # # imgs.append(image_name)
                try:
                    d["name"]= driver.find_element(By.XPATH,"//span[contains(@id,'productTitle')]").text.strip().encode('utf8')
                    print(d["name"])
                except NoSuchElementException:
                    pass
                try:
                    stars= driver.find_element(By.XPATH,"//span[contains(@class,'a-icon-alt')]").get_attribute('innerHTML')
                except NoSuchElementException:
                    pass
                stars=stars.split()
                d["stars"]=stars[0].encode('utf8')
                try:
                    price= driver.find_element(By.XPATH,"//span[contains(@class,'a-price-whole')]").get_attribute('innerHTML')
                except NoSuchElementException:
                    pass
                price=price.split("<")
                d["price"]=price[0].encode('utf8')
                # brand= driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-brand')]").text[6:]
                try:
                    details=driver.find_element(By.XPATH,"//table[contains(@class,'a-normal a-spacing-micro')]").get_attribute('innerHTML')
                except NoSuchElementException:
                    pass
                file = bs.BeautifulSoup(details, "lxml")
                li=file.findAll('tr')
                for i in li: #itterating through list of details
                    d_name= i.find('td',{'class':'a-span3'}).text.strip()
                    d_val= i.find('td',{'class':'a-span9'}).text.strip()
                    if d_name not in field_names:
                        field_names.append(d_name.encode('utf8'))
                    d[d_name.encode('utf8')]=d_val.encode('utf8')
                try:
                    d["about_item"]= driver.find_element(By.XPATH,"//ul[contains(@class,'a-unordered-list a-vertical a-spacing-mini')]").text.strip().encode('utf8')
                except NoSuchElementException:
                    pass
                data.append(d)
                driver.close() #closing product view
        driver.switch_to.window(parent_window) #returning to parent window 
        driver.implicitly_wait(5)
    page+=1
    print(page)
    driver.find_element(By.XPATH,"//a[contains(@class,'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')]").click() #going to next page
    driver.implicitly_wait(5) 

driver.close() #closing parent window
# d_items=d.items()
# for item in d_items:
#     print(item)
# print(field_names)

# import xlsxwriter
# workbook = xlsxwriter.Workbook('C:\\Users\\Vidip\\OneDrive\\Documents\\DiAnomic analytics internship\\excel_insert_images.csv')
# worksheet = workbook.add_worksheet()
# images = []
# image_row = 1
# image_col = 0
# for image in imgs:
#     worksheet.insert_image("A"+str(image_row), 
#                            image) 
    # positioning = 1 allows move and size with cells (may not always perform as expected)
#     image_row += 1
# workbook.close()

file01 = open(f"{current_dir}\\{item_name}.csv" , "w" )
writer = csv.DictWriter(file01, lineterminator='\n', fieldnames = field_names)
writer.writeheader()
writer.writerows(data)
print(count)
file01.close()