# IPK Projects
In this reopository you can find my solutions to the projects for the course IPK at FIT VUT Brno.

## 1. Project 1 - Client for IPKCP protocol
Implementation of client for IPKCP protocol. Client sends queries to server and prints the response.
The format of queries is described in the [protocol specification](https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Project%201/Protocol.md).<sup>[1]</sup>

Client connects to a server using TCP or UDP protocol, which is required by user to specify.
The server and port are also required to be specified by user. If any of the required arguments is missing, the client will print an error and exit.

The client is built utilising Makefile or CMake on UNIX or only CMake if built on Windows.

## 2. Project 2 - Server for IPKCP protocol
Implementation of server for IPKCP protocol. Server receives queries from client and responds with the result of the calculation or an error.
The format of queries is described in the [protocol specification](https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Project%201/Protocol.md).<sup>[1]</sup>

Server listens on a specified port for TCP or UDP connections, which is required by user to specify.
If any of the required arguments is missing, the server will print an error and exit.

The server is built utilising Makefile or CMake on UNIX or only CMake if built on Windows.

## License
This project is licensed under the GPL3.0 License - see the [LICENSE](LICENSE) file for details.

## Authors
* Jan Kalenda (xkalen07)

## References
[1] [Protocol specification](https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Project%201/Protocol.md)
