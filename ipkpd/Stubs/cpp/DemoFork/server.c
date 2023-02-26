/*
 * IPK
 *
 * Demonstration of a basic TCP server with fork.
 *
 * Ondrej Rysavy (rysavy@fit.vutbr.cz)
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#define WELCOME_MSG "Hi, type anything. To end type 'bye.' at a separate line.\n"

void SigCatcher(int n)
{
	int pid = wait3(NULL,WNOHANG,NULL);
	printf("Child %d spawned.\n",pid);
}

int main (int argc, const char * argv[]) {
	int rc;
	int welcome_socket;
	struct sockaddr_in6 sa;
	struct sockaddr_in6 sa_client;
	char str[INET6_ADDRSTRLEN];
	socklen_t sa_client_len=sizeof(sa_client);
	if ((welcome_socket = socket(PF_INET6, SOCK_STREAM, 0)) < 0)
	{
		perror("socket() failed");
		exit(EXIT_FAILURE);
	}
	
	memset(&sa,0,sizeof(sa));
	sa.sin6_family = AF_INET6;
	sa.sin6_addr = in6addr_any;
	sa.sin6_port = htons(11111);	
	if ((rc = bind(welcome_socket, (struct sockaddr*)&sa, sizeof(sa))) < 0)
	{
		perror("bind() failed");
		exit(EXIT_FAILURE);		
	}
	if ((rc = listen(welcome_socket, 1)) < 0)
	{
		perror("listen() failed");
		exit(EXIT_FAILURE);				
	}
	
	signal(SIGCHLD,SigCatcher);
	
	while(1)
	{
		int comm_socket = accept(welcome_socket, (struct sockaddr*)&sa_client, &sa_client_len);	
		if (comm_socket <= 0)
			continue;

		int pid = fork();
		if (pid < 0) 
		{
			perror("fork() failed");
			exit(EXIT_FAILURE);				
		}
		
		if (pid == 0)	// new process to maintain client's requests:
		{
			int child_pid = getpid();			
			close(welcome_socket);				// not necessary in child process
			printf("New connection (maintained by %d):\n",child_pid);			
			if(inet_ntop(AF_INET6, &sa_client.sin6_addr, str, sizeof(str))) {				
				printf("%d:Client address is %s\n", child_pid, str);
				printf("%d:Client port is %d\n", child_pid, ntohs(sa_client.sin6_port));
			}
			
			send(comm_socket, WELCOME_MSG, strlen(WELCOME_MSG), 0);
			
			char buff[1024];
			int res = 0;
			for (;;)		
			{	
				res = recv(comm_socket, buff, 1024,0);
				if (res > 0)
				{
					buff[res] = '\0';
					printf("%d:%s",child_pid,buff);
					buff[4] = '\0';
					if (strcmp(buff, "bye.") == 0)					
						break;
				}
				else	// error or end of connection
					break;
			}
			
			printf("Connection to %s closed\n",str);
			close(comm_socket);			
			exit(0);
		}
		else // welcome process
		{			
			close(comm_socket);
		}
	}	
}
