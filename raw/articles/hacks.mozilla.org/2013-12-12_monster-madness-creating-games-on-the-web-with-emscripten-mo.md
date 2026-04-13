---
title: Monster Madness – creating games on the web with Emscripten – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2013/12/monster-madness-creating-games-on-the-web-with-emscripten/
author: Jeremy Stieglitz
published: '2013-12-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When our engineering teams at Trendy Entertainment & Nom Nom Games decided on the strategy of developing one of our new Unreal Engine 3 games —[Monster Madness Online]— as a cross-platform title, we knew that a frictionless multiplayer web browser version would be central to this experience. The big question, however, was determining what essential technologies to utilize in order to bring our game onto the web. As a C++ oriented developer, we determined quickly that rewriting the game engine from the ground-up was out of the question. We’d need a solution that would allow us to port our existing code in an efficient manner into a format usable in the browser…

*TL;DR? Watch the video!*


## Playing the Field

We looked hard at the various options in front of us: FlasCC (a GCC Flash compiler), Google’s NaCl, a custom native C++ extension, or Mozilla’s Emscripten & asm.js.

In our tests, Flash ran slowly and had inconsistent behaviors between Pepper (Chrome) and Adobe’s plugin version. Combined with the increasingly onerous plugin requirement, we opted to look elsewhere for a more seamless, forward-thinking approach.

NaCl had the issue of requiring a walled-garden distribution site that would separate us from direct contact with our users, and also being processor-specific. pNaCL eliminated the walled-garden requirement and added dynamic code compilation support, but still had the issues of being processor-specific code necessitating in our view device-specific testing, and a potentially long startup time as the code would be linked on first run. Finally, only working in Chrome would be a dealbreaker for our desire to have our game run in all major browsers.

A custom plugin/extension with C++ would require lots of testing & maintenance efforts on our part to run across different browsers, processor architectures, and operating systems, and such an installation requirement would likely scare away many potential players.

As it turned out, for our team’s purposes the Emscripten compiler & asm.js proved to be the best solution to these challenges, and when combined with a set of other new-ish Web API’s, enabled the browser to become a fully featured platform for instant high-end 3D gaming. This just took a little trial & error to figure out exactly how we’d piece it together…and that’s what we’ll be reviewing here!

## First Steps into a Brave New World

We Trendy game engineers are primarily old-school C++ programmers, so it was something of a revelation that Emscripten could compile our existing application (built on Epic Game’s Unreal Engine 3) into asm.js optimized Javascript with little to no changes.

The primary Unreal Engine 3-specific code tweaks that were necessary to get the project to compile & run with Emscripten, were essentially… 1, 2, 3:

```
1.
// Esmcripten needs 4 byte alignment
FNameEntry* Allocate( INT Size )
{
#if EMSCRIPTEN
Size = Align( Size, 4 );
#endif
......
}
2.
// Script execution: llvm needs aligned data
#if EMSCRIPTEN
#define XFER(T)
{
T Temp;
if (!Ar.IsLoading())
{
appMemcpy(&Temp, &Script(iCode), sizeof(T));
}
Ar << Temp;
if (!Ar.IsSaving())
{
appMemcpy(&Script(iCode), &Temp, sizeof(T));
}
iCode += sizeof(T);
}
#else
#define XFER(T) { Ar << *(T*)&Script(iCode); iCode += sizeof(T); }
#endif
3.
// This function needs to synchronously complete IO requests for single-threaded Emscripten IO to work, so added a ServiceRequestsSynchronously() to the end of it which flushes & blocks till the IO request finishes.
FAsyncIOSystemBase::QueueIORequest()
```

No really, that was about it! Within a day of fiddling with it, we had our game’s Javascript ‘executable’ compiled & running in the browser. Crashing, due to not having a graphics API implememented -- but running with log output! Thankfully, we already had Unreal Engine3’s OpenGL ES2 version of the rendering subsystem ready to utilize, so porting the renderer to WebGL only took another day.

WebGL appeared to essentially have a superset of features compared to OpenGL ES2, so the shaders and methods used matched up by simply changing some API calls. In fact, we were able to do improvements by making use of WebGL’s floating point render targets for certain postprocessing effects, such as edge outlining and dynamic shadows.

