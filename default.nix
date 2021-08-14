# Currently using https://github.com/WolfangAukang/nixpkgs/tree/pyTwitchAPI-init
# Waiting for PR-133871 at NixOS/nixpkgs to be merged, so <nixpkgs> can be used
{ pkgs ? import /home/bjorn/Projektujo/Aliaj/nixpkgs/. {} }:
pkgs.callPackage ./derivation.nix {}
