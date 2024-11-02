from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import time

# Bilibili base URL
host = 'https:'
key = 'AMV'
opt = '%s.txt' % (key)


a1 = "2015-5-10 23:40:00"
a2 = "2020-5-10 23:40:00"
# 先转换为时间数组
timeArray1 = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
timeArray2 = time.strptime(a2, "%Y-%m-%d %H:%M:%S")

url = f'https://search.bilibili.com/all?keyword={key}&pubtime_begin_s={int(time.mktime(timeArray1))}&pubtime_end_s={int(time.mktime(timeArray2))}'

# url = 'https://space.bilibili.com/3493277087042285/video'

# Chrome driver configuration with headless mode disabled for debugging
chrome_options = Options()
# Uncomment below line to run in headless mode
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
# driver = webdriver.Chrome(service=ChromeService('/usr/bin/chromedriver'), options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

def scrape_page():
    """
    This function scrapes the current page and writes video information to a file.
    """
    with open(opt, 'a+') as f:
        try:
            # Parse the current page source with BeautifulSoup
            soup_mainpage = soup(driver.page_source, features='lxml')
            for i in soup_mainpage.find_all(class_='bili-video-card'):
                try:
                    title = i.find(class_='bili-video-card__info--tit').text.strip()
                    author = i.find(class_='bili-video-card__info--author').text.strip()
                    date = i.find(class_='bili-video-card__info--date').text.strip()
                    item_times, item_quotes = [stat.text for stat in i.find_all(class_='bili-video-card__stats--item')]
                    duration = i.find(class_='bili-video-card__stats__duration').text.strip()

                    # Extract view count and filter for videos with more than 5万 views
                    if '万' in item_times and float(item_times.replace('万', '')) > 5:
                        for t in i.find_all('a'):
                            video_link = host + t.get('href')
                            if 'www.bilibili.com/video' in video_link:
                                f.write("""JSON: {"text": "%s", "url": "%s"}\n""" % (title, video_link))
                                print(f"Saved: {title} - {video_link}")
                                break

                except Exception as inner_e:
                    print(f"Error extracting video details: {inner_e}")
        except Exception as outer_e:
            print(f"Error parsing page source: {outer_e}")

def navigate_and_scrape():
    """
    This function navigates through pages, scraping each one until no more pages are left.
    """
    while True:
        scrape_page()
        try:
            # Find the pagination button
            button = driver.find_element(By.CLASS_NAME, 'vui_pagenation--btns').find_elements(By.TAG_NAME, 'button')[-1]
            if button.is_enabled():
                # Scroll into view and click the button
                ActionChains(driver).move_to_element(button).perform()
                button.click()
                time.sleep(2)  # Wait for page to load
            else:
                break  # Exit loop if the button is disabled
        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

# Start scraping
navigate_and_scrape()

# Close the driver after scraping is complete 
driver.quit()
