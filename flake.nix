{
  description = "Alerts when a streamer is live";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    poetry2nix.url = "github:wolfangaukang/poetry2nix/overrides";
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
                 inherit projectDir;
               };
            }))
          ];
        };

        # Needed to build python-twitter 
        #customOverrides = self: super: {
        #  python-twitter = super.python-twitter.overrideAttrs(old: {
        #    buildInputs = old.buildInputs ++ [ self.pytest-runner ];
        #  });
        #  python-trovo = super.python-trovo.overrideAttrs(old: {
        #    buildInputs = old.buildInputs ++ [ self.poetry ];
        #  });
        #};
        #overrides = pkgs.poetry2nix.overrides.withDefaults (customOverrides);

        # Other project settings
        extraPkgs = with pkgs; [ gnumake poetry ];

      in rec {
        packages.${name} = pkgs.${name};
        packages.default = packages.${name};

        apps.${name} = utils.lib.mkApp {
          drv = packages.${name};
          exePath = "/bin/stream_alert_bot";
        };
        apps.default = apps.${name};

        devShells.default = pkgs.mkShell {
          inputsFrom = [ apps.default ];
          buildInputs = extraPkgs;
        };
      }
    )) //
    {
      hmModule = import ./nix/modules/home-manager;
    };
}
