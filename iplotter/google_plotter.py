from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from .iplotter import IPlotter


class GCPlotter(IPlotter):
    """
    Class for creating Google Charts in ipython  notebook
    """

    def __init__(self):
        super(GCPlotter, self).__init__()

        self.head = '''
                <!-- Load Google Charts -->
                <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>
        '''

        self.template = '''
            <div id={{div_id}} style='width: 100%; height: 100%' ></div>
            <script type='text/javascript'>
                google.charts.load('current', {'packages':['corechart']});
                google.charts.setOnLoadCallback(drawChart);

                function drawChart() {
                    var data = google.visualization.arrayToDataTable({{data}}
                    );

                    var chart = new google.visualization.{{chart_type|title}}Chart(document.getElementById('{{div_id}}'));

                    chart.draw(data, {{options}});
                }
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
