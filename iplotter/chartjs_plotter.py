from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from .base_plotter import IPlotter


class ChartJSPlotter(IPlotter):
    """
    Class for creating charts.js charts in ipython  notebook
    """

    head = '''
        <!-- Load Charts.js -->
       <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.bundle.min.js'></script>
    '''

    template = '''
        <canvas id='{{div_id}}'></canvas>
        <script>
            var ctx = document.getElementById('{{div_id}}').getContext('2d');
            ctx.canvas.width  = {{w}} - (.1 * {{w}});
            ctx.canvas.height = {{h}} - (.15 * {{h}});
            var myNewChart = new Chart(ctx,{ type: '{{chart_type}}', data: {{data}}, options: {{options}} });
        </script>
    '''

    def __init__(self):
        super(ChartJSPlotter, self).__init__()

    def render(self,
               data,
               chart_type,
               options=None,
               div_id="chart",
               head="",
               w=800,
               h=420):
        '''
        render the data in HTML template
        '''
        if not self.is_valid_name(div_id):
            raise ValueError(
                "Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(
                    div_id))

        return Template(head + self.template).render(
            div_id=div_id.replace(" ", "_"),
            data=json.dumps(
                data, indent=4).replace("'", "\\'").replace('"', "'"),
            chart_type=chart_type,
            options=json.dumps(
                options, indent=4).replace("'", "\\'").replace('"', "'"),
            w=w,
            h=h)

    def plot_and_save(self,
                      data,
                      chart_type,
                      options=None,
                      w=800,
                      h=420,
                      filename='chart',
                      overwrite=True):
        '''
        save the rendered html to a file and return an IFrame to display the plot in the notebook
        '''
        self.save(data, chart_type, options, filename, w, h, overwrite)
        return IFrame(filename + '.html', w, h)

    def plot(self, data, chart_type, options=None, w=800, h=420):
        '''
        output an iframe containing the plot in the notebook without saving
        '''
        return HTML(
            self.iframe.format(
                source=self.render(
                    data=data,
                    chart_type=chart_type,
                    options=options,
                    head=self.head,
                    w=w,
                    h=h),
                w=w,
                h=h))

    def save(self,
             data,
             chart_type,
             options=None,
             filename='chart',
             w=800,
             h=420,
             overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        html = self.render(
            data=data,
            chart_type=chart_type,
            options=options,
            div_id=filename,
            head=self.head,
            w=w,
            h=h)

        if overwrite:
            with open(filename.replace(" ", "_") + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(filename.replace(" ", "_") + '.html'):
                with open(filename.replace(" ", "_") + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')
