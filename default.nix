{ pkgs ? import ./nix/pkgs.nix {}}:

let
  inherit (pkgs) lib python39Packages;
  inherit (python39Packages) poetry-core;
  requirements = (import ./nix/requirements.nix {});

in requirements.pythonPackages.buildPythonApplication {
  pname = "stream-alert-bot";
  version = "0.2.2";
  format = "pyproject";

  src = lib.cleanSource ./.;

  nativeBuildInputs = [ poetry-core ];

  propagatedBuildInputs = requirements.base;

}
