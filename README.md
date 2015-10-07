IPlotter
=================

##C3.js and plotly.js charting in ipython/jupyter notebooks

- [Installation](#installation)
- [C3.js](#c3js)
- [plotly.js](#plotlyjs)
- [Usage](#usage)
- [Examples](#examples)

IPlotter is a simple library for generating interactive charts in C3.js or plotly.js from simple python data structures (dictionaries, lists, etc.)

## Installation
To install this package run `pip install git+git://github.com/niloch/iplotter.git@master` or `pip install iplotter`

## [C3.js](http://c3js.org/)

C3 is a charting library based on d3 for making interactive and easy to understand charts, graphs, and plots.

Charts can be conveniently declared as javascript objects and bound to DOM elements has animated transitions for hiding/displaying data.

## [plotly.js](https://plot.ly/javascript/)

Plotly.js is a charting library based on d3 from plotly.  plotly provides native clients in many languages including python which can be rendered in an ipython notebook.  However, the native python client requires the user to create an account and by default makes all plots public for free accounts. plotly.js can be used without creating an account and the results are rendered locally and kept private.  IPlotter makes use of the plotly.js library for chart rendering instead of the native python package from plotly.

## Usage

iplotter contains one class called IPlotter which is initialized according to the library that will be used ('c3/plotly').  An instantiated plotter's functions are called on supplied data with optional arguments for size and filename if needed.  The data should be a python dictionary, with an equivalent structure according the specifications for the chart json objects in either [C3.js](http://c3js.org/) or [plotly.js](https://plot.ly/javascript/).  plotly.js optionally allows specifying the chart layout as a separate dictionary.

## Examples

### C3 Stacked Area Spline Chart

```python
from iplotter.iplotter import IPlotter

plotter = IPlotter('c3')

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


### plotly.js Grouped Bar Chart

```python
from iplotter.iplotter import IPlotter

plotter2 = IPlotter('plotly')

trace1 = {
  "x": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  "y": [20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
  "type": 'bar',
  "name": 'Item 1',
  "marker": {
    "color": 'rgb(49,130,189)',
    "opacity": 0.7,
  }
}

trace2 = {
  "x": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  "y": [19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
  "type": 'bar',
  "name": 'Item 2',
  "marker": {
    "opacity": 0.7
  }
}

data = [trace1, trace2]

layout = {
  "title": 'Title',
  "xaxis": {
    "tickangle": -45
  },
  "barmode": 'group'
};

plotter2.plot(data,layout)
```
![Plot2](imgs/plot2.png?raw=true "Plot 2")

