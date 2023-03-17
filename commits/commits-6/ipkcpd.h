#ifndef IPKCPD_H
#define IPKCPD_H

#include "utils.h"

namespace ssocket {
	int master_socket;
	std::array<int, 30>client_sockets; // maximum number of clients is 30
	struct addrinfo *serverptr;
}

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

/// Handles the SIGINT signal
void sigint_handler(int);

#endif //IPKCPD_H
