---
title: 'Inside the Party Bus: Building a Web App with Multiple Live Video Streams
  + Interactive Graphics – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2014/04/inside-the-party-bus-building-a-web-app-with-multiple-live-video-streams-interactive-graphics/
author: Bill Stinson
published: '2014-04-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Gearcloud Labs is exploring the use of open technologies to build new kinds of shared video experiences. Party Bus is a demo app that mixes multiple live video streams together with interactive graphics and synchronized audio. We built it using a combination of node.js, WebSockets, WebRTC, WebGL, and Web Audio. This article shares a few things we learned along the way.

## User experience

First, [take a ride](http://mixology.gearcloudlabs.com/partybus/mixer3d.html) on the Party Bus app to see what it does. You need Firefox or Chrome plus a decent GPU, but if that’s not handy you can get an idea of the app by watching the [example video on YouTube](https://www.youtube.com/watch?v=BKLDKIwZs6o).

Since the app uses [WebRTC](http://www.webrtc.org/) getUserMedia(), you have to give permission for the browser to use your camera. After it starts, the first thing you’ll notice is your own video stream mounted to a seat on the 3D bus (along with live streams from any other concurrent riders). In most scenes, you can manipulate the bus in 3D using the left mouse (change camera angle), scroll wheel (zoom in/out), and right mouse (change camera position). Also try the buttons in the bottom control bar to apply effects to your own video stream: from changing your color, to flipping yourself upside down, bouncing in your seat, etc.

![](../../assets/2c72ad68f7eeaca7.png)


## How party bus uses WebRTC

Party Bus uses WebRTC to set up P2P video streams needed for the experience. WebRTC does a great job supporting native video in the browser, and punching out firewalls to enable peer connections (via [STUN](http://en.wikipedia.org/wiki/STUN)). But with WebRTC, you also need to provide your own signaler to coordinate which endpoints will participate in a given application session.

The Party Bus app uses a prototype platform we built called [Mixology](http://gearcloudlabs.com/introducing-mixology/) to handle signaling and support the use of dynamic peer topologies. Note that many apps can simply use [peer.js](http://peerjs.com/), but we are using Mixology to explore new and scalable approaches for combining large numbers of streams in a variety of different connection graphs.

For example, if a rider joins a bus that already has other riders, the system takes care of building the necessary connection paths between the new rider and peers on the same bus, and then notifying all peers through a WebSocket that the new rider needs to be assigned a seat.

Specifically, clients interact with the Mixology signaling server by instantiating a Mixology object

`var m = new Mixology(signalerURL);`

and then using it to register with the signaler

`m.register(['mix-in'], ['mix-out']);`

The two arguments give specific input and output stream types supported by the client. Typing inputs and outputs in this way allows Mixology to assemble arbitrary graphs of stream connections, which may vary depending on application requirements. In the case of Party Bus, we’re just using a fully connected mesh among all peers. That is, all clients register with the same input and output types.

The signaler is implemented as a [node.js](http://nodejs.org) application that maintains a table of registered peers and the connections among them. The signaler can thus take care of handling peer arrivals, departures, and other events — updating other peers as necessary via callback functions. All communications between peers and the signaler are implemented internally using WebSockets, using [socket.io.](http://socket.io)

For example, when a new peer is registered, the server updates the topology table, and uses a callback function to notify other peers that need to know about the new connection.

`m.onPeerRegistered = function(peer) { ... }`

In this function, peers designated to send streams initiate the WebRTC offer code. Peers designated to receive streams initiate the WebRTC answer code (as well as provide a callback function onAddStream() to be used when the new input stream is ready).

In the case of Party Bus, it’s then up to the app to map the new video stream to the right seat in the 3D bus model, and from then on, apply the necessary 3D transforms using three.js. Similarly, if a rider leaves the bus, the system takes care of notifying other clients that a peer has exited, so they can take appropriate action to remove what would otherwise be a dead video stream in the display.

Party Bus organizes the “riders” on a bus using an array of virtual screens:

`var vsArray = new Array(NUM_SEATS);`

After registering itself with Mixology, the app receives a callback whenever a new peer video stream becomes available for its bus instance:

```
function onAddStream(stream, peerId) {
var i = getNextOpenSeat();
vsArray[i] = new VScreen(stream, peerId);
}
```

The Party Bus app creates a virtual screen object for every video stream on the current bus. The incoming streams are associated with DOM video objects in the virtual screen constructor:

```
function VScreen(stream, id) {
var v = document.createElement(‘video’);
v.setAttribute(“id”, “monitor:” + id);
v.style.visibility = “hidden”;
v.src = window.URL.createObjectURL(stream); // binds stream to dom video object
v.autoplay = “true”;
document.body.appendChild(v);
}
```

## Movie or app?

Party Bus uses [three.js](http://threejs.org/) to draw a double decker bus, along with virtual screens “riding” in the seats. The animation loop runs about two minutes, and consists of about a dozen director “shots”. Throughout the demo, the individual video screens are live, and can be manipulated by each rider. The overall sequence of shots is designed to change scene lighting and present other visual effects, such as bus thrusters which were created with the particle engine of [Stemkoski](http://stemkoski.github.io/Three.js/).

Party Bus is a web app, but the animation is programmed so the user can just let it run like a movie. The curious user may try to interact with it, and find that in most scenes it’s also possible to change the 3D view. However, in shots with a moving camera or bus, we found it necessary to block certain camera translations (movements in x, y, z position), or rotations (turning on x, y, z axis) — otherwise, the mouse will “fight” the program, resulting in a jerky presentation.

But most of the fun in Party Bus is just hamming it up for the camera, applying visual effects to your own stream, and looking for other live riders on the bus.

## More info

For more information on the Party Bus app, or to stay in the loop on development of the Mixology platform, please check out [www.gearcloudlabs.com](http://stemkoski.github.io/Three.js/).

## About
[
Bill Stinson ](http://www.gearcloudlabs.com)

Co-Founder of Gearcloud Labs. Previously, Bill led development of web/mobile apps and key operational systems at Verizon, GTE Labs, and Bell Labs. He is interested in mobile technology, computer vision, augmented reality, and robotics.

## About
[
Rob Chang ](http://www.gearcloudlabs.com)

Rob is Co-Founder of Gearcloud Labs. Prior to founding Gearcloud, Rob has worked at Verizon, Nokia, and a number of mobile startups.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 6 comments

jr conlinApril 1st, 2014 at 10:59Rob ChangApril 2nd, 2014 at 08:00Dev ResearchApril 9th, 2014 at 04:19Bill StinsonApril 11th, 2014 at 12:05Bad browserApril 9th, 2014 at 06:47Bill StinsonApril 11th, 2014 at 12:19