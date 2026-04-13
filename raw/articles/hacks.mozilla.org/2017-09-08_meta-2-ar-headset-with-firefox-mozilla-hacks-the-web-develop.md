---
title: Meta 2 AR Headset with Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/09/meta-2-ar-headset-with-firefox/
author: Josh Marinacci
published: '2017-09-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

One of the biggest challenges in developing immersive WebVR experiences today is that immersion takes you away from your developer tools. With Meta’s new augmented reality headset, you can work on and experience WebVR content today without ever taking a headset on or off, or connecting developer tools to a remote device. Our friends at Meta have just released their [Meta 2 developer kit](https://buy.metavision.com/?utm_source=mozilla&utm_medium=blog&utm_content=ffwebvr) and it works right out of the box with the latest 64-bit [Firefox for Windows](https://www.mozilla.org/en-US/firefox/all/).

The Meta 2 is a tethered augmented reality headset with [six degrees of freedom](https://en.wikipedia.org/wiki/Six_degrees_of_freedom) (6DOF). Unlike existing 3D mobile experiences like Google Cardboard, the Meta 2 can track both your orientation (three degrees of freedom) and your position (another three degrees). This means that not only can you look at 3D content, you can also move towards and around it. (3+3 = 6DOF).

In the video above, talented Mozilla engineer [Kip Gilbert](https://twitter.com/kearwoodgilbert) is editing the [NYC Snowglobe demo](https://aframe.io/examples/showcase/snowglobe/) with the A-Frame inspector on his desktop. After he edits the project, he just lifts his head up to see the rendered 3D scene in the air in front of him. Haven’t tried [A-Frame](https://aframe.io/) yet? It’s the easiest way for web developers to build interactive 3D apps on the web. Best of all, Kip didn’t have to rewrite the snowglobe demo to support AR. It just works! Meta’s transparent visor combined with Firefox enables this kind of seamless 3D development.

The Meta 2 is stereoscopic and also has a 90-degree field of view, creating a more immersive experience on par with a traditional VR headset. However, because of the see-through visor, you are not isolated from the real world. The Meta 2 attaches to your existing desktop or laptop computer, letting you work at your desk without obstructing your view, then just look up to see virtual windows and objects floating around you.

In this next video, Kip is browsing a [Sketchfab](https://sketchfab.com/) gallery. When he sees a model he likes he can simply look up to see the model live in his office. Thanks to the translucent visor optics, anything colored black in the original 3D scene automatically becomes transparent in the Meta 2 headset.

Meta 2 is designed for engineers and other professionals who need to both work at a computer and interact with high performance visualizations like building schematics or a detailed 3D model of a new airplane. Because the Meta 2 is tethered it can use the powerful GPU in your desktop or laptop computer to render high definition 3D content.

Currently, the Meta team has released [Steam VR support](https://blog.metavision.com/the-meta-2-now-supports-rendering-of-steam-vr-applications) and is working to add support for hands as controllers. We will be working with the Meta engineers to transform their native hand gestures into Javascript events that you can interact with in code. This will let you build fully interactive high performance 3D apps right from the comfort of your desktop browser. We are also using this platform to help us [develop and test proposed extensions for AR devices](https://github.com/mozilla/webxr-api) to the existing WebVR specification.

You can get your own Meta 2 developer kit and headset on [the Meta website](https://buy.metavision.com/?utm_source=mozilla&utm_medium=blog&utm_content=ffwebvr). WebVR is supported in the [latest release version](https://hacks.mozilla.org/2017/08/webvr-for-all-windows-users/) of FireFox for Windows, with other platforms coming soon.

## About
[
Josh Marinacci ](https://joshondesign.com/)

I am an author, researcher, and recovering engineer. Formerly on the Swing Team at Sun, the webOS team at Palm, and Nokia Research. I spread the word of good user experiences. I live in sunny Eugene Oregon with my wife and genius Lego builder child.