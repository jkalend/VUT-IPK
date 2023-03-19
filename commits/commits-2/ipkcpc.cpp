#include "ipkcpc.h"


// global variable required for proper interruption of the program
std::string protocol;


struct sockaddr_in * get_adress(const char *hostname) {
	struct addrinfo hints = {AI_PASSIVE, AF_INET, SOCK_DGRAM, 0, 0, nullptr, nullptr, nullptr};

	csocket::serverptr = nullptr;

	if (getaddrinfo(hostname, nullptr, &hints, &csocket::serverptr) != 0)
		throw std::runtime_error("ERROR: getaddrinfo failed");

	return (struct sockaddr_in*)(csocket::serverptr->ai_addr);
}

int tcp_socket(struct sockaddr_in server_address) {
	int client_socket;
	if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) <= 0)
		throw std::runtime_error("ERROR: socket creation failed");

	if (connect(client_socket, (const struct sockaddr *) &server_address, sizeof(server_address)) != 0)
		throw std::runtime_error("ERROR: socket connection failed");
	return client_socket;
}

int udp_socket() {
	int client_socket;
	if ((client_socket = socket(AF_INET, SOCK_DGRAM, 0)) <= 0)
		throw std::runtime_error("ERROR: socket creation failed");
	return client_socket;
}


void sigint_handler(int) {
	std::cout << "Exiting" << std::endl;
	std::cout << "Bye..." << std::endl;
	if (protocol == "tcp") {
		send(csocket::client_socket, "BYE", 3, 0);
	}
	freeaddrinfo(csocket::serverptr);
	close(csocket::client_socket);
	exit(EXIT_SUCCESS);
}

int main (int argc, char **argv) {
	uint16_t port_number = 0;
	const char *server_hostname = nullptr;
	struct sockaddr_in server_address = {0, 0, 0, 0};

	std::signal(SIGINT, sigint_handler);

	// Checks the arguments and gets the server address
	try {
		check_args(argc, argv, &server_hostname, &port_number, &protocol, "ipkcpc");
		server_address = *get_adress(server_hostname);
		server_address.sin_port = htons(port_number);
	} catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		return 1;
	}

	// Creates a socket for the client
	try {
		if (protocol == "tcp") {
			csocket::client_socket = tcp_socket(server_address);
		} else {
			csocket::client_socket = udp_socket();
		}
	} catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		freeaddrinfo(csocket::serverptr);
		return 1;
	}
}
