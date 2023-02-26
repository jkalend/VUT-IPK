/*
 * IPK.2015L
 *
 * Demonstration of trivial UDP communication.
 *
 * Ondrej Rysavy (rysavy@fit.vutbr.cz)
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUFSIZE 512
int main (int argc, const char * argv[]) {
    char buf[BUFSIZE];
	int server_socket, port_number, bytestx, bytesrx;
    socklen_t clientlen;
    struct sockaddr_in client_address, server_address;
    int optval;
    const char * hostaddrp;
    struct hostent *hostp;

     
    /* 1. test vstupnich parametru: */
    if (argc != 2) {
       fprintf(stderr,"usage: %s <port>\n", argv[0]);
       exit(EXIT_FAILURE);
    }
    port_number = atoi(argv[1]);
      
    /* Vytvoreni soketu */
	if ((server_socket = socket(AF_INET, SOCK_DGRAM, 0)) <= 0)
	{
		perror("ERROR: socket");
		exit(EXIT_FAILURE);
	}
    /* potlaceni defaultniho chovani rezervace portu ukonceni aplikace */ 
    optval = 1;
    setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval , sizeof(int));

    /* adresa serveru, potrebuje pro prirazeni pozadovaneho portu */
    bzero((char *) &server_address, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons((unsigned short)port_number);
	
    if (bind(server_socket, (struct sockaddr *) &server_address, sizeof(server_address)) < 0) 
    {
        perror("ERROR: binding");
        exit(EXIT_FAILURE);
    }
    
    while(1) 
    {   
        printf("INFO: Ready.\n");
    	/* prijeti odpovedi a jeji vypsani */
        clientlen = sizeof(client_address);
        bytesrx = recvfrom(server_socket, buf, BUFSIZE, 0, (struct sockaddr *) &client_address, &clientlen);
        if (bytesrx < 0) 
            perror("ERROR: recvfrom:");
    
        hostp = gethostbyaddr((const char *)&client_address.sin_addr.s_addr, 
			  sizeof(client_address.sin_addr.s_addr), AF_INET);
              
        hostaddrp = inet_ntoa(client_address.sin_addr);
        printf("Message (%lu) from %s:  %s\n", strlen(buf), hostaddrp, buf);
    
    
        /* odeslani zpravy zpet klientovi  */        
        bytestx = sendto(server_socket, buf, strlen(buf), 0, (struct sockaddr *) &client_address, clientlen);
        if (bytestx < 0) 
            perror("ERROR: sendto:");
    }
    return 0;
}

