# Twitch Alert Bot

This bot will indicate which streamers are live on Twitch and announce them on Twitter.

## Steps

- On the `etc/` directory, copy or rename the `settings-example.yml` to `settings.yml`
- Get [Twitch](https://dev.twitch.tv/console/apps/create) and [Twitter](https://developer.twitter.com/en/portal/dashboard) credentials and add them to the settings
  - For Twitter, you will need the access token and secrets with Read and Write permissions
- Set a polling interval
- On the Streamers list, follow the provided examples and add the streamers you want to check.
- When you are done, run `./twitch_alert_bot path_to_settings_file`

## Project Environments

### Virtualenv 

- Create a virtual environment on the project directory (`virtualenv project_path`)
- Run `source bin/activate`
- Run `pip install -r requirements.txt`

### Nix

- Run `nix-shell nix/`

## Building the Application

### setup.py

- As a pre-requisite, verify GCC is available on your computer (necessary to build aiohttp)
- Run `python setup.py install`
- The binary will be located at bin/

### Nix

- Run `nix-build nix/release.nix`
- The binary will be located at result/bin/

## Thanks to
- [Roger Zanoni](https://gitlab.com/roger.zanoni)

