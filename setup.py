#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    name="twitch-alert-bot",
    version="0.1",
    url="https://gitlab.com/WolfangAukang/twitch-alert-bot",
    author="P. R. d. O.",
    author_email="liquid.query960@4wrd.cc",
    install_requires=['python-twitter', 'PyYAML', 'twitchAPI'],
    scripts=["twitch_alert_bot"]
)
