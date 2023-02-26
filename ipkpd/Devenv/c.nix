{
  mkShell,
  pkg-config,
  libpcap,
  libnet,
  valgrind,
  gdb,
}:
mkShell {
  buildInputs = [
    libpcap
    libnet
  ];

  packages = [
    valgrind
    gdb
  ];
}
