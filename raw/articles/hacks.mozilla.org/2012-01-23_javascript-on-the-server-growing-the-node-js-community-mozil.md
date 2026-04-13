---
title: 'JavaScript on the server: Growing the Node.js Community – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2012/01/javascript-on-the-server-growing-the-node-js-community/
author: Robert Nyman
published: '2012-01-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Cloud9 IDE](http://c9.io/) and Mozilla have been working together ever since their [Bespin and ACE](http://mozillalabs.com/skywriter/2011/01/18/mozilla-skywriter-has-been-merged-into-ace/) projects joined forces. Both organizations are committed to the success of Node.js, Mozilla due to its history with Javascript and Cloud9 IDE as a core contributor to Node.js and provider of the leading Node.js IDE. As part of this cooperation, this is a guest post written by Ruben Daniels and Zef Hemel of Cloud9 IDE.

While we all know and love JavaScript as a language for browser-based scripting, few remember that, early on, it was destined to be used as a server-side language as well. Only about a year after JavaScript’s original release in Netscape Navigator 2.0 (1995), [Netscape released Netscape Enterprise Server 2.0](http://www.thefreelibrary.com/NETSCAPE+INTRODUCES+NETSCAPE+ENTERPRISE+SERVER(TM)+2.0-a018056425):

Netscape Enterprise Server is the first web server to support the Java(TM) and JavaScript(TM) programming languages, enabling the creation, delivery and management of live online applications.


This is how the web got started, all the way back in the mid-nineties. Sadly, it was not meant to be then. JavaScript on the server failed, while JavaScript in the browser became a hit. At the time, JavaScript was still very young. The virtual machines that executed JavaScript code were slow and heavy weight, and there were no tools to support and manage large JavaScript code bases. This was fine for JavaScript’s use case in the browser at the time, but not sufficient for server-side applications.


Still, there are two obvious advantages that support this idea of using JavaScript not only in the browser, but on the server as well:

- Skill reuse. Developers only have to learn a single programming language that they can use for both client and server-side programming. Front-end developers can leverage their existing skills to build server applications too.
- Code reuse. The opportunity to write your code once and be able to run it on either client or server, opens up great opportunities. The most obvious example would be reusing code to validate forms, which you have to do on both sides anyway. But there are many more exciting opportunities to be explored, e.g. the ability to
[dynamically decide where to render your UI](http://ajaxian.com/archives/server-side-rendering-with-yui-on-node-js)(client or server, or a mix) based on device capabilities.

Over the past decade and a half, many projects have tried to reintroduce JavaScript on the server, but again and again there was very little uptake.

## A New Hope

Then, [Node.js](http://nodejs.org) happened. Node.js is the first implementation of JavaScript that people get genuinely excited about. Why is that? What makes Node.js different from previous attempts?

As it turns out, previous attempts dismissed one core, powerful and often overlooked feature of JavaScript: its single-threaded nature. JavaScript is single threaded in the browser. Nevertheless, previous server-side JavaScript implementations did have regular threading the way every server-side language does, like Java, Python or Ruby, for instance.

Node.js deliberately took a different path, the path more in line with browser JavaScript: Node.js is single threaded, and event based.

This has two advantages: it avoids concurrency issues and it supports the construction of super efficient high-performance servers.

Programming with threads is hard. Very hard. When things happen at the same time concurrency bugs can occur easily (e.g. two threads modifying the same piece of memory simultaneously), which are incredibly difficult to reproduce and fix. Courses are taught at universities to teach students how to avoid concurrency problems using locks, semaphores etc. Concurrency is difficult, it’s best to avoid it when possible — Node.js enables you to avoid concurrency by not supporting it at all, at least on a process level. In a Node.js process, only one thing happens at a time.

Servers built with Node.js are typically super fast and can handle thousands, tens of thousands, even hundreds of thousands of concurrent connections — something very difficult to achieve with threaded servers. How can that be?

It’s all based on the observation that server threads in typical web application servers spend most of their time doing nothing — just idly waiting for the result of a database query, waiting for the disk to spin and return a file that’s requested or waiting for data to come over the network. For every single connected client there’s a thread just sitting there, idly, using up resources.

Node.js servers work differently. Node.js uses asynchronous APIs for operations that require I/O such as fetching a file or sending a database query. This is exactly the same way AJAX calls work in the browser, as well as other recent asynchronous HTML5 JavaScript APIs such as various database APIs (IndexedDB and WebSQL) and Geolocation. All these APIs don’t want to block the browser thread, because it may take half a second or even multiple seconds to retrieve the results, which would freeze up the browser. Instead, they simply trigger the call and pass a callback function to be invoked when the results come in. In the mean time, the browser thread can keep rendering the page and do other things. This is *exactly* how any I/O API works in Node.js.

## The Node.js Community

The Node.js community has been growing rapidly over the past years. More and more companies build their servers with Node.js, especially for servers that require real-time communication and therefore have to handle a lot of simultaneous connections. As the real-time web grows, so will the use of Node.js.

Therefore, it is time to make Node.js more accessible to the developer community. To do this, Node.js needs a few things:

- Tooling
- Good documentation
- A community website with in-depth articles and tutorials
- Training

At [Cloud9 IDE](http://c9.io) we have set ourself the goal to build the best possible IDE for Node.js development. After all, Cloud9 IDE itself is a prime example of what we envision as the future of web development: Cloud9 IDE uses JavaScript front to back, using browser Javascript on the client and Node.js on the server.

Using Cloud9 IDE you can try out and play with Node.js without having to install anything. You can create Node.js projects, run, debug and deploy your project right from the IDE.

In collaboration with partners in the Node.js community, we are now launching three more initiatives:

[Nodebits.org](http://nodebits.org)is the new community website for Node.js developers with the latest news, in-depth articles and tutorials.[NodeManual.org](http://nodemanual.org)is the new one-stop source of Node.js documentation. The MDN of Node.js development, if you will.[Training](http://training.c9.io)provides three-day Node.js training courses for the enterprise.

Any example code used on Nodebits, NodeManual and our training material can be run in Cloud9 IDE with just a click of a button, lowering the barrier to try out the examples even more.

With these initiatives we aim to turn Node.js into the mainstream web development platform of the future: JavaScript front to back. It only makes sense.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 19 comments

jonJanuary 23rd, 2012 at 17:13RichJanuary 24th, 2012 at 00:13PedroJanuary 24th, 2012 at 01:20rob brownJanuary 24th, 2012 at 12:51Anand GeorgeJanuary 24th, 2012 at 20:16Joe ZhouJanuary 23rd, 2012 at 19:13dimas priyantoJanuary 23rd, 2012 at 22:33npivJanuary 23rd, 2012 at 23:45RABAHJanuary 24th, 2012 at 01:21Gian Angelo GeminianiJanuary 24th, 2012 at 05:21jonJanuary 24th, 2012 at 20:49TobyJanuary 24th, 2012 at 20:54Bogomil “Bogo” ShopovJanuary 26th, 2012 at 07:37JoeyJanuary 30th, 2012 at 09:55Buy CourseworkMarch 15th, 2012 at 00:23AlvinaApril 12th, 2012 at 10:47MikeJuly 3rd, 2012 at 20:31Master leeJanuary 24th, 2013 at 02:58Jeff NappiFebruary 6th, 2013 at 08:35