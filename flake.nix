{
  description = "Alerts when a streamer is live";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-21.11";
    poetry2nix.url = "github:nix-community/poetry2nix";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, poetry2nix, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          poetry2nix.overlay
        ];
      };

      customOverrides = self: super: {
        python-twitter = super.python-twitter.overrideAttrs(old: {
          buildInputs = old.buildInputs ++ [ self.pytest-runner ];
        });
      };

      # General poetry settings
      python = pkgs.python39;
      projectDir = ./.;
      overrides = pkgs.poetry2nix.overrides.withDefaults (customOverrides);

      env = pkgs.poetry2nix.mkPoetryEnv {
        inherit overrides python projectDir;
      };

      # Other project settings
      extraPkgs = with pkgs; [ gnumake poetry ];

    in {
      devShell = pkgs.mkShell {
        buildInputs = [ env ] ++ extraPkgs;
      };

      defaultPackage = pkgs.poetry2nix.mkPoetryApplication {
        inherit overrides projectDir;
      };
    }) //
    {
      hmModule = import ./nix/modules/home-manager;
    };
}
