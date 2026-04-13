---
title: The Cloud is a Lie
url: https://theinstructionlimit.com/the-cloud-is-a-lie
author: Author Renaud Bédard
published: '2010-09-02'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

The Cloud is a Lie is a game that me and [Aliceffekt](http://xxiivv.com/) (our team name was “Les Collégiennes”) made at a 36-hour gamejam/competition in Québec City called [Bivouac Urbain](http://www.bivouacurbain.com/). (Last year I also attended the event, and made [Stimergy](http://theinstructionlimit.com/?p=435) with Heather Kelley).

### Download

The game is available for [Windows](http://theinstructionlimit.com/collegiennes/clop.zip) or [Mac OS X](http://theinstructionlimit.com/collegiennes/clom.zip). [10 and 15Mb respectively]

### Controls

WASD or Arrows keys move. (you need to hold them)

Spacebar shoots.

M toggles the music.

Escape quits. (there may be a 2-5 seconds pause when quitting the game on Windows)

### Gameplay

The Cloud is a Lie is a LAN multiplayer game for any number of players, but best suited for 2 to 4 players. It can be played alone too, it’s just less fun.

Otherwise, it’s like Tower Defense meets Tron.

- There is a constant flow of enemies (the spinning cyan cylinders) coming in from the end of the map, and their goal is to reach your home base.
- By moving around, the players create walls that eventually fade out, but that can slow down the enemies’ movement.
- You can shoot lasers using your headpiece/weapon, and one shot kills an enemy (but there’s a cooldown time).
- You gain experience points by killing enemies, and experience points levels up your weapon (faster kills, up to 3 attacks per shot).
- The more experience you and other players gain, the more enemies are produced.
- If an enemy makes it through your defenses to your base, every player loses a level.
- The game never ends, but eventually there’s just too many enemies, everyone falls back to level 1 and the game falls back to its initial state.

### Concept

The idea was to make a multiplayer game without a server, that happens “on the wire” and free for any one to drop in or out.

So it kinda goes against the idea of cloud computing, where the client is as thin as possible and the server (or server farm) does all the work and keeps all the state. In our game, the clients are as heavy as can be, and try to maintain the state of the whole game based on the messages that are passed around.

Also, the theme of this year’s Bivouac Urbain was the song Dan Dan by [Misteur Valaire](http://blog.misteurvalaire.ca/). The song that is played in-game is Aliceffekt’s remix of that song, and it complements the gameplay nicely.

### Post-Mortem

This year’s jam was very different from last year’s. Aliceffekt is a super-productive multi-talented artist/designer/hacker and he was quite an asset at a gamejam.

The game’s design was already decided before the jam started, so that saved us a lot of time. And 12-hours in, most of the art was already done, and I was really lagging behind. :P

It was a huge challenge to me for two main reasons :

- It was my first real game in Unity (I only skimmed through tutorials before, but I use C# daily)
- It also was my first network-multiplayer game, and a weird one at that.

Most of my time at the jam was spent debugging the network code, and just messing around trying not to crash Unity. Even at the end of the 36-hours, the game had pretty bad synchronization issues between clients, different enemies on-screen and lasers shooting in the void. People seemed to like it nonetheless. :D

I can’t say I regret decisions that we’ve made, or that I/we should have done things differently. It was a great learning experience, stressful but gratifying, and jumping into unknown territory like that is one of the best ways to kick yourself in the butt and learn a technology for good. I feel infinitely more confident in using Unity now than before the jam.

About the initial concept (a headless LAN multiplayer game), I’d say that it’s feasible, but keeping the clients in sync is a big challenge. I’d also say that my implementation is pretty poor and doesn’t play well with lost packets (and it uses UDP, so no guarantee) or an unstable connection. I didn’t do any kind of client-side prediction either, but I literally flood the network with packets (every client sending 10 packets a second) so interpolation isn’t really necessary if the network can stand it.

A couple of things annoyed me with Unity, but I was at such an early learning stage that I probably did things all wrong, so they’re not worth pointing out. The general thing that stood out is that Unity is fantastic when you use the built-in stuff, and less fantastic when you want to hack it your way… but everything’s possible if you have sufficient google-fu and patience. :)

Hope you like the game!

Dear Renaud,

I was very impressed to see your and Aliceffect’s ‘The Cloud is a Lie’ game as well as your stereoscopic cube game ‘Super Hypercube’. I almost can’t believe that you did ‘TCIAL’ in 36 hours. And for hypercube: I was one of the few in our editorial office who practiced with anaglyphs and stereograms long before anyone spoke about stereoscopic television, and I always enjoyed stereo photography and wrote about it. My name is Peter Schmitz, and I work as an editor for c’t magazine in Germany. c’t is a bi-weekly printed magazine about computer technology (comparable to good old BYTE in the States), and about every 4th of its issues carries a topical cover DVD. I’m just preparing the sample DVD about the topic ‘some of the best contemporary game concepts of free and open source game development’ together with a twelve-page-article that will feature the programs that we chose. Of course, that’s free of any obligation or cost for the developers. Every developer whose game is included on the DVD will of course get a free copy of the issue of the printed magazine and of the cover DVD that his game is on.

I’d love to include both TCIAL and Super Hypercube on our DVD if you give me the permission to do so. Please get in contact with me if you like – my editorial address is psz@ct.de. But if I may ask you, please answer me quickly, for our editorial deadline for the DVD mastering is only less than a week ahead. Of course, your E-mail address will stay secret and won’t be given to anyone. No spam, that’s a question of honour. :-)

Please forgive my stumbling language (for English is not my mother tongue).

Looking forward to hearing from you,

Peter

Peter Schmitz, c’t magazine, Hannover, Germany (www.heise.de/ct)

Hi Renaud,

I found this game on the DVD mentioned above and just can say thanks that you gave your ok. I would love to play it in LAN mode, but can not find out, how to connect the clients. No Firewalls, just several win-systems in a LAN (XP and win7).

What am I supposed to do to connect the clients?

thanks for the nice game,

Dirk

Hi Dirk! Glad you found us :)

The game should run as-is in a wireless network connected to a router that works in DHCP, with all firewalls disabled. That’s the setup that I tested and I know that works.

The very first version worked with hub/switch (no router) but I had to change the code to work with routers and I lost the switch support.

If you can’t get it to work, I’ll look at it further.

Thanks!

Renaud

Hi Renaud,

thank you for the fast response. I tried in wired mode, directly connected to the router. Didn’t work, as I assume because of the internal switch in the router? I’m going to get another wireless module, test again and report.

Dirk

Hi! Look’s good. But logo on the floor look’s like “Bionic Commando” logo )

P.S. Bloom over the bots – it’s a shaders? Looks very good =)

Thanks! There is no bloom or fullscreen shader of any kind in the game, it’s just a plane with a flare on it and additive blending. :)