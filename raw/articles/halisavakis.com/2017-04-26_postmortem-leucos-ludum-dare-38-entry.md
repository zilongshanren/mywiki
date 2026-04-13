---
title: 'Postmortem : Leucos (Ludum Dare 38 entry)'
url: https://halisavakis.com/postmortem-leucos-ludum-dare-38-entry/
published: '2017-04-26'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

In case you missed my tweets (in which case shame on you), I participated in the 38th Ludum Dare game jam in the “Compo” section. Although it was not my first game jam, it was my first Ludum Dare and the first game jam that I worked completely alone. The theme of LD38 was “A small world” which, at first, made me think of little planets with custom spherical gravity that I wanted to try at some point. But then I thought that I wouldn’t be able to find some fun gameplay around that, not at that time at least. I also thought that lots of people would do something similar, and so they did. So, instead I went with a biology theme, specifically the concept of a leucocyte fighting virus cells and stuff (I don’t really know much about biology :S). As far as the game itself was concerned, I wanted to do some kind of 3D top-down shooter that is kinda fun and that has cute faces in there in some way. Hence, “Leucos” was born!

Here are some screenshots:

The game can be found here: [Leucos on itch.io](https://haliss.itch.io/leucos)

and the ludum dare entry here: [Leucos – LD38](https://ldjam.com/events/ludum-dare/38/leucos)

# Gameplay

The game ended up being like those annoying MMORPG missions where you have to protect something/somebody from waves of enemies. In this case, it was a vital organ (of unspecified nature) that the hero, “Leucos” had to protect from infinite waves of virus-like creatures.

Features:

- Somewhat fast paced shooting action
- 4 different enemies: the virus, the blob, the bouncer and the shooter
- 3 different pickups: health for the vital organ, speed and explosive damage
- Some mild platform jumping, as the pickups were on floating platforms

The enemies:

- Virus: Floating, just heading straight to damage the organ. It was the first, most basic enemy.
- Blob: Grounded, came from one of the three corridors. When it died it spawned 2 smaller blobs that had lower life and didn’t divide further. It also headed straight to damage the organ.
- Bouncer: Floating and it didn’t care about the organ. It headed straight for the player to block his projectiles and to ultimately push him off the platforms. It had the most health of all.
- Shooter: Floating, headed for the organ and when it got close enough it started shooting at it.

The pickups

- Health: Just replenished some of the lost health of the organ.
- Speed: Increased the speed and fire rate of Leucos for 10 seconds.
- Explosive damage: Increased the projectile damage and spawned explosions that damaged all nearby enemies. Lasted for 10 seconds.

# What went right

### Pretty good for 48 hours

Not to pat myself on the back (besides I almost can’t reach my back) but I thought that the overall result was pretty good. It was a somewhat complete mini-game, it wasn’t broken in any way and it wasn’t too boring.

### Game feel

Maybe it’s kinda bad in a game jam, but I always try to add some sense of game feel in my games. I would not be happy with the enemies just disappearing on death, and I would not be happy if there was no reaction on hit (either on the enemies or the organ). So I added screenshakes, chromatic aberration effects, sound effects, particles, image effects and anything I could so that it felt good. And, since the result is not really cringy (not to me at least), I think I managed that.

### Graphics

I wanted to try this kind of art style, where the model is unlit but with textures, basically faking a 2D effect. I also wanted to step out of my “low-saturation colors” comfort zone and try and use vibrant saturated colors, which in the end worked for me. I was also happy with Leucos’ animations. They were not good by any means, but I have never tried doing 3D animations for a game jam before, so I’m glad they at least worked. I also liked the blob’s splatting animation, though it could have been better.

### Music and SFX

Again, not the best thing ever, but I created all the music and SFX from scratch and it was nice that they weren’t a complete failure. I actually kinda liked the sound effects, I believe they worked pretty well. And the music was one of the better ones I made, and I’m having lots of fun learning SunVox.

# What went wrong

### Gameplay

I was a bit disappointed in me as far as the gameplay is concerned. I wanted it to be something new or innovative but I couldn’t think of anything. I added the “platforming action” at the end, just to spice things up, but it wasn’t enough. I guess with practice I will get better at making more interesting mechanics.

### The freaking UI text about waves

I could not fix that to save my life (and as always I’m sure it’s something simple and stupid). You may notice that the message “Wave <number_of_wave>” (where <number_of_wave> was actually a number) sometimes stayed for 5 seconds and other times it flashed for 0.1 second or something. Wasn’t anything too serious, but it bothered me.

### The level design & camera

I probably wouldn’t be able to do something better about the level design, but still, it was too basic. Also the camera was annoying. As it’s obvious, it’s just a child of the player. Which is annoying because I didn’t want it to follow him when he jumped. But, while I had a separate script to follow him, it didn’t work well with the screenshake script because it ended up changing the camera’s position. And I didn’t want to sacrifice the sweet screenshake for a lousy camera follow script. And as I was writing this, I thought of a possible solution. Thank you rubber duck debugging!

### The blobs

To synchronize the movement with the animation was just a hell I did not want to go through. It could be done through animation events I guess, BUT I COULDN’T GET THE DAMN THINGS TO WORK. So I just left it like that. Also, plot twist, the blobs are actually flowing too. There are no rigidbody components on them whatsoever. And since I didn’t want to use any navmesh or any fancy-smancy pathfinding algorithm, they just went in a straight line. Hence the corridors. Pretty elegant solution. Not.

# Conclusion

All in all, I’m happy with the result. Considering it was made from scratch in 48 hours by one man, I think it looks and plays well. As always, it was a great experience and I learned a lot from it. And there were some other entries in the jam that were really awesome and inspiring, and that’s always good! I definitely look forward for the next big game jam!

See you in the [next one](http://halisavakis.com/postmortem-breach-prometheus-game-jam-2017/)!