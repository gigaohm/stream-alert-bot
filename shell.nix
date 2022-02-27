{ pkgs ? import ./nix/pkgs.nix { }}:

let
  inherit (pkgs) gnumake poetry mkShell;
  requirements = (import ./nix/requirements.nix { refpkgs = pkgs; });

  pythonEnvironment = requirements.python.buildEnv.override {
    extraLibs = requirements.base ++ requirements.tests ++ requirements.dev;
  };
  extraPkgs = [ gnumake poetry ];
in
mkShell {
    buildInputs = [ pythonEnvironment ] ++ extraPkgs;
}
