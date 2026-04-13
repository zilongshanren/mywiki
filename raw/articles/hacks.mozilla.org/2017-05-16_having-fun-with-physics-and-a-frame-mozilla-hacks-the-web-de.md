---
title: Having fun with physics and A-Frame – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/05/having-fun-with-physics-and-a-frame/
author: Belén Albeza
published: '2017-05-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[A-Frame](https://aframe.io/) is a [WebVR](https://research.mozilla.org/mixed-reality/) framework to build virtual reality experiences. It comes with some bundled components that allow you to easily add behavior to your VR scenes, but you can download more –or even create your own.

In this post I’m going to share how I built **a VR scene that integrates a physics engine** via a third-party component. While A-Frame allows you to add objects and behaviors to a scene, if you want those objects to interact with each other or be manipulated by the user, you might want to use [a physics engine](https://en.wikipedia.org/wiki/Physics_engine) to handle the calculations you’ll need. If you are new to A-Frame, I recommend you check out the [Getting started guide](https://aframe.io/docs/0.5.0/introduction/getting-started.html) and play with it a bit first.

The scene I created is a bowling alley that works with the HTC Vive headset. You have a ball in your right hand which you can throw by holding the right-hand controller **trigger button** and releasing it as you move your arm. To return the ball back to your hand and try again, press the **menu button**. You can [try the demo here](https://belen-albeza.github.io/vr-bowling/)! (Note: You will need [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly) and an [HTC Vive](https://webvr.rocks/htc_vive). Follow the [the setup instructions in WebVR.rocks](https://webvr.rocks/firefox))

The ![Screenshot](../../assets/3b89720b9d09cb95.png)


[source code is at your disposal on Github](https://github.com/belen-albeza/vr-bowling)to tweak and have fun with.

## Adding a physics engine to A-Frame

I’ve opted for [ aframe-physics-system](https://github.com/donmccurdy/aframe-physics-system), which uses

[Cannon.js](http://www.cannonjs.org/)under the hood. Cannon is a pure JavaScript physics engine (not a compiled version to ASM from C/C++), so we can easily interface with it –and peek at its code.

`aframe-physics-system`

is middleware that **initialises the physics engine and exposes A-Frame components** for us to apply to entities. When we use its `static-body`

or `dynamic-body`

components, `aframe-physics-system`

creates a `Cannon.Body`

instance and “attaches” it to our A-Frame entities, so on every frame it adjusts the entity’s position, rotation, etc. to match the body’s.

If you wish to use a different engine, take a look at [ aframe-physics-system](https://github.com/donmccurdy/aframe-physics-system) or

[. These components are not very complex and it should not be complicated to mimic their behavior with another engine.](https://github.com/ngokevin/aframe-physics-components)

`aframe-physics-components`

## Static and dynamic bodies

**Static bodies** are those which are immovable. Think of the ground, or walls that can’t be torn down, etc. In the scene, the immovable entities are the ground and the bumpers on each side of the bowling lane.

**Dynamic bodies** are those which move, bounce, topple etc. Obviously the ball and the bowling pins are our dynamic bodies. Note that since these bodies move and can fall, or collide and knock down other bodies, the mass property will have a big influence. Here’s an example for a bowling pin:

```
<a-cylinder dynamic-body="mass: 1" ...>
```


## The avatar and the physics world

To display the “hands” of the user (i.e., to show the tracked VR controllers as hands) I used the [ vive-controls](https://aframe.io/docs/0.5.0/components/vive-controls.html) component, already bundled in A-Frame.

```
<a-entity vive-controls="hand: right" throwing-hand></a-entity>
<a-entity vive-controls="hand: left"></a-entity>
```


The challenge here is that the user’s avatar (“head” and “hands”) is not part of the physical world –i.e. it’s out of the physics engine’s scope, since the head and the hands must follow the user’s movement, without being affected by physical rules, such as gravity or friction.

In order for the user to be able to “hold” the ball, we need to fetch the position of the right controller and **manually set the ball’s position** to match this every frame. We also need to reset other physical properties, such as velocity.

This is done in the custom `throwing-hand`

component (which I added to the entity representing the right hand), in [its tick callback](https://aframe.io/docs/0.5.0/core/component.html#tick-time-timedelta):

```
ball.body.velocity.set(0, 0, 0);
ball.body.angularVelocity.set(0, 0, 0);
ball.body.quaternion.set(0, 0, 0, 1);
ball.body.position.set(position.x, position.y, position.z);
```


Note: a better option would have been to also match the ball’s rotation with the controller.

## Throwing the ball

The **throwing mechanism** works like this: the user has to press the controller’s trigger and when she releases it, the ball is thrown.

There’s a method in `Cannon.Body`

which **applies a force to a dynamic body**: `applyLocalImpulse`

. But how much impulse should we apply to the ball and in which direction?

We can get the right direction by calculating the velocity of the throwing hand. However, since the avatar isn’t handled by the physics engine, we need to calculate the velocity manually:

`let velocity = currentPosition.vsub(lastPosition).scale(1/delta);`


Also, since the mass of the ball is quite high (to give it more “punch” against the pins), I had to add a multiplier to that velocity vector when applying the impulse:

```
ball.body.applyLocalImpulse(
velocity.scale(50),
new CANNON.Vec3(0, 0, 0)
);
```


Note: If I had allowed the ball to rotate to match the controller’s rotation, I would have needed to apply that rotation to the velocity vector as well, since `applyLocalImpulse`

works with the ball’s local coordinates system.

To **detect when the controller’s trigger has been released**, the only thing needed is a listener for the `triggerup`

event in the entity representing the right hand. Since I added my custom `throwing-hand`

component there, I set up the listener in [its init callback](https://aframe.io/docs/0.5.0/core/component.html#init):

```
this.el.addEventListener('triggerup', function (e) {
// ... throw the ball
});
```


## A glitch

At the beginning, I was simulating the throw by pressing the space` `

bar key. The code looked like this:

```
document.addEventListener('keyup', function (e) {
if (e.keyCode === 32) { // spacebar
e.preventDefault();
throwBall();
}
});
```


However, this was outside of the A-Frame loop, and the computation of the throwing hand’s `lastPosition`

and `currentPosition`

was **out of sync**, and thus I was getting odd results when calculating the velocity.

This is why I set a flag instead of calling launch directly, and then, *inside* of the `throwing-hand`

’s `tick`

callback, `throwBall`

is called if that flag is set to `true`

.

## Another glitch: shaking pins

Using the `aframe-physics-system`

’s default settings I noticed a glitch when I scaled down the bowling pins: They were **shaking** and eventually falling to the ground!

This can happen when using a physics engine if the computations are not precise enough: there is a small error that carries over frame by frame, it accumulates and… you have things crumbling or tumbling down, especially if these things are small –they need less error for changes to be more noticeable.

One workaround for this is to **increase the accuracy of the physics simulation** — at the expense of performance. You can control this with the iterations setting at the `aframe-physics-system`

’s component configuration (by default it is set to `10`

). I increased it to `20`

:

`<a-scene physics="iterations: 20">`


To better see the effects of this change, here is a comparison side by side with iterations set to `5`

and `20`

:

*NOTE: Upload to Youtube this video and insert it here: **https://drive.google.com/a/mozilla.com/file/d/0B45CULzwzeLdNGdDTk9QOFFqQUE/view?usp=sharing*

The [“sleep” feature of Cannon](https://schteppe.github.io/cannon.js/demos/sleep.html) provides another possible workaround to handle this specific situation without affecting performance. When an object is in sleep mode, physics won’t make it move until it wakes upon collision with another object.

## Your turn: play with this!

I have [uploaded the project to Glitch](https://glitch.com/~vr-bowling) as well as to [a Github repository](https://github.com/belen-albeza/vr-bowling) in case you want to play with it and make your own modifications. Some things you can try:

- Allow the player to use both hands (maybe with a button to switch the ball from one hand to the other?)
- Automatically reset the bowling pins to their original position once they have all fallen. You can check the rotation of their bodies to implement this.
- Add sound effects! There is
[a callback for collision events](https://github.com/donmccurdy/aframe-physics-system#collision-events)you can use to detect when the ball has collided with another element… You can add a sound effects for when the ball clashes against the pins, or when it hits the ground.

If you have questions about A-Frame or want to get more involved in building WebVR with A-Frame, check out [our active community on Slack](https://aframe.io/community/#slack). We’d love to see what you’re working on.

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.