let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.wget
    (pkgs.python3.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.cloudscraper
      python-pkgs.requests
      python-pkgs.requests_toolbelt
      python-pkgs.beautifulsoup4
      python-pkgs.psycopg2
    ]))
  ];

  shellHook = ''
    export PIP_TARGET="$PWD/.python-packages"
    export PYTHONPATH="$PIP_TARGET:$PYTHONPATH"
    mkdir -p $PIP_TARGET
    pip install --no-cache-dir csgo
  '';
}
