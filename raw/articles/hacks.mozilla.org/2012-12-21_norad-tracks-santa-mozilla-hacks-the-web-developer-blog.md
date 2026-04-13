---
title: NORAD Tracks Santa – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/12/norad-tracks-santa/
author: Kevin Ring
published: '2012-12-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This year, Open Web standards like [WebGL](https://developer.mozilla.org/docs/WebGL), [Web Workers](https://developer.mozilla.org/docs/DOM/Using_web_workers), [Typed Arrays](https://developer.mozilla.org/docs/JavaScript/Typed_arrays), [Fullscreen](https://hacks.mozilla.org/2012/01/using-the-fullscreen-api-in-web-browsers/), and more will have a prominent role in NORAD’s annual mission to track Santa Claus as he makes his journey around the world. That’s because [Analytical Graphics, Inc.](http://www.agi.com) used [Cesium](http://cesium.agi.com) as the basis for the 3D [Track Santa](http://www.noradsanta.org/en/track.html) application.

![](../../assets/f007c6d814e62017.png)


Cesium is an open source library that uses JavaScript, WebGL, and other web technologies to render a detailed, dynamic, and interactive virtual globe in a web browser, without the need for a plugin. Terrain and imagery datasets measured in gigabytes or terabytes are streamed to the browser on demand, and overlaid with lines, polygons, placemarks, labels, models, and other features. These features are accurately positioned within the 3D world and can efficiently move and change over time. In short, Cesium brings to the Open Web the kind of responsive, geospatial experience that was uncommon even in bulky desktop applications just a few years ago.

