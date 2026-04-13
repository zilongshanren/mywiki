---
title: Our solution to handle multiple screen sizes in Android – Part three
url: https://blog.gemserk.com/2013/09/12/our-solution-to-handle-multiple-screen-sizes-in-android-part-three/
published: '2013-09-12'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

In the previous posts of this series we talked about our solution to handle multiple screen sizes for game menus, in particular we showed the main menu of the game Clash of the Olympians. In this post we are going to talk about what we did inside the game itself. As a side note, the solution we used here is simple and specific for this game, hope it could help as example but don’t expect a silver bullet.

### Scaling to match the physics world

As we use Box2D in Clash of the Olympians, the first step was to use a proper scale between Box2D bodies and our assets. The basic approach was to consider that 1m (meter in MKS system) was 32px, so in our target resolution of 800x480 could show 25m x 15m. We picked that scale because it gives pretty numbers both in terms of the game area and in terms of our assets, for example, a character of 64px of height is 2m tall. In particular, Achilles has a height of approx 60px which is equivalent to 1.875m using our scale, that sounds pretty reasonable for that character.

![clashoftheolympians-800x480](../../assets/0ebd8532c0bae9db.jpg)


The image shows the relation between screen size in pixels (800x480 in this case) and the game world in meters.

### Defining a virtual area to show

We previously said that we could show 25m x 15m, in fact, the height is not so important in Clash of the Olympians since the game mainly depends in the horizontal distance. So, if we had an imaginary with a resolution of 800x400 (really wide, an aspect ratio of 2) we would show in that case 12.5m of height, we could assume that if we show at least that height the game balance would be not affected at all (enemies are never spawned too high). However, in terms of horizontal distance we want to show always the same area across all devices to avoid changing the game balance (for example, if you could see less area you couldn’t react in the proper time to some waves), that is why we decided to show always 25m in terms of width.

The image shows how we still show the same game world width of 25m on a 800x600 device.

### Scaling the world back to match the screen size

Finally, in order to show this virtual area of 25m x H (with H >= 12.5m), we have to calculate the proper scale to set our game camera in each device. For example, in the case of having a Nexus 7 (1280x720 resolution device) the scale to show 25m of horizontal size is 51.2x since we know that 1280 / scale = 25, then 1280 / 25 = 51.2. In the case of a Samsung Galaxy Y (480x320 resolution device) the scale would be 19.2x since 480 / 25 = 19.2. Translating this inside the game would be something as easy as:

`camera.scale = screen.width / 25`


### Final thoughts

This is not a general solution, it depends a lot in the game we were making and the things we could assume like the game height doesn’t matter.

Even though the solution is specific and not so cool as the previous posts, we hope it could be of help when making your own game.