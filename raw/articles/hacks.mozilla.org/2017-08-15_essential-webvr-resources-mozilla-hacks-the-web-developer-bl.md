---
title: Essential WebVR resources – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/08/essential-webvr-resources/
author: Chris Mills
published: '2017-08-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The general [release of Firefox 55](https://hacks.mozilla.org/2017/08/firefox-55-supports-webvr/) brought a number of cool new features to the Gecko platform, one of which is the [WebVR API v1.1](https://w3c.github.io/webvr/spec/1.1/). This allows developers to create immersive VR experiences inside web apps, compatible with popular hardware such as [HTC VIVE](https://www.vive.com/uk/), [Oculus Rift](https://www.oculus.com/rift/), and [Google Daydream](https://vr.google.com/daydream/). This article looks at the resources we’ve made available to facilitate getting into WebVR development.

## Support notes

[Version 1.1 of the WebVR API](https://w3c.github.io/webvr/spec/1.1/) is very new, with varying support available across modern browsers:

[Firefox 55](https://developer.mozilla.org/en-US/Firefox/Releases/55)sees full support on Windows, and more experimental support available for Mac in the Beta/Nightly release channels only, until testing and final work is completed. Supported VR hardware includes HTC VIVE, Oculus Rift, and Google Daydream.- Chrome support is still experimental — you can currently only see support out in the wild on Chrome for Android with Google Daydream.
- Edge fully supports WebVR 1.1, through the Windows Mixed Reality headset.
- Support is also available in Samsung Internet, via their GearVR hardware.

Note that the 1.0 version of the API can be considered obsolete, and has been (or will be) removed from all major browsers.

Controlling WebVR apps using the full features of VR controllers relies on the [Gamepad Extensions API](https://w3c.github.io/gamepad/extensions.html). This adds features to the [Gamepad API](https://w3c.github.io/gamepad/) that provide access to controller features like haptic actuators (e.g. vibration hardware) and position/orientation data (i.e., [pose](https://developer.mozilla.org/en-US/docs/Web/API/GamepadPose)). This currently has even more limited support than the WebVR API; Firefox 55+ has it available in Beta/Nightly channels.

In other browsers, you’ll have to make do for now with basic Gamepad API functionality, like reporting button presses.

## vr.mozilla.org

[vr.mozilla.org](https://vr.mozilla.org) — Mozilla’s new landing pad for WebVR — features demos, utilities, news and updates, and all the other information you’ll need to get up and running with WebVR.

## MDN documentation

MDN has full documentation available for both the APIs mentioned above. See:

[WebVR API reference](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API)[Gamepad API reference](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API), which includes the[Gamepad Extensions API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API#Experimental_Gamepad_extensions)

In addition, we’ve written some useful guides to get you familiar with the basics of using these APIs:

## A-Frame and other libraries

WebVR experiences can be fairly complex to develop. The API itself is easy to use, but you need to use WebGL to create the 3D scenes you want to feature in your apps, and this can prove difficult to those not well-versed in low-level graphics programming. However, there are a number of libraries to hand that can help with this.

The hero of the WebVR world is Mozilla’s [A-Frame library](https://aframe.io/), which allows you to create nice looking 3D scenes using custom HTML elements, handling all the WebGL for you behind the scenes. A-Frame apps are also WebVR-compatible by default. It is perfect for putting together apps and experiences quickly.

There are a number of other well-written 3D libraries available too, which abstract away the difficulty of working with raw WebGL. Good examples include:

These don’t include VR capabilities out of the box, but it is not too difficult to write your own WebVR rendering code around them.

If you are worried about supporting older browsers that only include WebVR 1.0 (or no VR) as well as newer browsers with 1.1, you’ll be pleased to know that there is a [WebVR polyfill available](https://github.com/googlevr/webvr-polyfill/).

## Demos and examples

[vr.mozilla.org](https://vr.mozilla.org)— the main Mozilla landing pad for WebVR, with demos, utilities, and other information.[webvr-tests](https://github.com/mdn/webvr-tests)— very simple examples to accompany the MDN WebVR documentation.[Carmel starter kit](https://github.com/facebook/Carmel-Starter-Kit)— nice simple, well-commented examples that go along with Carmel, Facebook’s WebVR browser.[WebVR.info samples](https://webvr.info/samples/)— slightly more in-depth examples plus source code[WebVR.rocks Firefox demos](https://webvr.rocks/firefox#demos)— showcase examples[A-Frame homepage](https://aframe.io/)— examples showing A-Frame usage

## See also

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## One comment

Pete markiewiczAugust 16th, 2017 at 10:21