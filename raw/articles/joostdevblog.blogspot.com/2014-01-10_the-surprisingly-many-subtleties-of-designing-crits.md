---
title: The surprisingly many subtleties of designing crits
url: http://joostdevblog.blogspot.com/2014/01/the-surprisingly-many-subtleties-of.html
author: Joost van Dongen
published: '2014-01-10'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)we have had various implementations of crits and each time more subtleties surfaced. So today I would like to talk about their many aspects.

Crits can be applied to any weapon or attack and their core element is

*chance*: there is a small chance that a weapon does extra damage. Usually this chance is low, below 30%. Instead of damage, the crit might also add other effects, like a stun or knockback. Crits are mostly seen in RPGs, where they are a nice way of spicing up the weapon variation. A sword that does 10 damage feels quite different from a sword that does 7 damage and has a 25% chance of doing 19 damage. The average damage output of these two swords is the same, but they feel and play very differently. Crits also add extra variation to levelling and upgrading: one can upgrade not only the base damage, but also the crit damage and the crit chance.

![](../../assets/8b2ae99d777e0a0d.jpg)

Crits are often a fun and interesting mechanic. While a normal sword always has the same result and is thus entirely predictable, a sword with a crit chance makes the player curious for every next hit. “Will it crit?! I hope it will crit!”

Adding chance to a game adds unpredictability. Having a lot of unpredictability greatly changes the feel of a game. A great example of this is Mario Kart. In Mario Kart when you grab a pick-up you usually get a random item and the effectiveness of the items varies massively. Picking up the right item at the right time often makes the difference between winning or losing the game. This is great for beginning players: even if they are playing against much better opponents, there is still a chance that the beginner might win because she has some lucky pick-ups. This makes a world of difference in comparison to purely skill-based games, in which the beginner will basically

*always*lose until she becomes as good as her opponents.

![](../../assets/d9b0e84ea1c99862.jpg)

Luck also has a soothing effect. If you lose because your opponent was better, then the player can do little but blame her own lack of skill. This can be frustrating. On the other hand, if luck is involved, the player can always blame that, which is much easier to accept. Most losing players need scapegoats to be able to cope with their own failure. Luck is a great scapegoat, just like the referee's mistakes are in soccer.

Knowing that players need a scapegoat actually helps in understanding player feedback. Any competitive online game has players complaining about balance, and as a developer it is important to realise that part of that is completely unrelated to the actual balance, and is just players needing a scapegoat to be able to accept losing that match. (By which I am of course not suggesting that balance in Awesomenauts is perfect. I am merely saying that a

*part*of balance complaints are caused by players needing a scapegoat instead of actual problems in the balance.)

The above text may make it sound like crits only have benefits, but this is absolutely not the case. The big problem with crits and luck in general is that they take away part of the competitive nature of a game. If a player invests hundreds of hours into becoming highly skilled at a game, then losing a match because the opponent got lucky just plain sucks. Competitive players generally hate luck with a passion. This is the reason why in the end, we removed Leon's crits and turned them into a completely predictable consecutive-hit system.

![](../../assets/dffa2e3e60de1fb8.gif)

Bluntly summarising today's blogpost, one could claim that crits and luck make a game more casual, while complete predictability make it more hardcore and competitive.

The title of this blogpost said I was going to talk about the many subtleties of crits, but it turns out that there are so many that I cannot cramp it all into one single blogpost. Therefore I will come back to this topic next week and talk about how luck in games is rarely just a roll of the dice, and how modifying crit chances in the wrong way can be painfully destructive to balance.

*Edit: Here's a link to that next blogpost:*

I think that "RNG" is a very good system on a non-competitive game.









ReplyDeleteThe reason is that, when you have a game with opponants and luck is involved, the range of emotions a player can get is wider than a predictable system.

With a predictable system, if you lose to another player, the only thing you can think is "He is better than me". In Awesomenauts, a player can still get a "lucky kill", but that player was ultimatly here at the good time, at the right spot, and used what it took to take the kill, lessening the "luck" effect. The losing player can think he was unlucky, but kinda knows that it probably won't happen again if it was a "real" lucky kill, and the fact that this kill was /maybe/ because of the opponant skill.

On the other hand, a "RNG system" have a double effect on the players feelings. First, since the randomness is clearly the main thing here, luck is the primary reason a player got a loss. It's the opposite as a predictable system: luck is first, skill is second.

Secondly, players feelings are amplified by a simple fact: if he lost, he will think "I'm unlucky" AND "The other player is lucky", thus implying some sort of injustice. Not especially imbalance, but mostly "injustice". Something happening which isn't just. Which isn't /fair/. Unfair.

On the other hand, the player who benefits from the RNG will have the exact opposite feelings. "I'm lucky" AND "my opponant is unlucky".

Even if this player is not skilled enough, he will praise his luck and will be more confident.

