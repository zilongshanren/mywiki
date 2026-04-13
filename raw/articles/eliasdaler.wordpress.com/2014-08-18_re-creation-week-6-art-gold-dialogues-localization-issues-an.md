---
title: 're:Creation week #6. Art, gold, dialogues, localization issues and mini-quests'
url: https://eliasdaler.wordpress.com/2014/08/18/recreation-week-6/
published: '2014-08-18'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Here’s what I’ve been working on this week:

# Art

I’ve decided to return to old graphics style because this is the style I can draw in and because it looks better and more complete. See for yourself:

![](../../assets/9b4dbbb6145aeda0.png)



I’ve spent some time drawing attack animation. It was not as hard as I thought:

![](../../assets/b7fe78aa2ff3eb0f.gif)


What was a lot harder is road tile. It went through several iterations:

![](../../assets/94dd4df88b0a4e4f.png)


And here’s how the final thing looks.

![](../../assets/c6a80302915df8ad.png)


# Mini-quests

Here’s a gameplay gif to show what it is

![](../../assets/9f86891be1210d47.gif)


You need to kill three enemies to open the door. It was pretty easy to implement using Lua scripts! Enemies are spawned when the character approaches the screen with the wall. When he enters this screen, another trigger starts a short dialogue with archer. The door is opened because **isOpened** Lua function returns true when all enemies are killed.

# Gold

![](../../assets/99ef7fa78f3e75d1.gif)


Very easy. Just added one variable to **InventoryComponent** and made new entity which adds one gold when player collides with it. I love entity/component/system model!

# Dialogue system

It’s worth talking about dialogue system as I’ve spent lots of time implementing and improving it.

I started working on it with localization in mind. All text is stored in separate files so when it comes to translating, people won’t have to deal with script files (because it’s easy to introduce new bugs!). There’s also a problem with world lenghts. Consider, for example, German language. It’s well-known for its long words which make sentences a lot longer than equal sentences in English. With this in mind, I’ve implemented very simple function which separates words by spaces and then tries to fit as many words as possible in one line. There’s some problems with this, because some languages (Japanese, for example) don’t use spaces for word separation. I still have to find solution to this problem.

Another problem is encodings. I haven’t ever worked with them and after some failed attempts to print some Japanese and accented text, I’ve decided to work on this problem later.

Another thing worth mentioning is “phrases”. When I played **Ocarina of Time**, I’ve noticed that some things happen when some character says something special. Its animation changes or camera is set to another position, etc. . It was easy to implement. I’ve had every character “talk” separated into “phrases”. Each phrase may have **beginFunc** of **endFunc** functions which are triggered when phrase is shown on screen or when the phrase is finished. Here’s a small example of a phrase:

{ beginFunc = function(this) setAnimation(this, "Talking") end, text = "Good job, take this sword!", endFunc = function(this) addToInventory(player, "ITEM_SWORD") end }

Lua is making everything simple and flexible again!

I’ve also spent lots of time fixing bugs and improving engine so it’ll be easier for me to use. But there isn’t anything interesting to say about that.

I’ll work for a week or two on new exciting mechanics which may become **game’s main selling point**. I can’t say what it is but it has something to do with player being undead.

I hope to bring some exciting updates next week! See ya!

Good job! :)

Если не сложно, то скинь скрин кода, который открывает дверь после смерти стражников.

Thanks a lot!

I won’t post my code but I’ll explain how it works.

The door constantly calls Lua script which calls a function

bool allEnemiesKilled()which works like this:Lua’s flexibility is amazing :)