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
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from time import sleep
cwd = os.getcwd()
opts = Options()

opts.add_argument('--headless=chrome')
#pts.headless = False
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument("--window-size=500,800")
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
mobile_emulation = {
    "deviceMetrics": { "width": 660, "height": 1080, "pixelRatio": 3.4 },
    }
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

def scrape_text(index):
    #element_text = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//div[@data-ad-comet-preview="message"])[{index}]')))
    element_text = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//*[@id="screen-root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div)[{index}]')))
    return element_text

def click_next(get_element):
    wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f"//*[@id='{get_element}']//div[text()='See more' or text()='Lihat selengkapnya' or text()='see more'] or text()='lihat selengkapnya']"))).click()

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
        opts.add_experimental_option("mobileEmulation", mobile_emulation)
        opts.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36")
    
        browser = webdriver.Chrome(ChromeDriverManager().install(),options=opts, desired_capabilities=dc)
        #message = '{"rp_creation_time:0":"{\\"name\\":\\"creation_time\\",\\"args\\":\\"{\\\\\\"start_year\\\\\\":\\\\\\"'+year+'\\\\\\",\\\\\\"start_month\\\\\\":\\\\\\"'+year+'-1\\\\\\",\\\\\\"end_year\\\\\\":\\\\\\"'+year+'\\\\\\",\\\\\\"end_month\\\\\\":\\\\\\"'+year+'-12\\\\\\",\\\\\\"start_day\\\\\\":\\\\\\"'+year+'-1-1\\\\\\",\\\\\\"end_day\\\\\\":\\\\\\"'+year+'-12-31\\\\\\"}\\"}"}'
        # encoded_message = base64.b64encode(message.encode('utf-8'))
        # year = encoded_message.decode('utf-8')
        browser.get("https://www.facebook.com/")
        with open(f"cookies.json", 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.get(f"https://web.facebook.com/search/posts?q={keyword}&filters={year}")  
        browser.get(f'https://m.facebook.com/search_results/?q={keyword}')
        xpath_long('//div[@aria-label="Posts"]')
        xpath_long('//div[@aria-label="Date posted"]')
        wait(browser,30).until(EC.presence_of_element_located((By.XPATH, f"//div[text()='{year}']/parent::div/parent::div"))).click()
        sleep(5)
        fail = 1
 
        for index in range (1,limit+1):
            try:   
                name_post = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//*[@id="screen-root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div)[{index}]/parent::div/parent::div/parent::div/div[1]//span[@class="rtl-ignore f2 a"]'))).text
                date_post = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//*[@id="screen-root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div)[{index}]/parent::div/parent::div/parent::div/div[1]//span[@class="f5"]'))).text
                try:
                    clear_date = date_post[:date_post.index("󰞋")]
                except:
                    clear_date = date_post
                try:
                    wait(browser,1).until(EC.presence_of_element_located((By.XPATH, f'(//span[@class="rtl-ignore f2 a"])[{index}]/following-sibling::span[2]')))
                    click_more = "true"
                except:
                    click_more = "false"
                try:
                    if click_more == "false":
                        
                        element_all = scrape_text(index)
                        ele = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//*[@id="screen-root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div)[{index}]')))
                        browser.execute_script("window.scrollBy(0, 500);")
                        if "See more" in scrape_text(index).text or "Lihat selengkapnya" in scrape_text(index).text or "lihat selengkapnya" in scrape_text(index).text or "see more" in scrape_text(index).text:
                            element_all.click()
                            sleep(1)
                    content = scrape_text(index).text.strip()
                 
                except:
                    if click_more == "false":
                        
                        element_all = scrape_text(index)
                        ele = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, f'(//*[@id="screen-root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div)[{index}]')))
                        browser.execute_script("window.scrollBy(0, 500);")
 
                        if "See more" in scrape_text(index).text or "Lihat selengkapnya" in scrape_text(index).text or "lihat selengkapnya" in scrape_text(index).text or "see more" in scrape_text(index).text:
                            xpath_fast(f'(//*[@id="screen-root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div)[{index}]//span')
                            sleep(1)
                    content = scrape_text(index).text.strip()
                browser.execute_script("window.scrollBy(0, 500);")
                content = re.sub(r"\n", " ", content)
                content = re.sub(r"\t", " ", content)
                content = re.sub(r"\s+", " ", content)
                # Join the sentences in the content into one string with a separator
                content = " ".join(re.split(r"[\.\?!]\s+", content))
                print(f"{date_show()} Success scrape")
                # Write the data to the CSV file
                writer.writerow({"name": name_post.strip(),"date":clear_date,"content": content})
                fail = 1
            except Exception as e:
                fail = fail + 1
                try:
                    get_title = wait(browser,2).until(EC.presence_of_element_located((By.XPATH, f'//h2[@class="native-text"]'))).text
                    print(get_title, keyword)
                    if keyword not in get_title:
                        xpath_long('//div[@data-action-id="99"]')
                except:
                    pass
                if fail == 10:
                    browser.quit()
                    break   
                else:
                    browser.execute_script("window.scrollBy(0, 850);")
                    sleep(5)
                    
    
if __name__ == '__main__':
    print(f'{date_show()} Scrape facebook post from search')
    year_input = int(input(f'{date_show()} Filter Year: '))
    keyword_input = input(f'{date_show()} Keyword: ')
    limit = int(input(f'{date_show()} Limit data: '))
    main(year_input,keyword_input,limit)
