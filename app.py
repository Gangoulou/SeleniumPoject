from flask import Flask, Response
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)


def parse_pages():
    chrome_options = Options()
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=chrome_options.to_capabilities())
    driver.get('http://www.google.com')
    app.logger.warning(driver.get('http://www.google.com'))
    search = driver.find_element_by_name('q')
    search.send_keys('LNU')
    search.send_keys(Keys.RETURN)
    for i in range(0, 10):
        titles = driver.find_elements_by_tag_name('h3')
        for title in titles:
            print(title.text, '\n')
        nextpage = driver.find_element_by_id("pnnext")
        nextpage.click()
    return driver.quit()


@app.route("/")
def hello():
    start_parser_service()
    return Response("Parser started")

def start_parser_service():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=parse_pages, trigger="interval", seconds=5)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
