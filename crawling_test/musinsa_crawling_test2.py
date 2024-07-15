from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys

def get_href_links(driver, wait, actions, num_items_to_fetch=100):
    href_links = set()
    while len(href_links) < num_items_to_fetch:
        actions.send_keys(Keys.END)
        time.sleep(2)
        
        for x in range(1, 46):
            try:
                xpath = f'//*[@id="root"]/main/div/section[3]/div[1]/div/div[{x}]/div/div[2]/a[2]'
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                href = element.get_attribute('href')
                href_links.add(href)
            except (NoSuchElementException, TimeoutException):
                continue

        print(f"Current number of unique href links: {len(href_links)}")
        if len(href_links) >= num_items_to_fetch:
            break

    return list(href_links)

def get_titles_from_links(driver, wait, href_links):
    '''
    가져와야할 것
    
    '''
    titles = []
    for link in href_links:
        driver.get(link)
        try:
            title_xpath = '//*[@id="root"]/div[3]/h2'
            title_element = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
            title = title_element.text
            titles.append(title)
        except (NoSuchElementException, TimeoutException):
            print(f"Title not found for link: {link}")
            continue
        time.sleep(1)
    
    return titles

def main():
    URL = "https://www.musinsa.com/categories/item/001?device=mw&sortCode=emt_high"
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.get(URL)
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[3]/div/button').click()
    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    actions = driver.find_element(By.CSS_SELECTOR, 'body')

    href_links = get_href_links(driver, wait, actions, num_items_to_fetch=100)
    print("Href links extracted:")
    for href in href_links:
        print(href)

    titles = get_titles_from_links(driver, wait, href_links)
    print("Titles extracted:")
    for title in titles:
        print(title)

    # driver.quit()

if __name__ == '__main__':
    main()
