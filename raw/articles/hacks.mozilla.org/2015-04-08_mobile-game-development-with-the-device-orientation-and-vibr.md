---
title: Mobile game development with the Device Orientation and Vibration APIs – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/04/mobile-game-development-with-the-device-orientation-and-vibration-apis/
author: Andrzej Mazur
published: '2015-04-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The market for casual mobile gaming is keeping pace with the growing market for smartphones. There are Web tools that can help web developers like you build games that compete with native games. You’ll need great execution to stand out from the crowd – using the JavaScript APIs correctly can help. For game development, you’ll want to understand the Device Orientation API and the Vibration API.


## Cyber Orb

[Cyber Orb](http://orb.enclavegames.com/) is a simple HTML5 game demo created using the Phaser framework.

![cyber-orb](../../assets/089c146184fd5ab5.png)


I was interested in [Phaser](http://phaser.io/) as a mobile game framework, because it’s fast, optimized for various mobile devices, and easy to use, plus there’s a large Phaser community. The framework is open-sourced and available on GitHub, as is the [source code of my Cyber Orb demo](https://github.com/EnclaveGames/Cyber-Orb):

[Introduction to Phaser](https://developer.mozilla.org/en-US/docs/Games/Workflows/HTML5_Gamedev_Phaser_Device_Orientation) is an MDN article I wrote that walks you through the basic steps of building a mobile game with Phaser. It shows the practical use of the Device Orientation and the Vibration APIs – and how they were implemented.

### Using the framework

I’ve used the Phaser framework to create the game, because coding it from scratch would take a lot more time and effort. Phaser takes care of the boring, necessary parts like loading assets, manipulating images on screen, or managing user input. It helps you focus on the game code and game mechanics, so you don’t have to worry about differences in browser implementations. Let’s take the controls for example. In a game created from scratch you’d have to write something like this to implement keyboard controls:

document.addEventListener("keydown", keyDownHandler, false); document.addEventListener("keyup", keyUpHandler, false); function keyDownHandler(e) { if(e.keyCode == 37) { // left cursor key leftPressed = true; } else if(e.keyCode == 39) { // right cursor key rightPressed = true; } } function keyUpHandler(e) { if(e.keyCode == 37) { leftPressed = false; } else if(e.keyCode == 39) { rightPressed = false; } }

The event listeners for key up and key down would be needed – `keydown`

to know when the key is pressed and `keyup`

to manage the situation when it is released. You have to remember the `keyCode`

for every keyboard button – for example the left cursor key is `37`

. Then, in the main game loop, you could do something like this:

if(leftPressed) { // move the ball left }

Instead of doing all that from scratch and remembering the key codes you can leave it to Phaser:

this.keys = this.game.input.keyboard.createCursorKeys();

And then:

if(this.keys.left.isDown) { // move the ball left }

The code also looks a lot cleaner and simpler this way.

### Desktop vs mobile

Although we’ll focus on mobile in this post, it’s advised to have the controls built for desktop first. If you’re building the game in your code editor and browser on desktop, you can quickly test it. Then, using a progressive enhancement approach, you can add mobile controls on top of the desktop ones with the Device Orientation API and see how different the game experience is on mobile.

## Device orientation

The [Device Orientation](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent) API specification is still in the Working Draft status, so there might be some code-breaking changes introduced in the future. It’s an experimental technology and should be treated as such. All implementations are still missing the `compassneedscalibration`

event. Also, there are differences in browser implementations which should be taken into consideration. For instance, Chrome and Opera don’t support the `devicemotion`

event.

To use the Device Orientation API in the game you have to add the listener for the `deviceorientation`

event:

window.addEventListener("deviceorientation", this.handleOrientation, true);

Everything is then taken care of in the `handleOrientation`

function:

handleOrientation: function(e) { var z = e.alpha; var y = e.beta; var x = e.gamma; Ball._player.body.velocity.x += x; Ball._player.body.velocity.y += y; }

You can extract three variables from the passed object: `alpha`

, `beta`

and `gamma`

.

var z = e.alpha; var y = e.beta; var x = e.gamma;

Those three properties contain the orientation of the device in three dimensional space. We are interested in the last two to control the ball left-right and top-bottom. The first, `alpha`

variable can be used to determine the up-down movement of the ball to make it jump. The values have different ranges: `alpha`

is from 0 to 360, `beta`

-180 to 180 and `gamma`

-90 to 90.

Having those values available in the game we can move the ball on the screen with the last two lines of code:

Ball._player.body.velocity.x += x; Ball._player.body.velocity.y += y;

That’s it – you can control the game with the Device Orientation events and you can play with your phone by tilting and shifting it around. This API can add an extra feeling of responsiveness to the game and provide a richer experience for the player.

#### Browser support

The Device Orientation API is supported from Firefox 6, Chrome 7, Opera 27 and Internet Explorer 11 on desktop, and from Firefox Mobile 6, Android 3 and Safari Mobile 4.2 on mobile devices.

### Proximity Events API

There’s also the [Proximity Events API](https://developer.mozilla.org/en-US/docs/Web/API/Proximity_Events) that could be used in the game, if the proximity sensor is available in the mobile device. It’s an experimental API, but can act as an interesting addition to the ones you’ve already used. The implementation of the API is based on two events: `deviceproximity`

and `userproximity`

. The first one provides the value-based description of the distance between the device and the object (`value`

is in centimeters) while the second one gives the boolean-based description (`near`

property is `true`

or `false`

depending on the distance). Here’s an example:

window.addEventListener('deviceproximity', function(event) { if(event.value < 20) { // something is closer than 20 centimeters to the sensor, make action } }); window.addEventListener('userproximity', function(event) { if(event.near) { // something is near the sensor, perform action } });

It could be used to turn off the screen when talking, so you don’t press anything by mistake while holding the phone close to your ear. In the game it can be used as an interesting way to control the game – an equivalent of the tap action.

#### Browser support

The Proximity Events API is supported only in Firefox, but the W3C documentation status is Candidate Recommendation, so it could be implemented by other browser vendors without any problem.

## Vibration API

The Vibration API is another feature that can boost the mobile experience. Most devices support it (except iOS Safari and Opera Mini), and it works great on Firefox OS devices.

Using the Vibration API is even easier than the Device Orientation API – all you have to do is to check whether the `window.navigator.vibrate`

function is available, and if yes, use it:

if("vibrate" in window.navigator) { window.navigator.vibrate(100); }

There’s one parameter passed to the function – the duration of the vibration. Instead of one value you can also pass the array of values and thus vibrate multiple times, for example:

window.navigator.vibrate([1000,2000,1000]);

This will make the phone vibrate for 1 second (1000 miliseconds), wait for 2 seconds and then vibrate for another 1 second. If at some point you want to turn off the vibrations you can pass `0`

or `[]`

as an argument:

window.navigator.vibrate(0);

It will stop any actual or future vibrations.

#### Browser support

The [Vibration API](https://developer.mozilla.org/en-US/docs/Web/Guide/API/Vibration) is in the Proposed Recommendation status, it works on Firefox 16 (from version 11 with the `moz`

prefix), Chrome (with `webkit`

prefix) and lately Opera (from version 27) on desktop, Firefox Mobile 11 (`moz`

) and Android (`webkit`

) on mobile.

## Summary

As you can see, using these APIs is simple and straightforward, yet enrich the experience of gameplay. The mobile gaming experience is different than desktop and you can take advantage of that. The game will work without these additional features, but it feels a lot better when the new APIs are implemented.

You can [fork the Cyber Orb demo](https://github.com/EnclaveGames/Cyber-Orb) and [play with it](http://orb.enclavegames.com/) on your own. It’s easy to extend, you can add extra features and build a complete game. If you need help with the Phaser framework you can visit the [HTML5 Gamedevs forums](http://www.html5gamedevs.com/) and reach out to the community. There’s also an [HTML5 Gamedev Starter](http://html5devstarter.enclavegames.com/) list with the links to various resources, and the [Gamedev.js Weekly](http://gamedevjsweekly.com/) newsletter with the weekly gamedev news and resources, both run by me.

## MDN and sharing the knowledge

As a developer I have used [Mozilla Developer Network](https://developer.mozilla.org/) many times looking for the answers to my coding problems and usually finding them. MDN is a huge knowledge base, but it doesn’t have to work only one way – it’s not read-only. You can easily contribute back and share your knowledge and experience with others. You can write about something you’re good at, so others can find it if they need it. Sharing the knowledge is key here and the reason our community is so friendly.

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.

## 6 comments

Šime VidasApril 8th, 2015 at 19:06Andrzej MazurApril 8th, 2015 at 22:49Šime VidasApril 9th, 2015 at 08:50Andrzej MazurApril 11th, 2015 at 11:51subzeyApril 10th, 2015 at 02:49Andrzej MazurApril 11th, 2015 at 11:52