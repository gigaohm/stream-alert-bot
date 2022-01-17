with import ./nix/pkgs.nix {};
let
  requirements = (import ./nix/requirements.nix);
in
requirements.pythonPackages.buildPythonApplication {
  pname = "stream-alert-bot";
  version = "0.2";
  format = "pyproject";

  src = lib.cleanSource ./.;

  nativeBuildInputs = with pkgs.python39Packages; [ poetry-core ];

  propagatedBuildInputs = requirements.base;

}
