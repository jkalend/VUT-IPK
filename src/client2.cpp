#include <string>
#include <iostream>
#include <stack>
#include <vector>

enum Token {
	NL,
	HELLO,
	BYE,
	OK,
};

enum State {
	NUMBER,
	OPERATION,
	SPACE,
	EXPR,
	OPT_SPACE,
	OPT_EXPR,
};
using namespace std;

double calculate(vector<double> v, char op) {
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
				res /= v[i];
				break;
		}
	}
	return res;
}

int parse(string s, double *res, int index) {
	if (s == "\n") {
		return NL;
	}
	if (s == "HELLO") {
		return HELLO;
	}
	if (s == "BYE") {
		return BYE;
	}
	char op;
	string ops = "+-*/";
	std::stack<State> stack;
	std::vector<double> v;
	string num;
	double tres = 0;
	stack.push(OPT_SPACE);
	stack.push(EXPR);
	stack.push(SPACE);
	stack.push(EXPR);
	stack.push(SPACE);
	stack.push(OPERATION);

	if (s[index] != '(') {
		throw std::runtime_error("ERROR: parsing error");
	} else {
		index++;
	}

	for (int i = index; i < s.length(); i++) {
		if (s[i] == ')' && stack.empty()) break;
		if (stack.top() == OPERATION) {
			if (std::find(ops.begin(), ops.end(), s[i]) != ops.end()) {
				op = *std::find(ops.begin(), ops.end(), s[i]);
				stack.pop();
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == SPACE) {
			if (s[i] == ' ') {
				stack.pop();
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == EXPR) {
			if (s[i] == '(' ) {
				stack.pop();
				i = parse(s, &tres, i++);
				v.push_back(tres);
			} else if (isdigit(s[i])) {
				stack.pop();
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else {
				throw std::runtime_error("ERROR: parsing error");
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
				throw std::runtime_error("ERROR: parsing error");
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
				throw std::runtime_error("ERROR: parsing error");
			}
		} else if (stack.top() == OPT_EXPR) {
			if (s[i] == '(' ) {
				stack.pop();
				i = parse(s, &tres, i++);
				v.push_back(tres);
				stack.push(OPT_SPACE);
			} else if (isdigit(s[i])) {
				stack.pop();
				stack.push(OPT_SPACE);
				stack.push(NUMBER);
				num.append(1, s[i]);
			} else {
				throw std::runtime_error("ERROR: parsing error");
			}
		}
	}

	if (stack.empty() && v.size() >= 2) {
		*res = calculate(v, op);
		return OK;
	}
	return 1;
}

int main() {
	string s = "SOLVE (+ 1 1)\n";
	size_t pos = s.find("SOLVE ");
	s = s.substr(6, s.length() - 7);
	double res = 0;
	int index = 0;
	Token flag;
	try {
		int i = parse(s, &res, index);
		cout << res << endl;
		cout << s.length() << endl;
	} catch (const std::exception& e) {
		cout << e.what() << endl;
	}
}