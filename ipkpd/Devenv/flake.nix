{
  description = "IPK2022 Developer Environment";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
  };

  outputs = {
    self,
    flake-utils,
    nixpkgs,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShells = {
        c = pkgs.callPackage ./c.nix {};
        csharp = pkgs.callPackage ./csharp.nix {};
        clisp = pkgs.callPackage ./clisp.nix {inherit (pkgs.lispPackages_new) sbclWithPackages;};
      };
    });
}
