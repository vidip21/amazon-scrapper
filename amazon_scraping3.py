#importing libraries
from selenium import webdriver 
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import bs4 as bs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tabulate import tabulate
from PIL import Image 
import PIL 
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--headless") #running in headless mode
options.add_argument('--log-level=1')
# options.add_experimental_option("detach", True)

cur_dir= "C:\\Users\\Vidip\\OneDrive\\Documents\\DhiOmic analytics internship"
i_name= "t shirt" #item you want to search

#the XPATH will need to be altered accordingly 
col0= "image"
col1= "name"
col2= "stars"
col3= "price"
col4= "about_item"
fields = [col0,col1, col2, col3,col4] #fields you want to scrape

data_to_write=[]

def amazon_scrapper(current_dir, item_name, field_names=["image","name","stars","price","about_item"]):
    data=[]
    f_names=field_names
    driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.maximize_window()
    driver.get("https://www.amazon.in/")
    parent_window= driver.current_window_handle
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,"//input[contains(@id,'search')]").send_keys(item_name)
    driver.find_element(By.XPATH,"//input[contains(@id,'nav-search-submit-button')]").click() #seaching item name

    pages= driver.find_element(By.XPATH,"//span[contains(@class,'s-pagination-item s-pagination-disabled')]").text.strip()
    pages=int(pages) #number of pages
    count=0
    page=1

    while count<4 and page<pages:
        driver.implicitly_wait(5)
        try:
            element_present = EC.presence_of_element_located((By.ID, 'element_id')) #waiting to load all items in page
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")        
        items_in_page= driver.find_elements(By.XPATH,"//span[contains(@class,'a-size-medium a-color-base a-text-normal')]") #list of all items in page
        if len(items_in_page)==0:
            items_in_page= driver.find_elements(By.XPATH,"//span[contains(@class,'a-size-base-plus a-color-base a-text-normal')]") #list of all items in page
        print(item_name," in page: ",len(items_in_page))
        items_in_page[0].click()
        driver.implicitly_wait(5)
        windows=driver.window_handles
        for child in windows:
            if child!= parent_window:
                driver.switch_to.window(child)
                driver.implicitly_wait(5)
                try:
                    type_of_item=driver.find_element(By.XPATH,"//img[contains(@class,'nav-categ-image')]").get_attribute('alt')
                    print(type_of_item)
                except:
                    pass
                driver.close() #closing product view
            driver.switch_to.window(parent_window) #returning to parent window 
            driver.implicitly_wait(5)

        for item in items_in_page[:2]:
            count+=1
            driver.implicitly_wait(10)
            item.click() #opening product view 
            driver.implicitly_wait(5)
            windows=driver.window_handles
            for child in windows:
                if child!= parent_window:
                    driver.switch_to.window(child)
                    driver.implicitly_wait(5)
                    try:
                        driver.find_element(By.XPATH,"//div[contains(@id,'poToggleButton')]").click()
                    except:
                        pass
                    d=dict() # column name:value for each item
                    image=driver.find_element(By.XPATH,"//img[contains(@id,'landingImage')]").get_attribute('src')
                    image_name=f"{item_name}_{count}"
                    image_name=f"{current_dir}\\{item_name} images\\{image_name}.png"
                    d[col0]=image_name
                    with open(image_name, 'wb') as f:
                        im = requests.get(image)
                        f.write(im.content)
                    try:
                        name= driver.find_element(By.XPATH,"//span[contains(@id,'productTitle')]").text.strip().encode('utf8')
                        d[col1]=name.decode()
                        print(d[col1])
                    except NoSuchElementException:
                        pass
                    try:
                        stars= driver.find_element(By.XPATH,"//span[contains(@class,'a-icon-alt')]").get_attribute('innerHTML')
                    except NoSuchElementException:
                        pass
                    stars=stars.split()
                    stars=stars[0].encode('utf8')
                    d[col2]=stars.decode()
                    try:
                        price= driver.find_element(By.XPATH,"//span[contains(@class,'a-price-whole')]").get_attribute('innerHTML')
                    except NoSuchElementException:
                        pass
                    price=price.split("<")
                    price=price[0].encode('utf8')
                    d[col3]=price.decode()
                    try:
                        details=driver.find_element(By.XPATH,"//table[contains(@class,'a-normal a-spacing-micro')]").get_attribute('innerHTML')
                        file1 = bs.BeautifulSoup(details, "lxml")
                        li=file1.findAll('tr')
                        for i in li: #itterating through list of details
                            d_name= i.find('td',{'class':'a-span3'}).text.strip()
                            d_name=d_name.encode('utf8')
                            d_name=d_name.decode()
                            d_val= i.find('td',{'class':'a-span9'}).text.strip()
                            d_val=d_val.encode('utf8')
                            d_val=d_val.decode()
                            if d_name not in f_names:
                                f_names.append(d_name)
                            d[d_name]=d_val
                    except NoSuchElementException:
                        pass
                    try:
                        about_item= driver.find_element(By.XPATH,"//ul[contains(@class,'a-unordered-list a-vertical a-spacing-mini')]").text.strip().encode('utf8')
                        d[col4]=about_item.decode()
                    except NoSuchElementException:
                        pass
                    if type_of_item=="Amazon Fashion":
                        driver.implicitly_wait(10)
                        if "available sizes" not in f_names:
                            f_names.append("available sizes")
                        if "size chart" not in f_names:
                            f_names.append("size chart")
                        try:
                            size_select= driver.find_element(By.XPATH,"//select[contains(@class,'a-native-dropdown a-declarative')]").get_attribute('innerHTML')
                            file3= bs.BeautifulSoup(size_select, "lxml")
                            o=file3.findAll('option', {'class': ['dropdownAvailable','dropdownSelect']})
                            available_sizes=[]
                            for i in o:
                                available_sizes.append(i.text.strip())
                            d["available sizes"]= available_sizes
                        except:
                            pass
                        try:
                            button1=driver.find_element(By.XPATH,"//span[contains(@class,'a-size-small')]")
                            ActionChains(driver).move_to_element(button1).click(button1).perform()
                            # driver.find_element(By.XPATH,"//span[contains(@class,'a-size-small')]").click()
                            size_chart= driver.find_element(By.XPATH,"//table[contains(@id,'fit-sizechartv2-0-table-0')]").get_attribute('innerHTML')
                            file2 = bs.BeautifulSoup(size_chart, "lxml")
                            size_table=''
                            tab_space=[]
                            t_r0=file2.find('tr')
                            t_h=t_r0.findAll('th')
                            size_header=[]
                            for k in t_h:
                                size_table+=k.text.strip()
                                size_header.append(k.text.strip())
                                size_table+="\t"
                                tab_space.append(len(k.text.strip()))
                            rows=file2.findAll('tr')
                            size_rows=[]
                            for row in rows:
                                t_d=row.findAll('td')
                                size_table+="\n"
                                t=0
                                size_row=[]
                                for k in t_d:
                                    size_table+=k.text.strip()
                                    size_row.append(k.text.strip())
                                    size_table+=" "*(tab_space[t]+6-len(k.text.strip()))
                                    t=t+1
                                size_rows.append(size_row)
                            
                            # d["size chart"]= size_table
                            d["size chart"]= tabulate(size_rows, headers=size_header)   
                            print(tabulate(size_rows, headers=size_header) )
                            driver.find_element(By.XPATH,"//button[contains(@class,' a-button-close a-declarative')]").click()
                        except:
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
    print(count)
    print(f_names)
    return data, f_names

def data_writer(current_dir, item_name, field_names, data):
    file01 = open(f"{current_dir}\\{item_name}_try.csv" , "w" )
    writer = csv.DictWriter(file01, lineterminator='\n', fieldnames = field_names)
    writer.writeheader()
    writer.writerows(data)
    file01.close()
    print("data succesfully written")

data_to_write,final_fields=amazon_scrapper(cur_dir, i_name, fields)
print(final_fields)
data_writer(cur_dir, i_name, final_fields, data_to_write)