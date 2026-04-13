---
title: Introducing TogetherJS – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/10/introducing-togetherjs/
author: Ian Bicking
published: '2013-10-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## What is TogetherJS?

We’d like to introduce [TogetherJS](https://togetherjs.com), a real-time collaboration tool out of [Mozilla Labs](https://mozillalabs.com).

TogetherJS is a service you add to an existing website to add real-time collaboration features. Using the tool two or more visitors on a website or web application can see each other’s mouse/cursor position, clicks, track each other’s browsing, edit forms together, watch videos together, and chat via audio and [WebRTC](https://developer.mozilla.org/en-US/docs/WebRTC).

Some of the features TogetherJS includes:

- See the other person’s cursor and clicks
- See scroll position
- Watch the pages a person visits on a page
- Text chat
- Audio chat using WebRTC
- Form field synchronization (text fields, checkboxes, etc)
- Play/pause/track videos in sync
- Continue sessions across multiple pages on a site

## How to integrate

Many of TogetherJS’s features require no modification of your site. TogetherJS looks at the DOM and determines much of what it should do that way – it detects the form fields, detects some editors like [CodeMirror](http://codemirror.net/) and [Ace](http://ace.c9.io/), and injects its toolbar into your page.

All that’s required to try TogetherJS out is to add this to your page:

```
```

And then create a button for your users to start TogetherJS:

```
```

If you want to see some of what TogetherJS does, [jsFiddle](http://jsfiddle.net) has enabled TogetherJS:

![jsfiddle with Collaborate highlighted](../../assets/95f604a866c5ab93.png)


Just click on **Collaboration** and it will start TogetherJS. You can also *use* TogetherJS in your fiddles, as we’ll show below.

## Extending for your app

TogetherJS can figure out some things by looking at the DOM, but it can’t synchronize your JavaScript application. For instance, if you have a list of items in your application that is updated through JavaScript, that list won’t automatically be in sync for both users. Sometimes people expect (or at least hope) that it will automatically update, but even if we did synchronize the DOM across both pages, we can’t synchronize your underlying JavaScript objects. Unlike products like [Firebase](http://www.firebase.com/) or the [Google Drive Realtime API](https://developers.google.com/drive/realtime/) TogetherJS does not give you realtime persistence – your persistence and the functionality of your site is left up to you, we just synchronize sessions in the browser itself.

So if you have a rich JavaScript application you will have to write some extra code to keep sessions in sync. We do try to make it easier, though!

To give an example we’d like to use a simple drawing application. We’ve published the [complete example as a fiddle](http://jsfiddle.net/ianbicking/5M57n/8/) which you can fork and play with yourself.

### A Very Small Drawing Application

We start with a very simple drawing program. We have a simple canvas:

```
```

And then some setup:

```
// get the canvas element and its context
var canvas = document.querySelector('#sketch');
var context = canvas.getContext('2d');
// brush settings
context.lineWidth = 2;
context.lineJoin = 'round';
context.lineCap = 'round';
context.strokeStyle = '#000';
```

We’ll use `mousedown`

and `mouseup`

events on the canvas to register our `move()`

handler for the `mousemove`

event:

```
var lastMouse = {
x: 0,
y: 0
};
// attach the mousedown, mousemove, mouseup event listeners.
canvas.addEventListener('mousedown', function (e) {
lastMouse = {
x: e.pageX - this.offsetLeft,
y: e.pageY - this.offsetTop
};
canvas.addEventListener('mousemove', move, false);
}, false);
canvas.addEventListener('mouseup', function () {
canvas.removeEventListener('mousemove', move, false);
}, false);
```

And then the `move()`

function will figure out the line that needs to be drawn:

```
function move(e) {
var mouse = {
x: e.pageX - this.offsetLeft,
y: e.pageY - this.offsetTop
};
draw(lastMouse, mouse);
lastMouse = mouse;
}
```

And lastly a function to draw lines:

```
function draw(start, end) {
context.beginPath();
context.moveTo(start.x, start.y);
context.lineTo(end.x, end.y);
context.closePath();
context.stroke();
}
```

This is enough code to give us a very simple drawing application. At this point if you enable TogetherJS on this application you will see the other person move around and see their mouse cursor and clicks, but you won’t see drawing. Let’s fix that!

### Adding TogetherJS

TogetherJS has a “hub” that echoes messages between everyone in the session. It doesn’t interpret messages, and *everyone’s* messages travel back and forth, including messages that come from a person that might be on another page. TogetherJS also lets the application send their own messages like:

```
TogetherJS.send({
type: "message-type",
...any other attributes you want to send...
})
```

to send a message (every message must have a `type`

), and to listen:

```
TogetherJS.hub.on("message-type", function (msg) {
if (! msg.sameUrl) {
// Usually you'll test for this to discard messages that came
// from a user at a different page
return;
}
});
```

The message types are namespaced so that your application messages won’t accidentally overlap with TogetherJS’s own messages.

To synchronize drawing we’d want to watch for any lines being drawn and send those to the other peers:

```
function move(e) {
var mouse = {
x: e.pageX - this.offsetLeft,
y: e.pageY - this.offsetTop
};
draw(lastMouse, mouse);
if (TogetherJS.running) {
TogetherJS.send({type: "draw", start: lastMouse end: mouse});
}
lastMouse = mouse;
}
```

Before we send we check that TogetherJS is actually running (`TogetherJS.running`

). The message we send should be self-explanatory.

Next we have to listen for the messages:

```
TogetherJS.hub.on("draw", function (msg) {
if (! msg.sameUrl) {
return;
}
draw(msg.start, msg.end);
});
```

We don’t have to worry about whether TogetherJS is running when we register this listener, it can only be called when TogetherJS is running.

This is enough to make our drawing live and collaborative. But there’s one thing we’re missing: if I start drawing an image, and you join me, you’ll only see the *new* lines I draw, you won’t see the image I’ve already drawn.

To handle this we’ll listen for the `togetherjs.hello`

message, which is the message each client sends when it first arrives at a new page. When we see that message we’ll send the other person an image of our canvas:

```
TogetherJS.hub.on("togetherjs.hello", function (msg) {
if (! msg.sameUrl) {
return;
}
var image = canvas.toDataURL("image/png");
TogetherJS.send({
type: "init",
image: image
});
});
```

Now we just have to listen for this new `init`

message:

```
TogetherJS.hub.on("init", function (msg) {
if (! msg.sameUrl) {
return;
}
var image = new Image();
image.src = msg.image;
context.drawImage(image, 0, 0);
});
```

With just a few lines of code TogetherJS let us make a live drawing application. Of course we had to do some of the code, but here’s some of the things TogetherJS handles for us:

- Gives users a URL to share with another user to start the session
![Screenshot of invitation window](../../assets/0335fbc9bea51a6a.png)

- Establishes a WebSocket connection to our
[hub server](https://github.com/mozilla/togetherjs/blob/develop/hub/server.js), which echoes messages back and forth between clients - Let’s users set their name and avatar, and see who else is in the session
![Screenshot of avatar/name setting](https://hacks.mozilla.org/wp-content/uploads/2013/10/screenshot-name-avatar-250x325.png)

- Keeps track of who is available, who has left, and who is idle
- Simple but necessary features like text chat are available
![Screenshot of chat window](https://hacks.mozilla.org/wp-content/uploads/2013/10/screenshot-chat-250x275.png)

- Session initialization and tracking is handled by TogetherJS

Some of the things we didn’t do in this example:

- We used a fixed-size canvas so that we didn’t have to deal with two clients and two different resolutions. Generally TogetherJS handles different kinds of clients and using resolution-independent positioning (and even works with responsive design). One approach to fix this might be to ensure a fixed aspect ratio, and then use percentages of the height/width for all the drawing positions.
- We don’t have any fun drawing tools! Probably you wouldn’t want to synchronize the tools themselves – if I’m drawing with a red brush, there’s no reason you can’t be drawing with a green brush at the same time.
- But something like clearing the canvas
*should*be synchronized. - We don’t save or load any drawings. Once the drawing application has save and load you may have to think more about what you want to synchronize. If I have created a picture, saved it, and then return to the site to join your session, will your image overwrite mine? Putting each image at a unique URL will make it clearer whose image everyone is intending to edit.

## Want To Look At More?

- Curious about the architecture of TogetherJS? Read the
[technology overview](https://togetherjs.com/docs/#technology-overview). [Try TogetherJS out on jsFiddle](http://jsfiddle.net)- Find us via the
[button in the documentation](https://togetherjs.com/docs/): “Get Live Help” which will ask to start a TogetherJS session with one of us. - Find us
[on IRC](https://togetherjs.com/docs/#getting-help)in`#togetherjs`

on irc.mozilla.org. - Find the
[code on GitHub](https://github.com/mozilla/togetherjs), and please[open an issue](https://github.com/mozilla/togetherjs/issues/new)if you see a bug or have a feature request. Don’t be shy, we are interested in lots of kinds of feedback via issues: ideas, potential use cases (and challenges coming from those use cases), questions that don’t seem to be answered via our documentation (each of which also implies a bug in our documentation), telling us about potentially synergistic applications. - Follow us on Twitter:
[@togetherjs](https://twitter.com/togetherjs).

What kind of sites would you like to see TogetherJS on? We’d love to hear in the comments.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 35 comments

Phil LeggetterOctober 16th, 2013 at 03:05Robert Nyman [Editor]October 16th, 2013 at 03:15Ian BickingOctober 16th, 2013 at 08:11Ivan DejanovicOctober 16th, 2013 at 12:34Robert Nyman [Editor]October 16th, 2013 at 13:05Ian BickingOctober 17th, 2013 at 11:34Eleftherios KosmasOctober 16th, 2013 at 13:45Marcel DupontOctober 16th, 2013 at 15:04Ben WerdmullerOctober 16th, 2013 at 14:57Robert Nyman [Editor]October 17th, 2013 at 00:50Brett ZamirOctober 16th, 2013 at 16:39Robert Nyman [Editor]October 17th, 2013 at 00:50Mike ConleyOctober 16th, 2013 at 20:06Robert Nyman [Editor]October 17th, 2013 at 00:51Ian BickingOctober 17th, 2013 at 11:27Mike ConleyOctober 18th, 2013 at 12:26Jelle AkkermanOctober 17th, 2013 at 01:18Samuel BoschOctober 17th, 2013 at 01:35Ian BickingOctober 17th, 2013 at 11:32Vignesh SwaminathanOctober 17th, 2013 at 02:01Ian BickingOctober 17th, 2013 at 11:28Vignesh SwaminathanOctober 17th, 2013 at 21:45Carlos CabralOctober 17th, 2013 at 05:21Ian BickingOctober 18th, 2013 at 12:30Carlos CabralOctober 18th, 2013 at 12:47Bill McCoyOctober 17th, 2013 at 06:00Ian BickingOctober 18th, 2013 at 12:29Phil WolffOctober 17th, 2013 at 11:16Ian BickingOctober 18th, 2013 at 12:26Aaron DruckOctober 18th, 2013 at 14:03Arnaud SahuguetOctober 18th, 2013 at 12:29kmanOctober 18th, 2013 at 17:52ShaneOctober 19th, 2013 at 02:22JamesOctober 29th, 2013 at 17:11dotBufferOctober 29th, 2013 at 22:37