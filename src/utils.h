#include <iostream>
#include <string>
#include <string.h>
#include <sys/types.h>
#include <csignal>
#include <stack>
#include <vector>
#include <array>

#ifdef __WIN32
#pragma comment(lib, "Ws2_32.lib")
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <BaseTsd.h>
#include "getopt/getopt.h"
typedef SSIZE_T ssize_t;
#define close closesocket
#else
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

#ifndef UTILS_H
#define UTILS_H

constexpr size_t BUFSIZE = 1024;
constexpr size_t MAX_UDP = 257; // 255 + \0 + \length

extern std::string protocol;

enum Token {
	NL,
	HELLO,
	BYE,
	OK,
};

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

int check_args(int, char **, const char **, uint16_t *, std::string *, std::string);

#endif //UTILS_H
