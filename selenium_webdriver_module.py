from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Driver:
    """
    A class to simplify interaction with Selenium WebDriver.

    Args:
        url (str): The initial URL to load in the WebDriver.

    Methods:
        close_driver(): Closes the WebDriver.
        find_element(tag, name, text=False): Locates an element on the page.
        find_elements(tag, name): Locates all matching elements on the page.
        click_element(tag, name): Clicks on an element on the page.
        send_text(tag, name, text): Sends text to an element on the page.
        get_all_hrefs(tag_name, timeout=10): Gets all links based on the tag name.

    """

    _by = {            
        'id': By.ID,
        'class': By.CLASS_NAME,
        'name': By.NAME,
        'tag': By.TAG_NAME,
        'xpath': By.XPATH
    }
    
    def __init__(self, url) -> None:
        """
        Initializes an instance of the Chrome WebDriver and opens the provided URL.

        Args:
            url (str): The initial URL to load in the WebDriver.
        """
        _service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=_service)
        self.driver.implicitly_wait(2)
        self.url = url
        self.driver.get(self.url)
    

    def close_driver(self):
        """Closes the WebDriver."""
        self.driver.quit()


    def _find_by(self, value):
        """
        Internal method to map tag values to Selenium By objects.

        Args:
            value (str): The tag's value.

        Returns:
            By: The corresponding By object.
        """
        for key in self._by.keys():
            if value == key:
                return self._by[key]
        return None


    def find_element(self, tag, name, text=False):
        """
        Locates an element on the page based on tag and name.

        Args:
            tag (str): The element's tag (e.g., 'id', 'class', 'name', etc.).
            name (str): The element's name.
            text (bool): If True, returns the element's text instead of the element itself.

        Returns:
            WebElement or str: The found element or its text, depending on the 'text' value.
        """
        if not text:
            return self.driver.find_element(self._find_by(tag), name)
        return self.driver.find_element(self._find_by(tag), name).text


    def find_elements(self, tag, name):
        """
        Locates all matching elements on the page based on tag and name.

        Args:
            tag (str): The element's tag (e.g., 'id', 'class', 'name', etc.).
            name (str): The element's name.

        Returns:
            list[WebElement]: A list of matching elements.
        """
        return self.driver.find_elements(self._find_by(tag), name)
    

    def click_element(self, tag, name):
        """
        Clicks on an element on the page based on tag and name.

        Args:
            tag (str): The element's tag (e.g., 'id', 'class', 'name', etc.).
            name (str): The element's name.
        """
        self.find_element(tag, name).click()

    
    def send_text(self, tag, name, text):
        """
        Sends text to an element on the page based on tag and name.

        Args:
            tag (str): The element's tag (e.g., 'id', 'class', 'name', etc.).
            name (str): The element's name.
            text (str): The text to send to the element.
        """
        self.find_element(tag, name).send_keys(text)
    

    def get_all_hrefs(self, tag_name, timeout=10):
        """
        Gets all links based on the tag name.

        Args:
            tag_name (str): The tag name of the links.
            timeout (int): The maximum wait time for elements to load (default: 10 seconds).

        Returns:
            dict: A dictionary where keys are link text and values are the URLs of the links.
        """
        try:
            condition = EC.presence_of_all_elements_located((By.TAG_NAME, tag_name))
            WebDriverWait(self.driver, timeout).until(condition)

            elements = self.find_elements('tag', tag_name)

            result = {
                element.text: element.get_attribute('href') 
                for element in elements
            }
        except TimeoutException:
            print('Timed out while loading the page.')
        finally:
            self.close_driver()

        return result


