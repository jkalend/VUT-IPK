#include "ipkcpd.h"

/// Global variable to propagate to signal handler
std::string protocol;

struct sockaddr_in * get_adress(const char *hostname) {
	struct addrinfo hints = {AI_PASSIVE, AF_INET, SOCK_DGRAM, 0, 0, nullptr, nullptr, nullptr};

	ssocket::serverptr = nullptr;

	if (getaddrinfo(hostname, nullptr, &hints, &ssocket::serverptr) != 0)
		throw std::runtime_error("ERR: getaddrinfo failed");

	return (struct sockaddr_in*)(ssocket::serverptr->ai_addr);
}

int tcp_socket(struct sockaddr_in server_address) {
	int master_socket;
	if ((master_socket = socket(AF_INET, SOCK_STREAM, 0)) <= 0)
		throw std::runtime_error("ERROR: socket creation failed");

	if (int a = 1; setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, (char *)&a, sizeof(int)) < 0)
		throw std::runtime_error("ERROR: socket options setting failed");

	if (bind(master_socket, (struct sockaddr *) &server_address, sizeof(server_address)) < 0)
		throw std::runtime_error("ERROR: socket binding failed");

	if (listen(master_socket, 3) < 0)
		throw std::runtime_error("ERROR: socket listening failed");

	return master_socket;
}

int udp_socket(struct sockaddr_in server_address) {
	int master_socket;
	if ((master_socket = socket(AF_INET, SOCK_DGRAM, 0)) <= 0)
		throw std::runtime_error("ERROR: socket creation failed");

	if (int a = 1; setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, (char *)&a, sizeof(int)) < 0)
		throw std::runtime_error("ERROR: socket options setting failed");

	if (bind(master_socket, (struct sockaddr *) &server_address, sizeof(server_address)) < 0)
		throw std::runtime_error("ERROR: socket binding failed");
	return master_socket;
}


void sigint_handler(int) {
	std::cout << "Exiting" << std::endl;
	std::cout << "Bye..." << std::endl;
	freeaddrinfo(ssocket::serverptr);
	close(ssocket::master_socket);
	exit(EXIT_SUCCESS);
}

int main (int argc, char **argv) {
	uint16_t port_number = 0;
	const char *server_hostname = nullptr;
	static struct sockaddr_in server_address;

	std::signal(SIGINT, sigint_handler);

	try {
		check_args(argc, argv, &server_hostname, &port_number, &protocol, "ipkcpd");
		server_address = *get_adress(server_hostname);
		server_address.sin_port = htons(port_number);
	} catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		return 1;
	}

	std::cout << "INFO: Server socket: " << inet_ntoa(server_address.sin_addr) << " : " <<
	          ntohs(server_address.sin_port) << std::endl;

	std::cout << "INFO: Protocol: " << protocol << std::endl;

	try {
		if (protocol == "tcp") {
			ssocket::master_socket = tcp_socket(server_address);
		} else {
			ssocket::master_socket = udp_socket(server_address);
		}
	} catch (std::runtime_error &e) {
		std::cout << e.what() << std::endl;
		freeaddrinfo(ssocket::serverptr);
		return 1;
	}
}
