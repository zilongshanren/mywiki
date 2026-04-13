---
title: Archive for April, 2013
url: http://greyaliengames.com/blog/2013/04/
published: '2013-04-21'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

![13-04-21In-game iPad Portrait](../../assets/6497cc58f4e8a95e.jpg)


*game screen in iPad portrait mode*

Once again, it’s been a while since my last Titan Attacks mobile developer diary – 3 months in fact! That’s due to a bunch of things such as:

– Re-launching [Spring Bonus](http://www.greyaliengames.com/springbonus/index.php) on mobile.

– Overseeing the mobile port of [The Wonderful Wizard of Oz](http://www.greyaliengames.com/oz.php) (it’s shipping soon.)

– Starting [Techno Zombies](https://www.youtube.com/watch?v=EBx3Cyh_6nY) as my January #onegameamonth but going way overboard and deciding to put it on the backburner for when Titan Attacks mobile is done.

– Making two other #onegameamonth games.

– Family illness (February was pretty much a write off due to colds/flus.)

– Going to GDC and having a week of unproductive jetlag when I got back.

At least when I was working on other games my Monkey game framework has improved a lot (Monkey is the programming language I use) as well as my knowledge of the language as a whole, which benefits Titan Attacks mobile.

Now I have an empty schedule, which feels nice, and have began working on Titan Attacks in earnest.

Here’s what I’ve been up to:

**Controls**

– Added a second finger to fire in easy mode but after showing it to Cas (designer of original Titan Attacks) we decided to make the alien parachute immune to your bullets so that we can stick with a single finger in “easy mode” instead.

– Tweaked the placement of the slider and fire button and their hit boxes to make it easier to move the ship right to the edge of the screen and to not clash with the fire button. This mode is still a bit awkward on iPhone so it’s likely that it’ll only be available on iPad, or if it is on iPhone, it will be an option only and “easy mode” will be the default.

– Fixed a bug where I couldn’t tap fire faster than the auto-fire. When I first saw this I got paranoid the game wasn’t receiving input fast enough and boosted the update rate to 120FPS instead of 60FPS, but was worried this could be really slow on old devices. Luckily now I’ve fixed it, I can safely go back to 60FPS.

– Had a meeting with Cas and decided to only support portrait on iPhone as there’s no where to put the slider under the game screen in landscape mode. iPad can support both orientations though.

– Made it so that you the slide range for easy mode (single finger) is smaller than the screen width so it’s easier to drag the tank right to the edge on phones.

– Made sure any finger can be used for positioning in easy mode and that the finger must be below the HUD to fire so it doesn’t clash with HUD button presses. Multi-touch controls are complex btw!

– Added device detection to framework and different default controls based on device.

– Added ability to flip the slider controls for left-handed people.

**Testing**

– Did a bunch of testing on iphone and verified that there’s no memory leak when changing screens. Pretty important as the iDevices have low memory and just bomb out if you use too much.

– Added an FPS Counter. Runs at 60FPS no problems at the moment, yay!

– Showed the game to some press and a bunch of indie friends at the Game Developer Conference in San Francisco. They seemed to agree with our control choices and commented that the game felt smooth.

– Looked into why touching a finger onto the iPhone doesn’t show the ship right above it. It goes to the right with a right hand finger and left with a left hand finger! Can’t do anything about it as it just seems to be the way iDevices detect your finger. It’s not a big deal though, I was just being perfectionist and wanted it to detect the exact middle of my finger.

**GUI**

– Added button hover and click sounds.

– Add clicked and mouse over graphic for buttons.

– Added the ability to transistion screens on/off in sequence or at the same time. The transition state is exposed to the screen to do whatever it wants with such as slide on/off, fade in/out, alpha fade over another screen, zoom in/out etc. It’s pretty cool.

– Added ability to slide screens on/off and used it on the in-game menu and options menu.

– Added screen fade out/in including the music.

– Added word-wrapping to my framework. Had to learn how Monkey handles string functions differently from BlitzMax.

– Made game detect device orientation change and reconfigure GUI to either portrait or landscape mode based on device size. This looks pretty cool and people seem to be impressed when they see it in action.

– Zoomed out the game screen for iPad Landscape mode and placed controls underneath. Works well, although we may have the game screen full size and integrate the controls with the ground somehow instead.

– Increased hit box for in-game buttons and title screen buttons/URL on iPhone.

**Engine**

– Added floating text particle support to my framework and made aliens give out a floating “10”

– Made sure all images and sounds are properly discarded instead of relying on Garbage Collection. I did this because I read that GC can’t be trusted on all devices and I need to make sure I’m not wasting any previous Megabytes of memory on iDevices.

– Coded AnimdDef and Animator classes and applied to Sprite class. Supports Once, Loop (several or infinite), Ping Pong. Also supports reverse and a non-zero starting position (can be randomised).

– Coded Animation class which is an array of AnimFrames so that animations can come from a collection of randomly placed images on a texture atlas. This means I can use [TexturePacker](http://www.codeandweb.com/texturepacker) and create 2048×2048 optimised textures with whitespace (alpha) removed so that I consume as least memory as possible on iDevices.

– Coded AnimationBank class to hold animations.

**Game**

– Added in a wall of aliens to test collision, particle effects and animation.

– Added some placeholder particle effects for when the aliens explode.

**Next Up**

My framework is pretty much done now and I need to focus on getting the game content added and working. That’s quite a big task because there are 100 levels spread over 5 worlds with many different aliens (and bosses!) all with different behaviours and special effects. I also have to add a shop and do more GUI work. So there’s still a lot to do.

Here’s what I’m planning on doing next:

– Make a loader that works with TexturePacker’s output format. Should be easy.

– Read in the animation xml files from the original game and make sure they pick the correct images from the texture atlases.

– Animate tank when moving.

– Make all different tank sizes, add ons and bullet sizes work.

– Read in the level files and display the correct aliens. (They won’t be using their correct behaviours as that is a whole load more code to be done later.)

Well hopefully the next developer diary will be pretty soon as I need to get this game done and out by the summer.