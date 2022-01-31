with import ./pkgs.nix {};

rec {
    python = python39;

    pythonPackages = python39Packages;

    base = with pythonPackages; [
      python-twitter
      pytwitchapi
      pyyaml
      requests
    ];

    tests = [ pythonPackages.pytest ];

    dev = with pythonPackages; [
      black
      mypy
      types-requests
    ];
}
