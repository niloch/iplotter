from setuptools import setup
from setuptools import find_packages
import os


def get_version():
    version = os.popen('git describe', "r").read().strip()
    return version

if __name__ == '__main__':

    setup(name='iplotter',
          version=get_version(),
          description='C3.js and plotly.js for iPython/Jupyter notebooks',
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
          include_package_data=True)
