{ refpkgs }:

let
  inherit (refpkgs) python39 python39Packages;
  inherit (python39Packages) black buildPythonApplication buildPythonPackage fetchPypi poetry-core python-twitter pytest pytwitchapi pyyaml requests;
  python-trovo = buildPythonPackage rec {
    pname = "python-trovo";
    version = "0.1.5";

    src = fetchPypi {
      inherit pname version;
      sha256 = "sha256-JUJax9nk4NqpMMrbDmQhcy22GIqPha+K4tudQ98PvlE=";
    };

    propagatedBuildInputs = [ requests ];
  };
in rec {
    python = python39;
    buildMethod = buildPythonApplication;

    nativeBuildInputs = [ poetry-core ];

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
