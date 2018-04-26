import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

driver = webdriver.Chrome()
driver.get('http://www.cape.ucsd.edu/responses/Results.aspx')

select = driver.find_element_by_name('ctl00$ContentPlaceHolder1$ddlDepartments')
allOptions = select.find_elements_by_tag_name('option')

data = []
for option in allOptions:
    # search for each department
    option.click()
    if option.text != 'Select a Department':
        print('Now fetching ' + option.text + '...', end='')
        search = driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnSubmit')
        search.click()
        time.sleep(1) # wait for it to start loading
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_UpdateProgress1'))) # proceed only when finished loading

        # get the result here
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.select_one('table.styled')
        columns = []
        for th in table('th'):
            columns.append(th.text)

        for row in table('tr')[1:]:
            datum = {}
            for i, col in enumerate(columns):
                datum[col] = row.select('td')[i].text.strip()
            datum['Department'] = option.text
            data.append(datum)
        print('Done')


# save it to external file
pd.DataFrame(data).to_csv('cape.csv', index=False)


