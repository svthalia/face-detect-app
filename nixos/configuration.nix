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
      trustedUsers = [ "root" "deploy" ];
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
      face-detect-app-dir = {
        wantedBy = [ "multi-user.target" ];
        script = ''
          mkdir --parents ${vars.rootDir}/media
          chown --recursive ${vars.user} ${vars.rootDir}
        '';
      };
      face-detect-app = {
        after = [ "networking.target" "postgresql.service" "face-detect-app-dir.service" ];
        partOf = [ "face-detect-app-env.service" ];
        wantedBy = [ "multi-user.target" ];

        serviceConfig = {
          User = vars.user;
          KillSignal = "SIGQUIT";
        };

        script = ''
          if [ -f ${vars.envFile} ]; then
            source ${vars.envFile}
          else
            echo "Make sure to set a secret key!" >&2
            export DJANGO_SECRET=$(hostid)
          fi

          export DJANGO_ALLOWED_HOSTS="${vars.domain}"
          export STATIC_ROOT=${face-detect-app.face-detect-app-static}
          export MEDIA_ROOT=${vars.rootDir}/media
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
            locations."/" = {
              proxyPass = "http://127.0.0.1:${toString vars.port}";
              extraConfig = ''
                proxy_set_header Host            $host;
                proxy_set_header X-Forwarded-For $remote_addr;
              '';
            };
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
