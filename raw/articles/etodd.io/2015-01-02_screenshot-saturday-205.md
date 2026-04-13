---
title: Screenshot Saturday 205
url: https://etodd.io/2015/01/02/screenshot-saturday-205/
published: '2015-01-02'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 205

For the first time in the history of Lemma, I'm actually keeping up with my self-assigned pace of one new level per week.

These past two weeks I made two more frost levels. The plan calls for one more frost level, then it's on to the other two biomes.

![](../../assets/11c3e89a9520815f.jpg)


![](../../assets/11c3e89a9520815f.jpg)

Both of these levels have interesting quirks and unique features. They're probably too tough right now, but I'm scheduling plenty of time to playtest and sand down the sharp edges.

For me, the biggest challenge is to start with a blank slate and form new shapes out of nothing. It's much easier to playtest an existing design and think of ways to improve it. So I'm getting all the hard work out of the way first.

As I build these levels I finally get to implement story elements which have languished on the drawing board until now. I already have code for very simple cutscenes, and one of the five endings is basically done already.

![](../../assets/c4b8f4a1d4365093.jpg)


![](../../assets/c4b8f4a1d4365093.jpg)

I continue to solve old, long-standing gameplay annoyances.

Normally in Lemma, you can build floors by rolling or sliding off an edge, causing a blue platform to appear beneath you.

The problem is, you can spam this move and build an infinitely long blue platform. I originally prevented this with a strict rule: you can't build a platform if you're already standing on a blue surface. This rule gets the job done, but it's clunky, unintuitive, and difficult to explain to players.

I thought about another bothersome exploit that used to plague Lemma.
In older versions, you could get in a corner and climb up indefinitely by jumping between the two perpendicular walls.
The clunky solution was to nerf the wall-jump, which was admittedly ridiculous.
But the over-powered wall-jump was *fun*.

So I kept the crazy wall-jump and wrote code to specifically detect the corner case (ha). I kept a running counter of spammy corner jumps. After a certain number, it disables wall-jumping in that area.

Now, the *proper* solution is to design a game with mechanics so elegant and simple that this whole situation never arises in the first place.
But it's way too late for me to do that now, so we're stuck with this.
Surprisingly, it doesn't bother people at all. Experienced gamers immediately try to exploit the wall-jump, see that it doesn't work, and move on.
The rest of the game is unaffected, and I can keep my insane OP wall-jump.

Given the success of this exploit patch, I decided to do something similar to fix the issue with building floors. Now, when you try to build a floor on a blue surface, I do a breadth-first search to find solid ground. You can build on blue surfaces as long as you don't stray too far from solid ground.

Just like the wall-jump, the code is actually much more complicated now, but it boils down to this: you can always build floors unless you're trying to exploit.

And now for some random technical oddities. First, a quick tip if you're developing a game from scratch on Windows: make sure to handle DPI scaling properly. Lemma boots in fullscreen borderless window mode, and if the DPI scale setting is above 100%, Windows automatically scales the entire game window, which pushes most of it offscreen.

[Here's a Gist](https://gist.github.com/et1337/cd41664f88a983ec47c0) that features an app manifest which will disable auto DPI scaling for your game.

In other news, I stumbled on the [TextBelt](https://github.com/typpo/textbelt) library this week, which allows you to send SMS messages from a server for free.
It's a Node project, but the concept is simple enough to easily replicate in your server framework of choice: blast emails to every single mobile provider gateway, knowing that only one provider owns the phone number and will allow the message through.

I imagine it would be fairly easy to optimize if the gateways send back email errors. At any rate, I'm tempted to take a weekend, write a fun SMS-based party game using this library, and try it out on some friends.

That's it for this week! Thanks for reading.