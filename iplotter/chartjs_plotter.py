from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from .iplotter import IPlotter


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
