#include <iostream>
#include <string>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <csignal>
#include <stack>
#include <vector>
#include "utils.h"
#include <array>


/// Global variables to propagate to signal handler
std::string protocol;
namespace ssocket {
	int master_socket;
	std::array<int, 30>client_sockets;
	struct addrinfo *serverptr;
}

/// Calculate the result of expression based on the operator
/// \param v Vector of numbers
/// \param op Operator
/// \return Result of the expression
double calculate(std::vector<double> v, char op) {
	double res = v[0];
	for (int i = 1; i < v.size(); i++) {
		switch (op) {
			case '+':
				res += v[i];
				break;
			case '-':
				res -= v[i];
				break;
			case '*':
				res *= v[i];
				break;
			case '/':
				if (v[i] == 0) throw std::runtime_error("ERROR: division by zero");
				res /= v[i];
				break;
		}
	}
	return res;
}

/// Parse the expression
/// \param s The expression
/// \param res int pointer to store the result
/// \param index The starting index of the expression, used for recursion
/// \return The index of the last character of the parsed expression
int parse(std::string s, double *res, int index) {
	char op;
	std::string ops = "+-*/";
	std::stack<State> stack;
	std::vector<double> v;
	std::string num;
	double tmp_result = 0;
	stack.push(OPT_SPACE);
	stack.push(EXPR);
	stack.push(SPACE);
	stack.push(EXPR);
	stack.push(SPACE);
	stack.push(OPERATION);

	if (s[index] != '(') {
		throw std::runtime_error("ERROR: parsing error");
	} else {
		index++;
	}

	for (int i = index; i < s.length(); i++) {
		if (s[i+1] == '\n' && s[i] == ')' && stack.empty()) break;
		if (stack.top() == OPERATION) {
			if (std::find(ops.begin(), ops.end(), s[i]) != ops.end()) {
				op = *std::find(ops.begin(), ops.end(), s[i]);
				stack.pop();
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == SPACE) {
			if (s[i] == ' ') {
				stack.pop();
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == EXPR) {
			if (s[i] == '(' ) {
				stack.pop();
				i = parse(s, &tmp_result, i++);
				v.push_back(tmp_result);
			} else if (isdigit(s[i])) {
				stack.pop();
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == NUMBER) {
			if (isdigit(s[i])) {
				stack.pop();
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else if (s[i] == ' ' || s[i] == ')') {
				i--;
				stack.pop();
				v.push_back(std::stoi(num));
				num.clear();
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == OPT_SPACE) {
			if (s[i] == ' ') {
				stack.pop();
				stack.push(OPT_EXPR);
			} else {
				stack.pop();
				if (stack.empty() && v.size() >= 2 && s[i] == ')') {
					*res = calculate(v, op);
					num.clear();
					return i;
				}
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == OPT_EXPR) {
			if (s[i] == '(' ) {
				stack.pop();
				i = parse(s, &tmp_result, i++);
				v.push_back(tmp_result);
				stack.push(OPT_SPACE);
			} else if (isdigit(s[i])) {
				stack.pop();
				stack.push(OPT_SPACE);
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		}
	}

	if (stack.empty() && v.size() >= 2) {
		*res = calculate(v, op);
		return OK;
	}
	return 1;
}

/// Get the address of the server
/// \param hostname DNS name or IPv4 address of the server
/// \return Server address
struct sockaddr_in * get_adress(const char *hostname) {
	struct addrinfo hints = {AI_PASSIVE, AF_INET, SOCK_DGRAM, 0, 0, nullptr, nullptr, nullptr};

	ssocket::serverptr = nullptr;

	if (getaddrinfo(hostname, nullptr, &hints, &ssocket::serverptr) != 0)
		throw std::runtime_error("ERR: getaddrinfo failed");

	return (struct sockaddr_in*)(ssocket::serverptr->ai_addr);
}

/// Create a TCP socket
/// \param server_address Server address
/// \return The socket descriptor
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

/// Create a UDP socket
/// \param server_address Server address
/// \return The socket descriptor
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

/// Communicate with the client using TCP protocol
/// \param master_socket Socket descriptor of the server
/// \param server_address Server address
/// \param server_address_len Server address length
void tcp_communicate(int master_socket, struct sockaddr_in server_address, socklen_t server_address_len) {
	char buf[BUFSIZE] = {0};
	char incoming[BUFSIZE] = {0};
	std::string cli;
	fd_set set;
	int max_sock = master_socket;
	int expected[30] = {0};
	while (true) {

		FD_ZERO(&set);
		FD_SET(master_socket, &set);
		max_sock = master_socket;

		for (int client_socket : ssocket::client_sockets) {
			if (client_socket > 0)
				FD_SET(client_socket, &set);
			if (client_socket > max_sock)
				max_sock = client_socket;
		}

		int activity = select(max_sock + 1, &set, nullptr, nullptr, nullptr);
		if (activity < 0 && errno != EINTR)
			throw std::runtime_error("ERROR: select failed");

		if (FD_ISSET(master_socket, &set)) {
			int comm_socket = accept(master_socket, (struct sockaddr *) &server_address, &server_address_len);
			if (comm_socket < 0)
				throw std::runtime_error("ERROR: socket accepting failed");

			if(inet_ntop(AF_INET, &server_address.sin_addr, incoming, BUFSIZE)) {
				std::cout << "Connection from " << buf << ":" << ntohs(server_address.sin_port) << std::endl;
			} else {
				throw std::runtime_error("ERROR: inet_ntop failed");
			}

			for (int i = 0; i < 30; i++) {
				if (ssocket::client_sockets[i] == 0) {
					ssocket::client_sockets[i] = comm_socket;
					expected[i] = 1;
					break;
				}
			}
		}

		for (int i = 0; i < 30; i++) {
			int client = ssocket::client_sockets[i];
			if (FD_ISSET(client, &set)) {
				if (ssize_t res = recv(client, buf, BUFSIZE, 0); res < 0) {
					close(client);
					std::cerr << "ERR: message receiving failed" << std::endl;
				}

				std::string response = buf;
				double result = 0;

				if (response == "\n" || response == "") {
					memset(buf, 0, BUFSIZE);
					response.clear();
					continue;
				}

				std::cout << "Received message from: " << ntohs(server_address.sin_port) << " : " << response;

				if (expected[i] == 1 && response == "HELLO\n") {
					expected[i] = 2;
				} else if (expected[i] == 2 && response != "BYE\n") {
					size_t start = response.find("SOLVE ");
					if (start == std::string::npos) {
						response = "BYE\n";
					} else if (start == 0) {
						try {
							int res = parse(response.substr(6, response.length() - 7), &result, 0);
							if (res != response.substr(6, response.length() - 7).length() - 1) {
								response = "BYE\n";
							} else {
								response = "RESULT " + std::to_string(result) + "\n";
							}
						} catch (std::runtime_error &e) {
							response = "BYE\n";
						}
					} else {
						response = "BYE\n";
					}
				} else if (response == "BYE\n") {
					expected[i] = 0;
				} else {
					response = "BYE\n";
				}
				std::cout << response << std::endl;

				if (ssize_t sent = send(client, response.data(), response.length(), 0); sent <= 0) {
					close(client);
					std::cerr << "ERR: message receiving failed" << std::endl;
				}

				if (response == "BYE\n") {
					close(client);
					ssocket::client_sockets[i] = 0;
					expected[i] = 0;
					std::cout << "Connection closed" << std::endl;
				}

				memset(buf, 0, BUFSIZE);
				response.clear();
			}
		}
	}
}

/// Communicate with the client using UDP protocol
/// \param master_socket Socket descriptor of the server
/// \param server_address Server address
/// \param server_address_len Server address length
void udp_communicate(int master_socket, struct sockaddr_in server_address, socklen_t server_address_len) {
	char buf[BUFSIZE] = {0};
	char incoming[BUFSIZE] = {0};
	std::string cli;
	socklen_t len = sizeof(server_address);
	struct sockaddr_in client_address;
	while (true) {

        if (ssize_t bytesrx = recvfrom(master_socket, buf, BUFSIZE, 0, (struct sockaddr *) &client_address, &len); bytesrx < 0)
            perror("ERROR: recvfrom:");

		getnameinfo((struct sockaddr *) &client_address, len, incoming, BUFSIZE, nullptr, 0, 0);

        char const *hostaddrp = inet_ntoa(client_address.sin_addr);

		double result = 0;
		std::string response;
		std::string query = buf + 2;

		std::cout << "Message from " << hostaddrp << ": " << query;

		try {
			parse(query, &result, 0);
			response = std::to_string(result) + "\n";
			std::string start(1, (char)(response.length()));
			start = '\0' + start;
			start = '\1' + start;
			response = start + response;
		} catch (std::runtime_error &e) {
			response = e.what();
			std::string start(1, (char)(response.length() + 1));
			start = '\1' + start;
			start = '\1' + start;
			response = start + response + "\n";
		}

        if (ssize_t bytestx = sendto(master_socket, response.data(), response.length(), 0, (struct sockaddr *) &client_address, len); bytestx < 0)
			perror("ERROR: sendto:");
		memset(buf, 0, BUFSIZE);
	}
}

/// Signal handler for SIGINT
__attribute__((noreturn))
void sigint_handler(int) {
	std::cout << "Exiting" << std::endl;
	std::cout << "Bye..." << std::endl;
	if (protocol == "tcp") {
		for (int i = 0; i < 30; i++) {
			if (ssocket::client_sockets[i] != 0) {
				send(ssocket::client_sockets[i], "BYE\n", 4, 0);
				close(ssocket::client_sockets[i]);
			}
		}
	}
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

    std::cout << "INFO: Server socket: " << inet_ntoa(server_address.sin_addr) <<" : " <<
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

	for (int i = 0; i < 30; i++)
		ssocket::client_sockets[i] = 0;

	try {
		if (protocol == "tcp")
			tcp_communicate(ssocket::master_socket, server_address, sizeof(server_address));
		if (protocol == "udp")
			udp_communicate(ssocket::master_socket, server_address, sizeof(server_address));
	} catch (std::runtime_error &e) {
		std::cout << e.what() << std::endl;
		close(ssocket::master_socket);
		freeaddrinfo(ssocket::serverptr);
		return 1;
	}

	freeaddrinfo(ssocket::serverptr);
    close(ssocket::master_socket);
    return 0;
}
