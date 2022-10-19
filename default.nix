{ pkgs ? import ./nix/pkgs.nix {}}:

let
  inherit (pkgs) lib;
  requirements = (import ./nix/requirements.nix { refpkgs = pkgs; });

in requirements.buildMethod {
  pname = "stream-alert-bot";
  version = "0.3.1";
  format = "pyproject";

  src = lib.cleanSource ./.;

  nativeBuildInputs = requirements.nativeBuildInputs;

  propagatedBuildInputs = requirements.base;

}
