{
  sbclWithPackages,
  mkShell,
  stdenvNoCC,
}: let
  sbcl = sbclWithPackages (p: [
    p.slynk
    p.alexandria
    p.clingon
    p.iterate
    p.lisp-unit2
    p.str
    p.usocket
  ]);
in
  mkShell.override {stdenv = stdenvNoCC;} {
    propagatedBuildInputs = [sbcl];
  }
