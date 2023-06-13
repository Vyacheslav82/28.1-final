rom urllib.parse import urlparse



class BasePage(object):

    def __init__(self, driver, url, timeout=5):

        self.driver = driver

        self.url = url

        self.driver.implicitly_wait(timeout)



    def get_base_url(self):

        url = urlparse(self.driver.current_url)

        return url.hostname



    def get_relative_link(self):

        url = urlparse(self.driver.current_url)

        return url.path