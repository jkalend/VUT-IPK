//
//  main.c
//  messenger
//
//  Created by Ondrej Rysavy on 2/17/12.
//  Copyright 2012 Brno University Of Technology. All rights reserved.
//
//  Very plain SMTP client for demonstration purposes only. 
//
//
//
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#define SMTP_PORT 25
#define EHLO "EHLO %s"
#define MAIL_FROM "MAIL FROM: <%s>"
#define RCPT_TO "RCPT TO: <%s>"
#define DATA "DATA"
#define QUIT "QUIT"
#define BUFLEN 512
#define DIE(CODE,MSG) if(CODE < 0){perror(MSG);return EXIT_FAILURE;}    
#define EREPLY(CODE,EXPECTED) if (CODE/100 != EXPECTED){return EXIT_FAILURE;} 
#define READLINE(LABEL,BUFFER,MAXSIZE) printf(LABEL); fgets(BUFFER,MAXSIZE, stdin); BUFFER[strlen(BUFFER)-1]='\0';

FILE *client_socket_stream_in;
FILE *client_socket_stream_out;

/* 
 * Reads SMTP reply and returns its code.
 *
 * The format for multiline replies requires that every line, except the
 * last, begin with the reply code, followed immediately by a hyphen,
 * "-" (also known as minus), followed by text.  The last line will
 * begin with the reply code, followed immediately by <SP>, optionally
 * some text, and <CRLF>. */
int recv_smtp_reply()
{
    char line[1024];
    char strcode[4];
    int code = 0;
    memset(strcode, 0, 4);
    do {
        memset(line, 0, 1024);
        fgets(line, 1024,client_socket_stream_in);
        printf("S:%s", line);
        if (code==0)
        {
            memcpy(strcode, line, 3);
            code = atoi(strcode); 
        }
    } while (line[3] == '-');   
    return (code);
}

/*
 * Sends a single SMTP command. A command can have parameters.
 * 'cmd' is formatting string using the style of printf-family of functions.
 * It returns a status code replied by the server.
 *
 * Parameters:
 *   cmd - command with formatting options for parameters.
 */
int send_smtp_command(char *cmd, ...)
{
    va_list args;
    va_start(args, cmd);
    /* send the command */
    printf("C:"); vprintf(cmd, args); printf("\r\n");
    va_start(args, cmd);
    vfprintf(client_socket_stream_out, cmd, args);
    va_end(args);
    fprintf(client_socket_stream_out, "\r\n");
    fflush(client_socket_stream_out);   // necessary otherwise the data is not sent!
    return recv_smtp_reply();
}

/* 
 * All functionality is implemented in this main procedure. It 
 * parses input arguments, creates socket and connects to server, 
 * ask user for information, and exchanges data with SMTP server. 
 */ 
int main (int argc, const char * argv[])
{
    int client_socket;
    int error_code = 0;
    char buffer[128];
    char message[1024];
    
    if (argc <= 1)
    {
        perror("Usage: messenger -s SMTP_SERVER\n");
        return EXIT_FAILURE;
    }
    
    char *server_name = NULL;
    int c;
    while((c = getopt(argc, (char * const *)argv, "s:")) != -1)
        switch (c)
        {
            case 's':
                server_name = strdup(optarg);
                break;
            default:
                perror("Invalid argument.\n");
                perror("Usage: messenger -s SMTP_SERVER\n");
                return EXIT_FAILURE;
        }

    // This block parses server name and using DNS 
    // functions retrieves corresponding IP address.
    struct hostent *he = gethostbyname(server_name);
    if (he == NULL)
    {
        switch(h_errno)
        {
            case HOST_NOT_FOUND:
                perror("Server not found.");
                return EXIT_FAILURE;
            case NO_ADDRESS:
                perror("Server's address not found.");
                return EXIT_FAILURE;
            case NO_RECOVERY:
            case TRY_AGAIN:
                perror("DNS error.");
                return EXIT_FAILURE;
        }
    }

    // Thi sblock creates a new socket descriptor and connects to SMTP server.
    // In case of any error the program is terminated.
    client_socket = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    DIE(client_socket,"Could not create a socket.");

    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(SMTP_PORT);
    memcpy(&server_address.sin_addr, he->h_addr_list[0], he->h_length);
    error_code = connect(client_socket, (const struct sockaddr*)&server_address, sizeof(server_address));
    DIE(error_code,"Could not connect to the server.");

    // Following block creates two streams associated 
    // with the client_socket descriptor.
    // By this we can use usual stream oriented functions.
    client_socket_stream_in = fdopen(client_socket, "r");
    client_socket_stream_out = fdopen(client_socket, "w");
    
    int smtp_reply_code;
    // We implement a simple SMTP session:
    // An SMTP session is initiated when a client opens a connection to a
    // server and the server responds with an opening message.
    smtp_reply_code = recv_smtp_reply();
    // Once the server has sent the welcoming message and the client has
    // received it, the client normally sends the EHLO command to the
    // server, indicating the client's identity.
    char hostname[1024];
    memset(hostname,0, 1024);
    gethostname(hostname, 1023);
    smtp_reply_code = send_smtp_command(EHLO, hostname);
    EREPLY(smtp_reply_code,2);
    // There are three steps to SMTP mail transactions.  The transaction
    // starts with a MAIL command which gives the sender identification.
    READLINE("Mail from:", buffer, 128); 
    smtp_reply_code = send_smtp_command(MAIL_FROM, buffer);
    EREPLY(smtp_reply_code,2);
    // This command is used to identify an individual recipient of the mail
    // data. 
    READLINE("Receipt to:", buffer,128)
    smtp_reply_code = send_smtp_command(RCPT_TO, buffer);
    EREPLY(smtp_reply_code,2);
    // Data should follow RFC822 specification. We only consider 
    // Subject line and Content, in this demo.
    READLINE("Subject:", buffer,128);
    READLINE("Message:", message,1024);
    // The receiver normally sends a 354 response to DATA, and then treats
    // the lines following the command as mail data from the sender.
    smtp_reply_code = send_smtp_command(DATA);
    EREPLY(smtp_reply_code,3);
    fprintf(client_socket_stream_out,"Subject: %s\r\n", buffer);
    fprintf(client_socket_stream_out,"\r\n");
    fflush(client_socket_stream_out); // only for demonstration of TCP data comm.
    fprintf(client_socket_stream_out,"%s\r\n",message);
    // The mail data is terminated by a line containing only a period.
    fprintf(client_socket_stream_out,".\r\n");
    fflush(client_socket_stream_out); // This is really necessary!
    printf("C:Sending data...\n");
    smtp_reply_code = recv_smtp_reply();
    // QUIT
    smtp_reply_code = send_smtp_command(QUIT);
    shutdown(client_socket, SHUT_RDWR);
    return EXIT_SUCCESS;
}