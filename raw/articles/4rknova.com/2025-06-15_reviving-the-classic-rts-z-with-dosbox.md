---
title: Reviving the classic RTS “Z” with DOSBox
url: https://www.4rknova.com/blog/2025/06/15/dos-game-z
author: Nikolaos Papadopoulos
published: '2025-06-15'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

If you’re a fan of classic RTS games, you might remember Z by the Bitmap Brothers, a gem from the 90s that’s well worth revisiting. Today, I’ll walk you through how to revive this old DOS game on a modern Linux system using DOSBox.

# Creating a backup image of your original game

Before we get started, it’s important to mention that you should create an ISO backup of your original Z game CD. This ensures you preserve the original media and can easily mount the game inside DOSBox. You can use `dd`

on Linux to create the ISO image. Make sure the ISO file `z.iso`

is placed in your game directory.

Assuming your CD is mounted at `/mnt/cdrom`

, issue the following:

cd game dd if=/mnt/cdrom of=z.iso bs=4M status=progress

`if=/mnt/cdrom`

specifies the input device (your mounted CD).`of=z.iso`

specifies the output ISO file.`bs=4M`

sets the block size.`status=progress`

shows progress while creating the ISO.

# DOSBox Configuration

In the same game directory, create an empty directory called `bin`

. Then create a file called `z.conf`

. This is the configuration file for DOSBox. We’ll use it to launch the game smoothly. Here are the contents of `z.conf`

:

```
[sdl]
fullscreen=false
[dosbox]
memsize=16
[autoexec]
@echo off
mount c bin
imgmount d "z.iso" -t iso -fs iso
c:
if not exist c:\Z goto install
goto play
:install
d:
install.exe
goto play
:play
c:
cd Z
Z.bat
```


This config mounts your local `bin`

directory as drive C and mounts the ISO image as drive D. This is where the game files are installed. It then automatically starts the installation for the game if it’s not already installed and runs it otherwise.

![01](../../assets/f8d8bbde7531d58e.png)


In the first run, you will need to install the game into the `bin`

directory. It’s a fairly straight forward process, just follow the prompts on the screen.

# Running the Game

To start the game easily, create a simple bash script named `start.sh`

:

```
#!/bin/bash
dosbox -conf "./z.conf"
```


Make sure to give it execute permissions with:

chmod +x start-z.sh

Simply run the script from your terminal:

./start-z.sh

DOSBox will handle mounting your ISO, installing *Z* if necessary, and then launch the game in a windowed mode. This setup lets you relive the fast-paced RTS action of *Z* on your modern Linux machine without fuss. Happy gaming!

# Screenshots

![The main title screen](../../assets/ebd11414488c1f7f.png)

![In-game screenshot](../../assets/b50518fb246c6cf9.png)