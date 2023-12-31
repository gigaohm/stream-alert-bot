{
  description = "Alerts when a streamer is live";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, poetry2nix, utils }:
    let
      # General project settings
      inherit (utils.lib) eachDefaultSystem mkApp;
      inherit (nixpkgs.lib) composeExtensions;
      name = "stream-alert-bot";
      projectDir = ./.;

    in
    (eachDefaultSystem (system:
      let
        overlays = [
          poetry2nix.overlay
          (composeExtensions poetry2nix.overlay (final: prev: {
             ${name} = final.poetry2nix.mkPoetryApplication { inherit projectDir; };
          }))
        ];
        pkgs = import nixpkgs { inherit system overlays; };
        inherit (pkgs) mkShell black gnumake mypy poetry python3;
        inherit (pkgs.poetry2nix) mkPoetryEnv;

        devEnv = mkPoetryEnv {
          inherit projectDir;
          python = python3;
        };

      in rec {
        packages.${name} = pkgs.${name};
        packages.default = packages.${name};

        apps = {
          ${name} = mkApp {
            drv = packages.${name};
            exePath = "/bin/stream_alert_bot";
          };
          "make" = {
            type = "app";
            program = "${gnumake}/bin/make";
          };
          "format-code" = {
            type = "app";
            program = "${black}/bin/black";
          };
          "scan" = {
            type = "app";
            program = "${mypy}/bin/mypy";
          };
        };
        apps.default = apps.${name};

        devShells.default = mkShell {
          inputsFrom = [ devEnv poetry ];
          buildInputs = [ poetry ];
        };
      }
    )) //
    {
      hmModule = import ./nix/modules/home-manager;
    };
}
