---
title: Docker in Debian
url: https://www.4rknova.com/blog/2023/03/15/docker-debian
author: Nikolaos Papadopoulos
published: '2023-03-15'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

This post is a summary of how to setup Docker under Debian, and use the compose plugin to run services. Most of the information presented here is copied verbatim from the sources listed in the reference section below.

# Setting up docker and docker-compose

First remove any older versions of docker that are already installed in the system, and then install some useful tools.

$ sudo apt purge docker docker-engine docker.io containerd runc $ sudo apt update $ sudo apt install ca-certificates curl gnupg lsb-release

Next, add Docker’s official GPG key.

$ sudo mkdir -m 0755 -p /etc/apt/keyrings $ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

Setup Docker’s official repository for Debian.

$ echo \ "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \ https://download.docker.com/linux/debian \ $(lsb_release -cs) stable" \ | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

Finally, install the Docker engine:

$ sudo apt update $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

Docker is now installed and ready to use.

# Create configuration for compose plugin

Create a docker-compose.yml file with the configuration of the services you wish to run. For an example, click [here](https://docs.docker.com/get-started/08_using_compose/)

Start the services with:

$ docker compose up -d

Stop the services with:

$ docker compose down

Execute a shell inside a container with:

$ docker container exec -it container_name /bin/bash

# Cleaning up

To remove all images which are not used by existing containers, use:

$ docker image prune -a