![EmscriptenGamePost](https://hacks.mozilla.org/wp-content/uploads/2013/12/EmscriptenGamePost-500x281.jpg)


*Postprocessing makes everything prettier!*

## But how’s it run?

Now we had something rendering in the browser, and with a quick change to capture input, we could start playing the game and analyzing its performance. What we found was very encouraging: straight ‘out of the box’, in Firefox the asm.js version of the game was getting nearly 33% of the performance of the native executable. And this was comparing a single-threaded web application to the multi-threaded native executable (so really, not a fair comparison! ;). This was about 2x the performance we saw with our quick Flash port (which we still utilize as a fallback for older browsers that don’t yet support asm.js, though we eventually hope to deprecate entirely).

Its performance in Chrome was less astonishing, more towards 20% of native performance, but still within our target margins: namely, can it run on a 2011-model Macbook Air at 45-60 FPS (with Vsync disabled)? The answer, thankfully, was yes. We hope Google will continue to improve the performance of asm.js on their browser over time. But as it currently stands, we believe unless you’re making the browser version of ‘Crysis’ with this tech (which may not be far off), it seems you have enough performance even in Chrome to do most kinds of web games.

## Putting the Pieces into Place

So within a week from starting, we had turned our Unreal Engine 3 PC game into a well-running, graphically-rich web game. But where to take it from here? Well, it’d still need: Audio, Networking, Streaming, and Storage. Let’s discuss the various techniques used for each of these systems.

### Audio

This was a no-brainer, as there is only really one robust standardized web audio system apart from Flash: WebAudio. Again, this API matched up pretty well to its mobile cousin, OpenSL, for which we already had an integration. So once we switched out the various calls, we had .

There was an apparent issue in Mac Chrome where sounds flagged “looping” would sometimes never become destroyed, so we implemented a Chrome-specific hack to manually loop the sound, and filed a bug report with Google. Ah well, one thing we’ve seen with browser API’s is there’s not a 100% guarantee that every browser will implement the functionality to perfect specification, but it gets the job done!

### Networking

This proved a little trickier. First, we investigated WebRTC as used in the [Bananabread demo](https://developer.mozilla.org/en-US/demos/detail/bananabread), but WebRTC of course is for browser-to-browser communication which is actually not what we were looking to do. Our online game service uses a server-and-client architecture with centralized infrastructure, and so WebSockets is the API to utilize in that case. The tricky part is that we have to handle all the WebSockets incoming and outgoing data in JavaScript buffers, and then pass that along to the “C++” Emscripten-compiled game.

With some callbacks, this worked out, but we also had to take our UDP game server code and place the WebSockets TCP-style layer onto it -- some iteration was necessary to get the packets to be formatted in exactly the way that WebSockets expects, but once we did that, our browser game was communicating with our backend-hosted Linux dedicated game servers with no problems!

### Streaming & Storage

One advantage to being on the web is easy access to the browser’s asynchronous downloading functionalities to stream-in content. We certainly made use of this with our game, with the initial download clocking in at under 10 MB. Everything else streams in on-demand as you play using standard browser http download requests: Textures, Sound Effects, Music, even Skeletal Meshes and Level Packages. But the bigger question is how to reliably store this content. We don’t want to just rely on the browser cache, since it’s not good for guaranteed immediate gameplay loading as we can’t pre-query whether something exists on disk in the regular browser cache or not.

For this, we used the IndexedDB API, which lets us asynchronously save and retrieve data objects from a secure abstracted storage location. It works in both Chrome and Firefox, though it’s still finicky as the database can occasionally become corrupted (perhaps if terminated during async writes) and has to be regenerated. In the worst case, this simply results in a re-download of content the user already had received.

We’re currently looking into this issue, but that aside, IndexedDB certainly works well and has the advantage of providing our application standard file IO functionality, useful to store content that we download. (UPDATE: Firefox Nightly build as of 12/10 seems to automatically reset the IndexedDB storage if this happens and it may not recur.)

## Play it Now, and Embrace the Future!

While we still have more profiling and tweaking to, as we’re just now starting to use Firefox’s VTune support to symbolically profile the asm.js performance within the browser. Even still, we’re pretty pleased with where the things currently stand. But don’t take our word for it, please try it yourselves right here, no installation or sign-up required:

[Try our demo test anonymously In-browser Here!](http://www.playverse.com/Anonplayer/0-a2aadd1b76e14d0e848ea1de18dca4e8)

*(Please bear with us if our game servers limit access under load, we’re still testing our backend scalability!)*

We at Trendy envision a day when anybody can play any game no matter where they are or what device they happen to have, without friction or gateways or middlemen. With the right combination of these cutting-edge web technologies, that day can be today. We hope other enterprising game developers will join us in reaching players directly through the web, which thanks to Emscripten & asm.js, may well become the most powerful and far-reaching “game console” of all!

## About
[
Jeremy Stieglitz ](http://www.monstermadness.com)

Jeremy Stieglitz has been creating games & game technology since 2001, when he started co-developing "Reality Engine", a hobbyist 3D game engine that he sold to Epic Games in 2005. Since then, he has developed numerous Unreal Engine indie & studio titles, including Monster Madness: Battle for Suburbia and CellFactor. In 2009 he co-founded Trendy Entertainment, where he created Dungeon Defenders. For Dungeon Defenders 2, has has been focusing on Trendy's cross-platform Playverse online infrastructure, and recently founded Trendy-subsidiary "NomNom Games" to develop indie-scale titles for this service. He is a big believer in technology-driven cross-platform, device-agnostic game development, and the power of the Web to connect content creators directly to consumers with no barriers. Jeremy is the Co-Founder & Chief Technical Officer of Trendy Entertainment (www.trendyent.com), and the Director of Nom Nom Games (www.nomnomgames.com)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 11 comments

TomDecember 12th, 2013 at 11:28Jeremy StieglitzDecember 14th, 2013 at 21:45YuriDecember 13th, 2013 at 00:09Jeremy StieglitzDecember 14th, 2013 at 21:38ChristianDecember 13th, 2013 at 05:00TomJanuary 2nd, 2014 at 17:17Andre JaenischDecember 13th, 2013 at 07:58Paul IrishDecember 13th, 2013 at 12:18Jeremy StieglitzDecember 14th, 2013 at 21:37v792933579December 19th, 2013 at 04:31Karsten BruchDecember 29th, 2013 at 07:13