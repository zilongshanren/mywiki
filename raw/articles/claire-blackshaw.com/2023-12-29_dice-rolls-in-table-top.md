---
title: Dice Rolls in Table Top
url: https://claire-blackshaw.com/blog/2023/12/die_rolls/
author: Claire Blackshaw
published: '2023-12-29'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

I've been thinking a lot lately about dice rolls as I consider reviving my old Channels of Power ttrpg and doing a v2.0 and launching some new campaigns and modules but this got me thinking about my old friend, **dice probability**.

The classic d20 is a flat probability curve with a BROAD range with small bonus meaning that the curves are wild.

You ALWAYS have a 5% chance of guaranteed success or failure. No dice risk is without hope or dread. This leads to a very cinematic feel with a level 1 character still having a chance of hitting a big bad monster. The wildness of the dice is countered by rolling a lot of dice rolls. So the Dungeons and Dragons system tends traditionally to LARGE amount of dice rolls. The more dice rolls in a game the more the fairness or power scale levels out.

Also notice how huge the advantage and disadvantage system are in Dungeons and Dragons 5th edition. This replacement of situational bonus was a huge improvement. You don't really feel a +2 the same way as you feel disadvantage or advantage. So this becomes a key flavour mechanic for Dungeon Masters.

![The d20 probability curve](../../assets/a25ac38f7d6c1ca8.png)


Now my preferred story telling game is Fate which uses fudge dice. Roll 4d6 where [1,2] is failure (-1), [3,4] is neutral (0) and [5,6] is succes (+1). This is made simple by dice with minus, blank and plus sides and really is 4d3 roll. This is simple because you always roll the same number of dice and the swing trends towards a strong normal. So very few dice rolls still feel fair and infrequent rolls can be made to be pivotal.

![The curve of fate dice](../../assets/2e6818465d52fee2.png)


Both are solid and strongly flavoured systems but my original v1 of Channels of Power was based on the classic White Wolf style dice. Roll the number of d10 equal to your skill and any dice equal or higher than your target number is a success (+1) with the default target being 6. A controversial but awesome addition to this flavour of dice system is the exploding 10. When you roll the highest possible value it is a success then you reroll for more chances to succeed. This in theory leads to an infinte ceiling.

I'm also a huge fan of success based dice systems as **they avoid the secondary damage roll**. Wrapping up everything into a single roll feels more dynamic, faster paced and is often simplier to newer players. Especially with DnD wargaming inspired range of damage dice.

![The Exploding vs Non Exploding d10](../../assets/fd6dda0c9304f374.png)


You will see that immediately the exploding doesn't actually shift the numbers much, except on the very low end. Though I will say exploding dice feel very cool. I've often seen the house rule is that the Story Teller running the game does not explode but the players do. This feels great for players and avoids the random situation of runaway failure for the ST rolls which are enviromental and atongonistic.

I know a lot of Vampire, Werewolf, Mage ect... players who just love their tubes of d10s and the joy of exploding madness. Though many other table tops use the same system but with the much more ordinary d6 dice, often thought of as the normal dice as it rolls well and is the most common dice seen outside of tabletop games. So how does a d6 target system fare?

![The Exploding d6](../../assets/5f60b7440e2a417f.png)


As you can see the chances with a d6 vs a d10 aren't that different. So I think the difference between d10 and d6 are largely thematic. The difference being mostly in how the fumble and explode are handled. The d10 are slightly lower rolls but the players don't really FEEL it. Though the novelty of d10 is often cited as a reason to use them over d6. It puts the players in a different headspace and collecting tubes of d10s is often more fun than d6s. Though by the same token it does make it slightly more intimidating for newer players.

The next question which comes up is often around shifting the target numbers. So making things harder or easier by the ST setting a target number lower or higher than the average. I always liked this as the player rolls the same number of dice, which if you are really expert at a thing the feeling of rolling a lot of dice is epic, but it gives the ST a strong knob to turn which affects the high rollers more than the low rollers.

![Shifting Target Number D10](../../assets/e4ac60dee054120e.png)


Now this is often cited as a key reason to use d10s over d6s and while I can see the benefit I found often ST didn't adjust much more than a higer or lower roll. Let me show you what it looks like if we use d6 instead.

![Shifting Target Number D](../../assets/3cae2b398ccbc51d.png)


A nice subtle tuning mechanic but without the oomph of the D20 advantage and disadvantage system.

It can be a bit harder to intuit the sense of these target numbers so I've given you a small toy below to play with the system. The rainbow of colours showing the difference between rolling a single dice all the way up to 10 die. You can see that a bigger dice pool mostly makes the roll more reliable by flattening the curve.

The biggest change between 20 years ago when I designed the first version and now is my years of experience in game design, have taught me the most important aspect isn't the mathematics behind it. Rather how the dice mechanics feel during gameplay. Over time, I've encountered a variety of unique dice systems, each with their own interesting features.

Poker dice, fixed pools, pairs and set, target dice and all sorts of strange combos.

However, let me delve into one more concept: the use of target numbers, particularly with the introduction of 'advantage' or 'disadvantage' in the fifth edition. Consider a scenario where you roll multiple dice but only count the highest roll against a predetermined difficulty level (DC).

![Max d10](../../assets/44f9f65b2e90613c.png)


This is actually really simple and nice but it quickly gives diminishing returns on the high end. Which is not always a bad thing but might flatten the power curves more than some games which focus on getting really good at one thing could want. Though it is appealing if the damage is say the amount you beat the target by then the high end of the dice pool is interesting.

If you want to explore that idea further and stretch the power curve: What if you sum the TWO biggest dice?

Then you get this curve...

![Sum two highest d10](../../assets/aad36123f7d82490.png)


See that provides a lot more room at the top end. The introduction of a rule around 1s and 10s for stress, flair or explosion is of course interesting as well. I have a bunch more thoughts but I wanted to conclude this blog post on dice proabilities with that simple sum max system as I call it.

Please let me know your thoughts on Twitter (@evilkimau) or Mastodon (@kimau@mastodon.gamedev.place)

### Footnote on Probability Curves

All of these are run through a simple python script to just roll dice and add up the result. You can grab the code [here](https://gist.github.com/Kimau/11a35e2c7d9042760b4005ef8b15354e). While calculating the something like advantage on d20 roll is `P(highest 𝕥) = P(first_die 𝕥) × P(second_die ≤ 𝕥) + P(second_die 𝕥) × P(first_die < 𝕥) + P(both_dice 𝕥)`


while disadvantage is `P(lowest 𝕥) = P(first_die 𝕥) × P(second_die ≥ 𝕥) + P(second_die 𝕥) × P(first_die > 𝕥) + P(both_dice 𝕥)`

isn't that hard it becomes a mess with exploding dice. Also I found it quicker to iterate in code than math.

Btw for d20 that is

**Advantage**: `=(1/20)*((21-Target)/20+(20-Target)/20)+(1/20)^2`


**Disadvantage**: `=(1/20)*((Target/20)+(Target-1)/20)+(1/20)^2`