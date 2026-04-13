---
title: Asymmetrical Overbalance in Game Design - Game Wisdom
url: https://game-wisdom.com/critical/asymmetrical-overbalance-game-design
author: Josh Bycer
published: '2015-11-09'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

I recently tried to get into Skyshine’s Bedlam following its 2.0 update. The game came out of the gate with numerous problems about difficulty and imbalanced game design which the developers attempted to fix. After trying to get into the game, I found a major problem with the game’s combat system that has become a big point for any strategy-based title. Today’s post is about overbalancing design and when the AI gets too much of an advantage.


## Following the Rules:

Strategy games live or die based on the rules setup by the designer; specifically, how the player and the AI interact with each other. Strategy games are notorious for having complicated rules and systems for the player to dive into and the AI to be programmed to understand.

However, designing an AI that can not only follow the rules of a strategy game but also figure out synergies and advanced tactics is very hard to the point of impossible. The two big points are A: An AI can’t properly plan strategies and changing strategies multiple turns in advance like a human can. And B: the AI is limited by the expertise of the programmer and may not be able to create tactics at the same level as the player.

This is why designers for most strategy games go with two options to compensate. Either the AI will simply behave differently than the player (or asymmetrical balance,) or the AI is given unique advantages to compensate. For an example of the former, we can turn to XCOM Enemy Unknown and how the AI was always given a free movement action when discovered to prevent them from instantly getting killed by the out of cover defense penalty.

In terms of advantages, we can see this in any strategy game where the AI on the harder settings is given more resources, faster spawn times; anything that gives them an innate advantage at the same rules the player has to abide by.

The important distinction between the two is the fact that the advantage still operates within the confines of the rules of engagement; while the asymmetrical balance exists outside of those rules and is unique to the AI.

Both choices have their pros and cons, but for this post, I want to focus on the asymmetrical balance as that’s the more interesting of the two.

## Breaking the Rules:

Asymmetrical balance is typically seen in strategy games built around specific systems of play and interaction: XCOM, Skyshine’s Bedlam, and The Banner Saga. In these games, while the player and the AI are technically using the same systems and rules, the AI is given special consideration in order to compensate for not having an in-depth AI. Another factor is strategy games that are built around mechanics that requires thinking that is less numerical or optimization-based, and more about reading the field or situation and making a determination.

In the grand strategy games from Paradox, despite being very complicated games built around multiple systems of governance, everything can be boiled down to numbers and making the best choice. Because of that, the AI can be built to read the numbers and make the best determination based on the current situation.

![XCOM Enemy Unknown Game Design](../../assets/823283a756acb052.jpg)


![XCOM Enemy Unknown Game Design](../../assets/823283a756acb052.jpg)

Games with tactical elements require someone to analyze the situation and make multi step plans; something that an AI has trouble with

In a game like XCOM Enemy Unknown however, there is a lot more than just numbers to deal with: Special class powers, the use of overwatch and hunkering down, knowing when to advance, retreat, etc; basically, there is a lot to think about.

While you do have numbers in the form of percentages of attacks and damage, a lot of what makes playing XCOM so interesting is the tactical thinking that goes into the game.

You’re not just thinking about what’s best this turn, you’re thinking about where your units are positioned and what that means for the next turn and so on.

And creating an AI that can essentially “read” the field is borderline impossible right now. That’s where asymmetrical balance comes into play; allowing the developer to still make the AI a challenge by giving them a unique perk. This perk or perks lets the AI do something that the player is not allowed to do and therefore has a unique advantage.

On the plus side, is the as-mentioned ability to give the player a challenge without having to program a super AI. The problem is that many players consider this cheating and unfair in most situations. Imagine playing Football where each game, one team gets to give someone a baseball bat and can hit the opposing players; it would completely upset the balance of the game. And that’s where asymmetrical challenge is very hard to get right: You need to give the AI an advantage without it being seen as cheating.

One option that designers like to do is just say “screw it,” and make the AI and player essentially play two different games. In this situation: The player has one job to do on the map or during a game and the AI has a different job; thereby they can have different rules assigned to them and that’s just the nature of the experience. We see this in games built around rogue-like design, where the player gets unique gear and options that the enemies designed won’t, but the enemies have unique powers and abilities too.

A case in point would be a game like Demon’s Souls and how you’ll face bosses with strange and dangerous powers that you could only dream of having. However, you get the ability to level up your gear and your character and they don’t.

Another option is to give the player something special to compensate the enemy’s unique advantage, some kind of trump card or emergency power that the AI doesn’t get. In XCOM, the beauty of the game’s design was how much your options changed over the early, mid and late game thanks to the new abilities you get, MELD options and gear; none of which the AI will use.

And the final option is the hardest: Give the AI a perk and be really, really, careful with how you balance it; which takes us to Skyshine’s Bedlam and where things went wrong.

## Wasting Away:

Skyshine’s Bedlam ([which you can watch my video spotlight for more detail](https://www.youtube.com/watch?v=Er7wGcHj1Js),) features a very brutal combat system, where characters can be killed permanently very quickly. With the game’s two action per term system, it’s very easy to put a character in a position where they must either kill the enemy in one turn, or face counterattacks from his friends.

![Skyshine's Bedlam, originally posted on GMG game design](../../assets/6f633fabc6c938ac.png)


![Skyshine's Bedlam, originally posted on GMG game design](../../assets/6f633fabc6c938ac.png)

Skyshine’s Bedlam creates an asymmetrical situation that favors the AI and makes the game frustrating to play

Having the AI and the player make use of the system from that point is fair, but there is another twist. For every turn that someone is not killed, the blitz meter goes up; when this meter reaches full, the enemy gets three turns for their next round of combat.

Given the low health of your team, you can see where this can cause some big problems.

Imagine a boss who already has high damage getting the chance to kill 2 or more of your 4 person team in one round.

Because of how big the enemy groups get, sending one person to try and take down an enemy is suicide, as the enemy will focus them down during their round. So you have to wait for the enemy to close in, which causes the blitz meter to fill up and you can guess what happens next.

This is a game where the asymmetrical balance favors the AI too much with nothing given to the player to compensate. The player can use special equalizer attacks and dozer skills, but these are tied to a limited resource and cannot be used every time because of that; turning it into the classic “item hoarding” problem seen in JRPGs. With limited characters for your party, early losses and not getting upgraded troops will make the mid and late game impossible to win, because upgrading troops is the only way to make them better.

The upgrade system also presents a major design problem in my opinion, but we’ll have to talk about that in another post as this one is starting to run long.

## Reining it in:

Asymmetrical balance is a popular option for game developers to present the player with a challenge, but it can go too far in some cases. One of the more frustrating situations is when you know that the AI has an advantage that you can’t do anything about and it feels like an arbitrary addition to make life difficult for you.

Sometimes, you need to decide which side gets the advantage: Either the player or the AI. In these cases, who you pick will determine the overall difficulty of the game and as we’ve talked about, most cases you want to pick the player. Getting the balance between two different sides is a tough one, but a hallmark of a great game designer.