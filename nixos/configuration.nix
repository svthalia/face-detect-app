{ _config, pkgs, ... }:
let
  vars = import ../vars.nix;

  face-detect-app = import ../nix/face-detect-app.nix { };

in
{
  config = {
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
            export ALLOWED_HOSTS="${vars.domain}"
            export DJANGO_SECRET=$(hostid)
          fi

          export STATIC_ROOT=${face-detect-app.face-detect-app-static}
          ${face-detect-app.face-detect-app-gunicorn}/bin/face-detect-app-gunicorn --bind 127.0.0.1:${toString vars.port}
        '';
      };
      self-deploy =
        let
          workingDirectory = "/var/lib/self-deploy";

          owner = "svthalia";

          repository = "face-detect-app";

          repositoryDirectory = "${workingDirectory}/${repository}";

          build = "${repositoryDirectory}/result";

        in
        {
          wantedBy = [ "multi-user.target" ];

          after = [ "network-online.target" ];

          path = [ pkgs.gnutar pkgs.gzip ];

          serviceConfig.X-RestartIfChanged = false;

          script = ''
            if [ ! -e ${workingDirectory} ]; then
              ${pkgs.coreutils}/bin/mkdir --parents ${workingDirectory}
            fi
            if [ ! -e ${repositoryDirectory} ]; then
              cd ${workingDirectory}
              ${pkgs.git}/bin/git clone https://github.com/${owner}/${repository}.git
            fi
            cd ${repositoryDirectory}
            ${pkgs.git}/bin/git fetch https://github.com/${owner}/${repository}.git master
            ${pkgs.git}/bin/git checkout FETCH_HEAD
            ${pkgs.nix}/bin/nix-build --attr machine ${repositoryDirectory}
            ${pkgs.nix}/bin/nix-env --profile /nix/var/nix/profiles/system --set ${build}
            ${pkgs.git}/bin/git gc --prune=all
            ${build}/bin/switch-to-configuration switch
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
            # enableACME = true;
            # forceSSL = true;
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
