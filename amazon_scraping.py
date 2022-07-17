from selenium import webdriver 
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.amazon.in/")
parent_window= driver.current_window_handle
driver.implicitly_wait(3)

options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\WebDrivers\chromedriver.exe')

item="laptop"

driver.find_element(By.XPATH,"//input[contains(@id,'search')]").send_keys(item)
driver.find_element(By.XPATH,"//input[contains(@id,'nav-search-submit-button')]").click()
driver.find_element(By.XPATH,"//span[contains(@class,'a-size-medium a-color-base a-text-normal')]").click()
windows=driver.window_handles
for child in windows:
    if child!= parent_window:
        driver.switch_to.window(child)
        # driver.find_element(By.XPATH,"//a[contains(@class,'a-declarative')]").click()
        driver.find_element(By.XPATH,"//div[contains(@id,'poToggleButton')]").click()

        name= driver.find_element(By.XPATH,"//span[contains(@id,'productTitle')]").text
        print(name)
        stars= driver.find_element(By.XPATH,"//span[contains(@class,'a-icon-alt')]").get_attribute('innerHTML')
        stars=stars.split()
        stars=stars[0]
        price= driver.find_element(By.XPATH,"//span[contains(@class,'a-price-whole')]").get_attribute('innerHTML')
        price=price.split("<")
        price=price[0]
        brand= driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-brand')]").text[6:]
        # brand= driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-brand')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").text
        model_name= driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-model_name')]").text[11:]
        # model_name= driver.find_element(By.XPATH,"//tr[contains(@class,'po-model_name')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").find_element(By.XPATH,"//span").text
        screen_size= driver.find_element(By.XPATH,"//tr[contains(@class,'po-display.size')]").text[12:]
        colour= driver.find_element(By.XPATH,"//tr[contains(@class,'po-color')]").text[7:]
        hard_disk_size= driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-hard_disk.size')]").text[10:]
        cpu_model=driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-cpu_model.family')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").text[9:]
        ram_memory_installed_size=  driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-ram_memory.installed_size')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").text[10:]
        operating_system=driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-operating_system')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").text[3:]
        special_feature=  driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-special_feature')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").text[16:]
        graphics_card_description=  driver.find_element(By.XPATH,"//tr[contains(@class,'a-spacing-small po-graphics_description')]").find_element(By.XPATH,"//td[contains(@class,'a-span9')]").text[:21]
        driver.close()
driver.switch_to.window(parent_window)
driver.close()
print(name)
print(stars)
print(price)
print(brand)
print(model_name)
print(screen_size)
print(colour)
print(hard_disk_size)