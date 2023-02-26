//
// Created by Petr on 25.02.2023.
//

#include <string>
#include <iostream>

using namespace std;

int main() {
	string s = "Hello, World!";
	if (string b = "Hello, World!"; s == b) {
		cout << "s == b" << endl;
	}
	else {
		cout << "s != b" << endl;
	}
	return 0;
}