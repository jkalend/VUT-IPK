#ifndef IPKCPC_H
#define IPKCPC_H
#include "utils.h"

namespace csocket {
	int client_socket;
	struct addrinfo *serverptr;
}

/// Gets the address of the server
/// \param hostname either DNS or IP address
/// \return pointer to the address of the server
struct sockaddr_in * get_adress(const char *hostname);

/// Creates a socket for TCP communication
/// \param server_address Address of the server
/// \return Socket descriptor
int tcp_socket(struct sockaddr_in server_address);

/// Creates a socket for UDP communication
/// \return Socket descriptor
int udp_socket();

/// Handles the SIGINT signal
void sigint_handler(int);

#endif //IPKCPC_H
