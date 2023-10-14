#include <iostream>
#include <string>
#include <string.h>
#include <sys/types.h>
#include <csignal>
#include <stack>
#include <vector>
#include <array>

#define NOMINMAX 0 // To prevent the min and max macros from being defined

#ifdef __linux__
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#else
#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <BaseTsd.h>
#include "getopt/getopt.h"
typedef SSIZE_T ssize_t;
#define close closesocket
#endif

#ifndef UTILS_H
#define UTILS_H

constexpr size_t BUFSIZE = 1024;
constexpr size_t MAX_UDP = 257; // 255 + \0 + \length

enum State {
	START,
	PAREN,
	NUMBER,
	OPERATION,
	SPACE,
	QUERY,
	EXPR,
	OPT_SPACE,
	OPT_EXPR,
};

/// Checks the arguments passed to the program
/// \param argc number of arguments
/// \param argv arguments
/// \param hostname string to store the hostname
/// \param port integer to store the port number
/// \param protocol string to store the protocol
/// \return 0 if everything is ok, otherwise throws an exception
int check_args(int, char **, const char **, uint16_t *, std::string *, std::string);

#endif //UTILS_H
