# IPK project Docker

## Motivation
**\*\*ck VM. I don't want to use it.**

## Usage
```bash
docker-compose up --build
```
get docker container id
```bash
docker ps
```
connect to docker container
```bash
docker exec -it <container_id> /bin/bash
```


## Requirements
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

# Main issue
* On M1 Macs with docker on Colima. When sending request to server,
 you get 0 response, because socket is not connected directly to application,
 but to docker container.

# That means:
If you want to send request to server, you need to do it directly from docker container.

If anyone knows how to fix it, please let me know. And create Issue or PR.

If you using VSCode, you can use [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension to connect to docker container.

# PS
`src/client.c` is copy of `Stubs/cpp/DemoTcp/client.c`. Not my code, do what ever you want with it. 

# Questions
If you have any questions, feel free to contact me on:  
* Discord - `Pomo#1707`  
* Telegram - `@Mark_Eting` (more active)

## License
None. Do what ever you want with this code.