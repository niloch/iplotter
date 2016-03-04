from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from abc import ABCMeta, abstractmethod
import re


class IPlotter(object):
    """Abstract IPlotter"""

    __metaclass__ = ABCMeta

    def __init__(self):
        super(IPlotter, self).__init__()
        self.iframe = '<iframe srcdoc="{}" src="" width="{}" height="{}" sandbox="allow-scripts"></iframe>'
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


class C3Plotter(IPlotter):

    """
    Class for creating c3.js charts in ipython notebook
    """

    def __init__(self):
        super(C3Plotter, self).__init__()

        self.head = '''
            <!-- Load c3.css -->
            <link href='https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css' rel='stylesheet' type='text/css'/>

            <!-- Load d3.js and c3.js -->
            <script src='http://d3js.org/d3.v3.min.js' charset='utf-8'></script>
            <script src='http://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js'></script>

        '''

        self.template = '''
            <div id={{div_id}} style='width: 100%; height: 100%'></div>
            <script>
                var {{div_id}} = document.getElementById('{{div_id}}');
                var data = {{data}};
                data['bindto']='#{{div_id}}'
                c3.generate(data);
            </script>
        '''

    def render(self, data, div_id="chart", head=""):
        '''
        render the data in HTML template
        '''
        if not self.valid_name(div_id):
            raise ValueError("Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(div_id))

        return Template(head + self.template).render(div_id=div_id.replace(" ", "_"),
                                                     data=json.dumps(data).replace('"', "'"))

    def plot_and_save(self, data, w=800, h=420, filename='chart', overwrite=True):
        '''
        save the rendered html to a file and returns an IFrame to display the plot in the notebook
        '''
        self.save(data, filename, overwrite)
        return IFrame(filename + '.html', w, h)

    def plot(self, data, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(self.iframe.format(self.render(data=data, div_id="chart", head=self.head), w, h))

    def save(self, data, filename='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(data=data, div_id=filename, head=self.head)
        if overwrite:
            with open(filename.replace(" ", "_") + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(filename.replace(" ", "_") + '.html'):
                with open(filename.replace(" ", "_") + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')


class PlotlyPlotter(IPlotter):
    """
    Class for creating plotly.js charts in ipython  notebook
    """

    def __init__(self):
        super(PlotlyPlotter, self).__init__()

        self.head = '''
                <!-- Load d3.js and plotly.js -->
                <script src='https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js'></script>
                <script src='https://code.jquery.com/jquery-2.1.4.min.js'></script>
                <script src='https://d14fo0winaifog.cloudfront.net/plotly-basic.js'></script>
        '''

        self.template = '''
            <div id={{div_id}} style='width: 100%; height: 100%' ></div>
            <script>
                var {{div_id}} = document.getElementById('{{div_id}}');
                Plotly.plot({{div_id}}, {{data}}, {{layout}});
            </script>
        '''

    def render(self, data, layout=None, div_id="chart", head=""):
        '''
        render the data in HTML template
        '''
        if not self.valid_name(div_id):
            raise ValueError("Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(div_id))

        return Template(head + self.template).render(div_id=div_id.replace(" ", "_"),
                                                     data=json.dumps(data).replace('"', "'"),
                                                     layout=json.dumps(layout).replace('"', "'"))

    def plot_and_save(self, data, layout=None, w=800, h=420, filename='chart', overwrite=True):
        '''
        save the rendered html to a file and return an IFrame to display the plot in the notebook
        '''
        self.save(data, layout, filename, overwrite)
        return IFrame(filename + '.html', w, h)

    def plot(self, data, layout=None, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(self.iframe.format(self.render(data=data, layout=layout, head=self.head, ), w, h))

    def save(self, data, layout=None, filename='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(data=data, layout=layout, div_id=filename, head=self.head)

        if overwrite:
            with open(filename.replace(" ", "_") + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(filename.replace(" ", "_") + '.html'):
                with open(filename.replace(" ", "_") + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')
