from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='andabb',

    version='0.1.0',

    description='V-REP remote API python client',
    long_description=long_description,

    url='https://github.com/luwood/MO810-vrep-python',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Robotics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],

    keywords='vrep',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['numpy', 'scipy', 'scikit-fuzzy', 'matplotlib'],

    entry_points={
        'console_scripts': [
            'pioneer=andabb:main'
        ],
    },
)
