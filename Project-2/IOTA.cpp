// the core of the program is inspired by the following sources:
// https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
// https://www.geeksforgeeks.org/udp-server-client-implementation-c/
// https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Stubs/cpp
// https://learn.microsoft.com/en-us/windows/win32/api/winsock/
#include "IOTA.h"

//UDPServer udp_server;
//TCPServer tcp_server;

Server *server;

void sigint_handler(int) {
	delete server;
	exit(EXIT_SUCCESS);
}

int main (int argc, char **argv) {
	uint16_t port_number = 0;
    const char *server_hostname = nullptr;
	static struct sockaddr_in server_address;
	std::string protocol;

	std::signal(SIGINT, sigint_handler);

	try {
        check_args(argc, argv, &server_hostname, &port_number, &protocol, "ipkcpd");
    } catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		return 1;
	}

	// Initialize the server
	try {
		if (protocol == "udp") {
			server = new UDPServer();
			server->SetUpServer(server_hostname, port_number);
			server_address = server->server_address;
		}
		if (protocol == "tcp") {
			server = new TCPServer();
			server->SetUpServer(server_hostname, port_number);
			server_address = server->server_address;
		}
	} catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		delete server;
		return 1;
	}

    std::cout << "INFO: Server socket: " << inet_ntoa(server_address.sin_addr) <<" : " <<
		ntohs(server_address.sin_port) << std::endl;

	std::cout << "INFO: Protocol: " << protocol << std::endl;

	try {
		if (protocol == "tcp")
			server->communicate();
		if (protocol == "udp")
			server->communicate();
	} catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		delete server;
		return 1;
	}
    return 0;
}
