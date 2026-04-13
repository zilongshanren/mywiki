---
title: 'The Side Projects of Mozillians: JSFiddle and Meatspac.es – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2013/12/the-side-projects-of-mozillians-jsfiddle-and-meatspac-es/
author: Louis Stowasser
published: '2013-12-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At Mozilla, we are happy to get the chance to work with a lot of talented people. Therefore, as an on-going series, we wanted to take the opportunity to highlight some of the exciting projects Mozillians work on in their spare time.

## JSFiddle

[JSFiddle](http://jsfiddle.net) is a tool to write web examples (in HTML, JavaScript and CSS) called ‘fiddles’. They can be saved and shared with others or embedded in a website which is perfect for blogs, documentation or tutorials. Created by [Piotr Zalewa](https://twitter.com/zalun).

Piotr: I wanted a tool that could help me check if my frontend code was working. I was active on the MooTools scene at the time and we needed a tool to support our users who had questions about the framework and specific bugs to solve. The community is the best motivation. There are about 2,000 developers creating and watching fiddles right now! Many big projects are using JSFiddle for docs (MooTools, HighCharts) or bug requests (jQuery).

I’m always logged in on the #mootools IRC channel and one day we had a small competition to see who could be the first to answer support questions with only one line of JavaScript code. A user asked a non-trivial question which needed to be answered with both HTML and JavaScript. Our usual workflow was to write an HTML file, run it locally in the browser, copy the code to a Pastebin site then share the link. No one knew of a tool that could do this. The next day I had a prototype created in the evening and it was well accepted. The working but ugly version was completed shortly after. [Oskar Krawczyk](https://twitter.com/oskar) joined as a designer and the project was ready to be shown to the world.

It started as Django and MySQL on the server side with MooTools as a frontend framework. Since then the only major change was adding Memcache. Currently we run JSFiddle on 12 servers sponsored by DigitalOcean. 2 database servers, 3 application servers, 2 Memcache, then static files and development servers. I would ideally like to have the database structured in a way that would be easier to scale. The database is huge and updating tables takes a lot of time.

JSFiddle was designed in the time when most of the JavaScript libraries were running under one framework only. We want to allow users to mix frameworks and add more languages. At the moment you can write in HTML, JavaScript, Coffeescript, CSS and SCSS but I would like to support more languages. We’ve got a full hat of ideas to be implemented but I think it’s better to provide improvements than promises.

## Meatspac.es

[Meatspac.es](https://chat.meatspac.es) is a single public channel chat app that generates animated GIFs of users from their camera once they submit a new message. Created by [Jen Fong](https://twitter.com/ednapiranha) with GIF library support added by [Sole Penadés](https://twitter.com/supersole).

Jen: I’ve been working on various quirky chat apps that involved some form of embedded media so this was an idea I had about getting users to interact beyond typing by posing for the camera and doing a little movement. I also really like GIFs and the fact that they work everywhere. I had been playing with WebRTC here and there and Sole was working on her [RTCamera](https://developer.mozilla.org/en-US/Apps/Reference_apps/rtcamera) app when I thought: “Could we combine the two worlds? Chat and GIFs?”.

For the web server I used Nginx which proxies to a long running Node process using Express. The messages and GIFs are stored temporarily in LevelDB with a TTL (time-to-live) that deletes the message, including the GIFs stored as Base64 blobs, after 10 minutes. On the client-side, it uses jQuery, some GIF library files and updates with WebSockets with an AJAX fallback.

The biggest challenge of the project was surprisingly not code related! It was largely keeping up with all the craziness when a flood of people started using the chat, tweeting at me and contacting me. I first mentioned it publicly at ‘RealTimeConf’ in Portland a few weeks prior then started tweeting about it. After that a bunch of people checked it out, and someone posted it on Hacker News where even more people came (around 8,000 people on the heaviest day). It was mentioned on Twitter and various sources for a few days after.

People can be really creative during their GIF creation. It was also interesting to watch people give each other humorous ‘-bro’ nicknames; both women and men. They would always ask others what their name should be rather than giving themselves a name.

I am now working on a similar app but for one to many GIF chatting for Firefox OS called chatspaces. Anyone who is interested in contributing can watch the [repository](https://github.com/meatspaces/meatspace-chat) and check the README for what to contribute.

## About
[
Louis Stowasser ](http://louisstowasser.com)

I am a Partner Engineer for Mozilla, maintainer of [Gamedev Weekly](http://gamedevweekly.com) and creator of the [CraftyJS](http://craftyjs.com) game engine, based in Brisbane Australia.

## About Piotr Zalewa

Piotr Zalewa is a Senior Web Developer at Mozilla's Dev Ecosystem team. Working on web apps. He is the creator of JSFiddle.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.