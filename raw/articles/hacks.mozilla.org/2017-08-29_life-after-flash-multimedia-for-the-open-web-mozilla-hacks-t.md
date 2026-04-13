---
title: 'Life After Flash: Multimedia for the Open Web – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2017/08/life-after-flash-multimedia-for-the-open-web/
author: Dustin Driver
published: '2017-08-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Flash delivered video, animation, interactive sites and, yes, ads to billions of users for more than a decade, but [now it’s going away](https://hacks.mozilla.org/2017/08/flash-in-memoriam/ ). Adobe will [drop support for Flash by 2020](https://www.theverge.com/2017/7/25/16026236/adobe-flash-end-of-support-2020). Firefox [no longer supports Flash out of the box](https://blog.mozilla.org/futurereleases/2017/07/25/firefox-roadmap-flash-end-life/), and [neither does Chrome](https://www.theverge.com/2016/12/9/13903878/google-chrome-block-flash-html5). So what’s next? There are tons of open standards that can do what Flash does, and more.

**Truly Open Multimedia**

Flash promised to deliver one unifying platform for building and delivering interactive multimedia websites. And, for the most part, it delivered. But the technology was never truly open and accessible, and Flash Player was too resource-hungry for mobile devices. Now open-source alternatives can do everything Flash does—and more. These are the technologies you should learn if you’re serious about building tomorrow’s interactive web, [whether you’re doing web animation](https://developer.mozilla.org/en-US/docs/Web/API/Animation), [games](https://developer.mozilla.org/en-US/docs/Games), or [video](https://developer.mozilla.org/en-US/docs/Plugins/Flash_to_HTML5/Video).

**Web Animation**


**CSS**

[CSS animation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations) is relatively new, but it’s the easiest way to get started with web animation. CSS is made to style websites with basic rules that dictate layout, typography, colors, and more. With the release of CSS3, animations are now baked into the standard, and as a developer, it’s up to you to tell the browser how to animate. CSS is human readable, which means it basically does what it says on the tin. For example, the property “animation-direction,” does exactly that: specifies the direction of your animation.

Right now you can create smooth, seamless animations with CSS. It’s simple to create [keyframes](https://en.wikipedia.org/wiki/Key_frame), adjust timing, animate opacity, and more. And all the animations work with anything you’d style normally with CSS: text, images, containers, and so on.

You can do animation with CSS, even if you’re unfamiliar with programming languages. Like many open-source projects, the [code is out there on the web for you to play around with](https://daneden.github.io/animate.css/). Mozilla has also created (and maintains) [exhaustive CSS animation documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations). Most developers recommend using CSS animation for simple projects and JavaScript for more complex sites.

**JavaScript**

Developers have been animating with JavaScript since the early days. Basic mouseover scripts have been around for more than two decades and today JavaScript, along with HTML5 [<canvas>](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_usage) elements, can do some pretty amazing things. Even simple scripts can [yield great results](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_animations). With JavaScript, you can draw shapes, change colors, move and change images, and animate transparency. JavaScript animation uses the [SVG](https://developer.mozilla.org/en-US/docs/Mozilla/Mozilla_SVG_Project) (scalable vector graphics) format for animations, meaning artwork is actually drawn live based on math rather than being loaded and rendered. That means they remain crisp at any scale (thus the name) and can be completely controlled. SVG offers anti-aliased rendering, pattern and gradient fills, sophisticated filter-effects, clipping to arbitrary paths, text and animations. And, of course, it’s an open standard W3C recommendation rather than a closed binary. Using SVG, JavaScript, and CSS3, developers can create [impressive interactive animations](http://slides.com/sdrasner/svg-can-do-that#/) that don’t require any specialized formats or players.

JavaScript animation can be very refined, including bouncing, stop, pause, rewind, or slow down. It’s also interactive and can be programmed to respond to mouse clicks and rollovers. The new [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API), built with JavaScript, lets you fine-tune animations with more control over keyframes and elements, but it’s still in the early, experimental phases of development and some features may not be supported by all browsers.

Additionally, JavaScript animations can be programmed to respond to input fields, form submissions, and keystrokes. And that makes it perfect for building web games.

## Web Games

At one time, Flash ruled web games. It was easy to learn, use, and distribute. It was also robust, able to deliver massively multiplayer online games to millions. But today it’s possible to deliver the same—if not better—experience using JavaScript, HTML5, WebGL and WebAssembly. With modern browsers and open-source frameworks, it’s possible to [build 3D action shooters, RPGs, adventure games, and more](https://developer.mozilla.org/en-US/docs/Games/Introduction). In fact, you can now even create fully immersive virtual reality experiences for the web with technologies like [WebVR](http://vr.mozilla.org) and [A-Frame](https://aframe.io/).

Web games rely on an ecosystem of open-source frameworks and platforms to work. Each one plays an important role, from visuals to controls to audio to networking. The Mozilla Developer Network has a [thorough list of](https://developer.mozilla.org/en-US/docs/Games/Introduction) technologies that are currently in use. Here are just a few of them and what they’re used for:

[ WebGL
](https://developer.mozilla.org/en-US/docs/WebGL)Lets you create high-performance, hardware-accelerated 3D (and 2D) graphics from Web content. This is a Web-supported implementation of

[OpenGL ES](http://www.khronos.org/opengles/)2.0. WebGL 2 goes even further, enabling OpenGL ES 3.0 level of support in browsers.

[ JavaScript
](https://developer.mozilla.org/en-US/docs/JavaScript)JavaScript, the programming language used on the Web, works well in browsers and is getting faster all the time. It’s already used to build thousands of games and new game frameworks are being developed constantly.

[ HTML audio
](https://developer.mozilla.org/en-US/docs/HTML/Element/audio)The

[<audio>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio)element lets you easily play simple sound effects and music. If your needs are more involved, check out the

[Web Audio API](https://developer.mozilla.org/en-US/docs/Web_Audio_API)for real audio processing power!

[ Web Audio API
](https://developer.mozilla.org/en-US/docs/Web_Audio_API)This API for controlling the playback, synthesis, and manipulation of audio from JavaScript code lets you create awesome sound effects as well as play and manipulate music in real time.

[ WebSockets
](https://developer.mozilla.org/en-US/docs/WebSockets)The WebSocket API lets you connect your app or site to a server to transmit data back and forth in real-time. Perfect for multiplayer turn-based or even-based gaming, chat services, and more.

[ WebRTC
](https://developer.mozilla.org/en-US/docs/Glossary/WebRTC)WebRTC is an ultra-fast API that can be used by video-chat, voice-calling, and P2P-file-sharing Web apps. It can be used for real-time multiplayer games that require low latency.

[ WebAssembly
](https://research.mozilla.org/webassembly/)HTML5/JavaScript game engines are better than ever, but they still can’t quite match the performance of native apps.

[WebAssembly](https://research.mozilla.org/webassembly/)promises to bring near-native performance to web apps. The technology

[lets browsers run compiled C/C++ code](https://hacks.mozilla.org/2017/07/webassembly-for-native-games-on-the-web/), including games made with engines like

[Unity](https://unity3d.com/)and

[Unreal](https://www.unrealengine.com/en-US/what-is-unreal-engine-4).

With WebAssembly, web games will be able to [take advantage of multithreading](https://hacks.mozilla.org/2017/07/webassembly-for-native-games-on-the-web/). Developers will be able to produce staggering 3D games for the web that run close to the same speed as native code, but without compromising on security. It’s a tremendous breakthrough for gaming — and the open web. It means that developers will be able to build games for any computer or system that can access the web. And because they’ll be running in browsers, it’ll be easy to integrate online multiplayer modes.

Additionally, there are many [HTML5/JavaScript game engines](https://github.com/bebraw/jswiki/wiki/Game-Engines) out there. These engines take care of the basics like physics and controls, giving developers a framework/world to build on. They range from lightweight and fast, like [atom](https://github.com/nornagon/atom) and [Quick](https://github.com/diogoschneider/quick) 2D engines, to full-featured 3D engines like [WhitestormJS](https://github.com/WhitestormJS/whs.js) and [Gladius](https://github.com/gladiusjs/gladius-core). There are dozens to choose from, each with their own unique advantages and disadvantages for developers. But in the end, they all produce games that can be played on modern web browsers without plug-ins. And most of those games can run on less-powerful hardware, meaning you can reach even more users. In fact, games written for the web can run on tablets, smartphones, and even smart TVs.

MDN has [extensive documentation on building web games](https://developer.mozilla.org/en-US/docs/Games/Introduction) and several tutorials on building games using [pure JavaScript](https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript) and the [Phaser game framework](https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_breakout_game_Phaser). It’s a great place to start for web game development.

## Video

Most video services have already switched to HTML5-based streaming using web technologies and open codecs; others are sticking with the [Flash-based FLV or FV4 codecs](https://en.wikipedia.org/wiki/Flash_Video). As stated earlier, Flash video formats rely on software rendering that can tax web browsers and mobile platforms. Modern video codecs can use hardware rendering for video playback, greatly increasing responsiveness and efficiency. Unfortunately, there’s only one way to switch from Flash to HTML5: Re-encoding your video. That means converting your source material into HTML5-friendly formats via a free converter like [FFmpeg](http://ffmpeg.org/) and[ Handbrake](https://handbrake.fr/).

Mozilla is actively helping to build and improve the HTML5-friendly and [open-source video format WebM](https://www.webmproject.org/). It’s based on the [Matroska](https://www.matroska.org/technical/whatis/index.html) container and uses [VP8](https://en.wikipedia.org/wiki/VP8) and [VP9](https://www.webmproject.org/vp9/) video codecs and [Vorbis](http://www.vorbis.com/) or [Opus](http://www.opus-codec.org/) codecs.

Once your media has been converted to an HTML5-friendly format, you can repost your videos on your site. HTML5 has built-in media controls, so there’s no need to install any players. It’s as easy as pie. Just use a single line of HTML:


<video src="videofile.webm" controls></video>

Keep in mind that native controls are inconsistent between browsers. Because they’re made with HTML5, however, you can [customize them with CSS](https://developer.mozilla.org/en-US/Apps/Fundamentals/Audio_and_video_delivery) and link them to your video with JavaScript. That means you can build for accessibility, add your own branding, and keep the look and feel consistent between browsers.

HTML5 can also handle adaptive streaming with [Media Source Extensions (MSEs)](https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API). Although they may be difficult to set up on their own, you can use [pre-packaged players](https://en.wikipedia.org/wiki/Media_Source_Extensions#Players) like [Shaka Player](https://github.com/google/shaka-player) and [JW Player](https://www.jwplayer.com/) that can handle the details.

The developers at MDN have created an in-depth [guide for converting Flash video to HTML5 video](https://developer.mozilla.org/en-US/docs/Plugins/Flash_to_HTML5/Video) with many more details on the process. Fortunately, it’s not as difficult as it seems.

**Flash Forward **

The future of the web is open ([hopefully](https://advocacy.mozilla.org/en-US/net-neutrality/)) and Flash, despite being a great tool for creatives, wasn’t open enough. Thankfully, many open source tools can do what Flash does, and more. But we’re still in the early stages and creating animations, interactive websites, and web games takes [some coding knowledge](https://developer.mozilla.org/en-US/). Everything you need to know is out there, just waiting for you to learn it.

Open web technologies promise to be better than Flash ever was, and will be accessible to anyone with an Internet connection.

## About Dustin Driver

Journalist, tech writer, and video producer helping Mozilla keep the Web open and accessible for everyone.

## 3 comments

RichardAugust 31st, 2017 at 14:56Gaurav GangopadhyayAugust 31st, 2017 at 21:34Dan ZenSeptember 2nd, 2017 at 19:11