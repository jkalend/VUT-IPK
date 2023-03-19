CFLAGS:= -O0 -std=c++20
CC:= g++

default: ipkcpc

ipkcpc: ipkcpc.o utils.o
	$(CC) $(CFLAGS) -o $@ $^
clean:
	rm -f *.o ipkcpc

%.o: %.c %.h
	$(CC) $(CFLAGS) -c $<