---
title: Lock and Key Dungeons
url: https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/
author: Boris
published: '2021-02-27'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Lock and key dungeons are, well, video game levels with locks preventing progress, and collectable keys that let you proceed.

The concept is a lot broader than it sounds. Locks/keys aren’t necessary physical objects, but anything that works in a similar way, which can often be quite abstract.

![](../../assets/b18806dd115d3143.png)

Once you are familiar with the pattern, **you begin spotting it everywhere**. It’s most prominent in puzzle games and metroidvanias, but it’s applicable to any game which has an authored progression path.

In this article, we’ll look at lock and key dungeons, then how to analyse and design them.

Table of Contents

The first thing to get clear is what locks and keys are. Though they can be literal locks in the game, they can be anything that serves a similar purpose. A lock is something that stops further progress by the player, and a key something that enables that progress. Let’s pick a few examples.

A classic from the Zelda series are **items**. Each item in the game is paired with a particular obstacle that it is designed to overcome. Bombs break rocks, arrows press remote buttons, and the hookshot traverses wide chasms. Levels in Zelda games are almost always arranged so that these obstacles block progress to the boss or objective, forcing the player to explore to find the corresponding item.

![](../../assets/0c01dfe29071d6e3.jpg)

Similar to items are **upgrades**, often favoured by [Metroidvanias](https://en.wikipedia.org/wiki/Metroidvania). These work very similarly, just act internally on the character rather than externally.

A completely different sort of key are **passwords**. This is where the player (or the player’s character) knows something that lets them progress. That might mean entering it into a combination lock, or opening a new option in a conversation dialog. Often, it just means testing that the player has successfully learnt what a tutorial is trying to impart, ensuring that they won’t run into difficulties later in the game.

The most invisible sort of key is **event flags**. This is where completing some action sets a hidden variable in the game, which then changes or opens something elsewhere. Often the cause and effect have no logical connection whatsoever, it’s purely a way of controlling the player’s progress.

There are many more possible keys at the ingenuity of the designer.

Aside from defining lock/keys by type, it’s also worthwhile distinguishing them as either **hard**/**soft**. A hard requirement is one that the player must resolve in the intended fashion. A soft requirement is one that only encourages the player to proceed in a certain way, but has dev-intended ways to be ignored or bypassed.

For example, blocking the path with a [particularly tough monster](https://tvtropes.org/pmwiki/pmwiki.php/Main/BeefGate) is a soft requirement – it would be easier for the player to have done the in-game progress needed to defeat the foe, but a skilled or nimble player can defeat or evade the monster without them. Soft requirements are particularly valued by the speed-running community.

So what can we do with this lock/key concept?

A common way to design a plot, or a puzzle, or a game, is **top-down**. That means you define the broad strokes of the game first, then later fill in the details. Focussing at the locks and keys is a great way to **reverse **that process – find out what top level plan for a game or level is, and erase all the details that are unimportant for analysis.

Suppose we start with a simple level with 6 rooms. There’s two keys, A and B, and two corresponding locks. The player starts at the entrance and wants to get to the boss.

![](../../assets/43415f35a3f5ce19.png)

Images are using

[Mark Brown’s icons](https://www.patreon.com/posts/how-my-boss-key-13801754)– diamonds are keys and squares are locked doors.

We can simplify this a bit by ignoring the details of the rooms, and just consider the locks and keys. We’ll just draw lines to show what is physically connected.

Then instead of showing what is physically connected, we show what is **logically connected*** . *We’ll draw an arrow from one item to another

**if the first one is a requirement of the second**.

Clearly, for each lock, you require a corresponding key. And you cannot get to door B without unlocking door A. Similarly the boss needs door B unlocked. The keys themselves have no requirement except entering the level in the first place. We can omit other requirements as redundant.

We end up with a diagram like the above. It is a type of [graph](https://en.wikipedia.org/wiki/Graph) – the exact position of the items are irrelevant, just the relationships between them. It is often called a **mission graph**.

Mission graphs are a great tool for summarizing a level design. They’re often very simple, as all complex details of the level have been abstracted away. But you can still tell a lot from them.

We can immediately tell, by tracing arrows out from the entrance, that at the start, the player has a choice – both keys A and B are available to them. But by the time the player has unlocked B, they must have collected both keys, and there is no further choice to them.

Mission graphs can also help identify optional paths, impossible encounters, and the general feel of a puzzle design.

A traditional lock and key dungeon works like the above example – every locked door has a key somewhere in the level, and one key opens one lock.

But mission diagrams can actually be drawn for virtually every game. Remembers, locks and keys can stand for anything that block/unblock your progress. You don’t even need to consider locks and keys as coming in pairs.

That double-jump powerup (a type of key) might grant access to many different ledges (each a lock). Or a magical portal (a type a lock) may require you to collect all five mystic artifacts (each a key) before opening. Sometimes the same thing can act as both a lock and key.

To generalize further, you really might just call these these different things **encounters**. As long as you can still draw the dependencies between them, you can draw a mission graph.

Once you start including all encounters, mission graphs can get quite complex.

![](../../assets/b3055e36eef67293.png)

*Legend of Zelda: Twilight Princes*.

Right, how it corresponds to the actual map.


*Generating Missions and Spaces for Adaptable Play Experiences*,[Joris Dormans and Sander Bakkes](http://sander.landofsand.com/publications/Dormans_Bakkes_-_Generating_Missions_and_Spaces_for_Adaptable_Play_Experiences.pdf)

You can find other examples of Mission charts (called Dependency Graphs) at [Jérôme Kunegis’ blog](https://networkscience.wordpress.com/2021/03/13/game-dependency-graph-day-of-the-tentacle/).

Many games have a completely linear mission graph. You must do one thing, then the next, and so on, until the linear plot resolves. The player gets no choice in the overall structure, just about their execution of the details.

However, not all games with a linear mission graph *feel* linear. A labyrinth might have many twists and turns and dead end passage ways to confuse the physical layout, but if there’s only one correct path with no reason to ever travel down the dead ends, then it is effectively linear in terms of actual player choice. And many Zelda dungeons feature literal keys and locks and feel complex, but are actually laid out in such a way that the keys and locks can only be done in a fixed order.

Mission graphs deliberately omit this connective information and show you how little choice there really is. But sometimes you want to see how much exploration, dead ends, and backtracing there is too. Overlaying the mission graph on an actual map can help the situation. But I’d recommend [Mark Brown’s excellent Boss Keys diagrams](https://www.patreon.com/posts/how-my-boss-key-13801754). These display both physical connections and the locks/keys, giving you an understanding of what backtracking and navigation is required to complete the level.

Another classic chart type is the **flow chart**. Flow charts show encounters, like a mission graph, but assume that the player can be in a single state at a time. They’re useful for plots, AIs, and other situtations which don’t have any correspondance to a physical map. For example, these wonderful [Choose Your Own Adventure diagrams](https://www.atlasobscura.com/articles/cyoa-choose-your-own-adventure-maps), which show all the branching possibilities of a plot without considering dependencies at all.

Anyway, hopefully you can already see how these sorts of diagrams can boil games down to the essentials about their progression. There’s of course a lot more to a game, but it’s often useful to think about one aspect in isolation. Then you can pick another aspect, like [the primary loop](https://gameanalytics.com/blog/how-to-perfect-your-games-core-loop/), or [invisible design](https://www.youtube.com/watch?v=MMggqenxuZc), which can be considered completely separately from the overarching premise.

If you can create charts from games as a form of analysis, you can equally create games from charts as a form of design.

Drawing a quick chart is a great way to consider the high level first, before getting too bogged down into details. If you need to move things around, insert something, it’s extremely easy to do so at this stage.

[This article](https://www.narrabase.net/emily_short_bronze.html) for example shows how a mission graph allows the author to quickly analyse the complexity and difficulty of multiple routes through the game.

![](https://www.boristhebrave.com/wp-content/uploads/2021/02/bronze_puzz6.jpg)

Or here’s the [Puzzle Document](http://gameshelf.jmac.org/2008/11/13/GrimPuzzleDoc_small.pdf) for classic adventure game Grim Fandango, where mission charts are literally used as an overview before going into the details.

You can probably guess that mission graphs are also useful for designing procedural generation of levels. I’ve spoken many times about the advantage of decoupling generation of the high level plan from the low level details, and mission graphs take that even further, separating out physical layout entirely. We’ll look into this in more detail in later articles, such as [Dungeon Generation in Unexplored](https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/).

Lock and key designs are everywhere. They’re ubiquitous precisely because of their non-linear nature. Without them, you have games with no meaningful descisions, no exploration and less variation. Use the tools I’ve covered to understand them better, and incorporate them into your own design.