{
  lib,
  mkShell,
  stdenvNoCC,
  dotnetCorePackages,
  libpcap,
}: let
  dotnet = dotnetCorePackages.sdk_6_0;
in
  mkShell.override
  {stdenv = stdenvNoCC;}
  rec {
    packages = [dotnet];
    buildInputs = [libpcap];
    shellHook = ''
      export DOTNET_ROOT=${dotnet}
      export LD_LIBRARY_PATH="${dotnet.icu}/lib:${lib.makeLibraryPath buildInputs}"
      unset DOTNET_SKIP_FIRST_TIME_EXPERIENCE
    '';
  }
