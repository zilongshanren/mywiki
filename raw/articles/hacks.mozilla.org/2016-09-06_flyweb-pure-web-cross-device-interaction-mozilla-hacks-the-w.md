---
title: FlyWeb – Pure Web Cross-Device Interaction – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/09/flyweb-pure-web-cross-device-interaction/
author: Kannan Vijayan
published: '2016-09-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

FlyWeb is an experimental project we’ve been prototyping from within the depths of Mozilla’s platform division. It started as a side-project late last year, and since then a small, ad-hoc team has been working on implementing a “version zero” of the concept. We’ve been tinkering for the last 6 months on an implementation, and it’s getting to the point where we feel comfortable talking about it, in particular to web developers and hardware hackers that might be interested in the ideas it proposes.

Fundamentally, we’re aiming for one goal: making it easy for people or devices that are physically close to stream applications and content to each other. To do that, we want to make it dead simple for someone to stand up a “local area web server”, and for a person with a browser to discover and connect to that local area web server. What gets built on top of that architecture is up to you and other developers/hackers.

FlyWeb servers can live on a web-page loaded on your computer or smartphone, or they can live on tiny hardware devices on your network. FlyWeb servers are not designed to be accessible to “the internet”, but instead only to people on the local network (i.e., people already in physical proximity).

The design of FlyWeb is simple. A FlyWeb server is a web server that advertises itself on the local network using [mDNS](https://en.wikipedia.org/wiki/Multicast_DNS). In [Firefox Nightly](http://nightly.mozilla.org/), we’ve added a small UI element that lets you list locally advertised FlyWeb services (off by default, and only activated if the `dom.flyweb.enabled`

config pref is true). When you select a service to connect to, the browser creates a unique “UUID hostname” for the service, and routes all URLs with that host to the service. Additionally, we extend Web APIs with a new `navigator.publishServer()`

function, which allows a web page to publish a FlyWeb server on the local network. The user will be prompted to allow the web page to do this.

There are two major classes of use cases this design supports. One class relates to interactions between browsers, and the other concerns interactions between browsers and “smart hardware” that wants to expose a UI to users. Both are handled with the same architecture.

### Browser To Browser Interactions

Let’s say you write a multiplayer game designed for smartphones. I’m not talking about MMORPGs here, but casual games meant to be played by a group in the same room. Like a digital Catan, Scrabble or poker. You have a couple of options:

#### 1. Write a smartphone app

This solution will work, but you’ll need to publish the app on an app store, and have everybody download the app before playing. If somebody wants to switch to a different game, they all have to download the other game. The app will need to use some native communication protocol for manually discovering and connecting the phones to each other.

#### 2. Write a web-based game

This is also a reasonable solution, but comes with some problems. Everybody has to visit the game website, and possibly make an account on the website (or receive some sort of unique token) which they use to coordinate with each other. Communication between the players has to be bounced through the server the game is hosted on, which means games requiring low-latency input are difficult or impossible. Furthermore, everybody playing has to be connected to the internet.

#### FlyWeb approach

Both of the above approaches cause significant user friction. With FlyWeb, you can design the game as a web game, but instead of using the cloud to enable multiplayer, the game itself can host a local multiplayer experience. Here’s how that would work:

- One person in the group loads the game website, and asks the game to start a new multiplayer session.
- The game calls
`navigator.publishServer()`

, a FlyWeb API, to publish a local-area server.`publishServer`

returns a`Promise`

that resolves to a`FlyWebPublishedServer`

object, on which the game binds event handlers for HTTP/WebSocket requests. - The friends all discover the game via their browser, and connect to it directly.
- When they connect, the host web page’s
`FlyWebPublishedServer`

event handlers are called. The host web page is acting as a web server, and serves a copy of itself to all the connectors (and keeps track of them). The “client” web pages can make a web socket connection back to the host web page if the game needs low-latency communications. - Everybody plays together. As far as the game is concerned, communication between the “host page” and the players’ pages is accomplished using standard web technologies like HTTP fetch requests and WebSockets.

