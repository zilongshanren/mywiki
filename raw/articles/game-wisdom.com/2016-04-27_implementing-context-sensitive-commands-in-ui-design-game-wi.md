---
title: Implementing Context Sensitive Commands in UI Design - Game Wisdom
url: https://game-wisdom.com/critical/context-sensitive-commands-ui-design
author: Josh Bycer
published: '2016-04-27'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

For this next post on important elements of UI design in video games, we come to context sensitive controls. A major part of the turn towards standardization last decade, context sensitive controls are an important part of streamlining a control scheme and make a game easier to play.


## Context Sensitive:

Obviously, we can define context sensitive controls very easily:

**Context Sensitive Controls: Applying multiple commands to a single button, with the game dictating which ones will be used within each context.**

Before, many games filled keyboards and gamepads with commands for the player to memorize and learn. In most cases, having these additional options didn’t make a game better, but just made it more confusing to have to remember what key was the open button and which one was the close.

Context Sensitive commands work best when you have commands built around black and white contexts; situations where the player needs to perform a specific command and nothing else. One of the best examples of context sensitive commands came from the Assassin’s Creed series. Here, the player’s “paper doll” interface shows them how different buttons would function based on the situation at hand. The player didn’t need a separate “stealth kill” button, when the attack button could do it within the right context.

What happens is that instead of having to learn multiple commands, the player just needs to know the function of the button when the need arise. That last point is important, if commands have distinctive purposes that only occur at specific points, they are great candidates for context sensitive commands instead of having buttons designated for only their use.

![Assassin's Creed, originally posted on Forbes UI Design](../../assets/6a523f08b200cc35.png)


![Assassin's Creed, originally posted on Forbes UI Design](../../assets/6a523f08b200cc35.png)

The use of a “paper doll” UI allowed the developers to condensed a variety of commands into something easy to follow

One other thing before we move on; even though this should be self explanatory, it’s important to call out the fact that if you have generic actions all tied to a general action, those are definitely actions that could be assigned a context sensitive button.

The example I have is pretty simple: You don’t need separate buttons for “Open a door, close a door, pull a lever, press a button,” when you can simply have a context sensitive “Use” button.

With that said, while context sensitive controls are easy to program, their actual implementation needs some thought.

## The Right Tool for the Right Situation:

The challenge of context sensitive UI design is figuring out how to combine button commands; you don’t want the player jumping forward when they meant to hide.

Buttons should have commands assigned to them in such a way as the already mentioned black and white scenarios: Commands that the player would never need at the same time. You also need to watch out for putting commands on the same button that could be interacted with in the wrong context.

Let’s say as an example that the attack and open door commands are on the same button. While the player is busy fighting an enemy, there is the chance that the game will think the player wants to open a door if the player is fighting near a door; putting them in a position where the wrong command goes off. In this case, you would need to give the “door open” command either its own button or put it on a different button to avoid having the wrong command go off.

![Batman Arkham City UI Design](../../assets/00496a3388e87427.jpg)


![Batman Arkham City UI Design](../../assets/00496a3388e87427.jpg)

Context sensitive commands must be situational; something that can only occur at specific situations in the game

Another point to watch out for is when too many commands are tied to a single button press. Remember, the point of context sensitive commands is that you are dealing with conditionals; the more you have tied to one button, the greater the chance that the wrong command will go off.

There is one exception to this, if the commands are all similar to each other, but still different enough that their use is black and white.

For instance, you could tie different attack commands to one button and have both context and an additional button modifier control them.

For those who don’t know the term, a modifier is an additional button press that informs the game to make use of different commands depending on the modifier pressed. For instance: Having a modifier for “fire power” would then give you access to the fire’s list of commands and usage.

Speaking of modifiers, it’s also important to use modifiers if you have commands tied to commonly used controls such as movement.

The problem is that it’s very easy for the player to input the wrong command while they’re busy moving around. For instance, in Valdis Story, the command for dashing is tied to pressing the movement keys twice very quickly. The problem is that it’s very easy to dash when you are quickly moving back and forth to try and dodge attacks or move in for a closer hit on enemies.

If they implemented a modifier to confirm to the game that the player meant to dash, then that would have solved that issue. You can see this in the Souls series and how you can only perform a forward jump when you are running; preventing someone from jumping forward and off of a ledge.

One final point that we need to talk about, given the fact that context sensitive commands are not always known for the player, it’s becoming more and more important to show them on the game UI under the right situations. Going back to Assassin’s Creed, the paper doll constantly updates the UI and the player as to what commands are currently available based on the situation at hand.

While it may be immersion-breaking, you cannot expect the player to remember what button does what for every situation in your game. Some games will pop up the command onto the game space and then removes it when the player moves away; keeping the feeling that the world is immersive, but still providing the necessary information.

## Keeping Things Tidy:

Context Sensitive controls in UI Design work to reduce the number of commands the player needs to memorize over the course of playing. As we’ve talked about, it’s important to know what commands should be set up this way and where on the gamepad/keyboard.

You can go as small or as big as you want with context sensitive commands: From simply reducing the number of buttons needed, to even having different “modes” based on the situation at hand. Once again, the best way to figure out how your game controls and if you need context sensitive controls is to play test it. You’re never going to know how your game feels until someone picks up a controller or sits in front a computer and starts playing.

**If you enjoyed this post, please consider donating to the**** **[Game-Wisdom Patreon Campaign](https://game-wisdom.com/patreon.com/gwbycer). Your donations help keep Game-Wisdom going and allow me to continue putting out great content.