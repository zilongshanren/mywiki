---
title: Super Flying Thing - Update 03
url: https://blog.gemserk.com/2011/07/19/super-flying-thing-update-03/
published: '2011-07-19'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

We are testing new controller stuff on SFT for android, new controls sensibility depends on the touch position distance to the center of the screen, that means, press near the center to rotate slower and vice versa.

Also, we have a bug with Box2D on Android version, some times the ship is not attached to the planet and starts to go each time more far away and then game explodes. We are not 100% sure how to reproduce it, we will fix it but for now if you test the game on Android, be aware that this bug could happen.

Finally, the classic update list:

- New ship graphics based on a
[super 3d model](https://github.com/gemserk/superflyingthing/raw/459c03b516ad72af94bbd2211b4d8f850938259e/superflyingthing-desktop/src/main/resources/data/images/ship_animation.png)rendered with Blender (more info on a next post) - New texture for the obstacles
- Now items are a rotating star image
- New controls for Android version
- On Android, to release the ship from the planet, you have to touch over it
- One new level
- Removed thrust particle effects, at least for now (not sure about them)
- Fixed a bug that prevent instructions screen to be shown

(note: if you want, you can follow commit history [here](https://github.com/gemserk/superflyingthing/commits/master))

Remember, you can play it right now, just follow the next links:

** Play on PC** or

**:**

[play it on Android](http://www.gemserk.com/prototipos/superflyingthing-release/superflyingthing-android.apk)As always, hope you like it.