This is why I think that, a randomized system is the best in a non-competitive game, because you can't get this "my opponant is lucky and I'm unlucky, which is unfair".

Accepting that a computer got lucky is more doable than accepting it from a human opponant, because we don't "compete" against a computer, while we do in this kind of human interractions.

Try to think, in Awesomenauts, about a character only based on RNG. He got his main damage skill going as follow: "Does 30 direct damage OR 50 slow DoT damage, on a 50% chance". He can also apply debuffs such as "Apply a Slow OR a knockback on your attack, on a 50% chance". And so on.

Everything he does is based on RNG.

Well, it's pretty obvious that playing against or with this character will considerably amplify the fellings of the players on a win or a loss, because luck will play such an important role that it's not really controllable anymore (whilst simple crits kinda still are). This character will be the ultimate scapegoat everytime he's in a game. Once blamed for the loss, or praised for the win.

This range of emotions, while fun to code and to see in action, is not something players want in a competitive game.

and the only reason to that is: when humans compete against each other, they want to see how strong /they/ are, not how lucky.

Tossing a coin to see if they are able to overcome the challenge brought by another humain is not something people want. A good example of this is by playing Shifumi (Rock-Paper-Scissors). The first thing you will try to do is to play a mindgame with your opponant instead of relying on luck only. But against a computer? No, mindgame with a computer is irrelevant, in that case. You'll accept that luck will determine your fate.

I'm currently making a boardgame out of a dice-based system, and RNG is why I'm doing it. In the original game, the outcome of who win and who lose is only determined on luck, AND the first player has an advantage.

By making it a boardgame with some decisions involved and by allowing the players to alter their luck in some way, the game feels more "fair" and you're not only competing against luck, but against human decisions, which is way more satisfying.

Interesting essay, thanks for sharing! :)

DeleteI can never take critical hit chance into account on a weapon because it's too unpredictable. So 1 in 20 times I kill an enemy in one hit instead of four hits -- I still have to approach every enemy as if he's going to take four hits. I'd much rather have your "hit number 20 is a crit" thing, as then I could count on it being "due" or even tactically make sure it hit the enemy that counted. Genius.


ReplyDeleteAnother reason regular crits suck is they might as well just say "your weapon deals +0.3 damage". Pathfinder does it way better with their "critical feats" -- when you get a crit, based on your character build the enemy will start bleeding, or be staggered or fatigued. Something you will actually notice instead of just a different number floating up.

"I think that "RNG" is a very good system on a non-competitive game."
















ReplyDelete"This is why I think that, a randomized system is the best in a non-competitive game"

This is nonsense about competitive games not having RNG. Pure and simple: all fps's (good example) are by nature competitive, all the popular ones(afaict) have RNG, mostly it is used for things (especially) like bullet spread. As to how you let RNG influence a game you make is entirely subjective because you must decide for yourself what is fair.

In the end it comes down to this. Did you make RNG on your client or did you put it on your server.

This is why peer gaming is intrinsically flawed. Because the single hub (if using this peering model) can control how the game is influenced by this ENTIRELY. Even the meshed and parity model can be influenced by a single person.

Private servers are rubbish for this reason. Because if an admin can cheat and add plugins to his server, he will. Private server cheats are EXTREMELY OVERLOOKED in modern games. Why do you think ppl is always lobbying to have private hosting?

Securing a game can take years and too much money, so I'm not bashing.

The best and easiest way to fix RNG is to simply make it predictable in some sort of way so that it can't be used as the source of contention. Which means, removing ALL the randomization fxns from the game and replacing it with conditionals.

RNG is a huge hole. The next biggest would be the guys who code or admins the servers for these games. Think LoL and DOTA2.

After you secure this part of the game (moving everything you can to your server to make it fair), you must turn back to the client once again to deal with the behavioral aspect and analysis since there are countless idiots making bots for every game.

So, I know you don't want to hear this because its so easy to use Randomize() and int rng etc, but it is truly just an excuse for lazy.

For all these reasons, your intuition about making it fair by reducing the impact of RNG is correct. These are realizations that the majority of gamers don't come to understand. For most of them, random is the santa claus they always wanted to believe in.

Thanks for making such a cool game and sorry for going a little off-topic (crits vs fairness vs rng)! You probably know this stuff already Joost.

In summary: crits can and should be done without using rng, fairness is subjective, and rng is bs.

These are big and easy things to take care of next to hardware equality, latency and scheduling, and of course the handicaps of the players.

-G

This made me think of a post about damage calculations that I read recently at Amit Patel's game development blog.

ReplyDeleteIt's interesting to read your thoughts about a game design topic for once. The way you look at scapegoating in games seems awfully correct. It is also the reason I'm looking at co-operative game concepts.

ReplyDeletehttp://www.youtube.com/watch?v=bY7aRJE-oOY&t=18m24s


ReplyDeleteIt's the actual Sid Meier Keynote part about it...

Awesome, thanks! :) I have added it to the blogpost on random.

Delete