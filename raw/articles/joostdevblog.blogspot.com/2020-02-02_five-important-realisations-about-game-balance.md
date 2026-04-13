---
title: Five important realisations about game balance
url: http://joostdevblog.blogspot.com/2020/02/five-important-realisations-about-game.html
author: Joost van Dongen
published: '2020-02-02'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo](https://www.ronimo-games.com/)have all featured a heavy emphasis on competitive multiplayer. Designing, testing and iterating these games, especially our biggest hit

[Awesomenauts](https://www.awesomenauts.com/), has taught us many things about balancing. Today I'd like to share some of the most important lessons we've learned along the way.

### 1. Overpowered is much worse than underpowered

At first glance one might think that in game balance, underpowered and overpowered are equally bad: they both mean something is badly balanced and needs to be improved. This is true, but in practice overpowered things turn out to have way more impact than underpowered ones.

The reason for this is that players tend to flock to whatever is strongest and use only that. For example, Awesomenauts has 34 characters. If 3 of those would be

*under*powered, then most players wouldn't play those, leaving 31 valid characters. That's still plenty of choice and variation. On the other hand, if 3 characters were

*over*powered, then players would play only those 3 and would ignore the rest. That would make the game very repetitive and turn stale quickly.

This knowledge can be used as a crude tool in cases where no better solution is available. For example, if something is overpowered but only under certain circumstances, then you might choose to nerf it until it's okay under those circumstances only and is underpowered in all other situations. This way at least it isn't dominating the game anymore.

### 2. Variety always adds imbalance

A game with just one weapon on just one symmetrical map will pretty much automatically be balanced. Even if only because all players are in exactly the same situation. Such a game would however probably not just be balanced, but also be

*boring*. So we need to add variety: more weapons, more maps, more items, more builds, more everything. Maybe even asymmetrical maps. The key thing to realise when doing this, is that as the game becomes more complex, 'perfect' balance becomes ever more difficult to achieve. This quickly gets to the point were 'perfect' balance is impossible, and every bit of variation you add makes the game a bit more unbalanced.

Let's look at a really simple example: walking speed. Let's say some characters are fast and others are slow. This gives the slow characters a disadvantage that can be balanced by giving them more health and damage. However, now we also add maps of different sizes. On a bigger map, the disadvantage for the slow characters will be bigger than on a small map. This is because if the arena is small, slow characters can get to the other side fast enough anyway. No amount of health or damage tweaks will fix this, since it differs per map.

![](../../assets/4177eda5e1cac877.jpg)

One solution to this can be found in our game

[Swords & Soldiers 2](http://www.swordsandsoldiers2.com/). There in matchmade online matches, we only use certain maps: the ones that we feel are most balanced. On the other hand, when you invite a friend to play, you can choose from

*all*maps, including a bunch of pretty weird ones. Those might be less balanced, but they add a lot of spice and fun. Depending on how much you want to appeal to players with a competitive mindset, you can choose to include those varied but imbalanced maps, or not.

### 3. Competitive players often dislike randomness and luck

When Awesomenauts launched, the game had random crits, which dealt a lot of extra damage. This added surprise and suspense: every hit might be extra strong! It also means that even if the opponent is better than you, you might occasionally win because you got lucky. This makes a game a lot more friendly for beginners. An extreme example of this can be found in Mario Kart: this game includes a lot of randomness. Combined with a bunch of catch-up mechanics, Mario Kart is a game where occasionally a n00b can beat a pr0.

However, randomess also adds

*bad*luck: sometimes you clearly outplay an opponent and still lose, because the enemy got lucky and landed several crits in a row. In a sense this might feel nice: since the opponent clearly just got lucky, you don't need to blame yourself for losing. Many competitive players however don't want this to factor into the equation. They want a very simple thing: the best player should win. "

*If I practice more and get better, then I should*always

*win.*" In the years after release many players in the Awesomenauts community got better and more competitive, to the point where a lot of players really wanted the random crits to be removed from the game. For this reason we ended up changing crits into a predictable system where simply every third hit deals more damage.

![](../../assets/31e4fca3f28b162d.jpg)

### 4. Balance automatically becomes worse over time

Even if you think the balance in your game is in a good place, by simply leaving it as it is for a while, it will deteriorate. The reason for this is that as time passes, players get better at the game, learn new tricks and talk to each other. This changes how the game is played, thus also changing how the balance is experienced. Usually not for the better: as time progresses and no balance tweaks are made, balance usually becomes worse.

One example we've seen with Awesomenauts was that at some point after a few months of stable balance, one specific team discovered a new tactic that was super strong. This tactic had been possible for months, but somehow no one had found it yet. This tactic was then first used in a tournament, where that team gloriously beat everyone else and won. After the tournament, news spread like wildfire and suddenly this tactic was used in almost every match. We had no choice but to quickly do a balance patch specifically to nerf this one particular tactic. (The fact that our game is deep enough that players can discover new tactics this way is one of the things I'm most proud of in all of my career as a gamedev.)

Another example of balance getting worse over time might not even be caused by something actually being way too strong. Maybe there's something that's just slightly overpowered, so mildly that it really doesn't matter. As time passes, players write guides and talk about the best tactics. They will point each other at this subtle advantage, causing more and more people to use it. Even if the advantage is really small, or, even more extreme, even if the advantage doesn't exist and players are just imagining it, this still ruins the game for the simple reason that everyone starts doing the same thing. This makes the game predictable and boring.

Sometimes you get lucky and players start responding to that imbalance. Maybe an underpowered character happens to be really strong in that particular situation. Since that situation now happens so often, that underpowered character is suddenly super strong in most matches, causing lots of players to choose him. This makes the dominant strategy shift naturally from one thing to another, adding variation and fun. I've been told some games in the Super Smash Brothers series have balanced excellently for this: as soon as one character becomes dominant, its counter becomes extra interesting and lots of players start playing the counter, at which point the counter of the counter becomes useful, etc. This causes the balance to slowly but constantly shift.

### 5. 'Perfect' balance is impossible

The final point I'd like to share today is both soothing and intensely frustrating:

*for any game that has significant complexity and variation, perfect balance is impossible*. This is a soothing thought in the sense that it makes you realise that even if you were the best game designer in the world, your game would still not have perfect balance. It's also frustrating, because of course the goal of the game designer is to make the balance really good. Knowing that the balance will never be truly fantastic makes balancing a frustrating experience.

So, why is 'perfect' balance not possible? I've already mentioned above that as more variation is added, it becomes impossible to make all options equally strong under all circumstances. But there's more. What about players of different skills? Some characters/weapons/maps are bound to be more difficult to play than others. The result is that for beginners, the balance will be different than for pros. And what about simply different tastes? Some players prefer fun and variation, while other players prefer predictability and skill. The balance can't make both groups perfectly happy. Combined, all of these elements make it impossible to achieve 'perfect' balance.

This post has shared some of the things we've learned through the years about balance. What are your most valuable or most surprising insights regarding balance?


PS. Some of the topics in this blogpost have been discussed in more detail in previous blogposts. If you'd like to read more, have a look at the following posts:


PS. Some of the topics in this blogpost have been discussed in more detail in previous blogposts. If you'd like to read more, have a look at the following posts:

Please don’t abandon this game :( It has so much charm and such a loyal player base.

ReplyDeleteWe intend to keep the Awesomenauts servers running for a long time! :)


DeleteIn terms of development, we're currently fully focused on our unannounced new game, which is turning out to be really cool. :)

here's a really interesting bit of balance that has proven immensely valuable to me when it comes to this topic in particular.





ReplyDeleteany vs game you want to design needs a template character. a character that is specifically designed to have a reasonable response to every situation and which's various atributes, such as speed, their power, weight etc are specifically catered to the terrain and its competitors. Typically these characters don't often make it super high in tier lists but remain as an honest way to play the game, leaving them at the center of a spectrum, from here other characters stray at varying intervals of distance away from this template leaning either towards the most overpowered, to least powerful.

in the format of an online game, where every change in an update can potentially alter anything from the goal of the game or even the rules, turning it into a completely different game. Recognising the most honest character in that version is crucial to establishing anything from, what are the basic needs and weaknesses in this version? what is and isn't acceptable? what is a quote unquote: 'complete toolkit today'?

I Think what's important to realise is that any game with multiple different strategies available will always have a best and worst strategy, and the point isn't to eliminate, or to temper them per se, but rather you have to draw a line as to what is and isn't acceptable. the best characters are often the best due to one or more particular aspects of them being the correct response to everything, while the worst are in their position due to relying too much on their only acceptable response available, as a result of having too many wrong or 'situational' responses available.

this isn't accounting for archetypes of course which, depend entirely on the game itself to determine which strategy is the best and characters who fall under one of these should strive to the best or worst in their respective category, rather than be the best in everyone else's class. lots of observations to be made about your publication Joost.

Thanks for sharing, those are some really interesting thoughts! :)


DeleteI don't know how deliberately we did a template character, but Lonestar and Froggy for us were definitely a baseline. Many other characters were allowed to be weirder in terms of mechanics and tactics. We also deliberately alternated between making weird characters and making simpler, baseline characters. In that last category especially Scoop was a big success: deliberately designed to be easy to like and quick to learn for most players. Scoop indeed turned out to be one of our most popular characters.

I like your game, i bought it on 2012. I wish more people would play it! Regards from México!

ReplyDeleteGood to read.

ReplyDelete