The [NORAD Tracks Santa](http://www.noradsanta.org) web application goes live on December 24. Cesium, however, is freely [available](http://cesium.agi.com) today for commercial and non-commercial use under the Apache 2.0 license.

![](../../assets/71e50eb56a5162c9.png)


In this article, I’ll present how Cesium uses cutting edge web APIs to bring an exciting in-browser experience to millions of people on December 24.

The locations used in the screenshots of the NORAD Tracks Santa application are based on test data. We, of course, won’t know Santa’s route until NORAD starts tracking him on Christmas Eve. Also, the code samples in this article are for illustrative purposes and do not necessarily reflect the exact code used in Cesium. If you want to see the official code, check out our [GitHub repo](https://github.com/AnalyticalGraphicsInc/cesium).

## WebGL

Cesium could not exist without [WebGL](http://www.khronos.org/webgl/), the technology that brings hardware-accelerated 3D graphics to the web.

![](../../assets/de0a90a54d605ad9.png)


It’s hard to overstate the potential of this technology to bring a whole new class of scientific and entertainment applications to the web; Cesium is just one realization of that potential. With WebGL, we can render scenes like the above, consisting of hundreds of thousands of triangles, at well over 60 frames per second.

Yeah, you could say I’m excited.

If you’re familiar with [OpenGL](http://www.khronos.org/opengl), WebGL will seem very natural to you. To oversimplify a bit, WebGL enables applications to draw shaded triangles really fast. For example, from JavaScript, we execute code like this:

```
gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
gl.drawElements(gl.TRIANGLES, numberOfIndices, gl.UNSIGNED_SHORT, 0);
```

`vertexBuffer`

is a previously-configured data structure holding vertices, or corners of triangles. A simple vertex just specifies the position of the vertex as X, Y, Z coordinates in 3D space. A vertex can have additional attributes, however, such as colors and the vertex’s coordinates within a 2D image for texture mapping.

The `indexBuffer`

links the vertices together into triangles. It is a list of integers where each integer specifies the index of a vertex in the `vertexBuffer`

. Each triplet of indices specifies one triangle. For example, if the first three indices in the list are [0, 2, 1], the first triangle is defined by linking up vertices 0, 2, and 1.

The `drawElements`

call instructs WebGL to draw the triangles defined by the vertex and index buffers. The really cool thing is what happens next.

For every vertex in `vertexBuffer`

, WebGL executes a program, called a vertex shader, that is supplied by the JavaScript code. Then, WebGL figures out which pixels on the screen are “lit up” by each triangle – a process called rasterization. For each of these pixels, called fragments, another program, a fragment shader, is invoked. These programs are written in a C-like language called GLSL that executes on the system’s Graphics Processing Unit (GPU). Thanks to this low-level access and the impressive parallel computation capability of GPUs, these programs can do sophisticated computations very quickly, creating impressive visual effects. This feat is especially impressive when you consider that they are executed hundreds of thousands or millions of times per render frame.

Cesium’s fragment shaders approximate atmospheric scattering, simulate ocean waves, model the reflection of the sun off the ocean surface, and more.

![](../../assets/de0c5bf29c9b953a.png)


WebGL is well supported in modern browsers on Windows, Linux and Mac OS X. Even [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox) supports WebGL!

While I’ve shown direct WebGL calls in the code above, Cesium is actually built on a renderer that raises the level of abstraction beyond WebGL itself. We never issue `drawElements`

calls directly, but instead create command objects that represent the vertex buffers, index buffers, and other data with which to draw. This allows the renderer to automatically and elegantly solve esoteric rendering problems like the insufficient depth buffer precision for a world the size of Earth. If you’re interested, you can read more about Cesium’s [data-driven renderer](https://github.com/AnalyticalGraphicsInc/cesium/wiki/Data-Driven-Renderer-Details).

For more information about some of the neat rendering effects used in the NORAD Tracks Santa application, take a look at [our blog post](http://cesium.agi.com/2012/11/30/NORAD-Tracks-Santa-Tech-Preview/) on the subject.

## Typed Arrays and Cross-Origin Resource Sharing

Virtual globes like Cesium provide a compelling, interactive 3D view of real-world situations by rendering a virtual Earth combined with georeferenced data such as roads, points of interest, weather, satellite orbits, or even the current location of Santa Claus. At the core of a virtual globe is the rendering of the Earth itself, with realistic terrain and satellite imagery.

Terrain describes the shape of the surface: the mountain peaks, the hidden valleys, the wide open plains, and everything in between. Satellite or aerial imagery is then overlaid on this otherwise colorless surface and brings it to life.

The global terrain data used in the NORAD Tracks Santa application is derived from the [Shuttle Radar Topography Mission](http://www2.jpl.nasa.gov/srtm/) (SRTM), which has a 90-meter spacing between -60 and 60 degrees latitude, and the [Global 30 Arc Second Elevation Data Set](http://www1.gsi.go.jp/geowww/globalmap-gsi/gtopo30/gtopo30.html) (GTOPO30), which has 1-kilometer spacing for the entire globe. The total size of the dataset is over 10 gigabytes.

For imagery, we use [Bing Maps](http://www.bing.com/maps/), who is also a part of the NORAD Tracks Santa team. The total size of this dataset is even bigger – easily in the terabytes.

![](../../assets/4411749475cd033e.png)


With such enormous datasets, it is clearly impractical to transfer all of the terrain and imagery to the browser before rendering a scene. For that reason, both datasets are broken up into millions of individual files, called tiles. As Santa flies around the world, Cesium downloads new terrain and imagery tiles as they are needed.

Terrain tiles describing the shape of the Earth’s surface are binary data encoded in a [straightforward format](https://github.com/AnalyticalGraphicsInc/cesium/wiki/Cesium-Terrain-Server). When Cesium determines that it needs a terrain tile, we download it using `XMLHttpRequest`

and access the binary data using [typed arrays](http://www.khronos.org/registry/typedarray/specs/latest/):

```
var tile = ...
var xhr = new XMLHttpRequest();
xhr.open('GET', terrainTileUrl, true);
xhr.responseType = 'arraybuffer';
xhr.onload = function(e) {
if (xhr.status === 200) {
var tileData = xhr.response;
tile.heights = new Uint16Array(tileData, 0, heightmapWidth * heightmapHeight);
var heightsBytes = tile.heights.byteLength;
tile.childTileBits = new Uint8Array(tileData, heightsBytes, 1)[0];
tile.waterMask = new Uint8Array(tileData, heightsBytes + 1, tileData.byteLength - heightsBytes - 1);
tile.state = TileState.RECEIVED;
} else {
// ...
}
};
xhr.send();
```

Prior to the availability of typed arrays, this process would have been much more difficult. The usual course was to encode the data as text in JSON or XML format. Not only would such data be larger when sent over the wire(less), it would also be significantly slower to process it once it was received.

While it is generally very straightforward to work with terrain data using typed arrays, two issues make it a bit trickier.

The first is cross-origin restrictions. It is very common for terrain and imagery to be hosted on different servers than are used to host the web application itself, and this is certainly the case in NORAD Tracks Santa. `XMLHttpRequest`

, however, does not usually allow requests to non-origin hosts. The common workaround of using script tags instead of `XMLHttpRequest`

won’t work well here because we are downloading binary data – we can’t use typed arrays with JSONP.

Fortunately, modern browsers offer a solution to this problem by honoring Cross-Origin Resource Sharing (CORS) headers, included in the response by the server, indicating that the response is safe for use across hosts. Enabling CORS is [easy to do](http://enable-cors.org/) if you have control over the web server, and Bing Maps already includes the necessary headers on their tile files. Other terrain and imagery sources that we’d like to use in Cesium are not always so forward-thinking, however, so we’ve sometimes been forced to route cross-origin requests through a same-origin proxy.

The other tricky aspect is that modern browsers only allow up to six simultaneous connections to a given host. If we simply created a new `XMLHttpRequest`

for each tile requested by Cesium, the number of queued requests would grow large very quickly. By the time a tile was finally downloaded, the viewer’s position in the 3D world may have changed so that the tile is no longer even needed.

Instead, we manually limit ourselves to six outstanding requests per host. If all six slots are taken, we won’t start a new request. Instead, we’ll wait until next render frame and try again. By then, the highest priority tile may be different than it was last frame, and we’ll be glad we didn’t queue up the request then. One nice feature of Bing Maps is that it serves the same tiles from multiple hostnames, which allows us to have more outstanding requests at once and to get the imagery into the application faster.

## Web Workers

The terrain data served to the browser is, primarily, just an array of terrain heights. In order to render it, we need to turn the terrain tile into a triangle mesh with a vertex and index buffer. This process involves converting longitude, latitude, and height to X, Y, and Z coordinates mapped to the surface of the [WGS84 ellipsoid](http://en.wikipedia.org/wiki/World_Geodetic_System). Doing this once is pretty fast, but doing it for each height sample, of which each tile has thousands, starts to take some measurable time. If we did this conversion for several tiles in a single render frame, we’d definitely start to see some stuttering in the rendering.

One solution is to throttle tile conversion, doing at most N per render frame. While this would help with the stuttering, it doesn’t avoid the fact that tile conversion competes with rendering for CPU time while other CPU cores sit idle.

Fortunately, another great new web API comes to the rescue: [Web Workers](http://www.w3.org/TR/workers/).

We pass the terrain `ArrayBuffer`

downloaded from the remote server via `XMLHttpRequest`

to a Web Worker as a [transferable object](http://www.whatwg.org/specs/web-apps/current-work/multipage/common-dom-interfaces.html#transferable-objects). When the worker receives the message, it builds a new typed array with the vertex data in a form ready to be passed straight to WebGL. Unfortunately, Web Workers are not yet allowed to invoke WebGL, so we can’t create vertex and index buffers in the Web Worker; instead, we post the typed array back to the main thread, again as a transferable object.

The beauty of this approach is that terrain data conversion happens asynchronously with rendering, and that it can take advantage of the client system’s multiple cores, if available. This leads to a smoother, more interactive Santa tracking experience.

Web Workers are simple and elegant, but that simplicity presents some challenges for an engine like Cesium, which is designed to be useful in various different types of applications.

During development, we like to keep each class in a separate `.js`

file, for ease of navigation and to avoid the need for a time-consuming combine step after every change. Each class is actually a separate module, and we use the [Asynchronous Module Definition](http://requirejs.org/docs/whyamd.html) (AMD) API and [RequireJS](http://requirejs.org/) to manage dependencies between modules at runtime.

![](../../assets/d647d85eb7f10113.png)


For use in production environments, it is a big performance win to combine the hundreds of individual files that make up a Cesium application into a single file. This may be a single file for all of Cesium or a user-selected subset. It may also be beneficial to combine parts of Cesium into a larger file containing application-specific code, as we’ve done in the NORAD Tracks Santa application. Cesium supports all of these use-cases, but the interaction with Web Workers gets tricky.

When an application creates a Web Worker, it provides to the Web Worker API the URL of the `.js`

file to invoke. The problem is, in Cesium’s case, that URL varies depending on which of the above use-cases is currently in play. Worse, the worker code itself needs to work a little differently depending on how Cesium is being used. That’s a big problem, because workers can’t access any information in the main thread unless that information is explicitly posted to it.

Our solution is the `cesiumWorkerBootstrapper`

. Regardless of what the `WebWorker`

will eventually do, it is always constructed with `cesiumWorkerBootstrapper.js`

as its entry point. The URL of the bootstrapper is deduced by the main thread where possible, and can be overridden by user code when necessary. Then, we post a message to the worker with details about how to actually dispatch work.

```
var worker = new Worker(getBootstrapperUrl());
//bootstrap
var bootstrapMessage = {
loaderConfig : {},
workerModule : 'Workers/' + processor._workerName
};
if (typeof require.toUrl !== 'undefined') {
bootstrapMessage.loaderConfig.baseUrl = '..';
} else {
bootstrapMessage.loaderConfig.paths = {
'Workers' : '.'
};
}
worker.postMessage(bootstrapMessage);
```

The worker bootstrapper contains a simple `onmessage`

handler:

```
self.onmessage = function(event) {
var data = event.data;
require(data.loaderConfig, [data.workerModule], function(workerModule) {
//replace onmessage with the required-in workerModule
self.onmessage = workerModule;
});
};
```

When the bootstrapper receives the `bootstrapMessage`

, it uses the RequireJS implementation of `require`

, which is also included in `cesiumWorkerBootstrapper.js`

, to load the worker module specified in the message. It then “becomes” the new worker by replacing its `onmessage`

handler with the required-in one.

In use-cases where Cesium itself is combined into a single `.js`

file, we also combine each worker into its own `.js`

file, complete with all of its dependencies. This ensures that each worker needs to load only two `.js`

files: the bootstrapper plus the combined module.

## Mobile Devices

One of the most exciting aspects of building an application like NORAD Tracks Santa on web technologies is the possibility of achieving portability across operating systems and devices with a single code base. All of the technologies used by Cesium are already well supported on Windows, Linux, and Mac OS X on desktops and laptops. Increasingly, however, these technologies are becoming available on mobile devices.

The most stable implementation of WebGL on phones and tablets is currently found in Firefox for Android. We tried out Cesium on several devices, including a Nexus 4 phone and a Nexus 7 tablet, both running Android 4.2.1 and Firefox 17.0. With a few tweaks, we were able to get Cesium running, and the performance was surprisingly good.

We did encounter a few problems, however, presumably a result of driver bugs. One problem was that normalizing vectors in fragment shaders sometimes simply does not work. For example, GLSL code like this:

```
vec3 normalized = normalize(someVector);
```

Sometimes results in a `normalized`

vector that still has a length greater than 1. Fortunately, this is easy to work around by adding another call to `normalize`

:

```
vec3 normalized = normalize(normalize(someVector));
```

We hope that as WebGL gains more widespread adoption on mobile, bugs like this will be detected by the [WebGL conformance tests ](https://www.khronos.org/registry/webgl/sdk/tests/webgl-conformance-tests.html) before devices and drivers are released.

## The Finished Application

As long-time C++ developers, we were initially skeptical of building a virtual globe application on the Open Web. Would we be able to do all the things expected of such an application? Would the performance be good?

![](../../assets/b21568c6b3364251.png)


I’m pleased to say that we’ve been converted. Modern web APIs like WebGL, Web Workers, and Typed Arrays, along with the continual and impressive gains in JavaScript performance, have made the web a convenient, high-performance platform for sophisticated 3D applications. We’re looking forward to continuing to use Cesium to push the limits of what is possible in a browser, and to take advantage of new APIs and capabilities as they become available.

We’re also looking forward to using this technology to bring a fun, 3D Santa tracking experience to millions of kids worldwide this Christmas as part of the NORAD Tracks Santa team. Check it out on December 24 at [www.noradsanta.org](http://www.noradsanta.org).

## About Kevin Ring

I am a founding developer of [Cesium](http://cesium.agi.com), an open-source, web-based, virtual globe and map, and co-author of the book [3D Engine Design for Virtual Globes](http://www.virtualglobebook.com). I'm fortunate to work for [Analytical Graphics, Inc.](http://www.agi.com), a wonderful company that allows me the flexibility to develop open source projects and write books.