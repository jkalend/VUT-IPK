/*
 * IPK.2015L
 *
 * Demonstration of trivial TCP communication.
 *
 * Ondrej Rysavy (rysavy@fit.vutbr.cz)
 *
 */
#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

#define BUFSIZE 1024
#define UDP_BUFSIZE 512

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

	if (*endptr != '\0')
			throw std::runtime_error("ERROR: invalid port");

	//std::cout << "here" << std::endl;

	if (*protocol != "tcp" && *protocol != "udp")
		throw std::runtime_error("ERROR: invalid protocol");

	return 0;
}

struct sockaddr_in * get_adress(const char *hostname) {
	/* 2. ziskani adresy serveru pomoci DNS */
	struct addrinfo hints = {0};
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;
	hints.ai_flags = AI_PASSIVE;
	hints.ai_protocol = 0;

	struct addrinfo *serverptr = {0};

	if (getaddrinfo(hostname, nullptr, &hints, &serverptr) != 0) {
		perror("ERROR: no such host exists");
        exit(EXIT_FAILURE);
    }
	return (struct sockaddr_in*)(serverptr->ai_addr);
}

int tcp_socket(struct sockaddr_in server_address) {
	int client_socket;
	if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) <= 0) {
		//perror("ERROR: socket creation failed");
		throw std::runtime_error("ERROR: socket connection failed");
		//exit(EXIT_FAILURE);
	}

	if (connect(client_socket, (const struct sockaddr *) &server_address, sizeof(server_address)) != 0) {
		//perror("ERROR: socket connection failed");
		throw std::runtime_error("ERROR: socket connection failed");
		//exit(EXIT_FAILURE);
	}
	return client_socket;
}

int udp_socket() {
	int client_socket;
	if ((client_socket = socket(AF_INET, SOCK_DGRAM, 0)) <= 0) {
		perror("ERROR: socket creation failed");
		exit(EXIT_FAILURE);
	}
	return client_socket;
}

void tcp_communicate(int client_socket) {
	char buf[BUFSIZE] = {0};
	while (true) {
		/* nacteni zpravy od uzivatele */
		std::string buff;
		std::getline(std::cin, buff);
		buff += "\n";
		if (buff.length() > BUFSIZE) {
			std::cout << "Message is too long" << std::endl;
			continue;
		}
		strcpy(buf, buff.data());

		/* odeslani zpravy na server */
		if (ssize_t sent = send(client_socket, buf, strlen(buf), 0); sent < 0)
			perror("ERROR in sendto");


		/* prijeti odpovedi a jeji vypsani */
		memset(buf, 0, BUFSIZE);
		if (ssize_t res = recv(client_socket, buf, BUFSIZE, 0); res < 0)
			perror("ERROR in recvfrom");

		printf("Echo from server: %s", buf);

		if (strcmp(buf, "BYE\n") == 0) {
			break;
		}
	}
}

void udp_communicate(int client_socket, struct sockaddr_in server_address, socklen_t server_address_len) {
	char buf[UDP_BUFSIZE] = {0};
	while (true) {
		/* nacteni zpravy od uzivatele */
		server_address.sin_addr.s_addr = INADDR_ANY;
		std::string buff;
		socklen_t len;
		std::getline(std::cin, buff);
		buff += "\n";
		if (buff.length() > UDP_BUFSIZE) {
			std::cout << "Message is too long" << std::endl;
			continue;
		}
		strcpy(buf, buff.data());
//		for (char i : buf) {
//			std::cout << (int)i << " ";
//		}
//		exit(0);
//		bzero(buf, UDP_BUFSIZE);
//		fgets(buf, UDP_BUFSIZE, stdin);

		/* odeslani zpravy na server */
		if (ssize_t sent = sendto(client_socket, (const char *)buf, strlen(buf), MSG_CONFIRM, (const struct sockaddr *) &server_address, server_address_len); sent < 0)
			perror("ERROR in sendto");

		/* prijeti odpovedi a jeji vypsani */
		memset(buf, 0, UDP_BUFSIZE);
		ssize_t res = recvfrom(client_socket, (char *)buf, UDP_BUFSIZE, MSG_WAITALL, (struct sockaddr *) &server_address, &len);
		if (res < 0)
			perror("ERROR in recvfrom");

		buf[res] = '\0';
		std::cout << "Echo from server: " << buf << std::endl;
		//printf("Echo from server: %s", buf);

		if (strcmp(buf, "BYE\n") == 0) {
			break;
		}
	}
}

int main (int argc, char **argv) {
	uint16_t port_number;
	std::string protocol;
	int client_socket;
    const char *server_hostname;
    struct sockaddr_in server_address;

    /* 1. test vstupnich parametru: */
	try {
        check_args(argc, argv, &server_hostname, &port_number, &protocol);
    } catch (std::runtime_error &e) {
		std::cout << e.what() << std::endl;
		exit(EXIT_FAILURE);
	}

    /* 3. nalezeni IP adresy serveru a inicializace struktury server_address */
	server_address = *get_adress(server_hostname);
    server_address.sin_port = htons(port_number);

    /* tiskne informace o vzdalenem soketu */ 
    printf("INFO: Server socket: %s : %d \n", inet_ntoa(server_address.sin_addr), ntohs(server_address.sin_port));
    
    /* Vytvoreni soketu */
	try {
		if (protocol == "tcp") {
			client_socket = tcp_socket(server_address);
		} else {
			client_socket = udp_socket();
		}
	} catch (std::runtime_error &e) {
		std::cout << e.what() << std::endl;
		exit(EXIT_FAILURE);
	}

	/* komunikace s serverem */
	if (protocol == "tcp") {
		tcp_communicate(client_socket);
	}
	if (protocol == "udp") {
		udp_communicate(client_socket, server_address, sizeof(server_address));
	}

    close(client_socket);
    return 0;
}
