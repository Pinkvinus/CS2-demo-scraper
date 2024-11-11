{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.selenium
    pkgs.chromedriver
    pkgs.python3Packages.virtualenv
  ];

  # Create and activate a virtualenv, then install selenium-stealth
  shellHook = ''
    if [ ! -d ".venv" ]; then
      virtualenv .venv
    fi
    source .venv/bin/activate
    pip install selenium-stealth
  '';
}