import time
from selenium.webdriver import *
from selenium.webdriver.common.by import By
import pandas as pd



def scrape_olx_apartments():
    options = ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--no-first-run')
    driver = Chrome(options)
    start = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/kvartira/'
    driver.get(start)

    location = []
    square = []
    price = []
    stage = []
    num_of_stage = []

    #pagintation
    for j in range(1, 4):
        print(j)
        start = f'https://www.olx.ua/uk/nedvizhimost/kvartiry/prodazha-kvartir/?page={j}'
        elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="location-date"]')
        location += [element.text.split('-')[0] for element in elements]
        elements = driver.find_elements(By.CSS_SELECTOR, '[class="css-643j0o"]')
        square += [element.text for element in elements]
        elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="ad-price"]')
        price += [element.text for element in elements]
        elements = driver.find_elements(By.CSS_SELECTOR, '[class="css-rc5s2u"]')
        hrefs = [element.get_attribute('href') for element in elements]
        for i in range(len(hrefs)):
            driver.get(hrefs[i])
            time.sleep(5)
            elements_inside = driver.find_elements(By.CSS_SELECTOR, '[class="css-b5m1rv er34gjf0"]')
            print([element.text for element in elements_inside])
            stage += [element.text for element in elements_inside if 'Поверх:' in element.text]
            num_of_stage += [element.text for element in elements_inside if 'Поверховість:' in element.text]
            driver.get(start)
        driver.get(start)


    driver.close()
    df = pd.DataFrame({
    'location': location,
    'square': square,
    'price': price,
    'stage': stage,
    'num_of_stage': num_of_stage
})
    df.to_excel('olx_parse.xlsx')

if __name__ == '__main__':
    scrape_olx_apartments()
