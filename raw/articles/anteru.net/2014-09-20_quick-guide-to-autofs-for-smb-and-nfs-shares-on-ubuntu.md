---
title: Quick guide to autofs for SMB and NFS shares on Ubuntu
url: https://anteru.net/blog/2014/quick-guide-to-autofs-for-smb-and-nfs-shares-on-ubuntu
published: '2014-09-20'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you have to work with network shares, you’re probably familiar with [fstab](http://en.wikipedia.org/wiki/Fstab) and auto-mounting them on boot. This is great if your server is always reachable, but it becomes cumbersome if the connection is lost. In case the target server goes down or is not yet up when the machine boots, you have to mount the directory as root. This is particularly bad if your network takes a long time to get online, for example, if you have a wireless connection.

There’s a much better and robust way, which is to use [autofs](http://linux.die.net/man/5/autofs). With autofs, the shares will be only mounted when required and also get unmounted after some time. It handles disconnects much more gracefully. The setup is pretty simple, but there aren’t too many guides around to help you get started. Here’s a quick-start guide for Ubuntu, other Linux distributions will be similar. In this guide, I’ll be setting up autofs to connect to a Linux [NFS](https://en.wikipedia.org/wiki/Network_File_System) share and to a password-protected Windows [SMB](https://en.wikipedia.org/wiki/Server_Message_Block) share.

## Preparation

You need to install autofs and cifs-utils. On Ubuntu, you can use `apt-get`

to get these. You’ll also need a folder where you want to mount your shares, in my case, this will be `/mnt/net/smb`

for SMB shares and `/mnt/net/nfs`

for NFS shares.

## Configuration

Every time you change something in the config, use `sudo service autofs restart`

to restart the autofs service.

The main configuration file is `/etc/auto.master`

. Here, we define the mapping of folders to shares. Let’s add the two directories from above:

```
/mnt/net/smb /etc/auto.cifs-shares
/mnt/net/nfs /etc/auto.network
```


This tells autofs to check `auto.cifs-shares`

when you try to access a share in `/mnt/net/smb`

, and similarly for nfs. The configuration files contain one share per line. The first part of the line is the directory name that will be used for the share, after that, you have to provide how the connection should be made and finally the target. Let’s take a look at auto.network and add a NFS share there. In my case, the contents are:

```
Shared -fstype=nfs,rw,soft,tcp,nolock homeserver:/tank/Shared
```


If I go into the `/mnt/net/nfs/Shared`

directory now, it will automatically connect to the `/tank/Shared`

NFS share from the machine called `homeserver`

. That was easy, wasn’t it? Next up, SMB shares, in `auto.cifs-shares`

:

```
home -fstype=cifs,rw,credentials=/home/anteru/.smbcredentials,file_mode=0777,dir_mode=0777 ://homeserver/anteru
```


This is slightly more complicated. You don’t want to save your SMB credentials in the `auto.cifs-shares`

file (which may be visible to every user), so I’ve stored them in `/home/anteru/.smbcredentials`

. This is a very simple file which looks like this:

```
username=anteru
password=swordfish
```


When connecting to a SMB share, you’ll likely want to add `file_mode=0777`

and `dir_mode=0777`

so everything created there is readable and writable by default for all users. This is needed because the share is mounted as root. You can also force it to be mounted as a specific user. Remove the `file_mode`

and `dir_mode`

and replace it with `uid=1000`

(1000 is my user id). To find your user id, run:

```
id -u username
```


Finally, there’s a slightly tricky bit which is shares containing `$`

characters. You need to escape them in the `auto.cifs-shares`

file using `\$`

, otherwise, you’ll get errors.

That’s it, hope this quick guide will help you to get started with autofs!