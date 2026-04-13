---
title: Automatic mounts using systemd
url: https://anteru.net/blog/2019/automatic-mounts-using-systemd
published: '2019-05-03'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

A few years ago, [I set up autofs](https://anteru.net/blog/2014/quick-guide-to-autofs-for-smb-and-nfs-shares-on-ubuntu) to handle my network shares. While this works, occasionally I ran into some issues with autofs, and of course it’s one more thing you need to setup & install. Recently I learned that [ systemd](https://wiki.freedesktop.org/www/Software/systemd/) can also handle automatic mounting. Turns out, that’s as easy as setting up autofs and it fixed some of the issues I’ve had with autofs, so without further ado – let’s convert an existing autofs mount to systemd!

In this blog post, I’ll set up a SMB share, pointing to a network share `//my-server/myshare`

. The share will be mounted to `/mnt/net/smb/myshare`

. If you want to follow along, make sure you remember which directory you’re using as the target – this will become important in a second.

Before I continue, a brief interlude – I’ve not pieced this together by myself, instead I heavily relied on several [blog](https://blog.tomecek.net/post/automount-with-systemd/) [posts](https://codingbee.net/rhcsa/rhcsa-automounting-using-systemd-and-autofs) and of course, [ServerFault](https://serverfault.com/questions/766506/automount-usb-drives-with-systemd). For the rest of the post I’ll be linking to the official documentation where you’re supposed to find all this stuff :)

We’ll be saving our configuration in `/etc/systemd/system`

, which is the [recommended location for units created by the administrator](https://www.freedesktop.org/software/systemd/man/systemd.unit.html). The first file we’ll create describes the mount point. This is done using a [mount unit](https://www.freedesktop.org/software/systemd/man/systemd.mount.html). One thing to note here is that the filename needs to follow the naming scheme described in the [unit](https://www.freedesktop.org/software/systemd/man/systemd.unit.html) documentation, which basically boils down to replacing `/`

with `-`

. `/mnt/net/smb/myshare`

turns into `mnt-net-smb-myshare.mount`

. The contents are relatively straightforward, with `What`

providing the source path, `Where`

the target, and `Type`

/`Options`

storing the [cifs options](https://linux.die.net/man/8/mount.cifs) that will be used to mount the share:

```
[Unit]
Description=myshare mount
[Mount]
What=//my-server/myshare
Where=/mnt/net/smb/myshare
Type=cifs
Options=rw,file_mode=0700,dir_mode=0700,uid=1000
DirectoryMode=0700
[Install]
WantedBy=multi-user.target
```


There’s nothing else to do here, you can use [ systemctl daemon-reload](http://man7.org/linux/man-pages/man1/systemctl.1.html) to reload the config, and inspect the mount, but right now it’s a regular mount and no auto-mounting is happening yet. For that, we need an

[automount unit](https://www.freedesktop.org/software/systemd/man/systemd.automount.html). It follows the exact same naming convention, except the file extension

*must*be

`.automount`

. This file contains the `[Automount]`

section, and it has one mandatory entry, `Where`

:```
[Unit]
Description=myshare automount
[Automount]
Where=/mnt/net/smb/myshare
[Install]
WantedBy=multi-user.target
```


This is the unit we want to enable and start automatically, so we need to perform the following steps:

`systemctl daemon-reload`

to reload the configuration`systemctl start mnt-net-smb-myshare.automount`

to start the unit – so we can use it right away`systemctl enable mnt-net-smb-myshare.automount`

to enable the auto-start of the unit

And that’s it, at this point, if we `cd`

into `/mnt/net/smb/myshare`

, we should see the unit get triggered. We can check this using `systemctl status mnt-net-smb-myshare.automount`

. The output will tell you which process triggered the mounting.

And that’s it! Other types of mounts work the same – I’m using the same setup for `nfs`

mounts. Thanks for reading!