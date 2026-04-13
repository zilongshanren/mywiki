---
title: Pillars of Playability Part 1 - The Quality of Life - Game Wisdom
url: https://game-wisdom.com/critical/playability-part-1-quality-life
author: Josh Bycer
published: '2019-10-16'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

My piece about [accessibility vs playability](https://medium.com/super-jump/accessible-vs-playable-5f38dc32970d) has spurred a lot of discussions, but I still feel people aren’t grasping the difference between the two. Features that are designed for accessibility don’t always affect playability and vice versa. For this multi-part series, we’re going to take a deeper look at major elements behind playability, and we’re starting off with the concept of quality of life features.


## QOL FYI

Quality of Life (or QOL) elements cover a very broad category of elements designed to make a game easier to play without changing the gameplay itself. What makes QOL features hard to pin down is that unless you know what you’re looking for, they can be impossible to spot. This is an area where playtesting comes in to help.

As the designer, what you’re looking for are any areas in your game that are frustrating players or keeping them from enjoying the core gameplay loop. Think of it as being forced to do paperwork before you can do something enjoyable. Look for any pain points in your design — especially if your players are quitting after doing something — and use that as your first stop.

The next thing to look at are areas where the players are getting confused by your game. Tooltips, dynamic UIs, or even just better tutorial and onboarding can help in this regard.

It’s important to reiterate that what we’re talking about is not changing or adding anything to the gameplay, but making it easier to experience the core gameplay. Ultimately, anything that allows the player to focus on playing the game could be considered a quality of life feature, but I know that’s not the best answer.

If you’re looking for a wealth of examples, look no further than modding.

## Mod Life:

The discussion around modding games and culture is too extensive to delve into here, but for as long as there were games on the computer, people have been modding them in all manner of ways. For titles that shipped with SDKs (Software Development Kit) and especially those that have Steam workshop support, there is an incalculable number of mods out there.

Mods in games fall into three groups: Quality of Life, Partial Conversion, and Full Conversion. To be thorough, partial conversion mods are those that take what’s in the game and create new content using those assets as well as new ones. Third-party quests in RPGs like Skyrim, new missions in Half-Life, clothing options in games, and the famous “Long War” mod of XCOM are examples. The bonus buildings built in Cities Skylines would be another example

Full conversion means that the mod takes a game and creates an entirely new game out of those assets that may not even be the same genre as the base game. Due to the amount of work that goes into this, full conversion mods are rare, and I can’t think of any good examples off the top of my head; feel free to post your favorites in the comments.

Quality of Life mods are far-reaching and diverse, with every game having their own unique set. While it did feature several QOL examples, the DSfix mod for Dark Souls on the PC is a unique case and not every QOL mod goes that far.

Normally, QOL mods for PC games fall into two groups:

- Mods made for expert players to cut out elements they don’t like or could be done better (removing the opening splash screens in games is a popular one)
- Mods made to make the game easier to learn and play for people who aren’t experts

You can look at any Steam game that has a workshop, and you’ll find QOL mods for almost every aspect of the game. Both XCOM 2 and Grim Dawn had numerous mods built for them and were also cases where popular mods became adopted by the design team and put in officially.

In XCOM 2’s case, it was the ability to get target previews on the UI itself. With Grim Dawn, there is now a search bar that you can use to search shops or the devotion page for specific attributes. Even then, both games still have mods that people agree are must-haves, but haven’t been adopted yet.

While I’m not a fan of the game, I know that many people have used modded UIs and elements for World of Warcraft over the years to make the game easier to play.

That last example brings up a touchy point when it comes to mods and QOL features.

## Out designing the Designer:

A while ago I made a post about personalization features in games and I said that no matter how many a designer has it will never be enough, and the same can be said of QOL features. Sometimes QOL features and mods can purposely conflict with the design intentions of the developers.

In Payday 2, one of the more annoying things to keep track of during play was the number of times you could answer a pager before the alarms would go off during a stealth mission. There was a mod built that provides more information about what’s going on including the number of pagers left, how long the assault wave is going to last, and more.

While these mods were very popular, and many expert players swearing by them, they were never added officially in some capacity to the main game. The designers felt that they provided too much information and went against the spirit of the design. Another obvious factor is modding in any competitive game. If a mod can legitimately provide a competitive advantage, you need to be careful with allowing that; especially in ranked modes.

This is as the developer you need to be aware of intent vs. practice. If something has become so popular or widespread that people consider it required, then you may want to consider putting it officially in your game. QOL features tend to be overlooked when designing a game, and if your community has found a way to make your game easier to play and enjoy, then you should investigate it.

With that said, I know someone is going to leave a comment regarding mods for difficulty in a game, as with the infamous mod developed for the PC version of Sekiro that caused a lot of arguments. Mods along these kinds are fine to develop, but they also come with a caveat that we’ll talk about in a minute.

![playability](../../assets/be58d78f08905b84.jpg)


![playability](../../assets/be58d78f08905b84.jpg)

If something is so annoying that people are trying to mod it out, it may be worth considering to change it

I know that some of you will say what’s the big deal of formally adding in a mod feature if the mod is available, but having a feature be considered “standard” gives it a different connotation than being a mod. It’s also important that if you do add a mod’s feature to your game that you include a credit to the modder in the game.

One final point, it’s important for everyone to understand the difference of having mod support and features vs. the base experience. From a development standpoint you can’t and should not rely on your fans and modders to fix issues in your game.

Likewise, it is unfair to rate a game based on the mods it receives: Either giving a game a lower score for having bad mods, or a higher score for mods that improved it. Going back to the Sekiro example, you cannot treat the difficulty mod for the game as part of the experience of playing it. Until something has been formally adopted and integrated into the base game — IE: not requiring a secondary download — you cannot use that as the basis of a review.

With the DSFix mod still being the standout exception to this rule — to the point that Bandai Namco officially list it as a recommended feature for Dark Souls on steam.

For Part 2 of our feature, we’re going to turn to a formal look at difficulty, and how it can and can’t be used for playability.

*If you enjoy Game-Wisdom and want to talk design with me, be sure to *[check out our discord channel](https://www.youtube.com/redirect?redir_token=ZcQ6rIYruGxQSb79v1ssxKIoFzB8MTU2OTcwNTE1N0AxNTY5NjE4NzU3&q=https%3A%2F%2Fdiscord.gg%2FMFdkhMz&event=video_description&v=GWy4e1CvWEc)