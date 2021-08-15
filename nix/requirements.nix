with import ./pkgs.nix {};

rec {
    python = python38;

    pythonPackages = python38Packages;

    base = with pythonPackages; [
      python-twitter
      pytwitchapi
      pyyaml
    ];

    tests = [ pythonPackages.pytest ];

    dev = [ pythonPackages.pycodestyle ];
}
