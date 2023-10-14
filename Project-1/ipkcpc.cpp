// the core of the program is inspired by the following sources:
// https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
// https://www.geeksforgeeks.org/udp-server-client-implementation-c/
// https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Stubs/cpp
// https://learn.microsoft.com/en-us/windows/win32/api/winsock/
#include "ipkcpc.h"
#include "utils.h"

// global variable required for proper interruption of the program
std::string protocol;


struct sockaddr_in * get_adress(const char *hostname) {
	struct addrinfo hints = {AI_PASSIVE, AF_INET, SOCK_DGRAM, 0, 0, nullptr, nullptr, nullptr};

	csocket::serverptr = nullptr;

#ifdef _WIN32
	WSADATA wsaData;
	int iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != NO_ERROR) {
        throw std::runtime_error("ERR: WSAStartup failed");
    }
#endif

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

	struct timeval tv;
	tv.tv_sec = 2;
	tv.tv_usec = 0;
	if (setsockopt(client_socket, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv) < 0)
		throw std::runtime_error("ERROR: setsockopt() failed");

	return client_socket;
}

void tcp_communicate(int client_socket) {
	char buf[BUFSIZE] = {0};
	while (true) {
		// Gets the message from the standard input
		std::string buff;
		std::getline(std::cin, buff);

		// if EOF is reached, send BYE to the server and exit
		if (std::cin.eof()) {
			send(client_socket, "BYE\n", 4, 0);
			break;
		}

		buff += "\n";
		if (buff.length() > BUFSIZE) {
			std::cerr << "Message is too long" << std::endl;
			continue;
		}

		if (ssize_t sent = send(client_socket, buff.data(), buff.length(), 0); sent < 0)
			throw std::runtime_error("ERR: message sending failed");


		if (ssize_t res = recv(client_socket, buf, BUFSIZE, 0); res < 0)
			throw std::runtime_error("ERR: message receiving failed");

		std::cout << buf;

		if (strcmp(buf, "BYE\n") == 0 && buff != "BYE\n")
			throw std::runtime_error("ERR: server closed connection due to invalid request");

		if (strcmp(buf, "BYE\n") == 0 && buff == "BYE\n")
			break;

		memset(buf, 0, BUFSIZE);
	}
}

void udp_communicate(int client_socket, struct sockaddr_in server_address, socklen_t server_address_len) {
	char buf[BUFSIZE] = {0};
	while (true) {
		// Gets the message from the standard input
		std::string buff;
		std::getline(std::cin, buff);

		// if EOF is reached proceed to exit
		if (std::cin.eof())
			break;

		// Prepares the message to be sent by adding the length of the message and 0 for request
		std::string start(1, (char)(buff.length() + 1));
		buff = '\0' + start + buff;
		if (buff.length() > MAX_UDP) {
			std::cerr << "Message is too long" << std::endl;
			continue;
		}

		if (ssize_t sent = sendto(client_socket, buff.data(), buff.length(), 0, (struct sockaddr *) &server_address, server_address_len); sent < 0) {
			perror("ERROR in sendto");
			continue;
		}

		memset(buf, 0, BUFSIZE);
		if (ssize_t res = recvfrom(client_socket, buf, BUFSIZE, 0, (struct sockaddr *) &server_address, &server_address_len); res < 0) {
#ifdef _WIN32
			std::cerr << "ERROR: " << WSAGetLastError() << std::endl;
#endif
#ifdef __linux__
			perror("ERROR in recvfrom");
#endif
			continue;
		}

		if (buf[1] == 0) {
			std::cout << "OK:" << buf + 3 << std::endl;
		} else {
			std::cout << "ERR:" << buf + 3 << std::endl;
		}
	}
}

void sigint_handler(int) {
	if (protocol == "tcp") {
		send(csocket::client_socket, "BYE\n", 4, 0);
		char buf[BUFSIZE] = {0};
		recv(csocket::client_socket, buf, BUFSIZE, 0);
		std::cout << buf;
	}
	freeaddrinfo(csocket::serverptr);
	close(csocket::client_socket);
#ifdef _WIN32
	WSACleanup();
#endif
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
#ifdef _WIN32
	WSACleanup();
#endif
		return 1;
	}

	// Communicates with the server
	try {
		if (protocol == "tcp")
			tcp_communicate(csocket::client_socket);
		if (protocol == "udp")
			udp_communicate(csocket::client_socket, server_address, sizeof(server_address));
	} catch (std::runtime_error &e) {
		std::cerr << e.what() << std::endl;
		close(csocket::client_socket);
		freeaddrinfo(csocket::serverptr);
#ifdef _WIN32
	WSACleanup();
#endif
		return 1;
	}

	freeaddrinfo(csocket::serverptr);
    close(csocket::client_socket);
#ifdef _WIN32
	WSACleanup();
#endif
    return 0;
}
