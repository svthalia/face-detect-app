{ sources ? import ./sources.nix
}:
let
  # We import the nixpkgs and poetry2nix dependency from sources.nix which in turn
  # uses sources.json. These are managed by the niv command.

  # default nixpkgs
  pkgs = import sources.nixpkgs { };

  # gitignore.nix
  gitignoreSource = (import sources."gitignore.nix" { inherit (pkgs) lib; }).gitignoreSource;
  poetry2nix = (import sources."poetry2nix" { inherit pkgs; poetry = pkgs.poetry; });

  src = gitignoreSource ./..;

  vars = import ../vars.nix;

  # We need to override some things because poetry2nix doesn't have the required overrides
  # for Pillow. For dlib and numpy we use the packages provided by nixpkgs, because it was
  # too hard to get the fixes, and the exact version shouldn't be super important.
  face-detect-app-env = poetry2nix.mkPoetryEnv {
    projectDir = src;
    overrides = poetry2nix.overrides.withDefaults (
      self: super: {
        pillow = super.pillow.overridePythonAttrs (
          old: with pkgs; {
            preConfigure =
              let
                libinclude' = pkg: ''"${pkg.out}/lib", "${pkg.out}/include"'';
                libinclude = pkg: ''"${pkg.out}/lib", "${pkg.dev}/include"'';
              in
              ''
                sed -i "setup.py" \
                    -e 's|^FREETYPE_ROOT =.*$|FREETYPE_ROOT = ${libinclude freetype}|g ;
                        s|^JPEG_ROOT =.*$|JPEG_ROOT = ${libinclude libjpeg}|g ;
                        s|^JPEG2K_ROOT =.*$|JPEG2K_ROOT = ${libinclude openjpeg}|g ;
                        s|^IMAGEQUANT_ROOT =.*$|IMAGEQUANT_ROOT = ${libinclude' libimagequant}|g ;
                        s|^ZLIB_ROOT =.*$|ZLIB_ROOT = ${libinclude zlib}|g ;
                        s|^LCMS_ROOT =.*$|LCMS_ROOT = ${libinclude lcms2}|g ;
                        s|^TIFF_ROOT =.*$|TIFF_ROOT = ${libinclude libtiff}|g ;
                        s|^TCL_ROOT=.*$|TCL_ROOT = ${libinclude' tcl}|g ;
                        s|self\.disable_platform_guessing = None|self.disable_platform_guessing = True|g ;'
                export LDFLAGS="-L${libwebp}/lib"
                export CFLAGS="-I${libwebp}/include"
              ''
              # Remove impurities
              + stdenv.lib.optionalString stdenv.isDarwin ''
                substituteInPlace setup.py \
                  --replace '"/Library/Frameworks",' "" \
                  --replace '"/System/Library/Frameworks"' ""
              '';
            nativeBuildInputs = [ pkgconfig ] ++ old.nativeBuildInputs;
            propagatedBuildInputs = [ self.olefile self.magic ];
            buildInputs = [ freetype libjpeg openjpeg zlib libtiff libwebp tcl lcms2 ] ++ old.buildInputs;
          }
        );
        dlib = pkgs.python38Packages.dlib;
        numpy = pkgs.python38Packages.numpy;
      }
    );
  };

  # The location of the manage.py script
  manage-py = "${src}/manage.py";

  # Make a manage.py wrapper which sets the right environment variables
  face-detect-app-manage = pkgs.writeScriptBin "face-detect-app-manage" ''
    set -e
    test -f /run/face-detect-app.env && source /run/face-detect-app.env
    export ENVIRONMENT=NIX
    ${face-detect-app-env}/bin/python ${manage-py} $@
  '';

  # Run the manage.py wrapper with sudo to make sure the database connection works
  sudo-face-detect-app-manage = pkgs.writeScriptBin "face-detect-app-manage" ''
    sudo -u ${vars.user} ${face-detect-app-manage}/bin/face-detect-app-manage $@
  '';

  # Generate the static files
  face-detect-app-static = pkgs.runCommand "face-detect-app-static" { } ''
    export STATIC_ROOT=$out
    export DJANGO_SECRET=a
    export ENVIRONMENT=NIX

    ${face-detect-app-env}/bin/python ${manage-py} collectstatic
    ${face-detect-app-env}/bin/python ${manage-py} compress --force
  '';

  # The location of our application
  wsgi = "app.wsgi:application";

  # A command that wraps the gunicorn with some things. It also runs migrations
  # before starting.
  face-detect-app-gunicorn = pkgs.writeScriptBin "face-detect-app-gunicorn" ''
    export ENVIRONMENT=NIX
    ${face-detect-app-env}/bin/python ${manage-py} migrate
    ${face-detect-app-env}/bin/gunicorn ${wsgi} \
            --pythonpath ${src} $@
  '';
in
{
  inherit face-detect-app-env sudo-face-detect-app-manage face-detect-app-static face-detect-app-gunicorn;
}
