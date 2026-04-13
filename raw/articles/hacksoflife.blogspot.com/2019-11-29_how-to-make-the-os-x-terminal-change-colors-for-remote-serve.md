---
title: How to Make the OS X Terminal Change Colors for Remote Servers
url: http://hacksoflife.blogspot.com/2019/11/how-to-make-os-x-terminal-change-colors.html
author: Benjamin Supnik
published: '2019-11-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A thing I have done is attempt to hard shut down my Mac using the shell (e.g. sudo shutdown -r) and accidentally taken down one of our servers that I was ssh'd into.


To fix this and generally have more awareness of what the heck I am doing, I use a .profile script to change the Terminal theme when logging into and out of remote servers via SSH.






I am not sure where this comes from - possibly





To fix this and generally have more awareness of what the heck I am doing, I use a .profile script to change the Terminal theme when logging into and out of remote servers via SSH.

echo BashRC

function tabc {

NAME=$1; if [ -z "$NAME" ]; then NAME="Default"; fi

osascript -e "tell application \"Terminal\" to set current settings of front window to settings set \"$NAME\""

}

function ssh {

tabc "Pro"

/usr/bin/ssh "$@"

tabc "Basic"

}

[here](https://www.rngtng.com/2011/01/14/mac-os-x-terminal-visual-indication-for-your-ssh-connection/), but I see a few web references and I don't know which one I originally found. I'm posting it here so that I can find it the next time I get a new machine.
(Redoing this was necessary because I didn't migration-assistant my new laptop, and since it was going to Catalina, that was probably for the best.)

The script goes into ~/.profile for OS X 10.14 and older, or ~/.zprofile for OS X 10.15.

> A thing I have done is attempt to hard shut down my Mac using the shell (e.g. sudo shutdown -r) and accidentally taken down one of our servers that I was ssh'd into.


ReplyDeleteOne of the laws of administering complex systems is that there’s never a single root cause of any outage. This might be an exception to that... 😉😆