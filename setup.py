from setuptools import setup
from setuptools import find_packages
import os

__VERSION__ = '0.1.1'

if __name__ == '__main__':

    setup(name='iplotter',
          version=__VERSION__,
          description='C3.js and plotly.js for iPython/Jupyter notebooks',
          setup_requires=['setuptools-markdown'],
          long_description_markdown_filename='README.md',
          url='https://github.com/niloch/iplotter',
          author='Colin',
          author_email='csulliva@brandeis.edu',
          license='MIT',
          packages=find_packages(),
          install_requires=[
              'Jinja2>=2.0',
              'ipython>=3.0',
              'notebook>=3.0'
          ],
          zip_safe=False,
          include_package_data=True,
          classifiers=[
              'Development Status :: 3 - Alpha',
              'Intended Audience :: Data Scientists',
              'License :: OSI Approved :: MIT License',
              'Programming Language :: Python :: 2.7',
          ])
