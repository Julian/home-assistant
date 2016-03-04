#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from homeassistant.const import __version__

PACKAGE_NAME = 'homeassistant'
HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = ('https://github.com/balloob/home-assistant/archive/'
                '{}.zip'.format(__version__))

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'future',
    'requests>=2,<3',
    'pyyaml>=3.11,<4',
    'pytz>=2015.4',
    'vincenty==0.1.3',
    'jinja2>=2.8',
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
        'arduino' : ['PyMata==2.07a'],
        'aruba' : ['pexpect==4.0.1'],
        'bitcoin' : ['blockchain==1.2.1'],
        'blinkstick' : ["blinkstick==1.1.7"],
        'cast': ['pychromecast>=0.7.2'],
        'color': ['colorlog'],
        'conversation': ['fuzzywuzzy'],
        'cpuspeed' : ['py-cpuinfo>=0.2.3'],
        'discovery': ['netdisco>=0.5.4'],
        'dweepy' : ['dweepy==0.2.0'],
        'eliq' : ['eliqonline==1.0.11'],
        'forecastio' : ['python-forecastio'],
        'fritz' : ['fritzconnection==0.4.6'],
        'heatmiser' : ["heatmiserV3==0.9.1"],
        'hikvisioncam' : ['hikvision==0.4'],
        'honeywell' : ['evohomeclient==0.2.4', 'somecomfort==0.2.1'],
        'hue' : ['phue==0.8'],
        'icloud' : ['pyicloud==0.7.2'],
        'ifttt' : ['pyfttt==0.3'],
        'insteon' : ['insteon_hub==0.4.5'],
        'influxdb' : ['influxdb==2.12.0'],
        'isy994' : ['PyISY==1.0.5'],
        'keyboard' : ['pyuserinput==0.1.9'],
        'kodi' : ['jsonrpc-requests==0.1'],
        'lifx' : ['liffylights==0.9.4'],
        'limitlessled' : ['limitlessled==1.0.0'],
        'mfi' : ['mficlient>=0.3.0'],
        'mpd' : ['python-mpd2==0.5.4'],
        'mqtt' : ['paho-mqtt==1.1'],
        'nest' : ['python-nest==2.6.0'],
        'netgear' : ['pynetgear==0.3.2'],
        'nmap' : ['python-nmap==0.4.3'],
        'nx584' : ['pynx584==0.2'],
        'openweathermap' : ['pyowm==2.3.0'],
        'orvibo' : ['orvibo==1.1.1'],
        'plex' : ['plexapi==1.1.0'],
        'prolifix' : ['proliphix==0.1.0'],
        'pushbullet' : ['pushbullet.py==0.9.0'],
        'pushetta' : ['pushetta==1.0.15'],
        'pushover' : ['python-pushover==0.2'],
        'radiotherm' : ['radiotherm==1.2'],
        'rpi-gpio' : ['RPi.GPIO==0.6.1'],
        'samsungtv' : ['samsungctl==0.5.1'],
        'scsgate' : ['scsgate==0.1.0'],
        'slack' : ['slacker==0.6.8'],
        'sms' : ['freesms==0.1.0'],
        'snapcast' : ['snapcast==1.1.1'],
        'snmp' : ['pysnmp==4.2.5'],
        'sonos' : ['SoCo==0.11.1'],
        'speedtest' : ['speedtest-cli==0.3.4'],
        'statsd' : ['python-statsd==1.7.2'],
        'sun': ['astral'],
        'system-monitor' : ['psutil>=4.0.0'],
        'telegram' : ['python-telegram-bot==3.2.0'],
        'tellduslive' : ['tellive-py==0.5.2'],
        'tellstick' : ['tellcore-py==1.1.2'],
        'transmission' : ['transmissionrpc==0.11'],
        'twitch' : ['python-twitch==1.2.0'],
        'twitter' : ['TwitterAPI==2.3.6'],
        'uvc' : ['uvcclient>=0.8'],
        'vera' : ['pyvera==0.2.8'],
        'verisure' : ['vsure>=0.6.1'],
        'wemo' : ['pywemo>=0.3.12'],
        'wink' : ['python-wink>=0.6.2'],
        'xmpp' : ['sleekxmpp==1.3.1', 'dnspython3==1.12.0'],
        'yrno' : ['xmltodict'],
        'zigbee' : ["xbee-helper==0.0.6"],
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
