#ifndef IPK_UDPSERVER_H
#define IPK_UDPSERVER_H

#include "server.h"

class UDPServer: public Server {
public:
	UDPServer();
	~UDPServer() override;

	/// Set up the server
	/// \param hostname DNS name or IPv4 address of the server
	/// \param port Port number
	void SetUpServer(const char *hostname, const uint16_t port) override;

	/// Communicate with a client
	void communicate() override;
private:
	/// Create a UDP socket
	void create_udp_socket();

	/// Get the response to be sent to the client
	/// \param message The query
	/// \return The response
	std::string get_udp_response(std::string message);

	/// Send the response to the client
	/// \param client_address Client address
	/// \param query The response
	/// \param len Client address length
	void send_udp_message(struct sockaddr_in *client_address, std::string message, socklen_t len);
};

#endif //IPK_UDPSERVER_H
