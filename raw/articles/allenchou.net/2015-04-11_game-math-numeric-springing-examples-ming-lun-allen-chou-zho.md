---
title: 'Game Math: Numeric Springing Examples | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2015/04/game-math-numeric-springing-examples/
author: Allen Chou
published: '2015-04-11'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

Source files are on [GitHub](https://github.com/TheAllenChou/numeric-springing)

So, you have seen how to precisely control numeric springing in my [previous post](http://allenchou.net/2015/04/game-math-precise-control-over-numeric-springing/).

I showed this animation as an example.

![spring](../../assets/d85f4810a40e49be.gif)


Manually fine-tuning the animation with animation curves can possibly give better results, if it’s a **fixed** animation, that is.

One big advantage of numeric springing over animation curves is that it can be **dynamic** and **interactive**. For instance, when the springing simulation has not completely come to a stop, and you poke the system (modify the target value or velocity) based on user input, the system can handle it gracefully with numeric springing and everything looks natural. On the other hand, it’s usually hard to interrupt an animation using animation curves and have it animate to a new target value without making it look visually jarring.

I will show you several examples of numeric springing in this post.

Before that, let’s quickly review the spring function presented in my previous post.

/* x - value (input/output) v - velocity (input/output) xt - target value (input) zeta - damping ratio (input) omega - angular frequency (input) h - time step (input) */ void Spring ( float &x, float &v, float xt, float zeta, float omega, float h ) { const float f = 1.0f + 2.0f * h * zeta * omega; const float oo = omega * omega; const float hoo = h * oo; const float hhoo = h * hoo; const float detInv = 1.0f / (f + hhoo); const float detX = f * x + h * v + hhoo * xt; const float detV = v + hoo * (xt - x); x = detX * detInv; v = detV * detInv; }


### Positional Springing

We can dynamically set the target position based on user input and have object spring to the target position accordingly.

![button spring](../../assets/c2d603a4f88f19a6.gif)


Here’s the code for this example:

void OnButonClicked(int buttonIndex) { obj.targetY = buttons[buttonIndex].positionY; obj.velocityY = 0.0f; } void Update(float timeStep) { Spring ( obj.positionY, obj.velocityY, obj.targetY, zeta, omega, timeStep ); }

### Rotational Springing

Numeric springing can also be used to make a pointer try align itself to the mouse cursor.

![angular spring](../../assets/cbb8241d92051c9c.gif)


Here’s the code for this example:

void Init() { obj.angle = 0.0f; obj.angularVelocity = 0.0f; } void Update(float timeStep) { obj.targetAngle = Atan2(obj.positionY - mouse.y, obj.positionX - mouse.x); Spring ( obj.angle, obj.angularVelocity, obj.targetAngle, zeta, omega, timeStep ); }

### Animation Springing

We can even apply numeric springing to the frame number of an animation, creating a dynamic animation that has a springy feel.

Given this animation below:

![animation spring raw](../../assets/098dd99bc91b9884.gif)


If we apply numeric springing to the frame number shown based on the mouse position, we get this effect:

![animation spring](../../assets/973036afa294c675.gif)


Pretty neat, huh?

And here’s the code for this example:

void Init() { x = 0.0f; v = 0.0f; } void Update(float timeStep) { xt = mouse.x; Spring ( x, v, xt, zeta, omega, timeStep ); obj.frame = int(obj.numFrames * (x / window.width)); }

### Orientational Springing

Lastly, let’s bring numeric springing to the third dimension.

![cube spring](../../assets/e303a9197f120fbf.gif)


Here’s the code for this example:

void Init() { angle = 0.0f; angularVelocity = 0.0f; targetAngle = 0.0f; tiltDirection.Set(0.0f, 0.0f, 0.0f); } void Update(float timeStep) { if (mouse.isPressed) // true for one frame pressed { pressPosition.x = mouse.x; pressPosition.y = mouse.y; } if (mouse.isDown) // true when held down { const float dx = mouse.x - pressPosition.x; const float dy = mouse.y - pressPosition.y; tiltDirection.Set(dx, 0.0f, dy); targetAngle = Sqrt(dx * dx + dy * dy); } Spring ( angle, angularVelocity, targetAngle, zeta, omega, timeStep ); const Vector axis = Cross(yAxis, tiltDirection); obj.orientation = OrientationFromAxisAngle(axis, angle); }

### End of Numeric Springing Examples

That’s it!

I hope these examples have inspired you to get creative with numeric springing. 🙂

Pingback: GameMaker: Easy numeric springing | Nekuro

Thanks, these are super handy! 🙂

This thing is really cool for visual effects.

Btw, how do you do these high fps gifs?

I used FRAPS to record videos and converted them to gifs using Instagiffer.

Great write up! This really explains what I only understood intuitively through playing with http://inloop.github.io/interpolator/

In any of the examples do you pragmatically change the shapes while doing springing or do just do modification of the position/rotation/scale etc.? For example in the Rotational Springing case it looks like the red arrow is bending a little bit while springing. I’m curious if it’s just an optical illusion and the shape is actually constant.

It’s definitely an illusion. I did not change the shape at all. 🙂