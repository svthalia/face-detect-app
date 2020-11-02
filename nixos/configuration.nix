{ _config, _pkgs, ... }:
let
  # Some variables are used in multiple places so we import them
  vars = import ../vars.nix;

  # Import everything related to the actual app
  face-detect-app = import ../nix/face-detect-app.nix { };

in
{
  # We use cachix.org for binary chaches. These speed up the deployment process because the
  # CI does not need to rebuild everything every time. The cachix is also included in the
  # server because it can verify the signed caches.
  imports = [ ./cachix.nix ];
  config = {
    security.acme.email = "jelle@pingiun.com";
    security.acme.acceptTerms = true;

    nix = {
      # Automatically clean up things in the Nix store which aren't used anymore by the current
      # system
      gc.automatic = true;
      # The deploy user should be able to place items in the Nix store
      trustedUsers = [ "root" "deploy" ];
    };

    # Useful for the wheel user and so we don't need to set passwords
    security.sudo.wheelNeedsPassword = false;

    # Disables the mutable way to create users, so only users we define here exist
    users.mutableUsers = false;
    users.users.jelle = {
      isNormalUser = true;
      description = "Jelle Besseling";
      # Make this user an admin
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

    # Allow the face-detect-app-manage command to be run globally. This is the sudo
    # version of the command which runs everything as vars.user so it can connect to the database
    environment.systemPackages = [ face-detect-app.sudo-face-detect-app-manage ];
    # Make face-detect-app user, the default settings for this user are fine
    users.users.${vars.user} = { };

    systemd.services = {
      # Create the root directory of the face-detect-app, this is done in a seperate unit
      # because the main unit is run as the vars.user user
      face-detect-app-dir = {
        # This is the same as `systemctl enable face-detect-app-dir.service`
        wantedBy = [ "multi-user.target" ];
        script = ''
          mkdir --parents ${vars.rootDir}/media
          chown --recursive ${vars.user} ${vars.rootDir}
        '';
      };

      face-detect-app = {
        # Must be started after postgresql and the dir creation service
        after = [ "networking.target" "postgresql.service" "face-detect-app-dir.service" ];
        wantedBy = [ "multi-user.target" ];

        serviceConfig = {
          User = vars.user;
          # The uWSGI server requires a SIGQUIT to stop
          KillSignal = "SIGQUIT";
        };

        script = ''
          if [ -f ${vars.envFile} ]; then
            source ${vars.envFile}
          else
            # Used to test things when we don't have an env file yet. We don't actually want this in production
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

        # https://nixos.org/manual/nixos/stable/options.html#opt-services.nginx.recommendedGzipSettings
        recommendedGzipSettings = true;

        recommendedOptimisation = true;

        recommendedTlsSettings = true;

        enableReload = true;

        virtualHosts = {
          # This is the same as a server {} block in nginx
          "${vars.domain}" = {
            # This requests a certificate from letsencrypt in the acme-throwback.thalia.nu.service
            enableACME = true;
            # Redirect everyone to https (required by our HSTS policy)
            forceSSL = true;
            locations."/" = {
              proxyPass = "http://127.0.0.1:${toString vars.port}";
              # Pass the host header so Django can verify it, the X-Forwarded-For
              extraConfig = ''
                proxy_set_header Host            $host;
                proxy_set_header X-Forwarded-For $remote_addr;
              '';
            };
            # Serve static files from the built static directory
            locations."/static/".alias = "${face-detect-app.face-detect-app-static}/";
          };
        };
      };
      # Run postgresql and create a database with access for our user
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

    # Open ports in the firewall, if running on EC2 make sure the security group has these open as well
    networking.firewall.allowedTCPPorts = [ 22 80 443 ];
  };
}
