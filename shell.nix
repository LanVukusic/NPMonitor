{ pkgs ? import <nixpkgs> {}}:
let
  my-python-packages = p: with p; [
      # jupyter
      # ipykernel
      # ipython
      numpy
      matplotlib
      pandas
      requests
      beautifulsoup4
      tqdm
      scikit-learn

      # linter, formatter, etc.
      bandit
      black
    ];
    my-python = pkgs.python3.withPackages my-python-packages;
in
pkgs.mkShell {
  name="RIS 2023 tekmovanje";
  
  
  buildInputs = [
    pkgs.cudatoolkit
    pkgs.python3
    my-python
  ];
  shellHook = ''
    echo -e " ❄️ NMPonitor"
  '';
} 