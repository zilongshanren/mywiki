---
title: Archive for March, 2015
url: http://greyaliengames.com/blog/2015/03/
published: '2015-03-25'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

We are proud to announce that our Android port of Titan Attacks has debuted in the [Humble PC & Android Bundle 12](https://www.humblebundle.com/)!

As of writing the bundle is at 62,580 sales and $328,000. We’re hoping it’ll reach at least $500K by the end of the bundle in 6 days’ time.

The port was actually finished in August 2014, but because we agreed to debut in a Humble PC/Android bundle, we haven’t put the game on Google Play yet. We just missed our chance to get in the PC/Android bundle 11 in Sept 2014, which resulted in a 7 month wait until this one came around.

**Developer Diary**

The last [developer diary](http://greyaliengames.com/blog/titan-attacks-mobile-developer-diary-8-jupiter-and-titan/) I did for the port was in December 2013. Back then I had just finished porting the 5th and final world, Titan, including all the enemies.

However, there was still a ***lot*** to do to make it shippable. Here’s the full list of stuff I did since then:

– Parachute added after some critical hits.

– Boss looping sounds added.

– Animation offset command for moon and titan boss eyes.

– Made Animation scale command work (for player bullets as they appear).

– Tank now fires 9 different powers of bullets.

– Made supergun work. It’s cool.

– Made player and enemy bullets use correct radius if they are exploding e.g. for rockets and mines.

– Loaded in player tank graphic, glow, turret and shadow from xml file.

– Player flashes white during immune period at start of level

– Screen strobes red when player is hit

– 4x Add Ons coded and added to shop. Two bullets, an exploding rocket and a laser.

– Added explosion effect to enemy bombs and mines.

– Made it easier to pick up parachutes including when your tank has add ons.

– Tank invulnerability shield added

– Smartbomb coded and added to shop

– Saucer added

– Optimised iOS loading and memory use by only loading in images, anims, objects, levels for the current world.

– Make shop menu fit on screen in landscape mode

– Made teleporting enemies fade properly

– Added support for Offset Delta and Scale Delta animation commands.

– Powerups added (dropped by saucers)

– Made the HUD taller in portrait mode for longer devices and positioned the game screen accordingly.

– Made the game screen scale on landscape mode differently for phone/tablet.

– Added Smart Bomb button and positioned.

– Added in graphics for One Thumb slider mode and positioned/scaled appropriately for all devices.

– Added in graphics for Two Thumb slider mode and positioned appropriately for all devices.

– Added in proper shield bar graphics.

– Made sure that area behind HUD and controls are solid black so that aliens, smartbombs and bullets don’t draw there.

– Added HUD line in portrait mode and HUD gradient in landscape mode.

– Added new in-game Menu button.

– Added in cash, score and X (for multipler) label graphics and positioned in portrait and landscape mode.

– Added flashing red shield graphics for when shield is 0

– Added in basic background sides for landscape mode

– Fixed bug from original game where if multiple alien lasers hit tank at same time you would be instantly destroyed.

– Fixed bug from original game where Galaxian slaves (on Mars) were sometimes missing due to starting off screen.

– Finished About screen UI

– Finished Title screen UI in portrait and landscape (but not animated title image)

– Finished Loading screen UI including loading bar

– Finished in-game menu UI

– Finished options screen UI including sliders for sound/music and control method toggles.

– Made game save and restore sound/music volumes.

– Shop screen done in portrait and landscape. Everything works now including animated tank+blueprint in landscape mode.

– Added Choose Control screen to appear on first play.

– Added authentic particle emitters for: enemy/boss ricochet, enemy/boss explosion including slave and chained emitters, turret smoke ‘n’ sparks

– Got it running on Android phone!

– Added shop music

– Saucer explosion + floating score.

– Made all relevant particles glow using additive blending.

– Challenge mode added.

– Added authentic particle emitters for player bullets and addons.

– Added player death explosion.

– Added authentic enemy critical hit particle emitter.

– Added authentic enemy bullet particle emitters including rocket trail.

– Added authentic alien laser emitter and centipede pod emitter.

– Added teleport emitter and created sound for it as original game had none.

– Added authentic emitters for parachute death and collection.

– Added authentic emitters for powerup pickup.

– Missed powerups now have a different sound and a different emitter.

– Texture atlases are done!

– Added lerp to one thumb mode and sped up lerp in two thumb mode.

– Made it so you can slide anywhere on the screen in one thumb mode to move but bomb buttons still require a tap (and they have a smaller hitbox)

– Boosted radius of saucers so they are easier to hit.

– Added draw batching for glowing sprites to speed up rendering on phones.

– Layered all glowing sprites and emitter particles correctly.

– Optimised particle creation so the game should run faster on older phones.

– Make game support trimmed texture atlases to save memory on phones with small heap.

– Using original font for the floating scores and $ values.

– Fixed player bullets so that they disappear when off screen and not just before.

– Fixed enemy size so that firing when off screen calculation is more accurate.

– Added meteors.

– Prevented Quit from being used during the player death anim.

– Added enemy bullet shadow.

– Made sure background sides are drawn on top of all particles.

– Stopped smart bombs from showing at extreme edge of very wide screens.

– Added animated backgrounds to every level.

– Made a hard limit of 1000 particles and made sure it doesn’t crash.

– Animated title screen done!

– Added HSB color transition to smoke particles.

– Boosted Two Thumb Mode move button hitbox Y. So if your finger slips off it still works.

– Added flashing High Score to title screen.

– Music now changes every level.

– Made smartbomb sound louder.

– Converted all sounds and music to .ogg format.

– Android back button now works like Escape key on all screens and does a nice close of title screen.

– Boosted fire button hitbox to the side whenever possible (not in portrait on phones.)

– Moved controls up from bottom of screen a bit in portrait mode on >4:3 Android devices to avoid clashing with on-screen buttons that some androids have. Also same for landscape mode but only for two thumb controls on tablets as there’s no room to do this for one thumb controls or on phones.

– Added more steps to loadinging bar for sounds.

– Added sound triggers to stop multiple versions of common sounds playing in same frame.

– Tablet controls will now only be used on devices 8″ and larger. e.g. iPad size.

– Moved Slider control for Two Thumb mode in a bit from the side so that left can always be reached easily.

– Made player bullets disappear a bit sooner off screen so that firing feels faster to player.

– Made Moon boss a bit easier by allowing it to go higher up the screen.

– Made red text fade from yellow to red as per original game.

– Added an icon.

**– SHIPPED!**

Hopefully you can get some sense of the work involved in finishing a game from that list. Don’t forget that I’d already done a ton of work before that final push. Also there was a lot of testing and tweaking the mobile controls during those final stages.

I’m very pleased with the result, and so is Puppy Games. It’s an authentic port in every detail and I also made sure that it runs on slower Android devices without much memory. As a result we haven’t had any major launch issues and have received some nice positive feedback too. YAY!