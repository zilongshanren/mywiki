---
title: Procedurally Assisted Generation
url: http://david.fancyfishgames.com/2016/08/procedurally-assisted-generation.html
author: Legend
published: '2016-08-17'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

[Deity Quest](http://store.steampowered.com/app/340330/), I've done a lot of work and research on procedural generation and am quite proud of the results in

[I Can't Escape: Darkness](http://store.steampowered.com/app/346090), which is able to generate a different layout that is still solvable every time you start a new game. However, I've come to realize a few things about procedural generation, which is why I will

**NOT**be using traditional procedural generation in my next game.

## Procedural Generation

At a glance, procedural generation sounds amazing. Instead of having to painstakingly hand-craft levels, an algorithm can generate near infinite levels and provide variety and replayability for players. However, while procedural generation can create near infinite levels, how different are those levels from one another?Let's take No Man's Sky as an example for a moment, as everyone's talking about it anyways. There is no denying that all of the planets and animals are different, and that it is a marvel in terms of algorithms and technology. However, there are a ton of angry fans who find the game boring, stating that they are doing the same things at "basically" the same planets, over and over again.

![]() |

[No Man's Sky](http://www.no-mans-sky.com/)Here's the key point:

**Procedural generation is great at creating variations on content, but terrible at creating new content.**

**You might ask, how is adding new levels and new planets not adding new content?**


That's because I distinguish between

**content**and

**assets**. Lets say you make a game with infinite levels, where each level is the same except that the enemy model is replaced with a different model. This game would have infinite

**assets**, as it would have infinite enemy models. However, no matter how different or interesting those enemy models are, isn't the game still the same level over and over again? I would call this game having only one level of actual

**content**.

![]() |

**content**because they tend to add new puzzles, new gameplay mechanics, and/or advance the plot. Even new hand-crafted enemy types add

**content**if those enemy types have different attacks and movement patterns that have to be handled (by players) in different ways. It turns out to be very

*very*difficult to get a procedural generation algorithm to produce actual new

**content**(most experiments that attempt to do so are more in the realm of machine learning than procedural generation).

Lets go back to I Can't Escape: Darkness for a moment. As anyone who has played the game many times has probably figured out, while the actual paths you might take between rooms to get items are different every time, the general progression - the flow - of what you do is the same. For example, you have to collect the pick axe to break through walls before you can get the key to the cat door. While the details of the game are certainly

*different*every time, in terms of the actual

**content**, I would argue that it is actually the same every time (welp, there goes one of our major selling points). None of the gameplay mechanics or major points of progression change. And this

**content**of the game, I designed by hand.

![]() |

[I Can't Escape: Darkness](http://store.steampowered.com/app/346090)## Procedurally Assisted Generation

So, with the above said, procedural generation doesn't sound as amazing as it did before. What's the point of having infinite planets if there's not something interesting and unique about each one? Might as well go back to doing everything by hand, right?

Well, procedural generation is a tool. And even if it isn't the holy grail that makes entire games for you, it is still a useful tool. While the actual

**content**of the game still has to be created by hand, that doesn't mean procedural generation can't help out with some of the details and speed up the process of level design. And that's where my idea of Procedurally Assisted Generation came from.**Procedurally Assisted Generation is using procedural generation algorithms to take your basic content and turn it into fully detailed levels.**

It is a way to speed up level creation by handling the tasks of level design that aren't very important to the core gameplay anyways.

![]() |

[Onyx Computing](http://www.onyxtree.com/)
Already, there are simple forms of procedurally assisted generation in common use. If you need to add a forest around your city, you don't model and place each tree. You have an algorithm place several tree models automatically around your city for you (the algorithm might even generate the tree models for you). Having an algorithm handle these kinds of details for you can save a lot of time.

Some of the things Procedurally Assisted Generation could do for you are as follows:

**Add details to your scenes**- trees, brush, rocks, doodads, decals (like scratches on walls). Procedural generation is a great way to add variety to your scenes without actually changing the core layout.**Automatically place areas**- lets say you have a graph of areas and connections between those areas. Procedural generation can easily place those areas and paths between them, while adding obstacles to block players from going directly between areas that don't have connections between them.**Automatically generate layouts**- if you want a dungeon, you could have a procedural generation algorithm generate the layout for you, and then add the puzzles and boss encounters by hand so that it is interesting and unique from other dungeons with generated layouts. If you don't care about the exact shape an area takes, this can save a lot of time.**Automatically generate models/variations**- there are lots of algorithms out there for generating trees, buildings and making variations of other models. This can be a way to add variety to the objects and props you add to the game without having to hand-craft each one.

![]() |

This is how I plan to use procedural generation in my next games going forward. The core progression and

**content**of the game will ultimately need to be created by hand, to achieve design that is intelligent, original, and keeps the flow and player experience in mind. But, I can make a few low-detail areas by hand, and by using a progression graph, I can then string those areas together and add details to them. This method will save a lot of development time, while still ensuring that the game is exciting and that the progression and overall game structure are just as strong as if the entire game was hand crafted.
I agree with you and I came to basically the same conclusion, just infinitely mixing things up doesn't add variety, quite the opposite - it just makes everything the same. It concerns not only procedural generations. For example in old RTS Earth 2150 players can construct units from parts as they like, but if you can put any gun on any chassi, why do you care? You just take biggest one every time.

ReplyDeleteOn the other hand, there is a good example of procedural generation done well - Minecraft. The trick is to spice things up, add something that would stand out.

Also, occasionally abscence of some randomization is what bothers me. In some RPGs like Dark Messiah (of M&M) or VtM: Bloodlines there are skills that help you find items/traps/secrets, and they are quite helpful on your first run, but on next runs you already know all those locations so this skill value drops to near zero. If each time items/traps layout would be randomized a little, it would add a lot to replayability.

Yeah, the big trick is to spice things up - procedural generation doesn't add much that will stand out, so you have to intentionally add new blocks, gameplay, etc.


DeleteAnd yeah, I can definitely see how randomizing hidden items makes sense (I mean, they are hidden anyways, their exact location doesn't matter). Randomness can certainly add to replayability, but it doesn't really change the actual game, and so shouldn't be used for your entire game/content (you're still doing the same thing - searching for hidden items, even if you now can't memorize positions at least).