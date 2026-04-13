---
title: Building games for Firefox OS TV – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/01/building-games-for-firefox-os-tv/
author: Andrzej Mazur
published: '2016-01-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With Firefox OS focused on a world of connected devices, it’s a good time to start building games for new and different displays. Panasonic offers a variety of Firefox OS-powered TVs — in this article we’ll outline how developing HTML5 games for huge television screens differs from the smartphone approach.

## Captain Rogers revisited

My gamedev journey as [Enclave Games](http://enclavegames.com/) founder and developer started with the [first version of Captain Rogers](http://rogers.enclavegames.com/) (called Asteroid Belt of Sirius) — it was [built](https://hacks.mozilla.org/2013/12/write-elsewhere-run-on-firefox/) almost three years ago for low-end smartphones and optimized for small screens. I remember seeing it running smoothly on the Geeksphone Keon, a device with a 3.5″ screen; back then I couldn’t have imagined I would be working on the same game for a 50″ TV.

![captainrogers-mainmenu](../../assets/4fd108829d675777.png)


I was always interested in building HTML5 games using brand new technologies, implementing cutting-edge APIs, and developing for new platforms, that’s why I was so excited when I tested my game on the Keon device and realized it was working smoothly. When I saw the first smart TVs appearing on the market I wondered if one day we’d have one of those running Firefox OS, and how the performance and ease of development would compare to smartphones and the PC-based web. The [premiere of the new Panasonic TVs](https://blog.mozilla.org/blog/2016/01/05/firefox-os-will-power-new-panasonic-uhd-tvs-unveiled-at-ces/) is a great excuse to dust off the old Captain Rogers and see if he still has the spark to impress the audience, even though the audience itself has changed over these last few years.

## Planning the new version

I decided to rebuild Captain Rogers with current technologies and for bigger screens (with TV in mind). The original game was created using the [ImpactJS](http://impactjs.com/) game engine with a low base resolution of 480 x 320. Moving towards the present day, I’ve now been working with [Phaser](http://phaser.io/) to make games for more than two years, and I think it’s currently the best game engine out there for casual 2D games.

The performance of browser rendering engines has gotten a lot better, so it I didn’t think it would be a problem to make the game bigger and still keep the high frame rate. That’s why I decided to give the new version of Captain Rogers a base resolution of 960 x 640 pixels — more than enough to make the game look a lot better than the original.

![captainrogers2-cover](../../assets/9ff6cee3cfa4ff46.png)


At first I wanted to create an exact copy of the original game logic using the new framework. Originally it was going to be a direct HD remake, but I then decided to add extra features like shooting, floating enemies, and extra some visual effects. You can therefore consider it a second episode. You can already [play the demo](http://rogers2.enclavegames.com/tv/) that is being showcased now on Panasonic TVs running Firefox OS at CES 2016 in Las Vegas.

I’m currently working with [Blackmoon Design](http://blackmoondev.com/) on the full version of *Captain Rogers 2: Battle at Andromeda*, that will be released in the next month or two.

## Starting development

Many resources have been written over the years on [how to prepare your HTML5 game for Firefox OS smartphones](http://code.tutsplus.com/tutorials/preparing-for-firefox-os--mobile-18515). With the new medium, the approach is not much different (with some exceptions that are discussed below), so you can largely follow that. To start developing games for Panasonic TVs with Firefox OS you’ll need [Firefox Nightly](http://nightly.mozilla.org/) and WebIDE — all the step-by-step instructions on how to push the game to a TV through WebIDE’s remote debugging can be found in [this MDN article](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/TVs_connected_devices/How_to_connect_WebIDE_to_TV_%28VIErA%29).

## Considering huge screens

The TV in your living room is obviously different than the smartphone you’re holding in your hand, and games and other applications have to be designed somewhat differently for the new medium. And yet, building for the Web has taught us that a game should adjust its size to the screen no matter if it’s a smartphone, tablet, laptop or PC monitor, so a TV screen shouldn’t be much of a problem, and it isn’t.

### Scaling

Scaling in Phaser can be a one-liner:

this.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;

This will take care of scaling the game’s Canvas to the available screen space and maintaining the aspect ratio, so it won’t be stretched in any way. There are other ways to scale a game, but this one is the simplest, most universal solution. It will work for small smartphones and huge TVs — the only thing to consider is the resolution of the assets versus the performance of the game, so it looks good and performs reasonably well at the same time. Decisions about resolution depend on the type of game you’re building, how many assets there will be, or how much is going to happen on the screen, so it’s an individual choice.

### Controls

It’s good to know that the remote control can emulate keyboard keys, so if you have already implemented that for your game it will work out of the box:

```
this.cursors = this.input.keyboard.createCursorKeys();
//...
if(this.cursors.right.isDown) {
this.player.body.velocity.x += forcePush;
}
```


In this case, the cursor keys (corresponding arrows on the keyboard if you’re testing and playing the game on desktop) are created and can be checked later on. They have the same key codes as the arrows on the remote, that’s why it’s easier to implement and test them. If the right arrow key is pressed when playing the game, then the player’s ship will move right. You can find the exact same keys on the remote control:

![captainrogers2-remote](../../assets/41f315ff4843120b.png)


The four directional arrow keys have the exact same key codes as their keyboard counterparts, but how do you check the other keys on the remote? You can do it with a pure JavaScript approach:

```
window.addEventListener("keydown", function(evt) {
console.log(evt.keyCode);
}, this);
```


This way you’ll see the related key codes being printed in the console when pressing the buttons on your remote, so you can assign actions to them correctly in the game. You can also check the [TV remote control button mapping to keyboard](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/TVs_connected_devices/TV_remote_control_button_mapping_to_keyboard) article to make your life easier.

### Optimization

It’s important to know that TVs and other such devices tend to have hardware limitations. To make the game work smoothly it’s important to follow a few guidelines and test performance to remove any potential bottlenecks. See this [Power Surge article](https://hacks.mozilla.org/2015/06/power-surge-optimize-the-javascript-in-this-html5-game-using-firefox-developer-edition/) for tips.

## Going open source

When preparing the demo of the new Captain Rogers I decided to complete and open source my private template that I, as Enclave Games, use for game development — you can find the [Enclave Phaser Template](https://github.com/EnclaveGames/Enclave-Phaser-Template) on GitHub. I also realized that I already have a few gamedev projects there (like [Monster Wants Candy](http://gamedevelopment.tutsplus.com/tutorials/getting-started-with-phaser-building-monster-wants-candy--cms-21723) and [Cyber Orb](https://developer.mozilla.org/en-US/docs/Games/Workflows/HTML5_Gamedev_Phaser_Device_Orientation)), and it would be cool to list all of them on one page so developers can learn and benefit from them: I therefore also published [open.enclavegames.com](http://open.enclavegames.com/), a list of my most interesting open source projects.

## From MWC to CES

I was demoing the first Captain Rogers at [Mobile World Congress 2014](http://blog.end3r.com/260/enclave-games-jedzie-na-mobile-world-congress-do-barcelony/) in Barcelona on a range of Firefox OS smartphones. Since then, I’ve done a lot of talks about building games for Firefox OS with Captain Rogers included as a case study. Now it is time for the [new game](http://rogers2.enclavegames.com/tv/) to be shown on Firefox OS television at the [Consumer Electronics Show](https://www.cesweb.org/) in Las Vegas, where new Panasonic UHD TVs have been [unveiled](https://blog.mozilla.org/blog/2016/01/05/firefox-os-will-power-new-panasonic-uhd-tvs-unveiled-at-ces/). If you’re going to attend be sure to visit Mozilla at the Panasonic booth and check the game out. Give it a try and see if game development on TVs is something you’d like to do in the future. If it is, then feel free to [ping me on Twitter](https://twitter.com/end3r) and ask questions — I’m more than happy to help out.

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.

## 4 comments

Šime VidasJanuary 9th, 2016 at 20:32Andrzej MazurJanuary 10th, 2016 at 03:46StevenJanuary 18th, 2016 at 10:58Francis KimJanuary 18th, 2016 at 16:36