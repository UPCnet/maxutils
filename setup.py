from setuptools import setup, find_packages
import sys, os

version = '1.0.2.dev0'


setup(name='maxutils',
      version=version,
      description="Common utilities for mx software family",
      long_description="""\
A collection of methods and classes subject to be used accross all max components""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='max utils python',
      author='Carles Bruguera',
      author_email='carles.bruguera@upcnet.es',
      url='https://github.com/UPCnet/maxutils',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'pymongo',
          'setuptools',
          'ipdb'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
