#include "server.h"
#include <cmath>

Server::Server() {
	for (auto &i : client_sockets) {
		i = 0;
	}
	server_address_len = sizeof(server_address);
}

Server::~Server() {
	freeaddrinfo(serverptr);
	close(master_socket);
#ifdef _WIN32
	WSACleanup();
#endif
}

void Server::SetUpServer(const char *hostname, const uint16_t port) {

}

void Server::communicate() {
}

int Server::parse(std::string s, double *res, int index) {
	char op;
	std::string ops = "+-*/";
	std::stack<State> stack;
	std::vector<double> v;
	std::string num;
	double tmp_result = 0;

	// Push required states to the stack
	stack.push(OPT_SPACE);
	stack.push(EXPR);
	stack.push(SPACE);
	stack.push(EXPR);
	stack.push(SPACE);
	stack.push(OPERATION);

	// Check if the first character is '('
	if (s[index] != '(') {
		throw std::runtime_error("parsing error");
	} else {
		index++;
	}

	// Parse the string
	for (int i = index; i < s.length(); i++) {
		if (stack.top() == OPERATION) {
			if (std::find(ops.begin(), ops.end(), s[i]) != ops.end()) {
				op = *std::find(ops.begin(), ops.end(), s[i]);
				stack.pop();
			} else {
				throw std::runtime_error("parsing error");
			}
		} else if (stack.top() == SPACE) {
			if (s[i] == ' ') {
				stack.pop();
			} else {
				throw std::runtime_error("parsing error");
			}
		} else if (stack.top() == EXPR) {
			if (s[i] == '(' ) {
				stack.pop();
				i = parse(s, &tmp_result, i++);
				v.push_back(tmp_result);
			} else if (isdigit(s[i])) {
				stack.pop();
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else {
				throw std::runtime_error("parsing error");
			}
		} else if (stack.top() == NUMBER) {
			if (isdigit(s[i])) {
				stack.pop();
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else if (s[i] == ' ' || s[i] == ')') {
				i--;
				stack.pop();
				v.push_back(std::stoi(num));
				num.clear();
			} else {
				throw std::runtime_error("parsing error");
			}
		} else if (stack.top() == OPT_SPACE) {
			if (s[i] == ' ') {
				stack.pop();
				stack.push(OPT_EXPR);
			} else {
				stack.pop();
				if (stack.empty() && v.size() >= 2 && s[i] == ')') {
					*res = calculate(v, op);
					num.clear();
					return i;
				}
				throw std::runtime_error("parsing error");
			}
		} else if (stack.top() == OPT_EXPR) {
			if (s[i] == '(' ) {
				stack.pop();
				i = parse(s, &tmp_result, i++);
				v.push_back(tmp_result);
				stack.push(OPT_SPACE);
			} else if (isdigit(s[i])) {
				stack.pop();
				stack.push(OPT_SPACE);
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else {
				throw std::runtime_error("parsing error");
			}
		}
	}

	if (stack.empty() && v.size() >= 2 && index != s.length()) {
		*res = calculate(v, op);
		return index;
	} else {
		throw std::runtime_error("parsing error");
	}
}

double Server::calculate(std::vector<double> v, char op) {
	double res = v[0];
	for (int i = 1; i < v.size(); i++) {
		switch (op) {
			case '+':
				res += v[i];
				break;
			case '-':
				res -= v[i];
				break;
			case '*':
				res *= v[i];
				break;
			case '/':
				if (v[i] == 0) throw std::runtime_error("ERROR: division by zero");
				res /= v[i];
				res = std::trunc(res);
				break;
		}
	}
	return res;
}

struct sockaddr_in* Server::get_adress(const char *hostname) {
	struct addrinfo hints = {AI_PASSIVE, AF_UNSPEC, SOCK_DGRAM, 0, 0, nullptr, nullptr, nullptr};

	serverptr = nullptr;

#ifdef _WIN32
	WSADATA wsaData;
	int iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != NO_ERROR) {
        throw std::runtime_error("ERR: WSAStartup failed");
    }
#endif

	if (getaddrinfo(hostname, nullptr, &hints, &serverptr) != 0)
		throw std::runtime_error("ERR: getaddrinfo failed");

	return (struct sockaddr_in*)(serverptr->ai_addr);
}
