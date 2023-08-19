from selenium_webdriver_module import Driver
from time import sleep
from pprint import pprint

# Initialize the driver with the desired URL
driver = Driver('https://www.google.com/')


# Locate elements on the page
element = driver.find_element('class', 'gLFyf')


# Perform actions like clicking and sending text
driver.send_text('class', 'gLFyf', 'Selenium doc')
driver.click_element('class', 'gNO89b')


# Get all links on the page
links = driver.get_all_hrefs('a')
pprint(links)


# Close the driver when done
sleep(2)
driver.close_driver()