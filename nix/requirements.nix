{ refpkgs ? import ./pkgs.nix {}}:

let
  inherit (refpkgs) python39 python39Packages;
  inherit (python39Packages) black buildPythonPackage fetchPypi python-twitter pytest pytwitchapi pyyaml requests;
  python-trovo = buildPythonPackage rec {
    pname = "python-trovo";
    version = "0.1.4";

    src = fetchPypi {
      inherit pname version;
      sha256 = "sha256-N66Lrda/QvJIPF2FEHboiN2x22y5leXcXGhvlOJQpGU=";
    };

    propagatedBuildInputs = [ requests ];
  };
in rec {
    python = python39;

    pythonPackages = python39Packages;

    base = [
      python-trovo
      python-twitter
      pytwitchapi
      pyyaml
      requests
    ];

    tests = [ pytest ];

    dev = [ black ];
}
