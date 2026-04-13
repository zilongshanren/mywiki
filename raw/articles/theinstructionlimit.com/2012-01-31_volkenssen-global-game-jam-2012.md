---
title: Volkenssen – Global Game Jam 2012
url: https://theinstructionlimit.com/volkenssen-global-game-jam-2012
author: Author Renaud Bédard
published: '2012-01-31'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

**Volkenessen** is a game I made with [Aliceffekt](http://xxiivv.com) as *Les Collégiennes* on January 27-29 2012 as part of the 48h [Global Game Jam](http://globalgamejam.org/sites/2012/mtl-game-jam). We actually slept and took the time to eat away from our computer, so based on my estimate we spent at most 30 hours making it!

It’s a two-player, physics-based 2D fighting game. Each player starts with 9 random attached items on his back, and the goal is to strip the other player of his items by beating the crap out of him. When items are removed, they clutter up the playing area, making it even more cahotic and hilarious. The washing machine and sink in the background can also fall and bounce around!

**Controls**

You need two gamepads (so far the Xbox wired, wireless and a Logitech generic gamepad have been tested and work [you can use the [Tattiebogle driver](http://tattiebogle.net/index.php/ProjectRoot/Xbox360Controller/OsxDriver) to hook up an Xbox controller to a mac]) to play, there are no keyboard control fallback (yet). The controls are pretty exotic. To move around you can press either the D-Pad (or left analog stick) or the face buttons (A/B/X/Y), and the direction of the button does the same input as if you pressed that D-Pad direction. As you move, your player will throw a punch, kick or flail his ears to make you move as a result.

To hit the other player, you need to get close to him by hitting away from him, then hit him by moving away from him. Ramming into the opponent just doesn’t do it, you need to throw punches, and depending on the impact velocity, even that might not be enough. You can throw double-punches to make sure you land a solid hit and take off an item.

**Development**

It was made in Unity, with me on C# script and Aliceffekt on every asset including music and sound effects. I see it as one of our most successful jam games; it even won the judge award at our local GGJ space, and it was just so much fun to make, test and play.

I was surprised how well the rigid body physics worked out in the game. I had to use continuous physics on the players and tweak the gravity/mass to get the quick & reactive feel we wanted, but the game was basically playable 6 hours in! After that it was all tweaking the controls, adding visual feedback, determining the endgame condition and coerce [the GGJ theme](http://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Ouroboros-simple.svg/200px-Ouroboros-simple.svg.png) around the game.

I’ll be porting the game to the Arcade Royale in the coming days/weeks, and it should be a blast to play on a real arcade machine :)

**Downloads**

[Windows (32-bit)](http://theinstructionlimit.com/wp-content/uploads/2012/01/volkenessen_win32.zip)

[Windows (64-bit)](http://theinstructionlimit.com/wp-content/uploads/2012/01/volkenessen_win64.zip)

[Mac OS X (Universal) ](http://theinstructionlimit.com/wp-content/uploads/2012/01/volkenessen_mac.zip)

Enjoy!

Based on the trailer and the little bit that I’ve played it, great job! It’s really unique and fun. Game jams are definitely a great chance to try something different and new.

Woooww… I’m definitely liking Unity3D more and more.

– Just a quick question, the things you did in Fez? The “trixel”approach for FEZ (and I loved it by the way) do you think it is possible to port to Unity3D? I mean, it is super flexible and all that, but for example, is this just too low level? What do you think?

– What is this Arcade Royale thing? Is it this thing? <>. Are you in Montreal or something?.

Thanks!

1. No idea. Probably? I don’t know enough about custom geometry generation in Unity, or large-scale project building, to know if it’d be possible. From what I’ve seen Castle Story do (http://www.sauropodstudio.com/), I’m guessing there would be a way.

2. Mais oui j’suis à Montréal :)

Oh, it erased the webpage, (www) (montrealindies) (com/?p=222)

Volkenessen looks like an amazing game, especially for being made in just 30 hours or so. The video makes it look very retro and quirky. I’ll download it right now and try it out. I wonder if there’s any chance I could feature it on the Indie Punch website under the indie game section? Let me know.

Regards!

Andrew

Of course! :)

Just make sure to credit Aliceffekt as well.

Are you release the source code? obviously I am very curious

It is now !!

https://github.com/aliceffekt/volkenessen

Excuse me, I’m not very good with computers but, at the moment I am having a problem configuring the controls, because I am not sure what it means when it says move the joystick axis when I’m trying to configure the controls and I don’t know why, but I cannot move when in-game. I am not sure if I have to configure them but I have pressed most of the keys on my keyboard. I might be sounding like an idiot but I am not very computer-smart. Any ideas about my problem would be great, and if you have questions about it, please ask. Thank you.

Oops, sorry I did not read the part about game pads only working. But, I am happy because when you said there is no computer controls (yet) I was filled with excitement for when the computer controls will be added. I hope this game will be as good as I think it will be.

Hi,

I haven’t worked on the game ever since, so no version of the game with keyboard controls exists. Sorry!

However, the game is open source, I welcome anyone to try and add them :)

https://github.com/aliceffekt/volkenessen