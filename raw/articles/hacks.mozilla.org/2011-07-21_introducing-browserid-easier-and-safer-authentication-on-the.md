---
title: Introducing BrowserID – easier and safer authentication on the web – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/07/introducing-browserid-easier-and-safer-authentication-on-the-web/
author: Robert Nyman
published: '2011-07-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Security on the web is more important than ever. Almost weekly reports of exploits of information and leaks into the public make it hard for a lot of people to trust the internet.

One of the main annoyances is that every service expect us to have a login and password. As we use lots of services this means we have to remember a lot of login names and passwords. People deal with this in various ways. The most dangerous is [using a simple password](http://onemansblog.com/2007/03/26/how-id-hack-your-weak-passwords/) across different services. Another way is to not bother remembering your secure password and instead re-set it every time you come back to the site you want to access by going through a verification by email. This could also be a very dangerous approach – especially when the site you log in to [sends your password as plain text](http://plaintextoffenders.com/) rather than forcing you to create a new one. In any case, you spend a lot of time running in circles between you, the site you want to access and your email client.

There were a few ideas in the past how to work around the issue of logins and passwords. [OpenID](http://openid.org/) was the most ambitious one, but failed to get traction in the main market as having a URL as your identifier seemed alien to a lot of end users.

Taking the lessons and learnings from the mistakes of OpenID and other approaches Mozilla Labs is now proposing [BrowserID](http://browserid.org/) which moves from domains and sites to emails as your main identifier. In essence, we promote the “password recovery” mechanism of the traditional login approach to your main point of access.

## What is BrowserID?

BrowserID aims to offer you one single log-in to web sites and services, connected through your e-mail address (with the option to add more than one e-mail to the same account). The core idea is that you will always remember your e-mail address instead of a made-up user name or URL.

The main pillars of BrowserID are:

- Ease of use
- Security
- Cross-browser implementation
- Decentralized, web-wide validation
- Improved experience in future browsers
- Respecting the privacy of the user

Using one e-mail address and a master password, you only need to activate and verify your account once. As BrowserID is implemented with the [Verified E-mail Protocol](https://wiki.mozilla.org/Labs/Identity/VerifiedEmailProtocol) it has built-in security. Furthermore it offers a verification service to check against.

It works cross-browser, both on desktop and mobile, and it’s decentralized so that anyone can chose to implement it on their web site. Respecting user privacy is a very important factor for Mozilla. Therefore no information is shared with any service about your BrowserID usage (check the [BrowserID Privacy statement](http://browserid.org/privacy) for more information).

What makes it even more enticing in the long run is that BrowserID could be implemented natively in the web browser, for example through the URL bar, where the user could choose to log in/out. This will make it an even more secure measure against [phishing](http://en.wikipedia.org/wiki/Phishing) and other attacks, and give end users the most consistent and reliable experience.

## Try it out

If you want to try an example, you can go to the [TextChannels web site](http://textchannels.com/), create a BrowserID account and sign in with it.

After you have created a BrowserID account at TextChannels, you can go to [our other test web site](http://myfavoritebeer.org/) and see how easy the experience is when you have a BrowserID account.

Here is a video explaining the procedure:

## How to implement BrowserID

If you want to use BrowserID in a web site, you have to go through three main steps:

- Enable BrowserID
- Identify the user
- Verify the User’s Identity

Enabling BrowserID is quite easy: simply include the [BrowserID JavaScript](https://browserid.org/include.js) in your web page. Then add an event handler to a sign in button in your web page. This button will be used to identify the user. When that is done, you need to verify that user’s identity on the server-side. This can be easily done through the BrowserID verification service.

Here’s some complete sample code:

```
```


When you successfully received the assertion, send a request to https://browserid.org/verify with two GET parameters. For instance:

```
$ curl "https://browserid.org/verify?assertion=
```&audience=mysite.com"

```
{
"status": "okay",
"email": "lloyd@mozilla.com",
"audience": "mysite.com",
"valid-until": 1308859352261,
"issuer": "browserid.org:443"
}
```

## How does it work?

If you want to delve deeper into the flow and inner workings of BrowserID, check the [How BrowserID Works](http://lloyd.io/how-browserid-works) article.

## BrowserID is experimental – help us

Please note that while Mozilla Labs is putting a lot of work and thought into BrowserID, its current state is experimental. That means that it is not recommended to use in any real-world production web sites at this moment.

BrowserID is something Mozilla believe to be very beneficial to the web, but we need your help! Please try BrowserID out as a user, play around with the code and give us feedback! We are working on making this a great asset for users and developers alike, and any input we get will make it easier and faster to reach that goal!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 17 comments

MardegJuly 21st, 2011 at 01:40Thomas SvensonJuly 21st, 2011 at 03:55zubJuly 21st, 2011 at 06:00askdksdJuly 21st, 2011 at 06:56AdrianJuly 21st, 2011 at 08:45louisremiJuly 21st, 2011 at 09:38AnonymousJuly 21st, 2011 at 08:48JPFSeptember 26th, 2011 at 04:23Robert NymanSeptember 27th, 2011 at 00:12Stephanie DaughertyJuly 21st, 2011 at 09:19JustinJuly 21st, 2011 at 11:27Robert Nyman [Mozilla – post author]July 22nd, 2011 at 04:47Stephanie DaughertyJuly 22nd, 2011 at 09:17Robert NymanJuly 22nd, 2011 at 13:46Dan MillsJuly 22nd, 2011 at 14:50RégisJuly 18th, 2012 at 01:29Robert NymanJuly 31st, 2012 at 08:40