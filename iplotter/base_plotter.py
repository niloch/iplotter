from abc import ABCMeta, abstractmethod
import re
import time
from selenium import webdriver
import os


class IPlotter(object):
    """Abstract IPlotter"""

    __metaclass__ = ABCMeta
    iframe = '<iframe srcdoc="{source}" src="" width="{w}" height="{h}" sandbox="allow-scripts"></iframe>'
    invalid_name_pattern = re.compile(r'[^a-zA-Z0-9_\-\. ]+')

    def __init__(self):
        super(IPlotter, self).__init__()

    @classmethod
    def is_valid_name(cls, name):
        '''
        check whether plot div id or filenname are valid
        '''
        if (cls.invalid_name_pattern.search(name)):
            return False
        else:
            return True

    @abstractmethod
    def render(self):
        '''
        render the data in HTML template
        '''
        pass

    @abstractmethod
    def plot(self):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        pass

    @abstractmethod
    def save(self):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        pass

    @abstractmethod
    def plot_and_save(self):
        '''
        save the rendered html to a file and return an IFrame to display the
        plot in the notebook
        '''
        pass


class VirtualBrowser(object):
    """Helper class for converting html charts to png"""

    def __init__(self, driver=webdriver.Chrome):
        super(VirtualBrowser, self).__init__()
        self.driver = driver()

    def __enter__(self):
        return self

    def save_as_png(self, filename, width=300, height=250):
        '''
        open saved html file in an virtual browser and save a screen shot to PNG format
        '''
        self.driver.set_window_size(width, height)
        self.driver.get('file://{path}/{filename}'.format(
            path=os.getcwd(), filename=filename + ".html"))
        time.sleep(1)
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