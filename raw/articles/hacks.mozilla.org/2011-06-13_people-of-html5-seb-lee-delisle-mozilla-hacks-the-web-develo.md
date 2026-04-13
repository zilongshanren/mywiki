---
title: People of HTML5 – Seb Lee Delisle – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/06/people-of-html5-seb-lee-delisle/
author: Chris Heilmann
published: '2011-06-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![Seb](../../assets/ddf1c66386b048d7.jpg)

[Seb Lee Delisle](http://sebleedelisle.com/). Seb is a long-standing, award-winning Flash developer who lately focuses on “creative coding” independent of platform and technology.

In his workshops he makes web developers leave their comfort zone of defined and limited environments and shows what can be achieved if you play with technology rather than feeling hindered by it.

I’ve invited Seb as I see him as a great opportunity to learn from what the Flash world has been doing for years – in a lot of cases they already overcame problems the HTML5 world has yet to face.

## The video interview

You can [see the video on any HTML5 enabled device here](http://vid.ly/2m1w3f) (courtesy of vid.ly).

## Ten questions about HTML5 for Seb Lee Delisle

### 1) You are very known to give workshops and talk about very visual programming – creating beautiful, and highly technical stuff. How do people normally react and do you think we will see more of that in the mainstream?

Generally people seem to react really well! Particularly in the JavaScript community where people are now starting to discover the new creative possibilities in this medium. The part I love the most is showing how such simple code can create beautiful effects.

I’m already seeing subtle animated graphics crossing over into the mainstream – just look at what’s happening with the Google doodle lately. My job is to help programmers to develop a sensibility for animation and use it tastefully.

### 2) In the past you’ve been known as a pure Flash guy – and actually one of the few that released code outside the Flash community and tried to cross boundaries. Personally I am so tired of the “HTML5 as the Flash killer” and “Flash as the saviour of the web as it is truly cross-platform” arguments. How can we do more to break the barriers between the Flash and non-Flash communities?

Although known primarily for my (BAFTA winning ;-) ) Flash work, these days I seem to be growing into a polymath! In the last month I’ve worked in C++, Processing, JavaScript, and ActionScript and enjoy switching between them all.

The most important thing is to learn as much as we can about all technologies. Then you can make informed decisions about the best tool for the job.

I’m pleased to see other famous Flashers doing great work in JS. Mr Doob (of [three.js](http://mrdoob.com/blog/post/693)) used to be a Flash programmer and is an amazing visual coder. Grant Skinner is making a canvas graphics library called [Easel.js](http://easeljs.com/).

I think it’s unlikely that JSers will be keen to invest time into learning Flash, but it’s important to recognise the strengths of the plug-in and use it where appropriate.

### 3) Looking at the open web stack, what gets you most excited? Canvas? SVG? Processing? And why?

Canvas is fun but can be a bit CPU heavy if not treated with care. SVG is very interesting, particularly [Raphael.js](http://raphaeljs.com/) which is a library that neatly wraps SVG and falls back to VML – it even works in IE6! SVG is definitely under-used, particularly when IE9 can render it super fast with the GPU. But we’re lacking good tools to make animated content.

I love the Processing community and [Processing.js](http://processingjs.org/) makes things quite accessible, but for truly optimised canvas rendering you’re probably better off learning the native canvas API.

Canvas is the new thing so naturally everyone’s really excited about it but I think there’s still lots to explore in just moving DOM objects around. You get better backwards compatibility and often it’s faster than canvas.

### 4) What are the limits of open web technology? Where would you see the next phase of research into standards to go?

This is a really hard question to answer! I guess the biggest difficulty is the sheer number of different vendors that have to work together (or not ;-) ). But the proliferation of webkit means that we’re seeing browsers pop up in a variety of different devices from your eReader to your TV. As these devices get faster and faster it’s going to be a realistic possibility to have games and rich content everywhere. Whether we want that or not is a different matter!

Browsers are still far behind Flash in terms of video, camera access, socket connections and P2P. I would say the most important of these would be video. Browsers should just be able to play a video in the page. But this thorny codec issue doesn’t seem to be disappearing any time soon.

### 5) Beautiful things also need to perform well. What are your main tips to create smooth animations and interactions that don’t flicker?

This is a hugely wide ranging question! But it’s usually the rendering that’s the bottleneck, especially if you’re working on canvas. Only redraw pixels when you absolutely need to. I’ve just made a demo of the game Asteroids, where I move a little canvas around for the ship, rather than clearing a massive canvas every frame even when just a little bit of the screen needs updating.

If you’re moving DOM objects around, use the 3D CSS transform – even if you just set a z position of 0 you get hardware acceleration in webkit browsers. I’ve made a particle system that handles hundreds of DOM objects and is super fast, even on iOS.

And use `requestAnimationFrame`

rather than a `setInterval`

for your redraw loop. This ensures that you’ll sync with the monitor refresh rate avoiding screen tearing. Perhaps more importantly, it’s disabled when your browser tab isn’t visible which saves your battery.

### 6) A lot of the things we do when building games and animations is cheating. I remember working on very low-spec environments like Commodore 64 where you could have used real physics algos but found something much less computation heavy that did the job and relied on the human eye to be lazy and fix glitches for me. Is that what we still do?

It’s still what I do. There are very few resources that outline these easy solutions, most books are very advanced. I’ve accumulated and devised these techniques over the years which is why I love sharing and demystifying these techniques on my courses and presentations.

### 7) Where web design is very much fluent and you never know about resolutions and available screen space (which is why you test for it before you open for example a menu) most gaming seems to be within fixed boundaries. Canvas for example has a fixed size in pixels. Is that a limitation? I always found the unknown part of webdesign the thing that excited me the most as it meant my code has to be bullet-proof.

I agree, but of course this is a huge challenge if you’re building a game and you usually work to a fixed pixel size. Anything based around bitmaps is fixed although I guess you can scale them up and down. Even Flash games seem to use bitmaps these days. It’s ironic because Flash is very good at scaling vector graphics. Historically Flash games have been set to a fixed and small pixel size due to performance issues in the early FlashPlayer versions.

### 8) Animations just didn’t look right before libraries started implementing easing to simulate natural movement with acceleration and slowing things down naturally. The next step of that is bringing physics into animations. Is that easy these days?

There’s a technique that’s familiar to visual programmers – a real time ease-out that I like to call tweasing. In fact i made a library in Flash called Tweaser that wraps this technique. Traditional tweeners have a start and end point and a duration. Tweasing just has a target and the object eases towards it. If you keep a bit of momentum from the previous frame you can even implement a springy naturalistic movement.

The best reason for using this is that you can change the target at any time during the animation and your object updates its trajectory in a smooth way. It’s really powerful and responsive, especially with 3D. Check [tweaser.org](http://tweaser.org) for a full video explanation of the technique. Perhaps if enough people want it I’ll port it to JS!

### 9) What do you think will be the killer use for WebGL on the internet? I’ve played with Google’s Body Browser and I loved it – do you think the web and the open stack is ready for 3D or is Flash with Molehill still ruling that sector?

I’m not sure what the practical uses for in-browser 3D are yet. I expect we’ll probably see some pretty exciting 3D mapping from Google. But of course gaming is what everyone is excited about – it remains to be seen how these 3D gaming capabilities will affect the casual in-browser games market.

There’s something very pleasing about WebGL enabling GPU graphics right there within your browser, but it’s a big problem that IE has no plans to support it. Flash’s GPU enabled player (codename Molehill) has a huge advantage – FlashPlayer take up rates have been incredible with new versions of the player reaching 90% penetration within a few months. I don’t think there’ll ever be another plug-in with the penetration rates of Flash.

Both WebGL and Molehill have huge workflow issues, despite the open source libraries like three.js and Away3D. Thankfully Unity3D have announced that they’re targeting Molehill. Unity3D is truly a joy to work with – it seamlessly imports 3D models and bitmaps, has built in physics, lighting, shadows and a particle system. You even program it with a flavour of JavaScript! So if they could also target webGL…?

### 10) Inspiration time. What are things you think people should look at to catch the bug of visual programming and where are the tutorials to learn about them?

If you want code tips, you should look no further than [Keith Peters](http://www.bit-101.com/blog/). Keith is well known in the ActionScript world for his Making Things Move books. He’s just completed 30 JavaScript experiments in 30 days – well worth checking out.

Outside of JavaScript I’m hugely influenced by digital artists such as Robert Hodgin ([@flight404](http://twitter.com/flight404)), Chris O’Shea, Jared Tarbell, and Jer Thorp ([@blprnt](http://twitter.com/blprnt)), who all work in a variety of different programming languages.

It’s a really exciting time for interactive technology and in addition to my CreativeJS workshops, I’ll be continuing more large scale motion detection projection projects in openFrameworks and Processing.

Photo by [Andy Polaine](http://www.flickr.com/photos/apolaine/2921756307/in/photostream/)

Do you know anyone I should interview for “People of HTML5”? Tell me on Twitter: [@codepo8](http://twitter.com/codepo8)


## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## One comment

MeteorJune 14th, 2011 at 07:03