---
title: Diluvium – TOJam 7
url: https://theinstructionlimit.com/diluvium-tojam-7
author: Author Renaud Bédard
published: '2012-06-07'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

**Updated 15/06/2012!**

See bottom of the post for updated download links.

**Diluvium** is a game I made with [Aliceffekt](http://xxiivv.com), [Henk Boom](http://henk.ca/) and [Dom2D](http://dom2d.com) as *Les Collégiennes* over the course of TOJam The Sevening, a 48h game jam (though we had a ~8h headstart on that) which took place between May 11th and 13th 2012.

**Gameplay**

Diluvium is a versus typing tactics game.

There are two summoners on the battlefield, and you are one of them. Type animal names to summon them, and they will attack the enemy’s spawns and ultimately the enemy summoner himself. The first to kill the other one wins, as these things usually are.

You can type up to three animal names in a row, which spawns a totem of these three animals. Each animal has its own stats : speed, attack power, health and intelligence. The totem is as intelligent as its most intelligent member, and health is summed up, but movement speed is averaged.

If someone spawns a dog on the playfield, nobody can spawn another dog until it dies. No duplicate animal! Thankfully you have 284 animal names to choose from, 100 of which are illustrated differently.

The game has a half-assed single-player mode that you can access by typing “LOCAL” in the connection screen. Otherwise, the game should work fine in LAN and over the Internet, as long as you open up the server’s port 10000 (I’m not sure whether Unity networking uses TCP or UDP, so go for both). The connection screen lets you know your LAN and WAN IPs as you host the game.

Things you can also enter at the connection prompt : “MUTE” to kill the music, “IDDQD” for degreelessness mode, and one other secret code which will be revealed elsewhere on the interwebs!

For more information about the commands you can enter on the splash screen, see [Aliceffekt’s wiki page on Diluvium](http://wiki.xxiivv.com/146).

**Development**

This was the second network multiplayer game I’ve worked on that uses actual Unity networking instead of a hacked up UDP sender/receiver pair. It’s SO MUCH EASIER TO SET UP! And it works consistently, no threading bugs and random Unity crashes. Knowing this makes me much more comfortable in attempting more network-multiplayer games in jams. [The Cloud Is A Lie](http://theinstructionlimit.com/the-cloud-is-a-lie) was a nightmare to keep synchronized, it would’ve been so much easier with the built-in stuff.

We had sort of an Montréal Indie Superstar version of Les Collégiennes this time at TOJam, with [FRACT](http://fractgame.com/)‘s Henk with me on code and Dom2D as an animal portraits factory for the whole weekend. Aliceffekt and Dom’s visual styles merged really well, and having all this extra super talented manpower allowed us to create a much more ambitious game. Henk happened to have working pathfinding classes just lying around, and his deeper knowledge of Unity intricacies meant less time spent fighting bugs and oddities. It was such a great jam! ^_^

**Updates**

*Version 1.1 – 15/06/2012*

- Server Naming : You can now name your games and tell your friend to connect to it by name instead of IP! (IP still works, though)
- Anonymatching : Create a server and wait for a user, or join an anonymous server randomly!
- NAT Punchthrough : Server no longer needs to forward port 10000
- Adaptative AI : In local mode, AI opponent spawns more/less units per second depending on wins/losses
- Splash Redesign : Options better presented, no more accidental enter key press
- Balancing, a handful of new animal names supported
- Escape key quits to splash at any time during gameplay

**Downloads**

[Diluvium v1.1 – Windows version](http://theinstructionlimit.com/collegiennes/diluvium_win32.zip)

[Diluvium v1.1 – Mac version](http://theinstructionlimit.com/collegiennes/diluvium_mac.zip)

Enjoy!

Is the link for Windows broken? It’s giving me a corrupt .rar file. Thank you.

Rar file…? It’s a zip file. Works here!

it’s now working. thanks!

Posted this on Reddit! Can’t wait for more people to play it!

Can I get a link? :)

I tried to play this with a friend. But I’m stuck with “connecting to other player” and she’s stuck with “waiting for other players”. Help please?

Make sure the server (the person hosting) is redirecting port 10000 in UDP and TCP. That’s usually in the “Gaming & Applications” or “NAT Redirection” section of your router’s admin console. You need to forward the port to your local (LAN) IP.

how would i go about doing this on a mac?

Shouldn’t make a difference. It’s in the router’s web administration interface. Maybe if you use a firewall, make sure to whitelist the application so it doesn’t get blocked.

I’ve forwarded port 10000 for both TCP and UDP, and added it’s application to my list of hosted applications, but I’m still unable to play with friends. Also, as far as I can tell, my firewalls aren’t blocking the game. Any ideas?

Only the server needs to forward 10000, but otherwise as long as neither of you is behind a firewall, it should work… :S

Hey, My name is Cody and I run a blog called, Indie Game Audio Review. I loved this game and did a review of it. You can check it out here http://cflickster.noisepages.com/2012/06/diluvium-a-tojam-7-game/

Going to check out some of the other games on this site as well. Also dig Pax Britannica at the moment. Keep up the good work!

-Cody

Would love to see this on linux. I’ll be playing this from my mac later though. :-)

Linux version can only happen if Unity produces Linux builds… But once it does, sure! :)

Right, I forgot Unity doesn’t support Linux. It’s a shame, but I’m still looking forward to giving this a try. :)

Unity supports Linux now! How about a build? =)

This game is so cool. I have a couple typist friends who’d probably like this.

Works under wine, but a linux port would’ve been awesome.

Would it hurt the game too much to include a beastiary that players can refer to in and out of game so that their not forced to have to guess what has what stats?

In-game, not gonna happen. We didn’t design for that and I doubt we’ll be changing the game any more. However we have a table for the stats and names of every animal, if anyone wants to make that into a better format I’d be glad to hand it over. Someone started a wiki on wikia but it didn’t go anywhere.