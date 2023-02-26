/*
 * IPK.2015L
 *
 * Demonstration of non-blocking TCP server socket.
 *
 * Ondrej Rysavy (rysavy@fit.vutbr.cz)
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#define WELCOME_MSG "Hi, type anything. To end type 'bye.' at a separate line.\n"
#define BUFSIZE  1024
int main (int argc, const char * argv[]) {
	int rc;
	int welcome_socket;
	struct sockaddr_in6 sa;
	struct sockaddr_in6 sa_client;
	char str[INET6_ADDRSTRLEN];
    int port_number;
	socklen_t sa_client_len=sizeof(sa_client);
    
    if (argc != 2) {
       fprintf(stderr,"usage: %s <port>\n", argv[0]);
       exit(EXIT_FAILURE);
    }
    port_number = atoi(argv[1]);
    
    
    
	if ((welcome_socket = socket(PF_INET6, SOCK_STREAM, 0)) < 0)
	{
		perror("ERROR: socket");
		exit(EXIT_FAILURE);
	}

	int on = 1;
	rc = setsockopt(welcome_socket, SOL_SOCKET,  SO_REUSEADDR,
					(char *)&on, sizeof(on));
	if (rc < 0)
	{
		perror("ERROR: setsockopt");
		close(welcome_socket);
		exit(-1);
	}
	
	
	memset(&sa,0,sizeof(sa));
	sa.sin6_family = AF_INET6;
	sa.sin6_addr = in6addr_any;
	sa.sin6_port = htons(port_number);	
	if ((rc = bind(welcome_socket, (struct sockaddr*)&sa, sizeof(sa))) < 0)
	{
		perror("ERROR: bind");
		exit(EXIT_FAILURE);		
	}

	if ((rc = listen(welcome_socket, 1)) < 0)
	{
		perror("ERROR: listen");
		exit(EXIT_FAILURE);				
	}
	
	
	while(1)
	{
		int comm_socket = accept(welcome_socket, (struct sockaddr*)&sa_client, &sa_client_len);		
		if (comm_socket > 0)
		{
			/*************************************************************/
			/* Set socket to be non-blocking.                            */
			/*************************************************************/	
			int flags = fcntl(comm_socket, F_GETFL, 0);
			rc = fcntl(comm_socket, F_SETFL, flags | O_NONBLOCK);
			if (rc < 0)
			{
				perror("ERROR: fcntl");
				exit(EXIT_FAILURE);								
			}
						
			if(inet_ntop(AF_INET6, &sa_client.sin6_addr, str, sizeof(str))) {
				printf("INFO: New connection:\n");
				printf("INFO: Client address is %s\n", str);
				printf("INFO: Client port is %d\n", ntohs(sa_client.sin6_port));
			}
			
			send(comm_socket, WELCOME_MSG, strlen(WELCOME_MSG), 0);
			
			char buff[BUFSIZE];
			char input[BUFSIZE];
			
			
			for (;;)		
			{					
				int res = recv(comm_socket, buff, BUFSIZE,0);				
				if (res > 0)
				{
					buff[res] = '\0';
					printf("%s",buff);					
					if (strncmp(buff, "bye.", 4) == 0)					
					{
						printf("INFO: Closing connection to %s.\n",str);
						close(comm_socket);						
						break;
					}
				}
                else if (res == 0) 
                { 
                    printf("INFO: %s closed connection.\n",str);
					close(comm_socket);						
					break;
                }
                else if (errno == EAGAIN) // == EWOULDBLOCK
                {
                    printf(".");
                    continue;
                }
                else
                {
                    perror("ERROR: recv");
                    exit(EXIT_FAILURE);
                }
			}
		}
	}	
}
