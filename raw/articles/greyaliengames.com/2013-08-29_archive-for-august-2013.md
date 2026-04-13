---
title: Archive for August, 2013
url: http://greyaliengames.com/blog/2013/08/
published: '2013-08-29'
source_blog: Grey Alien Games
source_site: http://greyaliengames.com/blog
category: game programming
fetched: '2026-04-13'
---

![TAlevel11](../../assets/6de339288715a000.jpg)


Hello and welcome! I’ve done quite a lot of work on the game since the last developer diary and you can hear me talk about the new features in the video below.

Progress has been a bit slow mainly because I’ve been working on a commercial casual game called Spooky Bonus, which will be finished in a week or so and will ship in mid-October. Then I can get back to Titan Attacks mobile as my primary project and get it done for the Autumn.

**Video**

**New Features**

For those of you inclined to reading, here’s a bit more detail!

– Read in all 20 Earth levels and made them work in game with a shop screen placeholder in between each level.

– Gave enemies correct hit points and hit boxes based on their radius.

– Made Earth enemies have correct movement. This was complex due to the way the original PC behaviour system was coded. I had to support LeftRight (with either going off screen and wrapping or bouncing off the edge and moving down), Static (with teleport), Bounce, Rotating (slaves use this)

– Made enemies shoot a basic bullet.

– Gave player shields and a death state.

– Player and enemies flash when hit.

– Skip level button for iPhone (just so I could show off the levels on a portal device).

– Added bullet limit code. The player now starts with one on-screen bullet at a time like Space Invaders and can buy more in the shop.

– Added bullet limit boost button and shield button on placeholder shop screen that appears between levels.

– Created slaves around master enemy.

– Added a few sounds related the the work done so far.

– Start, Success, Death sequences added including floating text and the ability for the player and enemies to move during those sequences. The player can even die during the success sequence, but not beat the level during the death sequence.

– Added enemy collision with player. Enemy is destroyed and does one damage to player.

– Read in all enemy bullet images and animations.

– Read in all Earth enemy bullet templates and got them working in the test screen.

– Made global behaviour, shootbrain and enemybullet instances for each enemy type on the level (this was complex!)

– Made all the enemies shoot the correct bullets and made the bullet behaviours correct.

– Added in enemey firing sounds and sounds for mines and bombs.

– Read in moon images, anims, enemies, bullets and levels and got working in a basic way. Still need to code the correct moon enemy behaviours.

**Next Up**

– Finish the moon enemy behaviours

– Player bullet upgrades (bigger more powerful bullets and also extra guns)

– Particle effects for everything inc. making bomb/mine explosions work.

– Bosses

– Powerups

– Critical hits and parachuting aliens

– Saucers and saucer special stage.

– Shop

Then it should be a home run to the end!