---
title: Animated Loading Icon In UE4 UMG
url: https://www.gamedeveloper.com/art/animated-loading-icon-in-ue4-umg
author: James Rowbotham
published: '2018-09-04'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

My name is James, I'm an indie game developer ([@cbGameDev](http://twitter.com/cbGameDev)). I make bigger games with my friends in a studio I helped start up and make smaller games on my own in my spare time!


We started having issues with our loading screen icon when we updated “[The Black Death](https://store.steampowered.com/app/412450)” engine version to Unreal V4.20. We were using the UMG throbber widget at that point to display a rotating skull texture, however, after the update, it was fine in the editor but would only appear as a default icon in cooked builds for some reason.

I was going to try and fix it but then instead, I decided to spend a little more time creating a new custom loading icon that didn’t rely on the throbber widget and had a little more personality. I wanted to create a looping rat running silhouette (like a gif) as I thought it would fit nicely with the Plague theme of the game.

Initially, my plan was to use Unreals Paper 2D sprite system. However, I found that this was not currently supported by UMG (Unreals UI system). So I did a bit of research and in the end, I created a flipbook texture, made up a material and utilised the flipbook node instead. Below is the end result:


Here was my process:

We already had a rat in-game with running animations, so I went and rendered out a full loop from an orthographic view. You can do this from your 3D program of choice and you can probably screenshot in an orthographic view from within engine as well if you don’t have the original rig/animations. I chose to render the background as a solid colour to help me when it came to aligning in Photoshop.




I put these images into Photoshop using grid lines and the solid black background squares to help space them equally on the canvas.






When the images were aligned I needed to remove the background. We can select only the background by using “Colour Range” and colour picking the background colour. Once selected we can “Shift + Ctrl + I” to inverse the selection and then create a white solid colour layer to give us the silhouette of the rat that we want.




Then making sure that the image is a power of 2 (so it can benefit from UE4s texture compression etc) we can save the file off as a PNG and import this into Unreal, making sure to set the texture group to “UI”. I also optimised the texture by bringing the LOD bias to 1 as the loading icon didn’t need to be such a high resolution.




Next up I started working on a master material. The “Material Domain” needed to be set to “User Interface” so that it could work with UMG and I also set the blend mode to “Translucent”. Having it set to “Masked” would have been cheaper but I needed to be able to adjust its opacity with the rest of the UI, when transitioning/fading to gameplay.


I made sure to “Convert to parameter” a lot of elements so that we could play with them in its Material Instances. The time and “Playspeed” control the rate of play of the loop. The flipbook node does the main work, but we need to feed it some info so it knows how to split up the texture we give it: number of rows and number of columns (in our case 3 rows and 4 columns). Then at the end, I just multiply a colour over everything using the alpha as a mask. You can tint images in UMG but I thought it was useful to have it changeable at a base level as well, in case we needed to change it across the board.



Next up I created a Material Instance from our new material. The default settings were fine in this case as they were set up with this specific looping animation in mind. Then I applied the material to an image widget in the UI and hey hey it works.



And that's it! I could probably go back to the texture and optimise it by realigning and reducing the amount of dead space, but all in all, it's pretty simple,

I hope you find this useful!

Cheers

James