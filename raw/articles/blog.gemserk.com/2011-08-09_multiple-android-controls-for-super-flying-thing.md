---
title: Multiple Android controls for Super Flying Thing
url: https://blog.gemserk.com/2011/08/09/multiple-android-controls-for-super-flying-thing/
published: '2011-08-09'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Most people tell us that the game controls are not fine yet, at least for the Android version. Based on that, we are working on multiple control implementations to test and to let the user choose which controls fits best for him.

### How we manage the controls internally

To control the Ship, we created a structure named ShipController with two methods:

shouldReleaseShip() : boolean getMovementDirection() : float

The first one returns true if the Ship should be released from the planet, false otherwise. The second one returns a real number between [-1, 1] to determine the rotation direction of the Ship and the rotation speed.

That is just a structure with the values modified by the real controllers, explained next, and processed by the Ship behaviors.

### Classic controller

The classic control is the current one, you have to press one half of the screen to rotate the Ship to the right and the other half to rotate the Ship to the left.

![Classic Controller](../../assets/7085920032289649.jpg)


This controller performs an acceleration from 0 to 1 internally to the returned movement direction. This allows the player to rotate in slower but after pressing the controls for a while start rotating faster.

Problems with this controls are that it is too sensitive on Android, it may be enough to find better values for acceleration but we couldn’t find the best solution yet.

### Axis based controller

Determines the movement rotation based on a variable Axis and the current pressed position. The Axis could be horizontal or vertical its position is defined with the first pressed position.

![Axis based controller](../../assets/7fa91755df544acd.jpg)


We are just testing and we have to play a bit with the controller values to know exactly if this controller will work or not.

Some options of the controller could be to make the Axis fixed, not dependent of the first pressed position.

### Analog stick based controller

This controller behaves like an analog stick, you decide the desired Ship’s direction and the controller will do its magic to make the Ship points to that direction.

For now, the stick center is dynamic and defined with the first pressed position and the stick direction is defined with the current pressed position and the stick center.

![Analog based controller](../../assets/09bbd33af83d93f4.jpg)


A problem with this controller is we are afraid it could change all the original game play of the game, but could be for the best if it let players control the Ship in an easy way.

We are just testing it also, for now it doesn’t feel easy to use, but again, we need to test more controller values to know that better.

Same as the previous controller, one option could be to have the stick center fixed in some part of the screen.

### Tilt based controller

Finally, the Tilt based controller is just that (not implemented yet), control the Ship using device’s sensors, never worked with that before.

No image in this case, should be easy enough to imagine.

An interesting point of this controller is that it let us recover part of the screen and that could be very important for small resolution devices where your fingers could cover a great part of the screen.

### Final notes

One interesting point in testing different controls is to understand that different players need different controls, some times they need the game to adapt to them and not vice versa. We are thinking in having a controls menu or something to select the Controller you want to use and maybe some internal values.

Also, some of the controls could work for Desktop version too, have to test them a bit there to see if they fit, could be great to play using only the mouse.

As always, hope you enjoy these kind of posts.