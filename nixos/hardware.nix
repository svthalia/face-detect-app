{ sources ? import ../nix/sources.nix, ... }:
let
  pkgs = import sources.nixpkgs { };
in
{
  imports = [ "${pkgs}/nixos/modules/profiles/qemu-guest.nix" ];

  nixpkgs.system = "x86_64-linux";

  boot = {
    initrd.availableKernelModules =
      [ "ata_piix" "uhci_hcd" "ehci_pci" "sd_mod" "sr_mod" ];

    kernelParams = [ "console=ttyS0,19200n8" ];

    loader = {
      grub = {
        enable = true;

        extraConfig = ''
          serial --speed=19200 --unit=0 --word=8 --parity=no --stop=1;
          terminal_input serial;
          terminal_output serial;
        '';

        device = "nodev";

        version = 2;
      };

      timeout = 10;
    };
  };

  fileSystems."/" = { device = "/dev/sda1"; fsType = "ext4"; };

  swapDevices = [{ device = "/dev/sda2"; }];
}
