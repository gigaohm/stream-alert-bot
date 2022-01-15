with import ./nix/pkgs.nix { };
let
  requirements = import ./nix/requirements.nix;
  pythonEnvironment = requirements.python.buildEnv.override {
    extraLibs = requirements.base ++ requirements.tests ++ requirements.dev;
  };
  extraPkgs = [ gnumake poetry ];
in
mkShell {
    buildInputs = [ pythonEnvironment ] ++ extraPkgs;
}
