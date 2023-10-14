// the core of the program is inspired by the following sources:
// https://www.geeksforgeeks.org/udp-server-client-implementation-c/
// https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Stubs/cpp
// https://learn.microsoft.com/en-us/windows/win32/api/winsock/
#include "UDPServer.h"

UDPServer::UDPServer() : Server() {}

void UDPServer::SetUpServer(const char *hostname, const uint16_t port) {
	server_address = *get_adress(hostname);
	server_address.sin_port = htons(port);
	create_udp_socket();
}

UDPServer::~UDPServer() = default;

void UDPServer::create_udp_socket() {
	int socket_t;
	if ((socket_t = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) <= 0)
		throw std::runtime_error("ERROR: socket creation failed");

	if (int a = 1; setsockopt(socket_t, SOL_SOCKET, SO_REUSEADDR, (char *)&a, sizeof(int)) < 0)
		throw std::runtime_error("ERROR: socket options setting failed");

	if (bind(socket_t, (struct sockaddr *) &server_address, sizeof(server_address)) < 0)
		throw std::runtime_error("ERROR: socket binding failed");
	master_socket = socket_t;
}

std::string UDPServer::get_udp_response(std::string message) {
	double result = 0;
	try {
		if (int end = parse(message, &result, 0); end != message.length() - 1)
			throw std::runtime_error("Invalid query");

		int output = static_cast<int>(result);
		if (output < 0)
			throw std::runtime_error("Negative result");

		message = std::to_string(output);
		if (message.length() > 255)
			throw std::runtime_error("Result too long");

		std::string start(1, (char)(message.length()));
		start = '\0' + start; // status code
		start = '\1' + start; // opcode
		message = start + message;
	} catch (std::runtime_error &e) {
		message = e.what();
		std::string start(1, (char)(message.length() + 1));
		start = '\1' + start; // status code
		start = '\1' + start; // opcode
		message = start + message;
	}
	return message;
}

void UDPServer::send_udp_message(struct sockaddr_in *client_address, std::string message, socklen_t len) {
	char const *hostaddrp = inet_ntoa(client_address->sin_addr);

	std::cout << "Message from " << hostaddrp << ": " << message << std::endl;

	message = get_udp_response(message);

	std::cout << "Sending: " << message.substr(3, message.length() - 3) << std::endl;

    if (ssize_t bytestx = sendto(master_socket, message.data(), message.length(), 0, (struct sockaddr *) client_address, len); bytestx < 0)
		std::cerr << "ERROR: sendto:";
}

void UDPServer::communicate() {
	char buf[BUFSIZE] = {0};
	char incoming[BUFSIZE] = {0};
	socklen_t len = sizeof(struct sockaddr_in);
	struct sockaddr_in client_address;

	while (true) {

        if (ssize_t bytesrx = recvfrom(master_socket, buf, BUFSIZE, 0, (struct sockaddr *) &client_address, &len); bytesrx < 0)
			std::cerr << "ERROR: recvfrom:";

		getnameinfo((struct sockaddr *) &client_address, len, incoming, BUFSIZE, nullptr, 0, 0);

		if (buf[0] != '\0') {
			std::cerr << "ERROR: invalid opcode" << std::endl;
			send_udp_message(&client_address, "ERROR", len);
			memset(buf, 0, BUFSIZE);
			continue;
		}

		std::string query = buf + 2;
		query = query.substr(0, static_cast<size_t>(buf[1]));

		send_udp_message(&client_address, query, len);
		memset(buf, 0, BUFSIZE);
	}
}
