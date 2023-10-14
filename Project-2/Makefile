CFLAGS:= -std=c++20
CCX := g++

.PHONY: all clean ipkcpd

all: ipkcpd

default: ipkcpd

ipkcpd: IOTA.o utils.o server.o TCPServer.o UDPServer.o
	$(CCX) $(CFLAGS) -o $@ $^

clean:
	rm -f *.o ipkcpd

utils.o: ../Project-1/utils.cpp ../Project-1/utils.h
	$(CCX) $(CFLAGS) -c $<

%.o: %.cpp %.h
	$(CCX) $(CFLAGS) -c $<
