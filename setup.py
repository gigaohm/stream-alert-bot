from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    req = f.read().splitlines()

with open('requirements.dev.txt') as f:
    dev = f.read().splitlines()

setup(
    name="twitch-alert-bot",
    version="0.1.0",
    description="Bot that checks streams from Twitch and alerts on Twitter when they are live",
    long_description=readme,
    author="P. R. d. O.",
    author_email="liquid.query960@4wrd.cc",
    url="https://gitlab.com/WolfangAukang/twitch-alert-bot",
    license=license,
    long_description_content_type="text/markdown",
    install_requires=req,
    extras_require={
        'devel': dev
    },
    packages=find_packages(),
    entry_points={
        "console_scripts": [ "twitch_alert_bot=tab.__main__:main" ]
    },
)
