with import ./nix/pkgs.nix {};
let
  requirements = (import ./nix/requirements.nix);
in
requirements.pythonPackages.buildPythonApplication {
  pname = "twitch-alert-bot";
  version = "0.1.0";
  format = "pyproject";

  src = lib.cleanSource ./.;

  nativeBuildInputs = with pkgs.python39Packages; [ poetry-core ];

  propagatedBuildInputs = requirements.base;

}
