#ifndef IPKCPD_H
#define IPKCPD_H

#include "utils.h"

namespace ssocket {
	int master_socket;
	std::array<int, 30>client_sockets;
	struct addrinfo *serverptr;
}

/// Calculate the result of expression based on the operator
/// \param v Vector of numbers
/// \param op Operator
/// \return Result of the expression
double calculate(std::vector<double> v, char op);

/// Parse the expression
/// \param s The expression
/// \param res int pointer to store the result
/// \param index The starting index of the expression, used for recursion
/// \return The index of the last character of the parsed expression
int parse(std::string s, double *res, int index);

/// Get the address of the server
/// \param hostname DNS name or IPv4 address of the server
/// \return Server address
struct sockaddr_in * get_adress(const char *hostname);

/// Create a TCP socket
/// \param server_address Server address
/// \return The socket descriptor
int tcp_socket(struct sockaddr_in server_address);

/// Create a UDP socket
/// \param server_address Server address
/// \return The socket descriptor
int udp_socket(struct sockaddr_in server_address);


/// Communicate with the client using TCP protocol
/// \param master_socket Socket descriptor of the server
/// \param server_address Server address
/// \param server_address_len Server address length
void tcp_communicate(int master_socket, struct sockaddr_in server_address, socklen_t server_address_len);


/// Communicate with the client using UDP protocol
/// \param master_socket Socket descriptor of the server
/// \param server_address Server address
/// \param server_address_len Server address length
void udp_communicate(int master_socket, struct sockaddr_in server_address, socklen_t server_address_len);

/// Handles the SIGINT signal
void sigint_handler(int);

#endif //IPKCPD_H
