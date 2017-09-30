from abc import ABCMeta, abstractmethod
import re
import time
from selenium import webdriver
import os


class IPlotter(object):
    """Abstract IPlotter"""

    __metaclass__ = ABCMeta
    iframe = '<iframe srcdoc="{source}" src="" width="{w}" height="{h}" frameborder="0" sandbox="allow-scripts"></iframe>'
    invalid_name_pattern = re.compile(r'[^a-zA-Z0-9_\-\. ]+')

    def __init__(self):
        super(IPlotter, self).__init__()

    @classmethod
    def is_valid_name(cls, name):
        """Check whether plot div id or filenname are valid."""
        if (cls.invalid_name_pattern.search(name)):
            return False
        else:
            return True

    @abstractmethod
    def render(self):
        """Render the data in HTML template."""
        pass

    @abstractmethod
    def plot(self):
        """Output an iframe containing the plot in the notebook without saving."""
        pass

    @abstractmethod
    def save(self):
        """Save the rendered html to a file in the same directory as the notebook."""
        pass

    @abstractmethod
    def plot_and_save(self):
        """Save the rendered html to a file and return an IFrame to display the plot in the notebook."""
        pass
