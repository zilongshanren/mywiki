---
title: 'A practitioner’s perspective on A-Frame: —Interview with Roland Dubois – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/03/a-practitioners-perspective-on-a-frame-interview-with-roland-dubois/
author: Salva
published: '2017-03-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There is a growing awareness and interest in [WebVR](https://research.mozilla.org/mixed-reality/) among Web developers, and as a result, high-level tools and libraries are emerging to populate the JavaScript ecosystem.

One of the libraries is [A-Frame](http://aframe.io/), supported by Mozilla. A-Frame simplifies the boilerplate required to start creating virtual reality experiences, and uses HTML and the DOM API to build and manipulate the VR scene easily, in a way that is familiar to web developers.

Recently, our friends at Virtuleap, a WebVR demo destination and continuous hackathon website, announced the finalists of [their first WebVR contest](http://www.virtuleap.com/page/view/competition) with prizes up to $30 000. It turns out that [nine out of ten finalists used A-Frame](https://aframe.io/blog/awoa-49/) to build their projects. We wanted to talk with them to learn more about their experience developing VR for the Web, and what they liked working with A-Frame.

In this conversation, I chat with [Roland Dubois](http://rolanddubois.com/), a Virtuleap finalist and founding designer at [studio.zeldman](https://studio.zeldman.com/). Roland is the creator of [gravr.io](http://gravr.io/),

a cloud service that allows you to create a VR profile and ‘avatar’ and synchronize your VR preferences and pre-sets for accessibility and comfort across multiple VR devices.

**What is your background in development and VR?**

I went to school for design, and over time, I focused increasingly on development and code. I played with 3D software like Cinema4D, 3D Studio Max and Blender, mainly for modelling and animation. I worked on a 3D game project where you fly a mouse-sized spaceship through a family home and get chased by the cat. I was in charge of story, 3D models, textures and gameplay and a friend programmed in C# and compiled the game for native PC (.exe).

I have been working on websites for over a decade, and I’m a big fan of web standards which is why I’m so excited about A-Frame, a framework with semantic markup, which renders content in Canvas – the best of both worlds.

**Why did you use A-Frame?**

WebGL and WebVR are JavaScript bibraries and APIs. They are powerful but really complicated. To be fair, I am not a JavaScript ninja, and I’m used to working with libraries and plugins like jQuery or [Prototype](http://prototypejs.org/). Lately, I’m using vanilla JavaScript, but for web designers/developers like me, WebGL and WebVR come with a huge learning curve before any VR content can be created. I am working closely with [Jeffrey Zeldman](https://twitter.com/zeldman), and we are part of large community of web designers and developers that embrace the concept of a free and open web. A-Frame, a semantic HTML framework for VR on the web, is an incredibly useful and attractive tool for the community and all its creative minds. Consuming content in virtual experiences is going to be the future of the web and A-Frame will be essential to creating these experiences.

**Say something you love about A-Frame? And something you hate?**

Support is great and the community does help you. VR is a blank canvas, and there’s an opportunity to shape the standards, creatively look outside of the box, and make an impact on innovation.

I don’t really hate anything, but documentation is lacking. We need more samples focusing on gaze- or voice-based interactions and case studies that don’t require Vive controllers. I understand this is a space that grows over time, but currently, it’s hard to find answers to many questions that don’t require in-depth knowledge of [three.js](https://threejs.org/), [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API), and [WebVR](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API).

**What would you like to see in the next release?**

I would really like to see a way to manipulate “user-height”, “fov” and XYZ/ABC angles after you’ve entered vr view mode. I would also like to see some kind of CSS-like implementation for entity properties.

**What did you miss when developing for WebVR? Performance tools? Hardware emulation?**

I debug mostly with Chrome DevTools and Console. I develop locally in vagrant/VM and clean up my files with gulp. What I’m missing are measurement tools and framerate/performance count.

I’m using the A-Frame inspector mostly for orientation, and I think it makes a lot of sense. However, I would like to have the ability to modify the source code in HTML within an extra modal. I would love to know if there’s a way to add extra modal windows for camera views and simulate a preview in VR mode.

**At Mozilla, we understand the Internet as a universal shared resource and we are concerned about VR content not reaching certain audiences due to accessibility, exclusivity or affordability issues. Roland also seems to share these concerns. In his own words:**

In my opinion, WebVR interaction relies far too much on VR controllers from Vive, Oculus or Daydream. There are so many opportunities that lie within the hardware components of a generic smartphone of today that haven’t been considered. Why not just use the smartphone itself as a controller instead of needing to buy more and more expensive gadgets and controllers to do the same thing?

**So, aside from A-Frame, we wanted to ask a couple more questions around interaction:**

**What can you tell me about the components you created? Why do you provide the shake component? What’s your opinion of VR interaction?**

If we use our smartphones right now along with a $5 cardboard viewer, then we’ll need to think about ways to trigger content on a screen that is not touchable. We have gaze controls that access the gyrometer. We have voice controls that access the microphone, which would work great, except if you’re somewhere loud. However, my [shake component](https://github.com/rdub80/aframe-shake2show-component) provides an additional trigger independent of gaze and voice. The component accesses the accelerometer, a hardware feature in pretty much every smartphone today, which only requires a quick, light tap on the side of the device.

```
<head>
<title>My A-Frame Scene</title>
<script src="https://aframe.io/releases/0.3.0/aframe.min.js"></script>
<script src="https://rawgit.com/rdub80/aframe-shake2show-component/master/dist/aframe-shake2show-component.min.js"></script>
</head>
<body>
<a-scene>
<a-entity shake2show visible="false"></a-entity>
<a-entity camera look-controls></a-entity>
</a-scene>
</body>
```


**Do you believe in a sort of progressive enhancement of VR experiences? I mean, designing for limited hardware and improving interaction as you interact with upgraded hardware?**

I absolutely believe in the progressive enhancement of WebVR… The web is for everyone and a developer for the web should do their best to cater for everyone. Dropping $1500 or more on a new hardware setup just to consume WebVR content is against all my principles. We cannot focus on the newest gadgets to make VR mainstream.

…If you’re using the smartphone alone, you’ll navigate via gaze control or voice. If you are on a GearVR headset you’ll get an extra button to click. If you have a Bluetooth controller connected or a Leap Motion sensor, the WebVR experience will offer you an enhanced user experience. If you have none of the above, but you’re using your smartphone, you should be able to have a comparable experience without all the other expensive extra hardware out there.

The first Oculus Rift developer kit was released four years ago, but VR interaction is still uncharted territory and it exposes new and interesting usability challenges. Roland reminds us:

The VR developer is completely in charge of creating an entirely new world and can’t accommodate personal preferences and adjustments that we use every day in our normal digital setups. No developer has had this much responsibility since the birth of the iPhone.


The A-Frame project is committed to exploring and experimenting with Virtual and Augmented Reality as a medium, providing the Web community with accessible tools to create production quality content.

The feedback coming from developers like Roland while implementing projects like [gravr.io](https://gravr.io) is crucial to battle-test A-Frame and discover new use cases. We are eager to see more development that pushes the envelope and helps evolve the A-Frame API, from simple demos to full-featured experiences.

I would like to end this interview by thanking Roland for sharing his time: Roland, It’s been a pleasure talking with you directly about your impressions of working with A-Frame. From Mozilla, we wish you all the best with [gravr.io](https://gravr.io)

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## One comment

daizhilongMarch 30th, 2017 at 01:10