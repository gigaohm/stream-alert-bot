with import ./pkgs.nix {};
let
  requirements = (import ./requirements.nix);
in
requirements.pythonPackages.buildPythonApplication {
  pname = "twitch-alert-bot";
  version = "0.1.0";
  src = lib.cleanSource ../.;

  propagatedBuildInputs = requirements.base;

  #checkInputs = requirements.tests;
  #test = "pytest";
  # Disabling tests because there aren't any
  doCheck = false;

}
