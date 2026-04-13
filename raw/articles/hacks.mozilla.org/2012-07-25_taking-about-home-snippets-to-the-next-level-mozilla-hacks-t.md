---
title: Taking About:Home Snippets to the Next Level. – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/07/taking-snippets-to-the-next-level/
author: Chris Heilmann
published: '2012-07-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If you are a Firefox user and you start the browser this morning or you type “[about:home](about:home)” in the URL bar we have a surprise for you. Instead of the Firefox logo you’ll see an animation celebrating the global spirit of community. This is just one of many planned enhancements to mozilla.org pages and mozilla communication channels.

To give you a peek under the hood and insight as to how this was made, we asked Bruce MacFarlane from [Particle](http://www.particlebrand.com) a few questions about the animation. Particle has been working with the top silicon valley companies exploring ways to use HTML5 and CSS since their beginning. They have a unique blend of talent that hovers between creative development and engineering which allows projects like this possible.

**1) Hi there, when you get asked to do an animation like that, what is the creative process? Do you make sketches, animate in a tool like Flash or Maya or do you start right away with the code?**

I find it helpful to sit with a step-by-step list of what is going to happen and really try to visualize the entire animation, getting a feel for how it will most likely function under the hood. If there’s anything I’m not quite sure how to handle I’ll break that out into a separate proof of concept sandbox file where I can just focus on that one thing and make sure I get it right. After that it’s easy to put all the parts together.

**2) What is the main technology behind the animation? Canvas? CSS? And why did you choose it?**

The animation was done entirely in CSS to take advantage of it’s ease of use and fluidity.

Although something similar could have been accomplished with Canvas, going that route would have required a lot more setup code and we wouldn’t have been able to take advantage of CSS3’s handy timing functions.

Also, being able to fire animation sequences with class names the same way you would work with basic styling is a huge plus.

In the case of this animation we were able to define just one keyframe that played with scaling and opacity, then applied that to all five flame layers, having the variations coming from just playing with the animation durations and delays.

**3) I assume that the start page of Firefox is a special environment. What were the limitations you had to work around in terms of performance and connectivity?**

Since the code that runs the animation is being loaded onto a pre-existing page, we do end up having to do a little bit of logic when it loads to adjust some of the initial content and move our new content into position before running the animation.

A Snippet is a single file of code that gets loaded onto a pre-existing page, therefor certain considerations have to be made. To remove additional requests for assets, any images have to be base64 encoded and entered directly in the code. This is much easier than it sounds. There are plenty of websites out there where you can upload an image and have it give you back it’s base64 encoding. I tend to use a couple of simple PHP commands that accomplish the same thing:

```
$image = file_get_contents('image.png');
$imagedata = base64_encode($image);
echo($imagedata);
```

Also if an animation has to interact with content that’s already on the screen (and may be positioned relatively, which can cause problems with animations) a certain amount of work has to be done to structure the previous content to work with the new content (wrapping the moving parts in a container that can still move in relation to window size so you can absolutely position elements within that you need to, etc.).

**4) When optimising you sometimes find yourself having to do the same tasks over and over again and build tools to do them. Did you use already existing tools or are you building some?**

Developing on Macs we end up using the ‘Activity Monitor’ utility app quite a lot which can really help with monitoring memory and CPU usage. About:home snippets are a unique animal in that only Firefox users ever see them. For sites and web applications that are being viewed on a diversity of devices and browsers we have developed some internal tools that help simplify compatibility issues and greatly aid in the quick construction of projects that we’ll be releasing soon.

**5) With your experience in this, do you think there is a market for animation tools that have output like the code you did? Do you know of any yet? There were a few around a year ago (Adobe Edge, Animatable…), but I haven’t seen any being pushed heavily.**

There are definitely some animations where the keyframes can get so complex that these sorts of tools could help out a lot and save time. We don’t have a favorite yet, but we’re keeping our eyes open.

**6) What about legacy support? Is it worth testing and tweaking on older browsers or does it make more sense to have a static image fallback?**

It is always important to support a certain amount of legacy browsers, static image fallbacks can sometimes be your only reasonable choice.

**7) If developers wanted to start with their own similar animations, what would you say is the biggest time-sink to avoid? What are good shortcuts?**

It’s sometimes easy to get bogged down in animations that have a lot of moving parts, and go on for a long time. In those situations I find it helps to break things down into scenes that can be fired off with parent container class names.

Sometimes in those scenes I’ll apply the same animation duration to each element and work within the keyframe percentages to handle timing. This way it’s easy add adjustments to individual elements during the timeline later.

Thanks Bruce.

What do you think? Expect to see more experiments like this showing off new technologies. Anything you’d like to see, or information you’d want us to publish? Just comment below.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 12 comments

malexisJuly 25th, 2012 at 12:58BollieJuly 25th, 2012 at 17:30RainmakerJuly 25th, 2012 at 19:49Dmitry PashkevichJuly 26th, 2012 at 01:22Justin DolskeJuly 27th, 2012 at 12:14DonovanJuly 31st, 2012 at 16:43donovanAugust 1st, 2012 at 08:01DonovanAugust 3rd, 2012 at 01:49cCc vAdErAugust 3rd, 2012 at 13:05SharonSeptember 17th, 2012 at 17:44Robert NymanSeptember 18th, 2012 at 00:18DonovanOctober 8th, 2012 at 09:52