---
title: 'May Dev Derby: Show us what you can do with Websockets – Mozilla Hacks - the
  Web developer blog'
url: https://hacks.mozilla.org/2012/05/may-dev-derby-show-us-what-you-can-do-with-websockets/
author: John Karahalis
published: '2012-05-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The May [Dev Derby](https://developer.mozilla.org/demos/devderby) is underway. A monthly contest hosted by the [Mozilla Developer Network](https://developer.mozilla.org/), the Dev Derby gives you the chance to apply the technology you read about on this blog, push the web forward, and compete for fame, glory, and prizes.

![](../../assets/8edf1f06addeed39.png)


This month, we are excited to see what you can do with [Websockets](https://developer.mozilla.org/en/WebSockets). Websockets allow you to send messages to a server and receive event-driven responses in real time, without server polling. But this is about more than just sending messages. Websockets have been used in [BrowserQuest](https://hacks.mozilla.org/2012/03/browserquest/), [Rawkets](http://rawkets.com/), and many other highly interactive applications.

Setting up a Websockets demo is more involved than setting up a static demo, but we know you can do it. As long as you keep these three simple rules in mind, everything should work flawlessly.


- To use Websockets, you need a server to communicate with. Thankfully, free services like
[Heroku](http://www.heroku.com/)and[Nodejitsu](http://nodejitsu.com/#/)provide just that. - You do not need to use Heroku or Nodejitsu. If you use a different server, however, you must ensure that it has a signed SSL certificate.
- When building your demo, be sure to use the wss:// prefix (not the ws:// prefix) to specify the address of your server.

If you have any questions about setup, please let us know in the comments. We will work with you to resolve any issues you encounter. Otherwise, good luck and have fun!

*Want to get a head start on a future Derby? We are also accepting entries related to the WebGL (June Derby) and demos that push the limits of the web without using JavaScript (July Derby).*

## About
[
John Karahalis ](http://openjck.com)

John Karahalis is a software developer, a project manager, and a user experience enthusiast. He helps with web development on [mozilla.org](https://www.mozilla.org/) and project management on the [Mozilla Developer Network](http://developer.mozilla.org/), and he formerly led the [Dev Derby](https://developer.mozilla.org/demos/devderby) contest.

## 4 comments

Xeon06May 8th, 2012 at 21:15John KarahalisMay 9th, 2012 at 15:25PhilMay 24th, 2012 at 08:52John KarahalisMay 24th, 2012 at 13:27