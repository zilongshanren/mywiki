---
title: Converting a WebGL application to WebVR – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2018/09/converting-a-webgl-application-to-webvr/
author: Manish Goregaokar
published: '2018-09-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A couple months ago I [ported the Pathfinder demo app to WebVR](https://github.com/pcwalton/pathfinder/pull/76). It was an interesting experience, and I feel like I learned a bunch of things about porting WebGL applications to WebVR that would be generally useful to folks, especially folks coming to WebVR from non-web programming backgrounds.

[Pathfinder](http://github.com/pcwalton/pathfinder) is a GPU-based font rasterizer in Rust, and it comes with a demo app that runs the Rust code on the server side but does all the GPU work in WebGL in a TypeScript website.

We had a 3D demo showing a representation of the [Mozilla Monument](https://wiki.mozilla.org/Monument) as a way to demo text rasterization in 3D. What I was hoping to do was to convert this to a WebVR application that would let you view the monument by moving your head instead of using arrow keys.

I started working on this problem with a decent understanding of [OpenGL](https://www.opengl.org/) and [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API), but almost zero background in VR or WebVR. I’d written an Android Cardboard app three years previously and that was about it.

I’m hoping this article may be useful for others from similar backgrounds.

## What *is* WebVR?

[WebVR is a set of APIs](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API) for writing VR applications on the web. It lets us request jumping into VR mode, at which point we can render things directly to the eyes of a VR display, rather than rendering to a flat surface browser within the display. When the user is on a device like the Cardboard or Daydream where a regular phone substitutes for the VR display, this is the point where the user puts their phone within the headset.

WebVR APIs help with transitioning to/from VR mode, obtaining pose information, rendering in VR, and dealing with device input. Some of these things are being improved in the work in progress on the new [WebXR Device API specification](https://github.com/immersive-web/webxr).

## Do I need any devices to work with WebVR?

Ideally, a good VR device will make it easier to test your work in progress, but depending on how much resolution you need, a Daydream or Cardboard (where you use your phone in a headset casing) is enough. You can even test stuff without the headset casing, though stuff will look weird and distorted.

For local testing Chrome has a [WebVR API emulation extension](https://chrome.google.com/webstore/detail/webvr-api-emulation/gbdnpaebafagioggnhkacnaaahpiefil?hl=en) that’s pretty useful. You can use the devtools panel in it to tweak the pose, and you get a non-distorted display of what the eyes see.

Firefox supports WebVR, and Chrome Canary supports it if you [enable some flags](https://webvr.info/get-chrome/). There’s [also a polyfill](https://github.com/immersive-web/webvr-polyfill) which should work for more browsers.

## How does it work under the hood?

I think not understanding this part was the source of a lot of confusion and bugs for me when I was getting started. The core of the API is basically “render something to a canvas and then magic happens”, and I had trouble figuring how that magic worked.

Essentially, there’s a bunch of work we’re *supposed to do*, and then there’s extra work the browser (or polyfill) does.

Once we enter VR mode, there’s a callback triggered whenever the device requests a frame. Within this callback we have access to pose information.

Using this pose information, we can figure out what each eye should see, and provide this to the WebVR API in some form.

What the WebVR API expects is that we render each eye’s view to a canvas, split horizontally (this canvas will have been passed to the API when we initialize it).

That’s it from our side, the browser (or polyfill) does the rest. It uses our rendered canvas as a texture, and for each eye, it distorts the rendered half to appropriately work with the lenses used in your device. For example, the distortion for Daydream and Cardboard follows [this code in the polyfill](https://github.com/immersive-web/cardboard-vr-display/blob/77e992d9283a4c924ad284cc01c7d8dfc4500eec/src/cardboard-distorter.js).

It’s important to note that, as application developers, we don’t have to worry about this — the WebVR API is handling it for us! We need to render undistorted views from each eye to the canvas — the left view on the left half and the right view on the right half, and the browser handles the rest!

## Porting WebGL applications

I’m going to try and keep this self contained, however I’ll mention off the bat that some really good resources for learning this stuff can be found at [webvr.info](https://webvr.info/developers/) and [MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API/Concepts). [webvr.info](https://webvr.info/developers/) has a bunch of neat [samples](https://webvr.info/samples/) if, like me, you learn better by looking at code and playing around with it.

### Entering VR mode

First up, we need to be able to get access to a VR display and enter VR mode.

```
let vrDisplay;
navigator.getVRDisplays().then(displays => {
if (displays.length === 0) {
return;
}
vrDisplay = displays[displays.length - 1];
// optional, but recommended
vrDisplay.depthNear = /* near clip plane distance */;
vrDisplay.depthFar = /* far clip plane distance */;
}
```


We need to add an event handler for when we enter/exit VR:

```
let canvas = document.getElementById(/* canvas id */);
let inVR = false;
window.addEventListener('vrdisplaypresentchange', () => {
// no VR display, exit
if (vrDisplay == null)
return;
// are we entering or exiting VR?
if (vrDisplay.isPresenting) {
// We should make our canvas the size expected
// by WebVR
const eye = vrDisplay.getEyeParameters("left");
// multiply by two since we're rendering both eyes side
// by side
canvas.width = eye.renderWidth * 2;
canvas.height = eye.renderHeight;
const vrCallback = () => {
if (vrDisplay == null || !inVR) {
return;
}
// reregister callback if we're still in VR
vrDisplay.requestAnimationFrame(vrCallback);
// render scene
render();
};
// register callback
vrDisplay.requestAnimationFrame(vrCallback);
} else {
inVR = false;
// resize canvas to regular non-VR size if necessary
}
});
```


And, to enter VR itself:

```
if (vrDisplay != null) {
inVR = true;
// hand the canvas to the WebVR API
vrDisplay.requestPresent([{ source: canvas }]);
// requestPresent() will request permission to enter VR mode,
// and once the user has done this our `vrdisplaypresentchange`
// callback will be triggered
}
```


### Rendering in VR

Well, we’ve entered VR, now what? In the above code snippets we had a `render()`

call which was doing most of the hard work.

Since we’re starting with an existing WebGL application, we’ll have some function like this already.

```
let width = canvas.width;
let height = canvas.height;
function render() {
let gl = canvas.getContext("gl");
gl.viewport(0, 0, width, height);
gl.clearColor(/* .. */);
gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
gl.useProgram(program);
gl.bindBuffer(/* .. */);
// ...
let uProjection = gl.getUniformLocation(program, "uProjection");
let uModelView = gl.getUniformLocation(program, "uModelview");
gl.uniformMatrix4fv(uProjection, false, /* .. */);
gl.uniformMatrix4fv(uModelView, false, /* .. */);
// set more parameters
// run gl.drawElements()
}
```


So first we’re going to have to split this up a bit further, to handle rendering the two eyes:

```
<br />// entry point for WebVR, called by vrCallback()
function renderVR() {
let gl = canvas.getContext("gl");
// set clearColor and call gl.clear()
clear(gl);
renderEye(true);
renderEye(false);
vrDisplay.submitFrame(); // Send the rendered frame over to the VR display
}
// entry point for non-WebVR rendering
// called by whatever mechanism (likely keyboard/mouse events)
// you used before to trigger redraws
function render() {
let gl = canvas.getContext("gl");
// set clearColor and call gl.clear()
clear(gl);
renderSceneOnce();
}
function renderEye(isLeft) {
// choose which half of the canvas to draw on
if (isLeft) {
gl.viewport(0, 0, width / 2, height);
} else {
gl.viewport(width / 2, 0, width / 2, height);
}
renderSceneOnce();
}
function renderSceneOnce() {
// the actual GL program and draw calls go here
}
```


This looks like a good step forward, but notice that we’re rendering the same thing to both eyes, and not handling movement of the head at all.

To implement this we need to use the perspective and view matrices provided by WebVR from the `VRFrameData`

object.

The [ VRFrameData](https://developer.mozilla.org/en-US/docs/Web/API/VRFrameData) object contains a

[member with all of the head pose information (its position, orientation, and even velocity and acceleration for devices that support these). However, for the purpose of correctly positioning the camera whilst rendering,](https://developer.mozilla.org/en-US/docs/Web/API/VRPose)

`pose`

`VRFrameData`

provides projection and view matrices which we can directly use.We can do this like so:

```
let frameData = new VRFrameData();
vrDisplay.getFrameData(frameData);
// use frameData.leftViewMatrix / framedata.leftProjectionMatrix
// for the left eye, and
// frameData.rightViewMatrix / framedata.rightProjectionMatrix for the right
```


In graphics, we often find ourselves dealing with the model, view, and projection matrices. The *model matrix* defines the position of the object we wish to render in the coordinates of our space, the *view matrix* defines the transformation between the camera space and the world space, and the *projection matrix* handles the transformation between clip space and camera space (also potentially dealing with perspective). Sometimes we’ll deal with the combination of some of these, like the “model-view” matrix.

One can see these matrices in use in the [cubesea code](https://github.com/toji/webvr.info/blob/master/samples/js/vr-cube-sea.js) in the [stereo rendering example from webvr.info](https://webvr.info/samples/02-stereo-rendering.html).

There’s a good chance our application has some concept of a model/view/projection matrix already. If not, we can pre-multiply our positions with the view matrix in our [vertex shaders](https://www.khronos.org/opengl/wiki/Vertex_Shader).

So now our code will look something like this:

```
// entry point for non-WebVR rendering
// called by whatever mechanism (likely keyboard/mouse events)
// we used before to trigger redraws
function render() {
let gl = canvas.getContext("gl");
// set clearColor and call gl.clear()
clear(gl);
let projection = /*
calculate projection using something
like glmatrix.mat4.perspective()
(we should be doing this already in the normal WebGL app)
*/;
let view = /*
use our view matrix if we have one,
or an identity matrix
*/;
renderSceneOnce(projection, view);
}
function renderEye(isLeft) {
// choose which half of the canvas to draw on
let projection, view;
let frameData = new VRFrameData();
vrDisplay.getFrameData(frameData);
if (isLeft) {
gl.viewport(0, 0, width / 2, height);
projection = frameData.leftProjectionMatrix;
view = frameData.leftViewMatrix;
} else {
gl.viewport(width / 2, 0, width / 2, height);
projection = frameData.rightProjectionMatrix;
view = frameData.rightViewMatrix;
}
renderSceneOnce(projection, view);
}
function renderSceneOnce(projection, view) {
let model = /* obtain model matrix if we have one */;
let modelview = glmatrix.mat4.create();
glmatrix.mat4.mul(modelview, view, model);
gl.useProgram(program);
gl.bindBuffer(/* .. */);
// ...
let uProjection = gl.getUniformLocation(program, "uProjection");
let uModelView = gl.getUniformLocation(program, "uModelview");
gl.uniformMatrix4fv(uProjection, false, projection);
gl.uniformMatrix4fv(uModelView, false, modelview);
// set more parameters
// run gl.drawElements()
}
```


This should be it! Moving your head around should now trigger movement in the scene to match it! You can see the code at work in this [demo app](https://github.com/Manishearth/webgl-to-webvr) that takes a [spinning triangle WebGL application](https://manishearth.github.io/webgl-to-webvr/webgl.html) and turns it into a [WebVR-capable triangle-viewing application](https://manishearth.github.io/webgl-to-webvr/webvr.html) using the techniques from this blog post.

If we had further input we might need to use the [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API) to design a good VR interface that works with typical VR controllers, but that’s out of scope for this post.

## About
[
Manish Goregaokar ](https://manishearth.github.io/)

Manish works on the experimental Servo browser at Mozilla, and is quite active in the Rust community