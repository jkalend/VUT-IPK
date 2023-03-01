#include "utils.h"

int check_args(int argc, char **argv, const char **hostname, uint16_t *port, std::string *protocol) {
	int c;
	char *endptr = nullptr;
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
				fprintf(stderr, "usage: %s <hostname> <port>)\n", argv[0]);
		}
	}

	if (endptr != nullptr && *endptr != '\0')
		throw std::runtime_error("ERROR: invalid port");

	if (*protocol != "tcp" && *protocol != "udp")
		throw std::runtime_error("ERROR: invalid protocol");

	return 0;
}