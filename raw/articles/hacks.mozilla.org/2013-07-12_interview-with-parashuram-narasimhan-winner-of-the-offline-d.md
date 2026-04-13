---
title: Interview with Parashuram Narasimhan, winner of the Offline Dev Derby – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/interview-with-parashuram-narasimhan-winner-of-the-offline-dev-derby/
author: John Karahalis
published: '2013-07-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Parashuram Narasimhan won the Offline Dev Derby with The conference, his web utility for beating unreliable conference connectivity. Recently, I had the chance to learn more about Parashuram: his work, his ambitions, and his thoughts on the future of web development.*

## The interview

### How did you become interested in web development?

Like most computer science majors, I started with systems programming. However, during the early days of Firefox, I used to play around with [Venkman](https://developer.mozilla.org/docs/Venkman) (before Firebug) and other Firefox developer tools to take a peek at how web pages were written. The undocumented and nascent web platform got me interested, and I found myself hacking around the limitations of the web platform. That is how I started writing code for the web.

### Can you tell us a little about how The conference works?

The conference is a set of static [HTML](https://developer.mozilla.org/docs/Web/HTML) pages that sync data with a remote [CORS](https://developer.mozilla.org/docs/HTTP/Access_control_CORS) enabled CouchDB server. The Sync functionality is taken care by PouchDB which implements the Couch synchronization protocol.

With no server side code, all functionality and interactions are handled using on Backbone.js the browser. The static pages are styled using Twitter Bootstrap and are responsive for the mobile too.

### What was your biggest challenge in developing The conference?

[IndexedDB](https://developer.mozilla.org/docs/IndexedDB) is not supported by all browsers today. Given the nature of the application, it was important for it to run on mobile devices that are easiest to use between sessions in a conference. Getting WiFi right at conferences is also hard, and the application had to work great with flaky connectivity. I had to use [the IndexedDB polyfill](https://github.com/axemclion/IndexedDBShim) to ensure that it runs across all browser, and even on mobile platforms.

### What makes the web an exciting platform for you?

The openness of the web is the most exciting part. I just joined Microsoft Open Technologies and I am able to see how the open nature of the web is helping me with a lot of interesting projects at large scale. That combined with the current limitations is a great breeding ground for hackers and tinkerers to show amazing innovation. I like the idea of having to write once, and see it working everywhere. I am glad to see the web flowing out of the browser into systems like B2G and Windows 8.

### What new web technologies are you most excited about?

Offline storage has always been my favourite and I would love to see it gain more traction. I am also impressed by the work done on [pointer events](https://developer.mozilla.org/docs/Web/CSS/pointer-events) and the efficiency at which the W3C working group is finalizing the standards. I also follow [WebRTC](https://developer.mozilla.org/docs/WebRTC) and [CSS3](https://developer.mozilla.org/docs/Web/CSS/CSS3).

### If you could change one thing about the web, what would it be?

The web seemed to have frozen before the [HTML5](https://developer.mozilla.org/docs/Web/Guide/HTML/HTML5) revolution. This was the time when native applications seem to become popular. I wish the web platforms had moved as fast, so that app developers considered it an alternative to writing applications for specific platforms. Looks like its getting there though.

### Do you have any advice for other ambitious web developers?

In a project, the best code is the code that is not written. With so many web developers working on the web, I usually don’t have to reinvent the wheel and can always reuse someone else’s well tested code. It is good that I am embarrassed about the code I wrote in the past–it just tells me that I maturing as a programmer :P

## Further reading

[Building a Notes App with IndexedDB, Redis and Node.js](https://hacks.mozilla.org/2013/05/building-a-notes-app-with-indexeddb-redis-and-node-js/)[Embedding WebRTC Video Chat Right Into Your Website](https://hacks.mozilla.org/2013/05/embedding-webrtc-video-chat-right-into-your-website/)[There is no simple solution for local storage](https://hacks.mozilla.org/2012/03/there-is-no-simple-solution-for-local-storage/)