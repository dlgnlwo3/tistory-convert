import time
import subprocess
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium import webdriver
import os


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", element)
    return shadow_root


def download_location(driver):
    driver.get("chrome://settings/downloads")
    time.sleep(1)
    root1 = driver.find_element_by_tag_name("settings-ui")
    shadow_root1 = expand_shadow_element(driver, root1)
    root2 = shadow_root1.find_element_by_css_selector("#main")
    shadow_root2 = expand_shadow_element(driver, root2)
    root3 = shadow_root2.find_element_by_css_selector("settings-basic-page")
    shadow_root3 = expand_shadow_element(driver, root3)
    root4 = shadow_root3.find_element_by_css_selector(
        "#advancedPage > settings-section:nth-child(3) > settings-downloads-page"
    )
    shadow_root4 = expand_shadow_element(driver, root4)
    download_path = shadow_root4.find_element_by_css_selector("#defaultDownloadPath").text
    return download_path.replace("\\", "/")


def open_browser():
    # self.process = subprocess.Popen(cmd, env=self.env, close_fds=platform.system() != 'Windows', stdout=self.log_file, stderr=self.log_file, stdin=PIPE, creationflags=0x08000000 )

    browser = None

    try:
        browser = subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
        )  # 디버거 크롬 구동
    except:
        browser = subprocess.Popen(
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"'
        )  # 디버거 크롬 구동

    return browser


def chromedriver_install(options):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]
    driver_folder = os.path.join(os.getcwd(), "chromedriver")
    driver_version_folder = os.path.join(os.getcwd(), "chromedriver", chrome_ver)
    driver_path = os.path.join(driver_version_folder, "chromedriver.exe")

    if not os.path.isdir(driver_version_folder):
        os.makedirs(driver_version_folder)

    if not os.path.isdir(driver_folder):
        os.makedirs(driver_folder)

    try:
        driver = webdriver.Chrome(driver_path, options=options)
    except:
        chromedriver_autoinstaller.install(path=driver_folder)
        driver = webdriver.Chrome(driver_path, options=options)

    return driver


def get_chrome_driver(is_headless=False, is_secret=False):
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    if is_headless:
        options.add_argument("--headless")
    if is_secret:
        options.add_argument("incognito")  # 시크릿 모드

    # options.add_argument("start-maximized")

    driver = chromedriver_install(options)

    driver.implicitly_wait(10)  # 페이지가 로딩될 때 까지 10초동안 대기
    driver.set_page_load_timeout(10)
    return driver


def get_chrome_driver_new(is_headless=False, is_secret=False, tor=False, move_to_corner=False):
    options = Options()

    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if is_headless:
        options.add_argument("--headless")
    if is_secret:
        options.add_argument("-incognito")  # 시크릿 모드
    if tor:
        options.add_argument("--proxy-server=socks5://127.0.0.1:9150")  # 토르 적용

    options.add_argument("--disable-gpu")
    options.add_argument("lang=ko_KR")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    # )

    # 아이폰 환경
    # options.add_argument(
    #     "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    # )

    # 안드로이드 환경
    # options.add_argument(
    #     "--user-agent=Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
    # )

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split(".")[0]
    try:
        driver = webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=options)
    except:
        chromedriver_autoinstaller.install("./")
        driver = webdriver.Chrome(f"./{chrome_ver}/chromedriver.exe", options=options)
    driver.implicitly_wait(5)  # 페이지가 로딩될 때 까지 10초동안 대기
    driver.set_page_load_timeout(60)  # 브라우저의 로딩시간 대기

    driver.maximize_window()
    # driver.minimize_window()

    if move_to_corner:
        driver.set_window_position(3000, 3000)

    return driver


def close_browser(browser):
    try:
        # driver.quit()
        browser.kill()
    except:
        pass


def quit_driver(driver):
    try:
        driver.quit()
    except:
        pass


def accept_alert(browser):
    text = ""
    try:
        result = browser.switch_to.alert
        print(result.text)
        # # alert 창 확인
        text = result.text
        result.accept()
    except:
        pass

    return text


def remove_alert(browser):
    try:
        result = browser.switch_to.alert
        print(result.text)

        # # alert 창 확인
        # result.accept()

        # alert 창 끄기
        result.dismiss()
    except:
        "There is no alert"


if __name__ == "__main__":
    browser = open_browser()
    driver = get_chrome_driver()
    driver.get("www.naver.com")
    time.sleep(3000)
    browser.kill()
