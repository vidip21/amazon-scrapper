       #             d=dict() # column name:value for each item
        #             image=driver.find_element(By.XPATH,"//img[contains(@id,'landingImage')]").get_attribute('src')
        #             image_name=f"{item_name}_{count}"
        #             image_name=f"{current_dir}\\{item_name} images\\{image_name}.png"
        #             d[col0]=image_name
        #             # with open(image_name, 'wb') as f:
        #             #     im = requests.get(image)
        #             #     f.write(im.content)
        #             try:
        #                 name= driver.find_element(By.XPATH,"//span[contains(@id,'productTitle')]").text.strip().encode('utf8')
        #                 d[col1]=name.decode()
        #                 print(d[col1])
        #             except NoSuchElementException:
        #                 pass
        #             try:
        #                 stars= driver.find_element(By.XPATH,"//span[contains(@class,'a-icon-alt')]").get_attribute('innerHTML')
        #             except NoSuchElementException:
        #                 pass
        #             stars=stars.split()
        #             stars=stars[0].encode('utf8')
        #             d[col2]=stars.decode()
        #             try:
        #                 price= driver.find_element(By.XPATH,"//span[contains(@class,'a-price-whole')]").get_attribute('innerHTML')
        #             except NoSuchElementException:
        #                 pass
        #             price=price.split("<")
        #             price=price[0].encode('utf8')
        #             d[col3]=price.decode()
        #             try:
        #                 details=driver.find_element(By.XPATH,"//table[contains(@class,'a-normal a-spacing-micro')]").get_attribute('innerHTML')
        #             except NoSuchElementException:
        #                 pass
        #             file = bs.BeautifulSoup(details, "lxml")
        #             li=file.findAll('tr')
        #             for i in li: #itterating through list of details
        #                 d_name= i.find('td',{'class':'a-span3'}).text.strip()
        #                 d_name=d_name.encode('utf8')
        #                 d_name=d_name.decode()
        #                 d_val= i.find('td',{'class':'a-span9'}).text.strip()
        #                 d_val=d_val.encode('utf8')
        #                 d_val=d_val.decode()
        #                 if d_name not in f_names:
        #                     f_names.append(d_name)
        #                     print(f_names)
        #                 d[d_name]=d_val
        #             try:
        #                 about_item= driver.find_element(By.XPATH,"//ul[contains(@class,'a-unordered-list a-vertical a-spacing-mini')]").text.strip().encode('utf8')
        #                 d[col4]=about_item.decode()
        #             except NoSuchElementException:
        #                 pass
        #             data.append(d)
        #             driver.close() #closing product view
        #     driver.switch_to.window(parent_window) #returning to parent window 
        #     driver.implicitly_wait(5)
        # page+=1
        # print(page)
        # driver.find_element(By.XPATH,"//a[contains(@class,'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')]").click() #going to next page
        # driver.implicitly_wait(5) 