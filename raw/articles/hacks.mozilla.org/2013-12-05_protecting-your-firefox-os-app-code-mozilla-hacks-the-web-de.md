---
title: Protecting your Firefox OS App code – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/12/protecting-your-firefox-os-app-code/
author: Harald Kirschner
published: '2013-12-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One question we get asked quite often about developing web applications using HTML5, CSS3, and JavaScript, is about how to conceal code. Reasons range from preventing cheating, protecting intellectual property, hiding encryption algorithms and others. Since JavaScript is executed on the client side, even on Firefox OS, the users can get access the code if they have the skills and spend the time. But don’t get the wrong idea! Applications on Android, iOS and most mobile platforms can be reverse engineered with effort and the right tools.

We will present some measures that make it harder for copycats to reveal your application’s code. In various degrees they will increase the effort, skills and tools required to get the code.

## Compressing your code

This is the starting point for most developers. Compressing your code reduces the file size by removing what the browser doesn’t need to run your application. It starts by stripping comments and unnecessary white space. This is a good first step as comments usually reveal a lot of information on how the code is working.

The next level is shortening names of local variables and functions, the so called mangling. As this removes the meaning on those symbols, it further reduces readability.

More advanced compression tools, like [UglifyJS](http://lisperator.net/uglifyjs/), will actually parse your JavaScript to analyze and transform it. This allows not just renaming local symbols but also rewriting conditions and loops into shorter expressions, joining variable declarations (hoisting) and removing unreachable code. The resulting file is not only smaller and less readable but in many cases also faster.

You can take this one step further with the Google Closure optimizer in Advanced mode. The tool allows settings for all the aforementioned transformations. Advanced mode is the most aggressive and requires [greater consideration](https://developers.google.com/closure/compiler/docs/api-tutorial3) when used, to ensure that the output runs just as the input. It will rename, inline and even remove functions, properties and variables, so you need to make sure to either reference all symbols correctly or annotate them. The extra work pays off as the result is highly compressed and even gains a performance boost. As an example, let’s see what can happen to this code:

```
document.onload = function() {
var shareImage = document.querySelector("#share-image");
function share() {
var imgToShare = document.querySelector("#image-to-share");
if (!imgToShare.naturalWidth) {
alert("Image failed to load, can't be shared");
return;
}
// Create dummy canvas
var blobCanvas = document.createElement("canvas");
blobCanvas.width = imgToShare.width;
blobCanvas.height = imgToShare.height;
// Get context and draw image
var blobCanvasContext = blobCanvas.getContext("2d");
blobCanvasContext.drawImage(imgToShare, 0, 0);
// Export to blob and share through a Web Activitiy
blobCanvas.toBlob(function (blob) {
var sharingImage = new MozActivity({
name: "share",
data: {
type: "image/*",
number: 1,
blobs: [blob]
}
});
});
};
shareImage.onclick = share;
};
```

Once we’ll run this code through [Google Closure](http://closure-compiler.appspot.com/home), the code will look like:

```
var b=document.querySelector("#share-image"),
c=document.querySelector("#image-to-share");b&&c&&
(b.onclick=function(){if(0
```
Of course, the further you are writing custom logic, the more the code will be obfuscated, as the tools cannot change names from reserved word, or core functions. There are many tools online, and you can choose the one that fit your need. Most web frameworks offer interchangeable libraries and build steps that bundle and compress your JavaScript sources. For smaller projects your IDE, like Sublime Text, can be extended with [packages](https://sublime.wbond.net/search/minify) available.

## Using Emscripten

Did you remember that we said JavaScript is interpreted code? Well, you can bend that rule. [Mozilla's Emscripten tool](https://github.com/kripken/emscripten/wiki) compiles C and C++ to JavaScript. The output isn't JavaScript as you know it. It behaves more like native code and manages its own memory (stack and heap) in pre-allocated typed arrays. This reduces garbage collection and makes inspecting the memory harder. The output also benefits from asm.js, a highly optimizable subset of JS, that runs on all modern browsers. If you are moving your app from native to the web you can just convert your existing libraries. But even if that doesn't apply, moving your protected code into a C/C++ library that you compile to JavaScript is the best option to get blazing performance with the added benefits of obfuscation.

## Using a web service

Compression and compilation isn't the safest solution as people still have access to your code: it's just a bit harder to understand the logic. On the other side, one technique that moves the code to a place you have more control over is to use a web service. Your secret logic would run as a server-side script that your application will call when needed. Someone might be able to inspect the in- and outgoing data but there is no way they will be able to view your logic without access to your server. The major downside is that this feature will be only available when the user is online.

Let's see a simple example on how you can achieve this with a Firefox OS app, and a Node.js script: let's say we would like to hide our super exceptional fantastic code to do the addition to two numbers. Here is a simple node.js script (the goal is not to teach node.js, but show you a working basic example):

"use strict";
var express = require('express');
var app = express();
// Set up express to parse body
app.use(express.json());
app.use(express.urlencoded());
app.use(express.multipart());
// Only one route for web service
app.post('/', function(req, res) {
// Convert parameters from request body
var firstNumber = parseInt(req.body.firstNumber, 10);
var secondNumber = parseInt(req.body.secondNumber, 10);
if (isNaN(firstNumber) || isNaN(secondNumber)) {
// Bad request, fail with 400 status
return req.send(400);
}
var result = firstNumber + secondNumber;
res.send({'result': result});
});
app.listen(8000);

Now in your app, you'll call this script by sending the values you want to add, and the script will return you the result. Of course, users can see the call you make, and the results you'll get, but they won't be able to see the magic behind the hidden function.

"use strict";
var firstNumber = 4;
var secondNumber = 5;
var data = new FormData();
data.append("firstNumber", firstNumber);
data.append("secondNumber", secondNumber);
var xhr = new XMLHttpRequest({mozSystem: true});
xhr.open("POST", "http://fharper-nodejs.nodejitsu.com", true);
xhr.onload = function() {
// Parse the response and do something with it
var response = JSON.parse(xhr.response);
console.log(response.result);
};
xhr.onerror = function() {
console.log("Magic failed");
};
xhr.send(data);

This code is just showing the web service pattern and not best practices. As any server, it still needs security measures to prevent exploits. Make sure you mask the request and response data by using a secure HTTPS connection. Control client access to your service by checking the Referrer and Origin HTTP headers but don't trust what you see as they can be faked. You can limit replaying request with malicious parameters by using adding a secret time-limited or single-use token. As you can see, having your code in a web service is keeping it off the client but opens different attack vectors you need to consider.

## Be proactive, open your code

Of course, the best approach is to open your code: make your application open source, choose the right license, and show to the rest of the world that you were the first to create this piece of art. Choose the technology you want: you will make it harder to copy your code, but there is never a way to hide your idea. You need to be proactive: you need to be one of the best in your domain. Show your expertise, innovate, add features faster than the competitor do, be relevant for your market, and believe in what you do. How many knock offs of Angry Birds can you find on the web or on any marketplace/store? I don't have the exact number, but I can definitely say with a lot of confidence, that it's many! Rovio had an amazing idea, and they were the first to make it a reality: they are always innovating with brand new levels, new games with the characters we like, and more. You, your children, myself, we want to play to the original one, not the copy. Replace Angry Birds with any app or games you like, and you'll understand what I mean.

You have access to an amazing platform that open the web like never before: take advantage of it, build that app you want, and make your idea a reality!

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## About
[
Frédéric Harper ](http://outofcomfortzone.net)

As a Senior Technical Evangelist at Mozilla, Fred shares his passion about the Open Web, and help developers be successful with Firefox OS. Experienced speaker, t-shirts wearer, long-time blogger, passionate hugger, and HTML5 lover, Fred lives in Montréal, and speak Frenglish. Always conscious about the importance of unicorns, and gnomes, you can read about these topics, and other thoughts at outofcomfortzone.net.


## 22 comments

Willy AguirreDecember 5th, 2013 at 09:51Frédéric HarperDecember 5th, 2013 at 10:08SunboXDecember 5th, 2013 at 10:04Frédéric HarperDecember 5th, 2013 at 10:09Lisa BrewsterDecember 5th, 2013 at 13:57Frédéric HarperDecember 5th, 2013 at 14:00SunboXDecember 6th, 2013 at 00:38SheldonDecember 8th, 2013 at 05:19Andrew WilliamsonDecember 9th, 2013 at 18:29LukeDecember 9th, 2013 at 19:08Frédéric HarperDecember 10th, 2013 at 08:04Brett ZamirDecember 5th, 2013 at 20:09Frédéric HarperDecember 6th, 2013 at 13:45LukeDecember 6th, 2013 at 20:52Frédéric HarperDecember 7th, 2013 at 05:42niutechDecember 7th, 2013 at 03:57Frédéric HarperDecember 7th, 2013 at 05:44SteveDecember 7th, 2013 at 22:30Frédéric HarperDecember 9th, 2013 at 09:24SouravDecember 15th, 2013 at 07:35Frédéric HarperDecember 16th, 2013 at 06:24SouravDecember 18th, 2013 at 08:16