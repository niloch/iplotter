from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from .base_plotter import IPlotter


class C3Plotter(IPlotter):
    """Class for creating c3.js charts in ipython notebook."""

    head = """
        <!-- Load c3.css -->
        <link href='https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css' rel='stylesheet' type='text/css'/>

        <!-- Load d3.js and c3.js -->
        <script src='http://d3js.org/d3.v3.min.js' charset='utf-8'></script>
        <script src='http://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js'></script>

    """

    template = """
        <div id={{div_id}} style='width: 100%; height: 100%'></div>
        <script>
            var {{div_id}} = document.getElementById('{{div_id}}');
            var data = {{data}};
            data['bindto']='#{{div_id}}'
            c3.generate(data);
        </script>
    """

    def __init__(self):
        super(C3Plotter, self).__init__()

    def render(self, data, div_id="chart", head=""):
        """Render the data in HTML template."""
        if not self.is_valid_name(div_id):
            raise ValueError(
                "Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(
                    div_id))

        return Template(head + self.template).render(
            div_id=div_id.replace(" ", "_"),
            data=json.dumps(
                data, indent=4).replace("'", "\\'").replace('"', "'"))

    def plot_and_save(self,
                      data,
                      w=800,
                      h=420,
                      filename='chart',
                      overwrite=True):
        """Save the rendered html to a file and returns an IFrame to display the plot in the notebook."""
        self.save(data, filename, overwrite)
        return IFrame(filename + '.html', w, h)

    def plot(self, data, w=800, h=420):
        """Output an iframe containing the plot in the notebook without saving."""
        return HTML(
            self.iframe.format(
                source=self.render(
                    data=data, div_id="chart", head=self.head),
                w=w,
                h=h))

    def save(self, data, filename='chart', overwrite=True):
        """Save the rendered html to a file in the same directory as the notebook."""
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
