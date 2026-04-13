---
title: Fixing Wordpress Auto-Update Issues
url: http://hacksoflife.blogspot.com/2011/08/fixing-wordpress-auto-update-issues.html
author: Benjamin Supnik
published: '2011-08-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

There are a ton of posts from people having trouble auto-updating WordPress.




When WordPress auto-updates your blog, it doesn't do so as the "apache" user that usually runs httpd. Instead it uses your ftp login to place files into the local file system as "you".


This is very clever because it means that you don't have to give apache cart blanche over your site, protecting you from web daemons run amock (or whatever it is that web developers worry about).


So the first key point is that you need to allow httpd to make FTP calls out to servers. That's where


comes in. This gives httpd permission to make outgoing network connections so that it can call up your server via FTP as you.


Without this you get the "Failed to connect to FTP server XXX" error (because httpd isn't allowed to make the outgoing connection - what's tricky here is that it is the client side of FTP that's failing, not your FTP server).


The second key point is that if you have multiple users administrating WP, things aren't going to go well. The ownership of plugins will be 644 with the only person who has write permissions being you. If another site admin tries to update, you get an error saying that WP couldn't remove the old version of the plugin.


I don't have a great solution for this yet. I'll update this post when we fix the problem.

[This is the post](http://www.nerdgrind.com/wordpress-automatic-upgrade-plugin-failed-or-not-working/)that has the solution to the underlying problem. I will try to explain why it works, since I totally misunderstood this the first time and without understanding it, it's hard to fix.When WordPress auto-updates your blog, it doesn't do so as the "apache" user that usually runs httpd. Instead it uses your ftp login to place files into the local file system as "you".

This is very clever because it means that you don't have to give apache cart blanche over your site, protecting you from web daemons run amock (or whatever it is that web developers worry about).

So the first key point is that you need to allow httpd to make FTP calls out to servers. That's where

`/usr/sbin/setsebool -P httpd_can_network_connect=1`

comes in. This gives httpd permission to make outgoing network connections so that it can call up your server via FTP as you.

Without this you get the "Failed to connect to FTP server XXX" error (because httpd isn't allowed to make the outgoing connection - what's tricky here is that it is the client side of FTP that's failing, not your FTP server).

The second key point is that if you have multiple users administrating WP, things aren't going to go well. The ownership of plugins will be 644 with the only person who has write permissions being you. If another site admin tries to update, you get an error saying that WP couldn't remove the old version of the plugin.

I don't have a great solution for this yet. I'll update this post when we fix the problem.

## No comments:

## Post a Comment