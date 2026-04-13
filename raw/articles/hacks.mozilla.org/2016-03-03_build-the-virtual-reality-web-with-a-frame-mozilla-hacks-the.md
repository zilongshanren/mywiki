---
title: Build the Virtual Reality Web with A-Frame – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2016/03/build-the-virtual-reality-web-with-a-frame/
author: Kevin Ngo
published: '2016-03-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [WebVR team at Mozilla (MozVR)](https://mozvr.com) set out over a year ago asking, *“what would virtual reality (VR) on the Web look like?”* Today we click on links to jump from page to page, one day we will walk through portals to jump from world to world. Unfortunately, there are only a handful of WebGL developers in the world who know how to create highly interactive 3D experiences. But there are potentially millions of web developers, web designers, and 3D artists yearning for a tool to make VR content creation as easy as building a webpage.

We recently released an open-source framework called [A-Frame](https://aframe.io) for easily creating 3D and VR experiences on the Web. A-Frame puts VR content creation into our hands by allowing us to create scenes with **declarative HTML** that just work across desktop, Oculus Rift, and smartphones. We can manipulate scenes with vanilla JavaScript just as we would with ordinary HTML elements, and we can continue using our favorite JavaScript libraries and frameworks (e.g. [d3](https://www.youtube.com/watch?v=Tb2b5nFmmsM), [React](https://github.com/ngokevin/aframe-react)). A basic scene in A-Frame looks something like:

See the Pen [Hello A-Frame – 2](http://codepen.io/team/mozvr/pen/jqERjQ/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

In this scene:

- We have some basic geometries using
`<a-cube>`

,`<a-cylinder>`

,`<a-sphere>`

. - We have an image from the Web using
`<a-image>`

. - We have a 360-degree photo using
`<a-sky>`

for the background. - We can move around with the WASD keys and look around with mouse-drag.

To enter VR, we click the Goggles icon. This scene can be viewed on an Oculus Rift on desktop or on a smartphone using a Google Cardboard holder. Or, it can also function as a normal 3D scene. Read more about [entering VR](https://mozvr.com#start). The syntax above should seem familiar to most everyone; each element under `<a-scene>`

represents a 3D object, and we can modify these objects using HTML attributes. Underneath this simple markup, however, lies a flexible and extensible 3D framework.

## three.js + Entity-Component-System

Under the hood, A-Frame is a **three.js framework that brings the entity-component-system (ECS) pattern to the DOM**. A-Frame is built as an abstraction layer on top of

[three.js](http://threejs.org)and is extensible enough to do just about anything that three.js can do.

The ECS pattern is a pattern commonly used in game development that favors composability over inheritance. Since A-Frame aims to bring highly interactive 3D experiences to the Web, it adopts existing patterns from the game industry. In ECS, every object in the scene is an [entity](https://aframe.io/docs/core/entity.html), which is a general-purpose container that by itself does nothing. [Components](https://aframe.io/docs/core/component.html) are reusable modules that are then plugged into an entity in order to attach appearance, behavior, and/or functionality.

To give a simple abstract example, we might have color, tire, and engine components. We can compose entities by configuring, mixing, and plugging reusable components:

- Compose a blue car entity by using the color component set to blue, the tire components with the number set to four, and attaching the engine component.
- Compose a red bike entity by using the color component set to red, the tire components with the number set to two, and not attaching the engine component.
- Compose a yellow boat entity by using the color component set to yellow, the tire components with the number set to zero, and attaching the engine component.

![Entity-Component-System](http://thevrjump.com/assets/img/articles/aframe-system/aframe-example.jpg)


*Abstract representation of the entity-component-system pattern by Ruben Mueller of The VR Jump.*

In A-Frame:

- An entity is represented by
`<a-entity>`

. It is the core building block that comprises everything within a scene. - A component is represented by an HTML attribute (e.g.
`<a-entity engine>`

). - A component’s properties are passed via a string into a HTML attribute where it will be parsed later.
- If a component has only one property to define, then it looks like a normal HTML attribute (e.g.
`<a-entity visible="false">`

). - If a component has more than one property to define, then properties are passed in through a syntax similar to inline CSS styles (e.g.,
`<a-entity engine="cylinders: 4; horsepower: 158; mass: 200">`

).

Take `<a-cube>`

for example, we can break it down into geometry (shape) and material (appearance) components:

```
<!-- <a-cube>'s actual form. -->
<a-entity geometry="primitive: box; depth: 2; height: 10; width: 4"
material="color: #FFF; src: url(texture.png)">
```


Developers can write components to do just about anything and share them with other developers to plug-and-play. Let’s configure and attach more components to compose a more complex entity:

![Composing an Entity](../../assets/f0179737e732353d.gif)


In an ECS pattern, nearly all logic and behavior should be encapsulated within components to encourage modularity and reuse.

## Building an Interactive Scene

Let’s go through an example building a scene where the workflow revolves around writing components. We’ll build an interactive scene in which we fire lasers at enemies surrounding us. We can use the standard components that ship with A-Frame, or use components that A-Frame developers have published to the ecosystem. Better yet, we can write our own components to do whatever we want!

If you want to follow along, there are several ways to get coding with A-Frame:

- Play within
[CodePen](http://codepen.io/team/mozvr/pen/BjygdO?editors=100). - Grab the
[Boilerplate](https://github.com/aframevr/aframe-boilerplate). - Include the
[JS Build](https://aframe.io/releases/0.1.2/aframe.min.js). [Install from npm](https://www.npmjs.com/package/aframe).- Play with the
[finished example on CodePen](http://codepen.io/team/mozvr/pen/PNoWEz/?editors=1000).

Let’s start by adding an enemy target:

See the Pen [Laser Shooter – Step 1](http://codepen.io/team/mozvr/pen/wGBLeB/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

This creates a basic static scene where the enemy stares at you even as you move around. We can use A-Frame components from the ecosystem to do some neat things.

### Using Components

The [awesome-aframe repository](https://github.com/aframevr/awesome-aframe#components) is a great place to find components that the community has created to enable new features. Many of these components are started from the [Component Boilerplate](https://github.com/ngokevin/aframe-component-boilerplate) and should provide builds in the `dist/`

folders in their repositories. Take the [layout component](https://github.com/ngokevin/aframe-layout-component) for example. We can grab the build, drop it into our scene, and immediately be able to use a 3D layout system to automatically position entities. Instead of having one enemy, let’s have ten enemies positioned in a circle around the player:

See the Pen [Laser Shooter – Step 2](http://codepen.io/team/mozvr/pen/bpNPjp/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

It is messy in markup to have the enemy entity duplicated ten times. We can drop in the [template component](https://github.com/ngokevin/aframe-template-component) to clean that up. We can also use A-Frame’s [animation system](https://aframe.io/docs/core/animation.html) to have enemies march in a circle around us.

See the Pen [Laser Shooter – Step 3](http://codepen.io/team/mozvr/pen/JXoQBm/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

By mixing and matching the layout and template components, we now have ten enemies surrounding us in a circle. Let’s enable gameplay by writing our own components.

### Writing Components

Developers comfortable with JavaScript and three.js can write components to add appearance, behavior, and functionality to entities. As we’ve seen, these components can then be reused and shared with the community. Not all components have to be shared; they can be ad-hoc or one-off.

Components consist of data, which are defined by the schema and can be passed in through HTML, and lifecycle methods, which define how the data is used to modify the entity it’s attached to. The lifecycle methods usually interact with the three.js, DOM, and A-Frame APIs. My previous blog post on [How to Write an A-Frame VR Component](http://ngokevin.com/blog/aframe-component) goes into more detail on using the component API to register a component.

For the scene, we want to be able to fire lasers at the enemies to make them disappear. We will need components to create lasers on click, to generate clicks, to propel the lasers, and to check for when a laser hits an enemy.

#### spawner Component

Let’s start by being able to create lasers. We want to be able to spawn a laser entity that starts at the player’s current position. We’ll create a spawner component that listens to an event on the entity, and when that event is emitted, we’ll spawn an entity with a predefined [mixin](https://aframe.io/docs/core/mixin.html) of components:

```
AFRAME.registerComponent('spawner', {
schema: {
on: { default: 'click' },
mixin: { default: '' }
},
/**
* Add event listener to entity that when emitted, spawns the entity.
*/
update: function (oldData) {
this.el.addEventListener(this.data.on, this.spawn.bind(this));
},
/**
* Spawn new entity with a mixin of componnets at the entity's current position.
*/
spawn: function () {
var el = this.el;
var entity = document.createElement('a-entity');
var matrixWorld = el.object3D.matrixWorld;
var position = new THREE.Vector3();
var rotation = el.getAttribute('rotation');
var entityRotation;
position.setFromMatrixPosition(matrixWorld);
entity.setAttribute('position', position);
// Have the spawned entity face the same direction as the entity.
// Allow the entity to further modify the inherited rotation.
position.setFromMatrixPosition(matrixWorld);
entity.setAttribute('position', position);
entity.setAttribute('mixin', this.data.mixin);
entity.addEventListener('loaded', function () {
entityRotation = entity.getComputedAttribute('rotation');
entity.setAttribute('rotation', {
x: entityRotation.x + rotation.x,
y: entityRotation.y + rotation.y,
z: entityRotation.z + rotation.z
});
});
el.sceneEl.appendChild(entity);
}
});
```


#### click-listener Component

Now we need to a way to generate a click event on the player entity in order to spawn the laser. We could just write a vanilla JavaScript event handler in a content script, but it is more reusable to write a component that can allow any entity to listen for clicks:

```
AFRAME.registerComponent('click-listener', {
// When the window is clicked, emit a click event from the entity.
init: function () {
var el = this.el;
window.addEventListener('click', function () {
el.emit('click', null, false);
});
}
});
```


From HTML, we define the laser mixin and attach the spawner and click-listener components to the player. When we click, the spawner component will generate a laser starting in front of the camera:

See the Pen [Laser Shooter – Step 4](http://codepen.io/team/mozvr/pen/jqEjvB/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

#### projectile Component

Now lasers will spawn in front of us when we click, but we need them to fire and travel. In the spawner component, we had the laser point in the rotation of the camera, and we rotated it 90-degrees around the X-axis to align it correctly. We can add a projectile component to have the laser travel straight in the direction it’s already facing (its local Y-axis in this case):

```
AFRAME.registerComponent('projectile', {
schema: {
speed: { default: -0.4 }
},
tick: function () {
this.el.object3D.translateY(this.data.speed);
}
});
```


Then attach the projectile component to the laser mixin:

```
<a-assets>
<!-- Attach projectile behavior. -->
<a-mixin id="laser" geometry="primitive: cylinder; radius: 0.05; translate: 0 -2 0"
material="color: green; metalness: 0.2; opacity: 0.4; roughness: 0.3"
projectile="speed: -0.5"></a-mixin>
</a-assets>
```


The laser will now fire like a projectile on click:

See the Pen [Laser Shooter – Step 5](http://codepen.io/team/mozvr/pen/YqPmzK/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

#### collider Component

The last step is to add a collider component so we can detect when the laser hits an entity. We can do this using the [three.js Raycaster](http://threejs.org/docs/index.html#Reference/Core/Raycaster), drawing a ray (line) from one end of the laser to the other, then continuously checking if one of the enemies are intersecting the ray. If an enemy is intersecting our ray, then it is touching the laser, and we use an event to tell the enemy that it got hit:

```
AFRAME.registerComponent('collider', {
schema: {
target: { default: '' }
},
/**
* Calculate targets.
*/
init: function () {
var targetEls = this.el.sceneEl.querySelectorAll(this.data.target);
this.targets = [];
for (var i = 0; i < targetEls.length; i++) {
this.targets.push(targetEls[i].object3D);
}
this.el.object3D.updateMatrixWorld();
},
/**
* Check for collisions (for cylinder).
*/
tick: function (t) {
var collisionResults;
var directionVector;
var el = this.el;
var sceneEl = el.sceneEl;
var mesh = el.getObject3D('mesh');
var object3D = el.object3D;
var raycaster;
var vertices = mesh.geometry.vertices;
var bottomVertex = vertices[0].clone();
var topVertex = vertices[vertices.length - 1].clone();
// Calculate absolute positions of start and end of entity.
bottomVertex.applyMatrix4(object3D.matrixWorld);
topVertex.applyMatrix4(object3D.matrixWorld);
// Direction vector from start to end of entity.
directionVector = topVertex.clone().sub(bottomVertex).normalize();
// Raycast for collision.
raycaster = new THREE.Raycaster(bottomVertex, directionVector, 1);
collisionResults = raycaster.intersectObjects(this.targets, true);
collisionResults.forEach(function (target) {
// Tell collided entity about the collision.
target.object.el.emit('collider-hit', {target: el});
});
}
});
```


Then we attach a class to the enemies to designate them as targets, attach animations that trigger on collision to make them disappear, and finally attach the collider component to the laser that targets enemies:

```
<a-assets>
<img id="enemy-sprite" src="img/enemy.png">
<script id="enemies" type="text/x-nunjucks-template">
<a-entity layout="type: circle; radius: 5">
<a-animation attribute="rotation" dur="8000" easing="linear" repeat="indefinite" to="0 360 0"></a-animation>
{% for x in range(num) %}
<!-- Attach enemy class. -->
<a-image class="enemy" look-at="#player" src="#enemy-sprite" transparent="true">
<!-- Attach collision handler animations. -->
<a-animation attribute="opacity" begin="collider-hit" dur="400" ease="linear"
from="1" to="0"></a-animation>
<a-animation attribute="scale" begin="collider-hit" dur="400" ease="linear"
to="0 0 0"></a-animation>
</a-image>
{% endfor %}
</a-entity>
</script>
<!-- Attach collider that targets enemies. -->
<a-mixin id="laser" geometry="primitive: cylinder; radius: 0.05; translate: 0 -2 0"
material="color: green; metalness: 0.2; opacity: 0.4; roughness: 0.3"
projectile="speed: -0.5" collider="target: .enemy"></a-mixin>
</a-assets>
```


And there we have a complete basic interactive scene in A-Frame that can be viewed in VR. We package power into components that allow us to declaratively build scenes without losing control or flexibility. The result—a rudimentary FPS game that supports VR in ultimately **just 30 lines of HTML**:

See the Pen [Laser Shooter – Final](http://codepen.io/team/mozvr/pen/reaXNr/) by MozVR ([@mozvr](http://codepen.io/mozvr)) on [CodePen](http://codepen.io).

## Community

The community has built some great things with only the initial version of A-Frame. Check out what has been shared on [Made With A-Frame](http://aframevr.tumblr.com/) and [Awesome A-Frame](https://github.com/aframevr/awesome-aframe).

We all hang out on the [A-Frame Slack](https://aframevr-slack.herokuapp.com/) which currently has almost 350 people kicking the tires. Play with [A-Frame](https://aframe.io), and come tell us what you think! Virtual reality is coming, and you don’t want to miss the train.

## About
[
Kevin Ngo ](http://ngokevin.com)

Kevin is a virtual reality developer at Mozilla and a core developer on A-Frame, an open-source WebVR framework. He is @ngokevin_ on Twitter.

## 8 comments

动感小前端March 5th, 2016 at 08:36Ruben MüllerMarch 7th, 2016 at 22:02Mobilock ProMarch 11th, 2016 at 04:23MattMarch 11th, 2016 at 18:17niutechMarch 13th, 2016 at 14:26Kevin NgoMarch 13th, 2016 at 14:53Ardianorio773March 14th, 2016 at 21:38Mike BradfordMarch 29th, 2016 at 03:50