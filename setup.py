"""

"""

from setuptools import setup, find_packages

setup(
    name='labpyrinth',
    package_data={'': ['*.md', '*.txt', '*.json']},
    author='Alistair Broomhead',
    version='0.0.0',
    author_email='alistair.broomhead@gmail.com',
    description='A simple python-based generator for labyrinths and mazes.',
    license='BSD 3-clause',
    url='https://github.com/alistair-broomhead/labpyrinth',
    long_description=__doc__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
    ],
    extras_require={
        'dev': [
            'black'
        ]
    },
)
