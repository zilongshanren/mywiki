---
title: Login Forms over HTTPS, Please – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/01/login-forms-over-https-please/
author: Tanvi Vyas
published: '2016-01-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Update: This feature is now also enabled in Firefox Beta, starting with Firefox Beta 50.**

Pretty much everyone who uses the web has used a password to log into something. And pretty much everyone who has used a password has put that password at risk by entering it into an insecure form.

In [Firefox 46 Developer Edition](https://www.mozilla.org/en-US/firefox/developer/), we display a prominent warning to developers about this risk. When a page with a password field is not delivered securely, Firefox displays a lock with a red strikethrough in the address bar:

![Firefox Developer Edition 46 shows a struck-through lock icon for non-secure pages that have a password field](../../assets/99317e20f70b5388.png)


If you’re submitting your login form over HTTPS, that’s good, but it’s not enough. You have to **deliver** the form over HTTPS too. If the login form isn’t delivered over a secure channel, then an attacker can inject JavaScript code to steal the user’s password — *every character the user types can be stolen by the attacker*.

We’re releasing this feature in Developer Edition, since developers are ultimately the ones that need to make logins more secure on the sites they build. (There are no current plans to show these warnings to users of Beta and general release Firefox.) We’ve been displaying a warning in the [Developer Tools Web Console](https://developer.mozilla.org/en-US/docs/Web/Security/Insecure_passwords#Webconsole_Messages) for a long time; adding the struck-through lock icon to the URL bar makes the issue more prominent.

You can read more about this feature [here](http://blog.mozilla.org/tanvi/2016/01/28/no-more-passwords-over-http-please/).

## About
[
Tanvi Vyas ](https://blog.mozilla.org/tanvi/)

Security/Privacy Engineer and Tech Lead at Mozilla - @TanviHacks

## 12 comments

Bjarni R. EinarssonJanuary 29th, 2016 at 08:02Tanvi VyasJanuary 29th, 2016 at 10:06ChrisJanuary 29th, 2016 at 09:45Robert ThilleJanuary 29th, 2016 at 09:57Germ TorrentezJanuary 29th, 2016 at 13:06alloJanuary 29th, 2016 at 14:24voracityJanuary 30th, 2016 at 18:33FabioJanuary 31st, 2016 at 02:47zdiditFebruary 5th, 2016 at 08:30234234February 11th, 2016 at 10:40AlbertFebruary 22nd, 2016 at 19:00Wellington Torrejais da SilvaFebruary 24th, 2016 at 14:18