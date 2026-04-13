---
title: Stereoscopic Rendering in WebVR – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/09/stereoscopic-rendering-in-webvr/
author: Mozilla
published: '2015-09-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At Mozilla, a small recon team has been toying with the idea of blending the best features of the web such as interconnectedness, permissionless content creation, and safe execution of remote code with the immersive interaction model of Virtual Reality.

By starting out with support for [Oculus’s DK2 headset](https://www.oculus.com/en-us/dk2/), we’ve enabled those interested to begin experimenting with VR. As a quick introduction, I wanted to show some of the differences in rendering techniques developers have to account for when building their first VR experience. For this post, we’ll focus on describing rendering with the WebGL set of APIs.

My first rendering in [WebVR](http://mozvr.github.io/webvr-spec/webvr.html), the Stanford dragon. Firefox handles the vignetting effect, spatial, and chromatic distortion for us just by entering fullscreen.

## Multiple Views of the Same Scene

An important first distinction to make: With traditional viewing on a monitor or screen, we’re flattening our three-dimensional scene onto a plane (the view-port). While objects may have different distances from the view-port, everything is rendered from a single point of view. We may have multiple draw calls that build up our scene, but we usually render everything using one view matrix and one projection matrix that’s calculated at scene creation time.

For example, the view matrix might contain information such as the position of our virtual camera relative to everything else in the scene, as well as our orientation (Which way is forward? Which way is up?). The projection matrix might encode whether we want a perspective or orthographic projection, view-port aspect ratio, our field of view (FOV), and draw distance.

As we move from rendering the scene from one point of view to rendering on a head-mounted display (HMD), suddenly we have to render everything twice from two different points of view!

In the past, you might have used one view matrix and one projection matrix, but now you’ll need a pair of each. Rather than having the choice of field of view (FOV), you now must query the headset the user’s FOV setting for each eye. As anyone who’s visited an eye doctor or had an eye exam lately can attest, your eyes each have their own FOV! This is not necessary to correct for when rendering to a far away monitor, as the monitor usually is a subset within the current field of view, whereas a head-mounted display (HMD) encompasses the entire field of view (FOV).

The Oculus SDK has a configuration utility where the user can set individual FOV per eye and [interpupillary distance](https://en.wikipedia.org/wiki/Interpupillary_distance) (IPD), essentially the space between eyes, measured from pupil to pupil).

The unique fields of view give us two unique projection matrices. Because your eyes are also offset from one another, they also have different positions or translations from the position of the viewer. This gives us two different view matrices (one per eye) as well. It’s important to get these right so that the viewer’s brain is able to correctly fuse two distinct images into one.

Without accounting for the IPD offset, a proper [parallax](https://en.wikipedia.org/wiki/Parallax) effect cannot be achieved. Parallax is very important for differentiating distances to various objects and depth perception. Parallax is the appearance of objects further away from you moving slower than closer objects when panning side to side. [Github’s 404 page](https://github.com/nickdesaulniers/doesnotexist) is a great example of parallax in action.

That’s why some 360 degree video shot from a single view/lens per direction tends to smear objects in the foreground with objects farther away. For more info on 360 degree video issues, [this eleVR post](http://elevr.com/cg-vr-1/) is a great read.

We’ll also have to query the HMD to see what the size of the canvas should be set to for the native resolution.

When rendering a monoscopic view, we might have code like —

```
function init () {
// using gl-matrix for linear algebra
var viewMatrix = mat4.lookAt(mat4.create(), eye, center, up);
var projectionMatrix = mat4.perspective(mat4.create(), fov, near, far);
var mvpMatrix = mat4.multiply(mat4.create(), projectionMatrix, viewMatrix);
gl.uniformMatrix4fv(uniforms.uMVPMatrixLocation, false, mvpMatrix);
};
function update (t) {
gl.clear(flags);
gl.drawElements(mode, count, type, offset);
requestAnimationFrame(update);
};
```


in JS and in our GLSL vertex shader:

```
uniform mat4 uMVPMatrix;
attribute vec4 aPosition;
void main () {
gl_Position = uMVPMatrix * aPosition;
}
```


…but when rendering from two different viewpoints with webVR, reusing the previous shader, our JavaScript code might look more like:

```
function init () {
// hypothetical function to get the list of
// attached HMD's and Position Sensors.
initHMD();
initModelMatrices();
};
function update () {
gl.clear(flags);
// hypothetical function that
// uses the webVR API's to update view matrices
// based on orientation provided by HMD's
// accelerometer, and position provided by the
// position sensor camera.
readFromHMDPS();
// left eye
gl.viewport(0, 0, canvas.width / 2, canvas.height);
mat4.multiply(mvpMatrix, leftEyeProjectionMatrix, leftEyeViewMatrix);
gl.uniformMatrix4fv(uniforms.uMVPMatrixLocation, false, mvpMatrix);
gl.drawElements(mode, count, type, offset);
// right eye
gl.viewport(canvas.width / 2, 0, canvas.width / 2, canvas.height);
mat4.multiply(mvpMatrix, rightEyeProjectionMatrix, rightEyeViewMatrix);
gl.uniformMatrix4fv(uniforms.uMVPMatrixLocation, false, mvpMatrix);
gl.drawElements(gl.TRIANGLES, n, gl.UNSIGNED_SHORT, 0);
requestAnimationFrame(update);
};
```


In a follow-up post, once the webVR API has had more time to bake, we’ll take a look at some more concrete examples and explain things like quaternions! With WebGL2’s multiple render targets (WebGL1’s [WEBGL_draw_buffers](http://www.khronos.org/registry/webgl/extensions/WEBGL_draw_buffers/) extension, currently with [less than 50% browser support](http://webglstats.com/), more [info](https://hacks.mozilla.org/2014/01/webgl-deferred-shading/)), or WebGL2’s instancing (WebGL1’s [ANGLE_instanced_arrays](https://www.khronos.org/registry/webgl/extensions/ANGLE_instanced_arrays/) extension, currently 89% browser support) it should be possible to [not explicitly call draw twice](http://alex.vlachos.com/graphics/Alex_Vlachos_Advanced_VR_Rendering_GDC2015.pdf).

For more info on rendering differences, [Oculus docs](https://developer.oculus.com/documentation/intro-vr/latest/concepts/bp_app_imaging/) are also a great reference.

## 90 Hz Refresh Rate and Low Latency

When rendering, we’re limited in how fast we can show updates and refresh the display by the hardware’s refresh rate. For most monitors, this rate is 60 Hz. This gives us 16.66 ms to draw everything in our scene (minus a little for the browser’s compositor). `requestAnimationFrame`

will limit how quickly we can run our update loops, which prevents us from doing more work than is necessary.

The Oculus DK2 has a max refresh rate of 75 Hz (13.33 ms per frame) and the production version currently slated for a Q1 2016 release will have a refresh rate of 90 Hz (11.11 ms per frame).

So, not only do we need to render everything twice from two different viewpoints, but we only have two-thirds the time to do it (16.66 ms * 2 / 3 == 11.11)! While this seems difficult, hitting a lower frame time is doable by various tricks (lower scene complexity, smaller render target plus upscaling, etc). On the other hand, reducing the latency imposed by hardware is much more challenging!

Not only do we have to concern ourselves with frame rate, but also with latency on user input. The major difference between real-time rendering and pre-rendering is that a real-time scene is generated dynamically usually with input from the viewer. When a user moves their head or repositions themselves, we want to have a tight feedback loop between when they move and when they see the results of their movement displayed to them. This means we want to get our rendering results displayed sooner, but then we run into the classic double buffering vs [screen tearing](https://en.wikipedia.org/wiki/Screen_tearing#Prevention) issue. As [Oculus Chief Scientist Michael Abrash points out](http://blogs.valvesoftware.com/abrash/latency-the-sine-qua-non-of-ar-and-vr/), we want sub 20 ms latency between user interaction and feedback presentation.

Whether or not current desktop, let alone mobile, graphics hardware is up to the task remains to be seen!

To get more info or get involved in WebVR:

* [MozVR download page](http://mozvr.com/downloads/) (everything you need to get up and running with WebVR in Firefox)

* [WebVR spec](http://mozvr.github.io/webvr-spec/webvr.html) (in flux, subject to change, things **WILL** break.)

* [MDN docs](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getVRDevices) (in progress, will change when spec is updated)

* [web-vr-dicuss](https://mail.mozilla.org/listinfo/web-vr-discuss) public mailing list

* [/r/webvr](https://www.reddit.com/r/webvr) subreddit