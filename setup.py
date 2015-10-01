from setuptools import setup

setup(name='ipython_c3',
      version='0.1',
      description='c3.js plotting for iPython',
      url='None',
      author='csullivan',
      author_email='csullivan@crimsonhexagon.com',
      license='MIT',
      packages=['ipython_c3'],
      install_requires=[
          'Jinja2>=2.0',
          'ipython>=3.0'
      ],
      zip_safe=False)
