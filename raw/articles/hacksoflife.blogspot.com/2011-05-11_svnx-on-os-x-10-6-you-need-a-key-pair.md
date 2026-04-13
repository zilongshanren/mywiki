---
title: SvnX on OS X 10.6? You Need a Key Pair
url: http://hacksoflife.blogspot.com/2011/05/svnx-on-os-x-106-you-need-key-pair.html
author: Benjamin Supnik
published: '2011-05-11'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One minor hitch: SvnX can't log into a server that uses svn+ssh as its access method if ssh requires a manually typed password.

The work-around is to establish a private/public key pair for ssh. Once you do that, keychain will offer to store the password, and SvnX can function normally.

In theory sshkeychain should let the key chain remember plain passwords, but I couldn't get this to work on 10.6.

The keypair can be established as follows:

`cd ~/.ssh`

ssh-keygen -t rsa

(type desired password, accept default file name)

scp id_rsa.pub you@server.com:/home/you/.ssh/auhorized_keys

(where "you" is your unix login name. authorized_keys may need a different name for different servers.)

Instead of using scp to copy the public key into place, use



ReplyDeletessh you@yourserver.com 'cat - >> .ssh/authorized_keys' < id_rsa.pub

so you don't inadvertently overwrite existing public keys on the remote machine.