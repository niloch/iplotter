IPlotter
=================

## C3.js and plotly.js charting in ipython/jupyter notebooks


<!-- MarkdownTOC -->

- [Installation](#installation)
- [C3.js](#c3js)
- [plotly.js](#plotlyjs)
- [Usage](#usage)
- [Examples](#examples)
    - [C3 Stacked Area Spline Chart](#c3-stacked-area-spline-chart)
    - [plotly.js HeatMap](#plotlyjs-heatmap)
    - [Multple Charts and Mixing Libraries](#multple-charts-and-mixing-libraries)

<!-- /MarkdownTOC -->


iplotter is a simple package for generating interactive charts ipython/jupyter notebooks using C3.js or plotly.js from simple python data structures (dictionaries, lists, etc.)

## Installation
To install the most recent stable release run `pip install iplotter`.

To install the latest version run `pip install git+git://github.com/niloch/iplotter.git@master` or
`git clone https://github.com/niloch/iplotter.git` followed by `pip install -e iplotter/`

## [C3.js](http://c3js.org/)

C3 is a charting library based on d3 for making interactive and easy to understand charts, graphs, and plots.

Charts have animated transitions for hiding/displaying data.

## [plotly.js](https://plot.ly/javascript/)

Plotly.js is a charting library based on d3 from plotly.  plotly provides native clients in many programming languages including python which can be rendered in an ipython notebook.  However, the native python client requires the user to create an account and by default makes all plots public. plotly.js can be used without creating an account and are rendered locally to keep data private.  iplotter uses plotly.js to rendering charts locally while the native python client from renders charts remotely on their servers.

## Usage

iplotter attempts to maintain a consistent API across supported JavaScript Libraries with a separate class for each. The python chart data and layout must be structured according to the JSON equivalent for each library(see [C3.js](http://c3js.org/) and [plotly.js](https://plot.ly/javascript/) for details). Plots can be rendered in the ipython notebook and saved to the current directory as html, for later reference.

## Examples

### C3 Stacked Area Spline Chart

```python
from iplotter.iplotter import C3Plotter

plotter = C3Plotter()

chart = {
    "data": {
        "columns": [
            ['data1', 300, 350, 300, 0, 0, 120],
            ['data2', 130, 100, 140, 200, 150, 50],
            ['data3', 180, 75, 265, 100, 50, 100]
        ],
        "types": {
            "data1": 'area-spline',
            "data2": 'area-spline',
            "data3": 'area-spline'
        },
        "groups": [['data1', 'data2', 'data3']]
    }
}

plotter.plot(chart)
```
![Plot1](imgs/plot1.png?raw=true "Plot 1")

### plotly.js HeatMap

```python
from iplotter.iplotter import PlotlyPlotter

plotter = PlotlyPlotter()

data = [
    {
        'colorscale': 'YIGnBu',
        'reversescale': True,
        'type': 'heatmap',
        'x': ['class1', 'class2', 'class3'],
        'y': ['class1', 'class2', 'class3'],
        'z': [[0.7,  0.2,  0.1],
              [0.2,  0.7,  0.1],
              [0.15,  0.27,  0.56]]
    }
]

layout = {
    "title": 'Title',
    "xaxis": {
        "tickangle": -45
    },
}

plotter.plot_and_save(data, layout=layout, w=600, h=600, filename='heatmap1', overwrite=True)
```
![Plot3](imgs/plot3.png?raw=true "Plot 3")

### Multple Charts and Mixing Libraries

Saving multiple charts to one file or displaying multiple charts in one iframe can be achieved by concatenating html strings returned by the render function. The plotter's `head` attribute contains the script tags for loading the necessary JavasScript libraries and `div_ids` must be unique.  Charts from different libraries can be mixed together.

```python
from iplotter.iplotter import PlotlyPlotter, C3Plotter
from IPython.display import HTML

plotly_plotter = PlotlyPlotter()

c3_plotter = C3Plotter()

plotly_chart = [
    {
        "x": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        "y": [20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
        "type": 'bar',
        "name": 'Item 1',
        "marker": {
            "color": 'rgb(49,130,189)',
            "opacity": 0.7,
        }
    }
]

c3_chart = {
    "data": {
        "columns": [
            ['data1', 300, 350, 300, 0, 0, 120],
            ['data2', 130, 100, 140, 200, 150, 50],
            ['data3', 180, 75, 265, 100, 50, 100]
        ],
        "types": {
            "data1": 'area-spline',
            "data2": 'area-spline',
            "data3": 'area-spline'
        },
        "groups": [['data1', 'data2', 'data3']]
    }
}

# plotter.head will return the html string containing script tags for loading the plotly.js/C3.js libraries
multiple_plot_html = plotly_plotter.head + c3_plotter.head

multiple_plot_html += c3_plotter.render(data=c3_chart, div_id="chart_1")

multiple_plot_html += plotly_plotter.render(data=plotly_chart, div_id="chart_2")

# display multiple plots in iframe
HTML(c3_plotter.iframe.format(multiple_plot_html, 900, 900))

# Write multiple plots to file
with open("multiple_plots.html", 'w') as outfile:
    outfile.write(multiple_plot_html)
```
![Plot4](imgs/plot4.png?raw=true "Plot 4")