from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time,os,base64,json,csv,re
from selenium import webdriver
import warnings,io
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from time import sleep
cwd = os.getcwd()
opts = Options()

# opts.add_argument('--headless=chrome')
# #pts.headless = False
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
opts.add_argument('--ignore-certificate-errors')
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='vision_key.json'
from google.cloud import vision
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
 
def get_captcha_text(png):
 
    client = vision.ImageAnnotatorClient()

    with io.open(f"{cwd}\date.png", 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    text = response.text_annotations[0].description
     
    return text

def date_show():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def xpath_fast(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    #browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all) 

def xpath_long(el):
    element_all = wait(browser,30).until(EC.presence_of_element_located((By.XPATH, el)))
 
    return browser.execute_script("arguments[0].click();", element_all) 

def scrape_name(index):
    #element_text = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//div[@data-ad-comet-preview="message"])[{index}]')))
    element_text = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f"(//div[@data-ad-comet-preview='message']/parent::div/parent::div/parent::div//h3[contains(@id,'jsc_c')])[{index}]")))
    return element_text

def scrape_status(index):
    element_text = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f"(//div[@data-ad-comet-preview='message'])[{index}]")))
    return element_text
    
def scrape_date(index):
   
    element_text = wait(browser,25).until(EC.presence_of_element_located((By.XPATH, f'(//div[@data-ad-comet-preview="message"]/parent::div/parent::div/parent::div//span[contains(@aria-labelledby,"jsc_c")]/parent::span/parent::a/span/span)[{index}]')))
    return element_text
    
def click_next(get_element):
    wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f"//*[@id='{get_element}']//div[text()='See more' or text()='Lihat selengkapnya' or text()='see more' or text()='lihat selengkapnya']"))).click()

def main(year, keyword,limit):
    
    global browser
    date = time.strftime('%d-%m-%y %X')
    date = date.replace(":","-")
    with open(f"{year}-{keyword}-{date}.csv", "a", newline="",encoding="utf-8") as csvfile:
    # Define the field names
        fieldnames = ["name", "date","content"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=';')
        # Write the header row 
        writer.writeheader()
 
        opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    
        browser = webdriver.Chrome(ChromeDriverManager().install(),options=opts, desired_capabilities=dc)
        message = '{"rp_creation_time:0":"{\\"name\\":\\"creation_time\\",\\"args\\":\\"{\\\\\\"start_year\\\\\\":\\\\\\"'+year+'\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"'+year+'-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"'+year+'\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"'+year+'-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"'+year+'-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"'+year+'-12-31\\\\\\"}\\"}"}'
        encoded_message = base64.b64encode(message.encode('utf-8'))
        year = encoded_message.decode('utf-8')
        browser.get("https://www.facebook.com/")
        fail = 1
        with open(f"cookies.json", 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.get(f"https://web.facebook.com/search/posts?q={keyword}&filters={year}")  
        for index in range (1,limit+1):
            try:
                sleep(5)
                name_post = scrape_name(index).text
                name_post = name_post.strip().split('·')[0]
                name_post = re.sub(r"\n", " ", name_post)
                name_post = re.sub(r"\t", " ", name_post)
                name_post = re.sub(r"\s+", " ", name_post)
                print(name_post)
                sleep(10)
                date_img = scrape_date(index).screenshot("date.png")
                date_img_post = get_captcha_text(date_img)
                print(date_img_post)
                if "See more" in scrape_status(index).text or "Lihat selengkapnya" in scrape_status(index).text or "lihat selengkapnya" in scrape_status(index).text or "see more" in scrape_status(index).text:
                    get_id = scrape_status(index).get_attribute('id')
                    click_next(get_id)
                    sleep(1)
                content = scrape_status(index).text.strip()
                fail = 0
                content = re.sub(r"\n", " ", content)
                content = re.sub(r"\t", " ", content)
                content = re.sub(r"\s+", " ", content)
                # Join the sentences in the content into one string with a separator
                content = " ".join(re.split(r"[\.\?!]\s+", content))
                print(content)
                print(f"{date_show()} Success scrape")
                # Write the data to the CSV file
                writer.writerow({"name": name_post,"date":date_img_post,"content": content})
                fail = 1
                browser.execute_script("window.scrollBy(0, 500);")
            except Exception as e:
                print(e)
                fail = fail + 1
                if fail == 10:
                    browser.quit()
                    break   
                else:
                    browser.execute_script("window.scrollBy(0, 850);")
                    sleep(5)

        
if __name__ == '__main__':
    print(f'{date_show()} Scrape facebook post from search')
    year_input = input(f'{date_show()} Filter Year: ')
    keyword_input = input(f'{date_show()} Keyword: ')
    limit = int(input(f'{date_show()} Limit data: '))
    main(year_input,keyword_input,limit)
