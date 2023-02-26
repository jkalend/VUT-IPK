FROM ubuntu:22.04 as server

RUN apt update && \
    apt install -y gcc make && \
    apt install -y g++

WORKDIR /ipk/project1

RUN mkdir -p /nix/store/9xfad3b5z4y00mzmk2wnn4900q0qmxns-glibc-2.35-224/lib
RUN mkdir -p /ipk/project1/run /ipk/project1/src

RUN cp /lib64/ld-linux-x86-64.so.2 /nix/store/9xfad3b5z4y00mzmk2wnn4900q0qmxns-glibc-2.35-224/lib/ld-linux-x86-64.so.2

COPY bin/ipkpd ./
COPY ./Devenv /ipk/project1/Devenv
COPY ./Stubs /ipk/project1/Stubs
COPY start.sh ./

RUN chmod -R 777 ./ipkpd ./start.sh

ENTRYPOINT ["bash", "/ipk/project1/start.sh"]
