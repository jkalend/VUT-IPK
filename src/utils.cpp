#include "utils.h"

/// Checks the arguments passed to the program
/// \param argc number of arguments
/// \param argv arguments
/// \param hostname string to store the hostname
/// \param port integer to store the port number
/// \param protocol string to store the protocol
/// \return 0 if everything is ok, otherwise throws an exception
int check_args(int argc, char **argv, const char **hostname, uint16_t *port, std::string *protocol, std::string filename) {
	int c;
	char *endptr = nullptr;

	if (argc != 7)
		throw std::runtime_error("ERROR: invalid number of arguments");

	while ((c = getopt(argc, argv, "h:p:m:")) != -1) {
		switch (c) {
			case 'h':
				*hostname = optarg;
				break;
			case 'p':
				*port = (uint16_t) strtol(optarg, &endptr, 10);
				break;
			case 'm':
				*protocol = optarg;
				break;
			default:
				std::string usage = "usage: " + filename + " -h <hostname> -p <port> -m <protocol>\n";
				throw std::runtime_error(usage);
		}
	}

	if (endptr != nullptr && *endptr != '\0')
		throw std::runtime_error("ERROR: invalid port");

	if (*protocol != "tcp" && *protocol != "udp")
		throw std::runtime_error("ERROR: invalid protocol");

	return 0;
}