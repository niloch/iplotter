from jinja2 import Template
from IPython.display import IFrame
import os


class Plotter(object):

    """Class for creating c3js plots in ipython"""

    def __init__(self):
        super(Plotter, self).__init__()
        self.template = '''
<!-- Load c3.css -->
<link href='https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css' rel="stylesheet" type="text/css"/>

<!-- Load d3.js and c3.js -->
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script src='http://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js'></script>
<div id=chart></div>
<script> c3.generate({{data}}); </script>
    '''

    def plot(self, data, name='c3', w=800, h=420):
        html = Template(self.template).render(data=data)
        with open(name + '.html', 'w') as f:
            f.write(html)
        return IFrame(name + '.html', w, h)
