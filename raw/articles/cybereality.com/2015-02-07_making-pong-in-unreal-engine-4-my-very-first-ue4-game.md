---
title: Making Pong in Unreal Engine 4 (My Very First UE4 Game!)
url: https://cybereality.com/making-pong-in-unreal-engine-4-my-very-first-ue4-game/
author: Cybereality
published: '2015-02-07'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

Today I’d like to unveil what I’ve been working on for about 2 weeks: Pong in Unreal Engine 4. Most of that time was spent reading documentation and watching tutorial videos just to figure out the basics. There is actually a *lot* of good material out there for Unreal Engine 4, the docs have been helpful and there are plenty of videos. Disappointingly, there are barely any books out there for the engine, but I’m sure that will change quickly.

Pretty much anyone will tell you, when you are learning to develop games (or switching to a new engine/platform), the best thing to do is to start small and try to complete something. It’s really silly to try to make an MMORPG as your first game (I have fallen for this one!) and even relatively simple things can become complex fast when you are not familiar with the platform. So I chose to do Pong as my first excursion into Unreal 4. It was not without some trials, but I made it through alive. Oh, and, no. This will not be considered my “finished project of the new year”. There are some other, cooler, things I have in mind.![](../../assets/e4da106144eec10e.jpg)


Previously I was making multi-part blog posts with basically quick status updates. This was fine, but I think it will be more helpful for the community for me to do focused tutorials on a specific topic and post those more frequently. I learned quite a lot about Unreal with this project, and I think I can share some of that on this site. Some of the things I picked up working on this demo include: importing assets, working with Blueprint, basic flow and logic, movement, collision, HUD, events, keyboard control, functions and variables, and just getting familiar with the Unreal Editor interface. Not sure I will make tutorials on everything, but I plan to break this into a few posts. Below you can see the level Blueprint for the game, just to give you an idea of the complexity.

Overall I have been impressed with Unreal Engine 4, and I can’t imagine purchasing a more capable piece of commercial software for less than the pennies they are giving this away for. People can complain about the 5% royalty but, really, if you get to the point where 5% is a significant dollar amount, you will be rolling in the the dough and shouldn’t care if Epic wants a piece of the pie. Cost aside, I do like the engine a lot. Granted, I ran into some bugs, and more crashes and stability issues than I’d care to admit. At one point, the project saved in a corrupted state and I was blocked from even opening it at all. Luckily, I was able to update the engine and convert the project, but I was sweating pretty hard for a little while. That said, I’m sure this can be improved in time and it didn’t stop me from developing (I’d just recommend using source control and committing often).

The visual programming system, Blueprint, is very powerful and I used that alone for this demo (no C++). I did start checking out the C++ support and it seems to add some extra power and flexibility, but I haven’t got that far yet. However, I can see building some simple games and experiences using the visual coding by itself. This is also great for designers, who may be able to rig up some basic stuff themselves. Keep in mind, it’s still programming (just not with text). You have to understand the basics of logic and control flow and, in some ways, it may even seem alien to veteran programmers. I know there were definitely a few cases where I had a non-trivial amount of nodes and connections and thinking “I could have done this in 1 line of code”. Once I got beyond that, I think I may prefer it to coding manually, as it’s much harder to make mistakes (or to create stuff that doesn’t work).

I hope to continue working with UE4 in the future and I’ll continue updating my blog as I make major developments. Thanks for watching.