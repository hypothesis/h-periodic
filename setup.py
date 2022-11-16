import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.markdown')) as f:
    README = f.read()

setup(
    name='h-periodic',
    description='Hypothesis Celery Beat Process',
    long_description=README,
    url='https://github.com/hypothesis/h-periodic',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points="",
)