No one needs to download apps, no one needs to register accounts, or cross-reference unique codes or anything complicated. Only the browser hosting the game needs to be connected to the internet to fetch the host “server” page (and with new web features like Service Workers, even that doesn’t require an internet connection). The game can be built on pure web protocols, and everything is low-latency and playable. Basically, multi-user experiences can be created without ANY supporting infrastructure outside of a local network, and a browser supporting FlyWeb.

As an example, Justin integrated FlyWeb into a Unity WebGL-based car racing demo, inspired by the 4-player split-screen Mario Kart gameplay, and Kannan held a quick gaming session at the Mozilla Toronto office:

In our example, a laptop browser acts as “the console”, and smartphone FlyWeb clients act as game controllers. The smartphone browser discovers and connects to the game server hosted on the laptop web page, and receives a “controller UI” web page. This controller page on the phone establishes a web socket connection back to the host page, and uses that for sending touch and steering input back.

If you have an Android phone and a laptop, you can play this demo today (and download the source code and hack it, if you want). Just visit [flyweb.github.io](https://flyweb.github.io/) and follow the instructions, then visit the “Showcase” section of the page for a link to the demo. The game is hosted via GitHub Pages and the source code is available in our [GitHub repo](https://github.com/flyweb/examples) under the “flyweb-gp” folder.

You can also take a look at the “flyfile” and “photo-wall” subfolders in that GitHub repo for much simpler demos of web-based file sharing between smartphones.

### Smart Hardware

Let’s say you are building a hardware device. Maybe it’s a fancy new thermostat, or your own home-made quadcopter. Great! Now you need a UI to control it. You have a few options at your disposal:

#### 1. Write a smartphone app

This is probably the first thing that’ll come to mind, but it has a few problems. Writing smartphone apps is hard. You need to set up a development environment, download an SDK/build tools and all the other stuff for your platform of choice. You need to write the app, compile it into a bundle and load it on your phone. If you want other people to be able to use your app easily, you need to publish it on an app store (hoping it gets accepted) and maintain it. It’s a HUGE hassle.

Additionally, you need to build this app for every different platform you want to target. Want to access it from your Windows or Mac laptop in addition to your phone? Write another app. Not exactly the most convenient developer experience.

#### 2. Build a web UI served from your device

This approach is a lot simpler. You don’t need to build a native app. The UI works on different platforms. You don’t need to host an app on an app store. You don’t need to build an app bundle to distribute for side-loading. But, accessing the UI is hard. You have to open up your browser, somehow figure out the device’s IP address, and type it in.

This approach is also error prone. If you later happen to access some other service with the same private IP, on some other local network (for example, 192.168.1.1:80), that service can steal the cookies stored by the first service. The services have to be careful about using caching because you might get the cached page for the first service when you visit the second service.

#### FlyWeb approach

FlyWeb’s approach is basically option 2, but with some extra magic. The first bit of magic is advertising over mDNS, and a browser UI to discover the service by name, instead of having to find out and type in an IP address manually. The second bit of magic is the unique hostname generation. Currently, every time you connect to a service, the browser generates a UUID to use as the hostname for that service. No two UUIDs will ever be shared between services, so we avoid issues like leaking cookies, or cache cross-contamination.

With the help of the amazingly talented [Kate Glazko](https://www.linkedin.com/in/yglazko), we built a demo of this approach with a Parrot AR quadcopter and a Raspberry PI (controlling the copter and exposing a FlyWeb server), and presented it in June 2016 at a Mozilla All-Hands meeting. Here’s a video of that demo:

The source code for this demo is also available in our [examples repo](https://github.com/flyweb/examples) (under the flyweb-quadcopter folder). We’ve built other demos on hardware as simple as the ESP8266, which is a $5 WiFi chip with an embedded microcontroller. FlyWeb servers can run on extremely minimal hardware. Even tiny, low-power devices can present extremely rich UIs because the web platform lets them dynamically stream their control UIs to a far more powerful smartphone or computer.

### What Next

Currently, this feature is implemented and exposed ONLY in Firefox Nightly (not in Aurora or Beta), and hidden behind a pref that’s off by default. The current implementation is basically a “version 0” implementation, which is enough to build some pretty amazing demos and get a taste for the potential of FlyWeb.

The team’s goal right now is to let early-adopter developers and enthusiasts play with this implementation and get feedback on the viability of the feature as a future “true” web standard. If you’re a web developer looking to create neat multi-user “local area” experiences, or you’re a hardware hacker looking for an easy way to give a UI to your creations, we hope you’ll take a look at this, play with it, and let us know what you think.

If you are excited by the potential of this feature, want to build things with it, or help with the implementation (our team has 2 people in it, we are not some massive project – this is very much an experimental “skunkworks” project), please visit us at [flyweb.github.io](https://flyweb.github.io). You can also chat with us on Slack at [mozflyweb.slack.com](https://mozflyweb.slack.com) (sign up [here](https://mozflyweb-slack-invite.herokuapp.com/)) or follow us on Twitter at [@MozFlyWeb](https://twitter.com/MozFlyWeb).

### Caveats

Please keep in mind that this is a very early-stage implementation. There are probably bugs and security issues. If you DO experiment with FlyWeb, we advise [creating a new Firefox profile](https://developer.mozilla.org/en-US/Firefox/Multiple_profiles) just for that purpose and recommend that you DO NOT browse the general web using that profile. Use a separate profile only for running FlyWeb demos or your own code.

Happy hacking! :)

## About Kannan Vijayan

Kannan is a systems developer that has built everything from web tools for RNA sequence analysis, to JIT compilers for Javascript engines, to infrared stacks for embedded OSes, to experimental new web platform technologies. Ask him about any of the above things if you have a few hours to waste getting your ears talked off.

## About
[
Justin D'Arcangelo ](https://github.com/justindarc)

Software engineer at Mozilla creating cutting-edge mobile web apps. Proud father, husband, musician, vinyl record aficionado and all-around tinkerer.

## 28 comments

EndylSeptember 6th, 2016 at 11:01Kannan VijayanSeptember 6th, 2016 at 12:48EndylSeptember 7th, 2016 at 01:01Kannan VijayanSeptember 7th, 2016 at 08:29EndylSeptember 7th, 2016 at 12:23Kannan VijayanSeptember 7th, 2016 at 14:18EndylSeptember 8th, 2016 at 01:45PerrySeptember 6th, 2016 at 20:22Kannan VijayanSeptember 7th, 2016 at 08:44Gervase MarkhamSeptember 7th, 2016 at 07:22Kannan VijayanSeptember 7th, 2016 at 08:45wrykSeptember 7th, 2016 at 08:31Kannan VijayanSeptember 7th, 2016 at 08:46wrykSeptember 7th, 2016 at 08:59wrykSeptember 8th, 2016 at 07:41Kannan VijayanSeptember 9th, 2016 at 08:46PierreSeptember 7th, 2016 at 12:43Kannan VijayanSeptember 7th, 2016 at 14:14PierreSeptember 18th, 2016 at 06:01Caspy7September 7th, 2016 at 21:58soSeptember 9th, 2016 at 04:06Kannan VijayanSeptember 9th, 2016 at 08:52Justin D’ArcangeloSeptember 9th, 2016 at 10:05Kartik RishiSeptember 10th, 2016 at 18:43Justin D’ArcangeloSeptember 13th, 2016 at 11:08Jim PorterSeptember 29th, 2016 at 11:31JakobSeptember 11th, 2016 at 12:28Chi-Jui WuSeptember 27th, 2016 at 22:30