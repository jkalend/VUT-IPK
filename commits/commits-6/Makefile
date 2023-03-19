CFLAGS:= -O0 -std=c++20
CC:= g++

default: ipkcpd

ipkcpc: ipkcpd.o utils.o
	$(CC) $(CFLAGS) -o $@ $^
clean:
	rm -f *.o ipkcpd

%.o: %.c %.h
	$(CC) $(CFLAGS) -c $<