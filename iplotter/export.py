import time
from selenium import webdriver
import os


class VirtualBrowser(object):
    """Helper class for converting html charts to png"""

    def __init__(self, driver=webdriver.Chrome):
        super(VirtualBrowser, self).__init__()
        self.driver = driver()

    def __enter__(self):
        return self

    def save_as_png(self, filename, width=300, height=250, render_time=1):
        '''
        open saved html file in an virtual browser and save a screen shot to PNG format
        '''
        self.driver.set_window_size(width, height)
        self.driver.get('file://{path}/{filename}'.format(
            path=os.getcwd(), filename=filename + ".html"))
        time.sleep(render_time)
        self.driver.save_screenshot(filename + ".png")

    def __exit__(self, type, value, traceback):
        self.driver.quit()
        return True

    def quit(self):
        '''
        shutdown virtual browser when finished
        '''
        self.driver.quit()
        return True