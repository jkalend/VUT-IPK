#ifndef IPK_TCPSERVER_H
#define IPK_TCPSERVER_H

#include "server.h"

class TCPServer: public Server {
public:
	std::array<int, 30>expected;

	TCPServer();
	~TCPServer() override;

	/// Set up the server
	/// \param hostname DNS name or IPv4 address of the server
	/// \param port Port number
	void SetUpServer(const char *hostname, const uint16_t port) override;

	/// Communicate with a client
	void communicate() override;
private:
	/// Create a TCP socket
	void create_tcp_socket();

	/// Get the response to be sent to the client
	/// \param message The query
	/// \param expected The expected query
	/// \return The response
	std::string get_tcp_response(std::string message, int* expected);

	/// Get the query from the client
	/// \param client Socket descriptor of the client
	/// \param buf Buffer to store the query
	/// \return The query
	std::string get_tcp_query(const int* client, char* buf);

	/// Send the response to the client
	/// \param client Socket descriptor of the client
	/// \param message The response
	/// \param expected The status to be reset
	/// \param socket The socket descriptor of the server
	void send_tcp_message(const int *client, std::string message, int* expected, int* socket);
};

#endif //IPK_TCPSERVER_H
