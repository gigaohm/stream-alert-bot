{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "twitch-alert-bot";
  version = "0.1";
  src = ./.;

  propagatedBuildInputs = [ python-twitter pyyaml pyTwitchAPI ];
  doChecks = false;
}
