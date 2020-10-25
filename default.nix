{ sources ? import ./nix/sources.nix
}:
let
  # default nixpkgs
  pkgs = import sources.nixpkgs { };

  pre-commit-hooks = (import sources."pre-commit-hooks.nix");

  gitignoreSource = (import sources."gitignore.nix" { inherit (pkgs) lib; }).gitignoreSource;

  src = gitignoreSource ./.;

  face-detect-app = import ./nix/face-detect-app.nix { };

  vm = (
    import "${sources.nixpkgs}/nixos" {
      configuration = {
        imports = [ ./nixos/configuration.nix ];

        networking.hostName = "face-detect-app";

        users = {
          mutableUsers = false;

          users.root.password = "";
        };

        virtualisation = {
          cores = 2;

          memorySize = "4096";
        };
      };
      system = "x86_64-linux";
    }
  ).vm;

  # _machine = (
  #   import "${sources.nixpkgs}/nixos" {
  #     configuration = {
  #       imports = [ ./nixos/configuration.nix ];

  #       networking.hostName = "face-detect-app";
  #     };
  #     system = "x86_64-linux";
  #   }
  # ).system;
in
{
  inherit pkgs src;

  # provided by shell.nix
  devTools = {
    inherit (pkgs) niv;
    inherit (pre-commit-hooks) pre-commit;
    inherit (pre-commit-hooks) nixpkgs-fmt;
    inherit (face-detect-app) face-detect-app-env;
  };

  # to be built by github actions
  ci = {
    pre-commit-check = pre-commit-hooks.run {
      inherit src;
      hooks = {
        shellcheck.enable = true;
        nixpkgs-fmt.enable = true;
        nix-linter.enable = true;
      };
      # generated files
      excludes = [ "^nix/sources\.nix$" ];
    };
    inherit src vm;
    inherit (face-detect-app) face-detect-app-env;
  };
}
