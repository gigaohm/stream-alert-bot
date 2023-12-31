# Stream Alert Bot

[![status-badge](https://ci.codeberg.org/api/badges/wolfangaukang/stream-alert-bot/status.svg)](https://ci.codeberg.org/wolfangaukang/stream-alert-bot)

This bot will indicate which streamers are live. It supports the following consumers (streaming platforms) and publishers (notification platforms):
- Consumers
  - [Trovo](https://trovo.live)
  - [Twitch](https://twitch.tv)
- Publishers
  - [Twitter](https://twitter.com)

## How To Use

```
usage: stream_alert_bot [-h] [--debug] [--publisher {twitter} [{twitter} ...]] settings_file_path {trovo,twitch}

Alerts when a streamer is live

required arguments:
  settings_file_path    Path to the settings file
  {trovo,twitch}        Consumer to use. Must be one

optional arguments:
  -h, --help            show this help message and exit
  --debug, -d           Starts debug mode
  --publisher {twitter} [{twitter} ...], -p {twitter} [{twitter} ...]
                        Publishers to use. Can be more than 1
```

## How To Build

You have two ways to do it:
- The project uses Poetry. Simply run `poetry build`
- If using Nix, you can build it the old way (`nix-build`) or through flakes (`nix build`)

## How To Contribute

Again, two ways to do it:
- Create an environment with `poetry shell`
- If using Nix, you can run `nix-shell` or `nix develop` if using flakes

In any of both cases, you can create a quick file at the root of the repo with the following content:
```python
#!/usr/bin/env python3

import sys

from sab.__main__ import main

if __name__ == "__main__":
    sys.exit(main())

```

Just throw the PR so I can check it :)

### Issues using `nix build`?

If there is a Python dependency not being built successfully, you should try checking the `nix-community/poetry2nix` repository
and see any related issues. For example, when you see something like `ModuleNotFoundError: No module named 'pytest-runner'` when
building `python-twitter`, you can do this to the `flake.nix` file, on a `let` section of the outputs:

```nix
  customOverrides = self: super: {
    python-twitter = super.python-twitter.overrideAttrs(old: {
      buildInputs = old.buildInputs ++ [ self.pytest-runner ];
    });
  };
  overrides = pkgs.poetry2nix.overrides.withDefaults (customOverrides);

  pkgs = import nixpkgs {
    inherit system;
    overlays = [
      poetry2nix.overlay
      (nixpkgs.lib.composeExtensions poetry2nix.overlay (final: prev: {
         ${name} = final.poetry2nix.mkPoetryApplication {
           inherit overrides projectDir;
         };
      }))
    ];
  };

```

## Steps

- On the `etc/` directory, there is the `settings-example.yml` file. It contains the whole configuration for the bot.
  - Adapt it to your needs. The idea is:
    - Must have the `credentials`, `streamers` and `message` settings.
    - Must have at least one consumer and one publisher credentials.
- Get the corresponding API keys:
  - [Trovo](https://developer.trovo.live)
  - [Twitch](https://dev.twitch.tv/console/apps/create)
  - [Twitter](https://developer.twitter.com/en/portal/dashboard) 
    - For Twitter, you will need the access token and secrets with Read and Write permissions
- On the Streamers list, follow the provided examples and add the streamers you want to check.
- When you are done, run `./stream_alert_bot path_to_settings_file consumer`
  - If you want to see the application in debug mode, provide the `--debug` flag.
  - As there is only one publisher supported, it is the default value.
  - For more information, add the `-h|--help` flag.

## Thanks to
- [Roger Zanoni](https://gitlab.com/roger.zanoni)

