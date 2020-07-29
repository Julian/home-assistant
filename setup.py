#!/usr/bin/env python
import os
from setuptools import setup, find_packages
from homeassistant.const import __version__

PACKAGE_NAME = 'homeassistant'
HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = ('https://github.com/home-assistant/home-assistant/archive/'
                '{}.zip'.format(__version__))

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'cherrypy==6.1.1',
    'future',
    'jinja2>=2.8',
    'pytz>=2016.6.1',
    'pyyaml>=3.11,<4',
    'requests>=2,<3',
    'sqlalchemy==1.0.14',
    'static3==0.7.0',
    'voluptuous==0.9.1',
    'werkzeug==0.15.3',
]

setup(
    name=PACKAGE_NAME,
    version=__version__,
    license='MIT License',
    url='https://home-assistant.io/',
    download_url=DOWNLOAD_URL,
    author='Paulus Schoutsen',
    author_email='paulus@paulusschoutsen.nl',
    description='Open-source home automation platform running on Python 3.',
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIRES,
    extras_require={
        'apcupsd' : ["apcaccess==0.0.4"],
        'arduino' : ['PyMata==2.12'],
        'aruba' : ['pexpect==4.0.1'],
        'bitcoin' : ['blockchain==1.3.3'],
        'blinkstick' : ["blinkstick==1.1.7"],
        'cast': ['pychromecast>=0.7.2'],
        'color': ['colorlog'],
        'conversation': ['fuzzywuzzy>=0.11.0'],
        'cpuspeed' : ['py-cpuinfo>=0.2.3'],
        'discovery': ['netdisco>=0.7.0'],
        'dweepy' : ['dweepy==0.2.0'],
        'eliq' : ['eliqonline==1.0.12'],
        'forecastio' : ['python-forecastio==1.3.4'],
        'fritz' : ['fritzconnection==0.4.6'],
        'heatmiser' : ["heatmiserV3==0.9.1"],
        'hikvisioncam' : ['hikvision==0.4'],
        'honeywell' : ['evohomeclient==0.2.5', 'somecomfort==0.2.1'],
        'hue' : ['phue==0.8'],
        'icloud' : ['pyicloud==0.8.3'],
        'ifttt' : ['pyfttt==0.3'],
        'insteon' : ['insteon_hub==0.4.5'],
        'influxdb' : ['influxdb==3.0.0'],
        'isy994' : ['PyISY==1.0.6'],
        'keyboard' : ['pyuserinput==0.1.9'],
        'kodi' : ['jsonrpc-requests==0.3'],
        'lifx' : ['liffylights==0.9.4'],
        'limitlessled' : ['limitlessled==1.0.0'],
        'mfi' : ['mficlient>=0.3.0'],
        'mpd' : ['python-mpd2==0.5.5'],
        'mqtt' : ['paho-mqtt==1.2'],
        'nest' : ['python-nest==2.9.2'],
        'netgear' : ['pynetgear==0.3.3'],
        'nmap' : ['python-nmap==0.6.0'],
        'nx584' : ['pynx584==0.2'],
        'openweathermap' : ['pyowm==2.3.2'],
        'orvibo' : ['orvibo==1.1.1'],
        'plex' : ['plexapi==1.1.0'],
        'prolifix' : ['proliphix==0.1.0'],
        'pushbullet' : ['pushbullet.py==0.10.0'],
        'pushetta' : ['pushetta==1.0.15'],
        'pushover' : ['python-pushover==0.2'],
        'radiotherm' : ['radiotherm==1.2'],
        'rpi-gpio' : ['RPi.GPIO==0.6.1'],
        'samsungtv' : ['samsungctl==0.5.1'],
        'scsgate' : ['scsgate==0.1.0'],
        'slack' : ['slacker==0.9.24'],
        'sms' : ['freesms==0.1.0'],
        'snapcast' : ['snapcast==1.2.1'],
        'snmp' : ['pysnmp==4.3.2'],
        'sonos' : ['SoCo==0.11.1'],
        'speedtest' : ['speedtest-cli==0.3.4'],
        'statsd' : ['statsd==3.2.1'],
        'sun': ['astral>=1.2'],
        'system-monitor' : ['psutil>=4.3.0'],
        'telegram' : ['python-telegram-bot==5.0.0'],
        'tellduslive' : ['tellive-py==0.5.2'],
        'tellstick' : ['tellcore-py==1.1.2'],
        'transmission' : ['transmissionrpc==0.11'],
        'twitch' : ['python-twitch==1.3.0'],
        'twitter' : ['TwitterAPI==2.4.1'],
        'uvc' : ['uvcclient>=0.9.0'],
        'vera' : ['pyvera==0.2.8'],
        'verisure' : ['vsure==0.8.1'],
        'wemo' : ['pywemo>=0.3.12'],
        'wink' : ['python-wink>=0.7.11', "pubnub>=3.8.2"],
        'xmpp' : [
            'dnspython3==1.12.0',
            'pyasn1==0.1.9',
            'pyasn1-modules==0.0.8',
            'sleekxmpp==1.3.1',
        ],
        'yrno' : ['xmltodict==0.10.2'],
        'zigbee' : ["xbee-helper==0.0.7"],
        'zwave' : ['openzwave-cffi'],
        ':python_version=="2.7"': ['enum34'],
    },
    test_suite='tests',
    keywords=['home', 'automation'],
    entry_points={
        'console_scripts': [
            'hass = homeassistant.__main__:main'
        ]
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Home Automation'
    ],
)
