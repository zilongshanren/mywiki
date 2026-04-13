---
title: 'The Web Developer Toolbox: ThreeJS – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/06/the-web-developer-toolbox-threejs/
author: Jeremie Patonnier
published: '2012-06-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This is the second of a series of articles dedicated to the useful libraries that all web developers should have in their toolbox. The intent is to show you what those libraries can do and help you to use them at their best. This second article is dedicated to the ThreeJS library.

## Introduction

[ThreeJS](https://github.com/mrdoob/three.js/) is a library originally written by [Ricardo Cabello Miguel](http://ricardocabello.com/blog) aka “[Mr. Doob](http://mrdoob.com/)“.

This library makes WebGL accessible to common human beings. [WebGL is a powerful API](https://developer.mozilla.org/en/WebGL) to manipulate 3D environments. This web technology is [standardized by the Kronos group](http://www.khronos.org/webgl/) and Firefox, Chrome and Opera now implement it as a 3D context for the HTML [canvas](https://developer.mozilla.org/en/HTML/Canvas) tag. WebGL is basically a web version of another standard : OpenGL ES 2.0. As a consequence, this API is a “low level” API that require skills and knowledge beyond what web designers are used to. That’s where ThreeJS comes into play. ThreeJS gives web developers access to the power of WebGL without all the knowledge required by the underlying API.

## Basic usage

The library has [good documentation with many examples](http://mrdoob.github.com/three.js/). You’ll notice that some parts of the documentation are not complete yet (feel free to help). However, the library and examples source code are very well structured, so do not hesitate to read the source.

Even though ThreeJS simplifies many things, you still have to be comfortable with some basic 3D concepts. Basically, ThreeJS uses the following concepts:

- The scene: the place where all 3D objects will be placed and manipulated in a 3D space.
- The camera: a special 3D object that will define the rendering point of view as well as the type of spatial rendering (perspective or isometric)
- The renderer: the object in charge of using the scene and the camera to render your 3D image.

Within the scene, you will have several 3D objects which can be of the following types:

- A mesh: A mesh is an object made of a geometry (the shape of your object) and a material (its colors and texture)
- A light point: A special object that defines a light source to highlight all your meshes.
- A camera, as described above.

The following example will draw a simple wireframe sphere inside an HTML element with the id “myPlanet”.

```
/**
* First, let's prepare some context
*/
// The WIDTH of the scene to render
var __WIDTH__ = 400,
// The HEIGHT of the scene to render
__HEIGHT__ = 400,
// The angle of the camera that will show the scene
// It is expressed in degrees
__ANGLE__ = 45,
// The shortest distance the camera can see
__NEAR__ = 1,
// The farthest distance the camera can see
__FAR__ = 1000
// The basic hue used to color our object
__HUE__ = 0;
/**
* To render a 3D scene, ThreeJS needs 3 elements:
* A scene where to put all the objects
* A camera to manage the point of view
* A renderer place to show the result
*/
var scene = new THREE.Scene(),
camera = new THREE.PerspectiveCamera(__ANGLE__,
__WIDTH__ / __HEIGHT__,
__NEAR__,
__FAR__),
renderer = new THREE.WebGLRenderer();
/**
* Let's prepare the scene
*/
// Add the camera to the scene
scene.add(camera);
// As all objects, the camera is put at the
// 0,0,0 coordinate, let's pull it back a little
camera.position.z = 300;
// We need to define the size of the renderer
renderer.setSize(__WIDTH__, __HEIGHT__);
// Let's attach our rendering zone to our page
document.getElementById("myPlanet").appendChild(renderer.domElement);
/**
* Now we are ready, we can start building our sphere
* To do this, we need a mesh defined with:
* 1. A geometry (a sphere)
* 2. A material (a color that reacts to light)
*/
var geometry, material, mesh;
// First let's build our geometry
//
// There are other parameters, but you basically just
// need to define the radius of the sphere and the
// number of its vertical and horizontal divisions.
//
// The 2 last parameters determine the number of
// vertices that will be produced: The more vertices you use,
// the smoother the form; but it will be slower to render.
// Make a wise choice to balance the two.
geometry = new THREE.SphereGeometry( 100, 20, 20 );
// Then, prepare our material
var myMaterial = {
wireframe : true,
wireframeLinewidth : 2
}
// We just have to build the material now
material = new THREE.MeshPhongMaterial( myMaterial );
// Add some color to the material
material.color.setHSV(__HUE__, 1, 1);
// And we can build our the mesh
mesh = new THREE.Mesh( geometry, material );
// Let's add the mesh to the scene
scene.add( mesh );
/**
* To be sure that we will see something,
* we need to add some light to the scene
*/
// Let's create a point light
var pointLight = new THREE.PointLight(0xFFFFFF);
// and set its position
pointLight.position.x = -100;
pointLight.position.y = 100;
pointLight.position.z = 400;
// Now, we can add it to the scene
scene.add( pointLight );
// And finally, it's time to see the result
renderer.render( scene, camera );
```

And if you want to animate it (for example, make the sphere spin), it’s this easy:

```
function animate() {
// beware, you'll maybe need a shim
// to use requestAnimationFrame properly
requestAnimationFrame( animate );
// First, rotate the sphere
mesh.rotation.y -= 0.003;
// Then render the scene
renderer.render( scene, camera );
}
animate();
```

## Advanced usage

Once you master the basics, ThreeJS provides you with some advanced tools.

### Rendering system

As an abstraction layer, ThreeJS offer options to render a scene other than with WebGL. You can use the [Canvas 2D API](https://developer.mozilla.org/en/Drawing_Graphics_with_Canvas) as well as [SVG](https://developer.mozilla.org/en/SVG) to perform your rendering. There is some difference between all these rendering contexts. The most obvious one is performance. Because WebGL is hardware accelerated, the rendering of complex scene is amazingly faster with it. On the other hand, because WebGL does not deal always well with anti-aliasing, the SVG or Canvas2D rendering can be better if you want to perform some cell-shading (cartoon-like) stuff. As a special advantage, SVG rendering gives you a full DOM tree of objects, which can be useful if you want access to those objects. It can have a high cost in term of performance (especially if you animate your scene), but it allows you to not rebuild [a full retained mode graphic API](http://en.wikipedia.org/wiki/Retained_mode).

### Mesh and particles

ThreeJS is perfect for rendering on top of WebGL, but it is not an authoring tool. To model 3D objects, you have a choice of 3D software. Conveniently, ThreeJS is available with many scripts that make it easy to import meshes from several sources (Examples include: [Blender](http://www.blender.org/), 3DSMax or the widely supported [OBJ format](http://www.eg-models.de/formats/Format_Obj.html)).

It’s also possible to easily deploy particle systems as well as using Fog, Matrix and custom shaders. ThreeJS also comes with a few pre-built materials: Basic, Face, Lambert, Normal, and Phong). A WebGL developer will be able to build his own on top of the library, which provide some really good helpers. Obviously, building such custom things requires really specific skills.

### Animating mesh

If using requestAnimationFrame is the easiest way to animate a scene, ThreeJS provides a couple of useful tools to animate meshes individually: a full API to define how to animate a mesh and the ability to use “bones” to morph and change a mesh.

## Limits and precaution

One of the biggest limitations of ThreeJS is related to WebGL. If you want to use it to render your scene, you are constrained by the limitations of this technology. You become hardware dependent. All browsers that claim to support WebGL have strong requirements in terms of hardware support. Some browsers will not render anything if they do not run with an appropriate hardware. The best way to avoid trouble is to use a library such as [modernizr](http://modernizr.com/) to switch between rendering systems based on each browser’s capabilities. However, take care when using non-WebGL rendering systems because they are limited (e.g. the Phong material is only supported in a WebGL context) and infinitely slower.

In terms of browser support, ThreeJS supports all browsers that support WebGL, Canvas2D or SVG, which means: Firefox 3.6+, Chrome 9+, Opera 11+, Safari 5+ and even Internet Explorer 9+ if you do not use the WebGL rendering mode. If you want to rely on WebGL, the support is more limited: Firefox 4+, Chrome 9+, Opera 12+, Safari 5.1+ only. You can forget Internet Explorer (even the upcoming IE10) and almost all mobile browsers currently available.

## Conclusion

ThreeJS drastically simplifies the process of producing 3D images directly in the browser. It gives the ability to do amazing visual effects with an easy to use API. By empowering you, it allow you to unleash your creativity.

In conclusion, here are some cool usages of ThreeJS:

[http://highrise.nfb.ca/onemillionthtower/1mt_webgl.php](http://highrise.nfb.ca/onemillionthtower/1mt_webgl.php)[http://www.thewildernessdowntown.com/](http://www.thewildernessdowntown.com/)(To watch this one, check that your browser is allowed to move and resize pop-up windows.)[http://www.playmapscube.com/](http://www.playmapscube.com/)[http://www.ro.me](http://www.ro.me)

## About
[
Jeremie Patonnier ](https://developer.mozilla.org)

Jeremie is a long time contributor/employee to the Mozilla Developer Network, and a professional web developer since 2000. He's advocating web standards, writing documentation and creating all sort of content about web technologies with the will to make them accessible to everybody.

## 4 comments

SlimJune 14th, 2012 at 04:21Jeremie PatonnierJune 14th, 2012 at 10:13SlimJune 18th, 2012 at 06:35StormgateJune 25th, 2012 at 07:42