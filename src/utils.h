#include <iostream>
#include <string>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <csignal>
#include <stack>
#include <vector>
#include <array>

#ifndef TEST_UTILS_H
#define TEST_UTILS_H

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

#endif //TEST_UTILS_H
