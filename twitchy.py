from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import sys

# Put your own path of chromedriver
ChromeDriverPATH = "/Users/loayakram/Downloads/chromedriver"

# Put your own file path of your streamers names
InputPath = "/Users/loayakram/PycharmProjects/Twitchy/streamers.txt"


browser = webdriver.Chrome(ChromeDriverPATH)
url = 'https://www.twitch.tv/'


# Wait until class loads
def wait_class(class_name):
    try:
        element = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    except NoSuchElementException:
        return False


# Wait until XPATH loads
def wait_xpath(xpath_name):
    try:
        element = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_name)))
    except NoSuchElementException:
        return False


def live_card(element_name):
    try:
        online_card = browser.find_element_by_css_selector(element_name)
        return online_card
    except NoSuchElementException:
        return False


streamers = {}
system_stdout = sys.stdout
with open(InputPath) as f:
    streamers = f.read().splitlines()

for streamer in streamers:
    streamer_info_file = streamer+".txt"
    print "Gathering information from ", url + 'search?term=' + streamer + "\n"
    with open(streamer_info_file, 'w') as f_out:
        sys.stdout = f_out
        print streamer+"'s info bellow is taken from:", url + 'search?term=' + streamer + "\n"
        browser.get(url + 'search?term=' + streamer)

        wait_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]')

        # If streamer name is Offline now
        offlineCard = browser.find_elements_by_class_name(
            'search-result-offline_channel--body.tw-full-width.tw-mg-t-3.tw-overflow-hidden')
        if offlineCard:
            print(offlineCard[0].text.partition('Latest')[0])

        # If streamer name is Online now
        onlineCard = live_card('[data-test-selector="search-result-live-channel__viewer-count"]')
        if onlineCard:
            streamerName = browser.find_element_by_class_name(
                'tw-interactive.tw-link.tw-link--hover-underline-none.tw-link--inherit').text
            browser.find_element_by_link_text(streamerName).click()
            wait_class('tw-flex.tw-justify-content-center.tw-pd-b-1')
            streamerFollowers = browser.find_element_by_class_name(
                'social-media-space.tw-full-width').find_element_by_class_name('tw-align-center')
            streamerAbout = browser.find_element_by_class_name(
                'tw-flex.tw-flex-column.tw-full-width.tw-pd-y-1.tw-xs-pd-l-3.tw-xs-pd-r-1.tw-xs-pd-y-1')
            print streamerFollowers.text, "\n", streamerAbout.text, "\n"
            browser.back()
            wait_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div[1]/div/div[1]/div[1]/div[2]')

        # Other streamers have substring of streamer name
        cards = browser.find_elements_by_class_name('tw-align-items-center.tw-full-width.tw-inline-flex.tw-mg-b-0')
        print "We found", len(cards), "related results: \n"
        for follower in cards:
            if "followers" in follower.text:
                if 'Latest' in follower.text:
                    print(follower.text.partition('Latest')[0].encode('utf-8') + "\n")
                else:
                    print(follower.text.partition('Last')[0].encode('utf-8') + "\n")
        print "Thank you for using twitchy :)"
        sys.stdout = system_stdout
browser.quit()