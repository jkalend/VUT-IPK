build:
	g++ client.cpp utils.h utils.cpp -o ipkcpc -std=c++20
clean:
	rm ipkcpc
udp : build
	./ipkcpc  -h 127.0.0.1 -p 2023 -m udp
tcp : build
	./ipkcpc  -h 127.0.0.1 -p 2023 -m tcp
