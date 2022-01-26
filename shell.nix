with import ./nix/pkgs.nix { };
let
  requirements = import ./nix/requirements.nix;

  python-trovo = requirements.pythonPackages.buildPythonPackage rec {
    pname = "python-trovo";
    version = "0.1.3";

    src = requirements.pythonPackages.fetchPypi {
      inherit pname version;
      sha256 = "sha256-iKG6UGc3pUjN00kxkBRL0ZbzB8OCbWOi1kb+YpLzOfE=";
    };

    propagatedBuildInputs = with requirements.pythonPackages; [ requests ];
  };
  pythonEnvironment = requirements.python.buildEnv.override {
    extraLibs = requirements.base ++ requirements.tests ++ requirements.dev ++ [python-trovo];
  };
  extraPkgs = [ gnumake poetry ];
in
mkShell {
    buildInputs = [ pythonEnvironment ] ++ extraPkgs;
}
