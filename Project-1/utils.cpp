#include "utils.h"

int check_args(int argc, char **argv, const char **hostname, uint16_t *port, std::string *protocol, std::string filename) {
	int c;
	char *endptr = nullptr;

	if (argc != 7)
		throw std::runtime_error("ERROR: invalid number of arguments\n"
								 "usage: " + filename + " -h <hostname> -p <port> -m <protocol>");

	while ((c = getopt(argc, argv, ":h:p:m:")) != -1) {
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

	if (*port < 1024 || *port > 65535)
		throw std::runtime_error("ERROR: invalid port");

	return 0;
}
