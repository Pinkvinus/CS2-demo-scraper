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
    ]))
  ];
}
