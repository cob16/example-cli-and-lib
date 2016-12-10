# example taken from https://python-packaging.readthedocs.io/en/latest/about.html

# Always prefer setuptools over distutils
import sys
from setuptools import setup

if sys.version_info.major < 3:
    sys.stderr.write("This package only supports Python 3!\n")
    sys.exit(1)

setup(
    name='broadcast_cli',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0',

    description='An educational test package for REST communication with the a API',

    # The project's main homepage.
    # url='https://github.com/pypa/sampleproject',

    # # Author details
    author='cormac brady',
    author_email='cormac.brady@hotmail.co.uk',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=[
        'broadcast',
        'broadcast_cli',
    ],

    install_requires=[
        'clint',
        'begins',
        'requests',
        'furl',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        # 'dev': ['check-manifest'],
        'test': ['nose'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'broadcast=broadcast_cli.commands:broadcast.start',
        ],
    },
)
