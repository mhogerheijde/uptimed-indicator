from setuptools import setup

import uptime_indicator


setup(
    name = uptime_indicator.__name__,
    version = uptime_indicator.__version__,
    author = uptime_indicator.__author__,
    author_email = uptime_indicator.__email__,
    license = uptime_indicator.__license__,
    description = uptime_indicator.__doc__.strip().splitlines()[0],
    long_description = open('README.rst').read(),
    url = 'http://github.com/mhogerheijde/uprecords-indicator',
    download_url = 'http://github.com/mhogerheijde/uprecords-indicator/archives/master',
    packages = ['uptime_indicator'],
    include_package_data = True,
    zip_safe = False,
    platforms = ['all'],
    test_suite = 'tests',
    entry_points = {
        'console_scripts': [
            'uptimed-indicator = uptime_indicator.indicator:main',
        ],
    },
    install_requires=[],
)
