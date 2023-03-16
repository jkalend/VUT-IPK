#ifndef TEST_IPKCPC_H
#define TEST_IPKCPC_H
#include "utils.h"

// global variables required for proper interruption of the program
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

/// Sends messages to the server and receives responses using TCP protocol
/// \param client_socket TCP socket descriptor
void tcp_communicate(int client_socket);

/// Sends messages to the server and receives responses using UDP protocol
/// \param client_socket TCP socket descriptor
/// \param server_address Address of the server
/// \param server_address_len Length of the server address
void udp_communicate(int client_socket, struct sockaddr_in server_address, socklen_t server_address_len);

/// Handles the SIGINT signal
void sigint_handler(int);

#endif //TEST_IPKCPC_H
