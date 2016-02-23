from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from abc import ABCMeta, abstractmethod


class IPlotter(object):
    """Abstract IPlotter"""

    __metaclass__ = ABCMeta

    def __init__(self):
        super(IPlotter, self).__init__()
        self.iframe = '<iframe srcdoc="{}" src="" width="{}" height="{}" sandbox="allow-scripts"></iframe>'

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
    Plotting Object for c3.js charts in ipython  notebook
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
            <div id={{name}}></div>
            <script>
                var {{name}} = document.getElementById('{{name}}');
                var data = {{data}};
                data['bindto']='#{{name}}'
                c3.generate(data);
            </script>
        '''

    def render(self, data, name, head=""):
        '''
        render the HTML template with supplied data to build the plot
        '''
        return Template(head + self.template).render(name=name, data=json.dumps(data).replace('"', "'"))

    def plot_and_save(self, data, w=800, h=420, name='chart', overwrite=True):
        '''
        save the rendered html to a file and returns an IFrame to display the plot in the notebook
        '''
        self.save(data, name, overwrite)
        return IFrame(name + '.html', w, h)

    def plot(self, data, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(self.iframe.format(self.render(data=data, name="chart", head=self.head), w, h))

    def save(self, data, name='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(data=data, name=name, head=self.head)
        if overwrite:
            with open(name + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(name + '.html'):
                with open(name + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')


class PlotlyPlotter(IPlotter):
    """
    Plotting Object for plotly.js charts in ipython  notebook
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
            <div id={{name}}></div>
            <script>
                var {{name}} = document.getElementById('{{name}}');
                Plotly.plot({{name}}, {{data}}, {{layout}});
            </script>
        '''

    def render(self, data, layout=None, name="chart", head=""):
        '''
        render the HTML template with supplied data to build the plot
        '''
        return Template(head + self.template).render(name=name, data=json.dumps(data).replace('"', "'"),
                                                     layout=json.dumps(layout).replace('"', "'"))

    def plot_and_save(self, data, layout=None, w=800, h=420, name='chart', overwrite=True):
        '''
        save the rendered html to a file and returns an IFrame to dislay the plot in the notebook
        '''
        self.save(data, layout, name, overwrite)
        return IFrame(name + '.html', w, h)

    def plot(self, data, layout=None, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(self.iframe.format(self.render(data=data, layout=layout, name="chart", head=self.head), w, h))

    def save(self, data, layout=None, name='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(data=data, layout=layout, name=name, head=self.head)
        if overwrite:
            with open(name + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(name + '.html'):
                with open(name + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')
