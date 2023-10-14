CFLAGS:= -O0 -std=c++2a
CC:= g++

default: ipkcpc

ipkcpc: ipkcpc.o utils.o
	$(CC) $(CFLAGS) -o $@ $^
clean:
	rm -f *.o ipkcpc

utils.o: utils.cpp utils.h
	$(CC) $(CFLAGS) -c $<

ipkcpc.o: ipkcpc.cpp ipkcpc.h
	$(CC) $(CFLAGS) -c $<
