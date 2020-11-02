{ project ? import ./default.nix { }
}:

# This is used when running nix-shell. It uses the definitions in default.nix,
# so look there for info
project.pkgs.mkShell {
  buildInputs = builtins.attrValues project.devTools;
  shellHook = ''
    ${project.ci.pre-commit-check.shellHook}
  '';
}
