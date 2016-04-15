from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from .iplotter import IPlotter


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
