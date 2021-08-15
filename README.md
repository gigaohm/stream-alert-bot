# Twitch Alert Bot

This bot will indicate which streamers are live on Twitch and announce them on Twitter.

## Steps

- On the `etc/` directory, copy or rename the `settings-example.yml` to `settings.yml`
- Get [Twitch](https://dev.twitch.tv/console/apps/create) and [Twitter](https://developer.twitter.com/en/portal/dashboard) credentials and add them to the settings
  - For Twitter, you will need the access token and secrets with Read and Write permissions
- Set a polling interval
- On the Streamers list, follow the provided examples and add the streamers you want to check.
- When you are done, run `./twitch_alert_bot`

## Project Environments

### Virtualenv

- Create a virtual environment on the project directory (`virtualenv project_path`)
- Run `source bin/activate`
- Run `python setup.py install`

### Nix

- Run `nix-shell`
- If you want to build the application (not recommended), run `nix-build`

## Thanks to
- [Roger Zanoni](https://gitlab.com/roger.zanoni)

