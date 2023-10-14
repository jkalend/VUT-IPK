// the core of the program is inspired by the following sources:
// https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/
// https://git.fit.vutbr.cz/NESFIT/IPK-Projekty/src/branch/master/Stubs/cpp
// https://learn.microsoft.com/en-us/windows/win32/api/winsock/
#include "TCPServer.h"

TCPServer::TCPServer() : Server() {}

void TCPServer::SetUpServer(const char *hostname, const uint16_t port) {
	server_address = *get_adress(hostname);
	server_address.sin_port = htons(port);
	create_tcp_socket();
	for (auto &i : expected) {
		i = 0;
	}
}

TCPServer::~TCPServer() {
	for (int i = 0; i < MAX_CLIENTS; i++) {
		if (client_sockets[i] != 0) {
			send(client_sockets[i], "BYE\n", 4, 0);
			close(client_sockets[i]);
		}
	}
}

void TCPServer::communicate() {
	char buf[BUFSIZE] = {0};
	char incoming[BUFSIZE] = {0};
	std::string cli;
	fd_set set;

	while (true) {
		FD_ZERO(&set);
		FD_SET(master_socket, &set);
		int max_sock = master_socket;

		for (int client_socket : client_sockets) {
			if (client_socket > 0)
				FD_SET(client_socket, &set);
			max_sock = std::max(max_sock, client_socket);
		}

		if (int activity = select(max_sock + 1, &set, nullptr, nullptr, nullptr); activity < 0 && errno != EINTR)
			throw std::runtime_error("ERROR: select failed");

		if (FD_ISSET(master_socket, &set)) {
			int comm_socket = accept(master_socket, (struct sockaddr *) &server_address, &server_address_len);
			if (comm_socket < 0)
				throw std::runtime_error("ERROR: socket accepting failed");

			if(inet_ntop(AF_INET, &server_address.sin_addr, incoming, BUFSIZE)) {
				std::cout << "Connection from " << buf << ": " << ntohs(server_address.sin_port) << std::endl;
			} else {
				throw std::runtime_error("ERROR: inet_ntop failed");
			}

			//adds client to client_sockets
			for (int i = 0; i < MAX_CLIENTS; i++) {
				if (client_sockets[i] == 0) {
					client_sockets[i] = comm_socket;
					expected[i] = 1;
					break;
				}
			}
		}

		//reads messages from clients and sends responses back
		for (int i = 0; i < MAX_CLIENTS; i++) {
			int client = client_sockets[i];
			std::string query;

			if (FD_ISSET(client, &set)) {
				//gets message from client
				query = get_tcp_query(&client, buf);

				if (query == "\n" || query == "") {
					memset(buf, 0, BUFSIZE);
					query.clear();
					continue;
				}

				//sends message to client
				while (query.find('\n') != std::string::npos && !query.empty()) {
					send_tcp_message(&client, query.substr(0, query.find('\n')+1), &expected[i], &client_sockets[i]);
					query = query.substr(query.find('\n') + 1);
				}
				memset(buf, 0, BUFSIZE);
				query.clear();
			}
		}
	}
}

void TCPServer::create_tcp_socket() {
	int socket_t;
	if ((socket_t = socket(AF_INET, SOCK_STREAM, 0)) <= 0)
		throw std::runtime_error("ERROR: socket_t creation failed");

	if (int a = 1; setsockopt(socket_t, SOL_SOCKET, SO_REUSEADDR, (char *)&a, sizeof(int)) < 0)
		throw std::runtime_error("ERROR: socket_t options setting failed");

	if (bind(socket_t, (struct sockaddr *) &server_address, sizeof(server_address)) < 0)
		throw std::runtime_error("ERROR: socket_t binding failed");

	if (listen(socket_t, 3) < 0)
		throw std::runtime_error("ERROR: socket_t listening failed");

	master_socket =  socket_t;
}

std::string TCPServer::get_tcp_response(std::string message, int* expected) {
	double result = 0;

	if (*expected == 1 && message == "HELLO\n") {
		*expected = 2;
	} else if (*expected == 2 && message != "BYE\n") {
		size_t start = message.find("SOLVE ");
		if (start == std::string::npos) {
			return "BYE\n";
		}
		if (start == 0) {
			try {
				if (int res = parse(message.substr(6, message.length() - 7), &result, 0);
					res != message.substr(6, message.length() - 7).length() - 1)
					return "BYE\n";

				int output = static_cast<int>(result);
				if (output < 0)
					return "BYE\n";

				return "RESULT " + std::to_string(output) + "\n";
			} catch (std::runtime_error &e) {
				return "BYE\n";
			}
		} else {
			return "BYE\n";
		}
	} else if (message == "BYE\n") {
		*expected = 0;
	} else {
		return "BYE\n";
	}
	return message;
}

std::string TCPServer::get_tcp_query(const int *client, char* buf) {
	std::string message;
	while (message.find('\n') == std::string::npos) {
		if (ssize_t res = recv(*client, buf, BUFSIZE, 0); res < 0) {
			send(*client, "BYE\n", 4, 0);
			close(*client);
			std::cerr << "ERR: message receiving failed" << std::endl;
		}
		if (message.length() > BUFSIZE) {
			send(*client, "BYE\n", 4, 0);
			close(*client);
			std::cerr << "ERR: message too long" << std::endl;
			message.clear();
			break;
		}

		message += buf;
	}

	for (auto &c : message)
		c = toupper(c);
	return message;
}

void TCPServer::send_tcp_message(const int *client, std::string message, int* expected, int* socket) {
	std::cout << "Received message: " << message;

	message = get_tcp_response(message, expected);

	std::cout << "Sending: " << message;

	if (ssize_t sent = send(*client, message.data(), message.length(), 0); sent <= 0) {
		close(*client);
		std::cerr << "ERR: message receiving failed" << std::endl;
	}

	if (message == "BYE\n") {
		close(*client);
		*socket = 0;
		*expected = 0;
		std::cout << "Connection closed" << std::endl;
	}
}
