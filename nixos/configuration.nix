{ _config, _pkgs, ... }:
let
  vars = import ../vars.nix;

  face-detect-app = import ../nix/face-detect-app.nix { };

in
{
  imports = [ ./cachix.nix ];
  config = {
    security.acme.email = "jelle@pingiun.com";
    security.acme.acceptTerms = true;

    nix = {
      gc.automatic = true;
    };

    security.sudo.wheelNeedsPassword = false;
    users.mutableUsers = false;
    users.users.jelle = {
      isNormalUser = true;
      description = "Jelle Besseling";
      extraGroups = [ "wheel" ];
      openssh.authorizedKeys.keys = [
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICunYiTe1MOJsGC5OBn69bewMBS5bCCE1WayvM4DZLwE jelle@Jelles-Macbook-Pro.local"
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID+/7ktPyg4lYL0b6j3KQqfVE6rGLs5hNK3Q175th8cq jelle@foon"
      ];
    };
    users.users.sebas = {
      isNormalUser = true;
      description = "Sébastiaan Versteeg";
      extraGroups = [ "wheel" ];
      openssh.authorizedKeys.keys = [
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHphCugRKsPI/YT53lO/7i7z6yP48kPjNltq5VFu/PbN Sebastiaan@Jupiter.local"
      ];
    };
    users.users.deploy = {
      isNormalUser = true;
      description = "Deploy user";
      extraGroups = [ "wheel" ];
      openssh.authorizedKeys.keys = [
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJIk0EpjiVLQrL4gHAUl7YrvQZrjbycb+BIYyVp7A81O deploykey"
      ];
    };

    environment.systemPackages = [ face-detect-app.sudo-face-detect-app-manage ];
    # Make face-detect-app user
    users.users.${vars.user} = { };

    systemd.services = {
      face-detect-app = {
        after = [ "networkig.target" "postgresql.service" ];
        partOf = [ "face-detect-app-env.service" ];
        wantedBy = [ "multi-user.target" ];

        serviceConfig = {
          User = vars.user;
          KillSignal = "SIGQUIT";
        };

        script = ''
          if [ -f /run/face-detect-app.env ]; then
            source /run/face-detect-app.env
          else
            export DJANGO_SECRET=$(hostid)
          fi

          export ALLOWED_HOSTS="${vars.domain}"
          export STATIC_ROOT=${face-detect-app.face-detect-app-static}
          ${face-detect-app.face-detect-app-gunicorn}/bin/face-detect-app-gunicorn --bind 127.0.0.1:${toString vars.port}
        '';
      };
    };

    services = {
      nginx = {
        enable = true;

        recommendedGzipSettings = true;

        recommendedOptimisation = true;

        recommendedTlsSettings = true;

        enableReload = true;

        virtualHosts = {
          "${vars.domain}" = {
            enableACME = true;
            forceSSL = true;
            locations."/".extraConfig = ''
              proxy_pass http://127.0.0.1:${toString vars.port};
            '';
            locations."/static/".alias = "${face-detect-app.face-detect-app-static}/";
          };
        };
      };
      postgresql = {
        enable = true;
        ensureDatabases = [ vars.user ];
        ensureUsers = [
          {
            name = vars.user;
            ensurePermissions = {
              "DATABASE ${vars.user}" = "ALL PRIVILEGES";
            };
          }
        ];
      };
    };

    networking.firewall.allowedTCPPorts = [ 22 80 443 ];
  };
}
