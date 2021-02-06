from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class WebAccessor(object):
        __instance = None
        __driver_options = None
        __driver = None

        def __init__(self):
                if WebAccessor.__instance is None:
                        WebAccessor.__instance = self
                        WebAccessor.__driver_options = webdriver.FirefoxOptions()
                        WebAccessor.__driver_options.set_headless()
                        WebAccessor.__driver = webdriver.Firefox(options=WebAccessor.__driver_options)
                else:
                        raise(Exception("This is a Singleton"))

        @staticmethod
        def instance():
                if WebAccessor.__instance is None:
                        WebAccessor.__instance = WebAccessor()
                return WebAccessor.__instance
        
        def get(self, url, logging = False, delay=1):
                try:
                        if logging: 
                                print(f"GET {url}")
                        if delay < 1:
                                delay = 1
                        sleep(delay)
                        WebAccessor.__driver.get(url)
                        return WebAccessor.__driver
                except Exception as e:
                        print("An error was encountered when requesting info")
                        return None

                

        
        def close(self):
             WebAccessor.__driver.close()   



