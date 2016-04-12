from abc import ABCMeta, abstractmethod
import re


class IPlotter(object):
    """Abstract IPlotter"""

    __metaclass__ = ABCMeta

    def __init__(self):
        super(IPlotter, self).__init__()
        self.iframe = '<iframe srcdoc="{source}" src="" width="{w}" height="{h}" sandbox="allow-scripts"></iframe>'
        self.invalid_name_pattern = re.compile(r'[^a-zA-Z0-9_\-\. ]+')

    def valid_name(self, name):
        if (self.invalid_name_pattern.search(name)):
            return False
        else:
            return True

    @abstractmethod
    def render(self):
        return NotImplementedError()

    @abstractmethod
    def plot(self):
        return NotImplementedError()

    @abstractmethod
    def save(self):
        return NotImplemented()

    @abstractmethod
    def plot_and_save(self):
        return NotImplemented
