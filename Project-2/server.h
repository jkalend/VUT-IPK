#ifndef IPK_SERVER_H
#define IPK_SERVER_H

#include "../Project-1/utils.h"

#define MAX_CLIENTS 30

class Server {
public:
	int master_socket;
	struct sockaddr_in server_address;
	struct addrinfo *serverptr;
	socklen_t server_address_len;
	std::array<int, 30>client_sockets;

	Server();
	virtual ~Server();

	/// Set up the server
	/// \param hostname DNS name or IPv4 address of the server
	/// \param port Port number
	virtual void SetUpServer(const char *hostname, const uint16_t port);

	/// Communicate with a client
	virtual void communicate();
protected:
	/// Parse the expression
	/// \param s The expression
	/// \param res int pointer to store the result
	/// \param index The starting index of the expression, used for recursion
	/// \return The index of the last character of the parsed expression
	int parse(std::string s, double *res, int index);

	/// Calculate the result of expression based on the operator
	/// \param v Vector of numbers
	/// \param op Operator
	/// \return Result of the expression
	double calculate(std::vector<double> v, char op);

	/// Get the address of the server
	/// \param hostname DNS name or IPv4 address of the server
	/// \return Server address
	struct sockaddr_in * get_adress(const char *hostname);
};

extern Server *server;

#endif //IPK_SERVER_H
