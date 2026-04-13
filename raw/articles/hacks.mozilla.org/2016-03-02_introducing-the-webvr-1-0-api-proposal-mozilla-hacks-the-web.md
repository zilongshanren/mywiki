---
title: Introducing the WebVR 1.0 API Proposal – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/03/introducing-the-webvr-1-0-api-proposal/
author: Casey Yee
published: '2016-03-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

2016 is shaping up to be a banner year for Virtual Reality. Many consumer VR products will finally be available and many top software companies are ramping up to support these new devices. The new medium has also driven demand for web-enabled support from browser vendors. Growth in WebVR has centered on incredible [viewing experiences](http://mozvr.com/#showcase) and the [tools](http://mozvr.com/#developers) used to create online VR content.

![VR_images](../../assets/2cf03ece8e4cf022.png)


The [Mozilla VR team](https://twitter.com/MozillaVR) has been working hard to support the online creation and display of VR content in the browser. This week marks a WebVR milestone. Working closely with [Brandon Jones](https://twitter.com/tojiro) of the Google Chrome team, the Mozilla team is excited to announce the version 1.0 release of the WebVR API proposal.

Recent VR technology advances and community feedback have allowed us to improve the API to address developer needs.

Some of the improvements include:

- VR-specific handling of device rendering and display.
- The ability to traverse links between WebVR pages.
- An input handling scheme that can enumerate VR inputs, including
[six degrees of freedom (6DoF)](https://en.wikipedia.org/wiki/Six_degrees_of_freedom#Game_controllers)motion controllers. - Accommodation of both sitting and standing experiences.
- Suitability for both desktop and mobile usage.

We are excited to share these improvements to the API. Keep in mind the list above represents a small sample of what has changed. For all the details, take a look at the [full API draft](https://mozvr.github.io/webvr-spec/) and check out [Brandon’s blog post](http://blog.tojicode.com/2016/02/moving-towards-webvr-10.html).

This article is focused on basic usage of the proposed API, which requires an understanding of some complex concepts like [matrix math](https://en.wikipedia.org/wiki/Matrix_%28mathematics%29). As an alternative, you can get a quick start in WebVR by looking at [A-Frame](https://aframe.io/) or the [WebVR boilerplate](https://github.com/borismus/webvr-boilerplate/), both built on top of the API.

Before we dive in, we’d like to give special thanks to [Chris Van Wiemeersch](https://twitter.com/cvanw) (Mozilla), [Kearwood “Kip” Gilbert](https://twitter.com/kearwoodgilbert) (Mozilla), [Brandon Jones](https://twitter.com/tojiro) (Google), and [Justin Rogers](https://twitter.com/JustRogDigiTec) (Microsoft) for contributing to the creation of this specification.

### Implementation roadmap

We plan to land a stable implementation of the 1.0 APIs in [Firefox Nightly](https://nightly.mozilla.org/) in the first half of the year. You can follow along on [Bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=1250244) for all the details, or see status updates on platform support on [iswebvrready.org](https://iswebvrready.org/).

Want to get started today? Currently developers can experiment with a proof-of-concept implementation of the new API using Brandon Jones’ [experimental builds](https://drive.google.com/a/mozilla.com/folderview?id=0BzudLt22BqGRbW9WTHMtOWMzNjQ&usp=sharing#list) of Chromium.

Both [three.js](http://threejs.org/) and the [WebVR Polyfill](https://github.com/borismus/webvr-polyfill/) (used by the [WebVR Boilerplate](https://github.com/borismus/webvr-boilerplate/) mentioned above) have open pull requests to support the latest APIs.

### Components of a VR experience

Let’s take a look at the key components required for any VR experience:

- The VR display that we are rendering content to.
- The user’s pose. The orientation and positioning of the headset in space.
- Eye parameters that define stereo separation and field of view.

Here’s a look at the workflow sequence for getting content into the headset:

`navigator.getVRDisplays()`

to retrieve a VR Display.- Create a
`<canvas>`

element which we will use to render content. - Use
`VRDisplay.requestPresent()`

to pass in the canvas element. - Create the VR device-specific animation loop in which we will perform content rendering.
`VRDisplay.getPose()`

to update the user’s pose.- Perform calculations and rendering.
- Use
`VRDisplay.submitFrame()`

to indicate to the compositor when the canvas element content is ready to be presented in the VR display.


The following sections describe each of these actions in detail.

### Working with VR displays

Devices that display VR content have very specific display requirements for [frame rate](https://en.wikipedia.org/wiki/Frame_rate), [field of view](https://en.wikipedia.org/wiki/Field_of_view), and content presentation that are handled separately from standard desktop displays.

#### Enumerating VR displays

To retrieve VR displays available to the browser, use the `navigator.getVRDisplays()`

method, which returns a Promise that resolves with an array of `VRDisplay`

objects:

```
navigator.getVRDisplays().then(function (displays) {
if (!displays.length) {
// WebVR is supported, no VRDisplays are found.
return;
}
// Handle VRDisplay objects. (Exposing as a global variable for use elsewhere.)
vrDisplay = displays.length[0];
}).catch(function (err) {
console.error('Could not get VRDisplays', err.stack);
});
```


Keep in mind:

- You must have your VR headset plugged in and powered on before any VR devices will be enumerated.
- If you do not have a VR headset, you can simulate a device by opening
`about:config`

and setting`dom.vr.cardboard.enabled`

to`true`

. - Users of
[Firefox Nightly for Android](https://nightly.mozilla.org/#Android)or[Firefox for iOS](https://www.mozilla.org/en-US/firefox/ios/)will enumerate a Cardboard VR device for use with[Google Cardboard](https://www.google.com/get/cardboard/).

#### Creating a render target

To determine the render target size (i.e., your canvas size), create a render target large enough to hold both the left and right eye viewports. To find the size (in pixels) of each eye:

```
// Use 'left' or 'right'.
var eyeParameter = vrDisplay.getEyeParameters('left');
var width = eyeParameter.renderWidth;
var height = eyeParameter.renderHeight;
```


#### Presenting content into the headset

To present content into the headset, you’ll need to use the `VRDisplay.requestPresent()`

method. This method takes a WebGL <canvas> element as a parameter which represents the viewing surface to be displayed.

To ensure that the API is not abused, the browser requires a user-initiated event in order for a first-time user to enter VR mode. In other words, a user must choose to enable VR, and so we wrap this into a `click`

event handler on a button labeled “Enter VR”.

```
// Select WebGL canvas element from document.
var webglCanvas = document.querySelector('#webglcanvas');
var enterVRBtn = document.querySelector('#entervr');
enterVRBtn.addEventListener('click', function () {
// Request to present WebGL canvas into the VR display.
vrDisplay.requestPresent({source: webglCanvas});
});
// To later discontinue presenting content into the headset.
vrDisplay.exitPresent();
```


#### Device-specific `requestAnimationFrame`


Now that we have our render target set up and the necessary parameters to render and present the correct view into the headset, we can create a render loop for the scene.

We will want to do this at an optimized refresh rate for the VR display. We use the `VRDisplay.requestAnimationFrame`

callback:

```
var id = vrDisplay.requestAnimationFrame(onAnimationFrame);
function onAnimationFrame () {
// Render loop.
id = vrDisplay.requestAnimationFrame(onAnimationFrame);
}
// To cancel the animation loop.
vrDisplay.cancelRequestAnimationFrame(id);
```


This usage is identical to the standard `window.requestAnimationFrame()`

callback that you may already be familiar with. We use this callback to apply position and orientation pose updates to our content and to render to the VR display.

#### Retrieving pose information from a VR display

We will need to retrieve the orientation and position of the headset using the `VRDisplay.getPose()`

method:

```
var pose = vrDisplay.getPose();
// Returns a quaternion.
var orientation = pose.orientation;
// Returns a three-component vector of absolute position.
var position = pose.position;
```


Please note:

- Orientation and position return
`null`

if orientation and position cannot be determined. - See
and`VRStageCapabilities`

for details.`VRPose`


#### Projecting a scene to the VR display

For proper stereoscopic rendering of the scene in the headset, we need eye parameters such as the offset (based on [interpupillary distance or IPD](https://en.wikipedia.org/wiki/Interpupillary_distance)) and field of view (FOV).

```
// Pass in either 'left' or 'right' eye as parameter.
var eyeParameters = vrDisplay.getEyeParameters('left');
// After translating world coordinates based on VRPose, transform again by negative of the eye offset.
var eyeOffset = eyeParameters.offset;
// Project with a projection matrix.
var eyeMatrix = makeProjectionMatrix(vrDisplay, eyeParameters);
// Apply eyeMatrix to your view.
// ...
/**
* Generates projection matrix
* @param {object} display - VRDisplay
* @param {number} eye - VREyeParameters
* @returns {Float32Array} 4×4 projection matrix
*/
function makeProjectionMatrix (display, eye) {
var d2r = Math.PI / 180.0;
var upTan = Math.tan(eye.fieldOfView.upDegrees * d2r);
var downTan = Math.tan(eye.fieldOfView.leftDegrees * d2r);
var rightTan = Math.tan(eye.fieldOfView.rightDegrees * d2r);
var leftTan = Math.tan(eye.fieldOfView.leftDegrees * d2r);
var xScale = 2.0 / (leftTan + rightTan);
var yScale = 2.0 / (upTan + downTan);
var out = new Float32Array(16);
out[0] = xScale;
out[1] = 0.0;
out[2] = 0.0;
out[3] = 0.0;
out[4] = 0.0;
out[5] = yScale;
out[6] = 0.0;
out[7] = 0.0;
out[8] = -((leftTan - rightTan) * xScale * 0.5);
out[9] = (upTan - downTan) * yScale * 0.5;
out[10] = -(display.depthNear + display.depthFar) / (display.depthFar - display.depthNear);
out[12] = 0.0;
out[13] = 0.0;
out[14] = -(2.0 * display.depthFar * display.depthNear) / (display.depthFar - display.depthNear);
out[15] = 0.0;
return out;
}
```


#### Submitting frames to the headset

VR is optimized to minimize the discontinuity between the user’s movement and the content rendered into the headset. This is important for a comfortable (non-nauseating) experience. This is enabled by giving direct control of how this happens using the `VRDisplay.getPose()`

and `VRDisplay.submitFrame()`

methods:

```
// Rendering and calculations not dependent on pose.
// ...
var pose = vrDisplay.getPose();
// Rendering and calculations dependent on pose. Apply your generated eye matrix here to views.
// Try to minimize operations done here.
// ...
vrDisplay.submitFrame(pose);
// Any operations done to the frame after submission do not increase VR latency. This is a useful place to render another view (such as mirroring).
// ...
```


The general rule is to call `VRDisplay.getPose()`

as late as possible and `VRDisplay.submitFrame()`

as early as possible.

### Demos, feedback and resources

Looking for ways to get started? Here’s a [collection of example apps](https://toji.github.io/webvr-samples/) that use the WebVR 1.0 API. Also, check out the resources listed below.

**And please keep sharing your feedback!**

The development of this API proposal has been in direct response to evolving VR technology, and also from community feedback and discussion. We’re off to a good start, and your ongoing feedback can help us make it better.

We invite you to submit issues and pull requests to the [WebVR API specification GitHub repository](https://github.com/MozVR/webvr-spec/).

#### Resources

[Is WebVR Ready?](https://iswebvrready.org/)[webvr.info](http://webvr.info/)[MDN WebVR API Docs](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API)[MozVR.com](http://MozVR.com)[A-Frame](https://aframe.io/)[WebVR Polyfill](https://github.com/borismus/webvr-polyfill/)and[WebVR Boilerplate](https://github.com/borismus/webvr-boilerplate/)

## About Casey Yee

I work on the WebVR team at Mozilla and work on researching how we can use web technology to build high performance Virtual Reality experiences.

## 5 comments

动感小前端March 2nd, 2016 at 17:30Finbar MaginnMarch 16th, 2016 at 07:28Casey YeeMarch 22nd, 2016 at 10:49JonasMarch 16th, 2016 at 07:47Casey YeeMarch 22nd, 2016 at 12:53