from setuptools import setup

setup(name='iplotter',
      version='0.1',
      description='c3.js and plotly.js for iPython',
      url='https://github.com/niloch/iplotter',
      author='csullivan',
      author_email='csullivan@crimsonhexagon.com',
      license='MIT',
      packages=['iplotter'],
      install_requires=[
          'Jinja2>=2.0',
          'ipython>=3.0'
      ],
      zip_safe=False)
