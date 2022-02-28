{
  description = "Alerts when a streamer is live";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-21.11";
    poetry2nix.url = "github:nix-community/poetry2nix";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, poetry2nix, utils }:
    let
      # General project settings
      name = "stream-alert-bot";
      projectDir = ./.;

    in
    (utils.lib.eachDefaultSystem (system:
      let
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

        # Needed to build python-twitter 
        customOverrides = self: super: {
          python-twitter = super.python-twitter.overrideAttrs(old: {
            buildInputs = old.buildInputs ++ [ self.pytest-runner ];
          });
        };
        overrides = pkgs.poetry2nix.overrides.withDefaults (customOverrides);

        # Other project settings
        extraPkgs = with pkgs; [ gnumake poetry ];

      in rec {
        packages.${name} = pkgs.${name};
        defaultPackage = packages.${name};

        apps.${name} = utils.lib.mkApp {
          drv = packages.${name};
          exePath = "/bin/stream_alert_bot";
        };
        defaultApp = apps.${name};

        devShell = pkgs.mkShell {
          inputsFrom = [ defaultPackage ];
          buildInputs = extraPkgs;
        };
      }
    )) //
    {
      hmModule = import ./nix/modules/home-manager;
    };
}
