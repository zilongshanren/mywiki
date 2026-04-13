---
title: Story Design and Loading/Saving
url: https://etodd.io/2012/09/25/story-design-and-loadingsaving/
published: '2012-09-25'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Story Design and Loading/Saving

I now have the complete backstory and in-game story options written out!

After the initial tutorial, you'll get to a central area of the island which connects to four other areas. At that point, you'll be able to leave the island whenever you want, or you can visit one or more of the four adjacent areas before leaving. In each area you'll have to make a yes/no decision. You'll get a different ending depending on which decisions you make and at what point you exit the island. Your choices also affect how many parkour abilities you unlock. There are 5 major possible outcomes, and each outcome has a number of variations, for a total of 15.

Since the player will be twinking around different sections of the world at will and not in a linear manner, I needed to implement a load/save system and a way to handle transitions between world sections. The load/save menu is simple; saves are identified by a timestamp and thumbnail.

If you're into XNA, I implemented the screenshot feature by rendering to a RenderTexture for one frame, and subsequently copying the RenderTexture to the back buffer to prevent flickering for that one frame.

I also finally switched my voxel renderer to a more sane solution. Before, each face of the voxel was actually a hardware instance of an FBX model. I finally switched to a dynamic vertex buffer system. Everything is faster and more memory efficient now. Yay.

I forgot to mention last time that I've also made a lot of improvements to the editor (which will certainly be released for everyone to mess around with).

To help with all the obscure commands, I added a context-sensitive autocomplete menu that shows the commands you can perform based on what you currently have selected. If you're familiar with the Blender 2.5 interface, it's a lot like that.

I also added voxel copy/paste support, and the ability to move large chunks of voxel around. I also made it easier to add new material types; you can even have custom materials specific to a certain map. This should make it easier for me to create more varied and interesting maps.

More stuff that got done this week:

- When doing a roll into a low-ceiling area, the player now stays in a crouched state until they get out. Before, it just sorted of glitched.
- Fixed a really annoying bug from the alpha that had the player model spinning around the wrong way after performing a parkour move.
- Added scriptable settings that control which moves the player is allowed to perform. This will allow me to do unlockable abilities.
- Added separate crosshairs that indicate when the player can do a precision jump and when they can do a build/jump move. Before it was just one crosshair that changed color, and I think it was a little confusing.

Before I go, let me just say Borderlands 2 is a blast! And also outrageously hilarious. [Hit me up on Steam](https://steamcommunity.com/id/et1337) if you want to play sometime.

Thanks for reading!