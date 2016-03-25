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
                                                     data=json.dumps(data, indent=4).replace("'", "\\'").replace('"', "'"))

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
        return HTML(self.iframe.format(source=self.render(data=data, div_id="chart", head=self.head), w=w, h=h))

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
                <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
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
                                                     data=json.dumps(data, indent=4).replace(
                                                         "'", "\\'").replace('"', "'"),
                                                     layout=json.dumps(layout, indent=4).replace("'", "\\'").replace('"', "'"))

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
        return HTML(self.iframe.format(source=self.render(data=data, layout=layout, head=self.head, ), w=w, h=h))

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


class ChartsJSPlotter(IPlotter):
    """
    Class for creating charts.js charts in ipython  notebook
    """

    def __init__(self):
        super(ChartsJSPlotter, self).__init__()

        self.head = '''
                <!-- Load Charts.js -->
               <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.min.js'></script>
        '''

        self.template = '''
            <canvas id='{{div_id}}'></canvas>
            <script>
                var ctx = document.getElementById('{{div_id}}').getContext('2d');
                ctx.canvas.width  = window.innerWidth;
                ctx.canvas.height = window.innerHeight;
                var myNewChart = new Chart(ctx).{{chart_type}}({{data}});
            </script>
        '''

    def render(self, data, chart_type, div_id="chart", head=""):
        '''
        render the data in HTML template
        '''
        if not self.valid_name(div_id):
            raise ValueError("Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(div_id))

        return Template(head + self.template).render(div_id=div_id.replace(" ", "_"),
                                                     data=json.dumps(data, indent=4).replace(
                                                         "'", "\\'").replace('"', "'"),
                                                     chart_type=chart_type)

    def plot_and_save(self, data, chart_type, w=800, h=420, filename='chart', overwrite=True):
        '''
        save the rendered html to a file and return an IFrame to display the plot in the notebook
        '''
        self.save(data, chart_type, filename, overwrite)
        return IFrame(filename + '.html', w, h)

    def plot(self, data, chart_type, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(self.iframe.format(source=self.render(data=data, chart_type=chart_type, head=self.head), w=w, h=h))

    def save(self, data, chart_type, filename='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(data=data, chart_type=chart_type, div_id=filename, head=self.head)

        if overwrite:
            with open(filename.replace(" ", "_") + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(filename.replace(" ", "_") + '.html'):
                with open(filename.replace(" ", "_") + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')


class ChartistPlotter(IPlotter):
    """
    Class for creating chartist.js charts in ipython  notebook
    """

    def __init__(self):
        super(ChartistPlotter, self).__init__()

        self.head = '''
                <!-- Load Chartist.js -->
                <link rel='stylesheet' href='https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.css'>
                <script src='https://cdn.jsdelivr.net/chartist.js/latest/chartist.min.js'></script>
        '''

        self.template = '''
             <div id={{div_id}} class='ct-chart' style='width: 100%; height: 100%' ></div>
            <script>
                new Chartist.{{chart_type}}('#{{div_id}}', {{data}}, {{options}});
            </script>
        '''

    def render(self, data, chart_type, options=None,  div_id="chart", head=""):
        '''
        render the data in HTML template
        '''
        if not self.valid_name(div_id):
            raise ValueError("Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(div_id))

        return Template(head + self.template).render(div_id=div_id.replace(" ", "_"),
                                                     data=json.dumps(data, indent=4).replace("'", "\\'")
                                                     .replace('"', "'"), chart_type=chart_type,
                                                     options=json.dumps(options, indent=4).replace("'", "\\'")
                                                     .replace('"', "'"))

    def plot_and_save(self, data, chart_type, options=None, w=800, h=420, filename='chart', overwrite=True):
        '''
        save the rendered html to a file and return an IFrame to display the plot in the notebook
        '''
        self.save(data, chart_type, options, filename, overwrite)
        return IFrame(filename + '.html', w, h)

    def plot(self, data, chart_type, options=None, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(self.iframe.format(source=self.render(data=data, options=options, chart_type=chart_type, head=self.head), w=w, h=h))

    def save(self, data, chart_type, options=None, filename='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(data=data, chart_type=chart_type, options=options, div_id=filename, head=self.head)

        if overwrite:
            with open(filename.replace(" ", "_") + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(filename.replace(" ", "_") + '.html'):
                with open(filename.replace(" ", "_") + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')
