---
title: 'A Lesson on Control in Game Design: Modifiers - Game Wisdom'
url: https://game-wisdom.com/critical/game-design-modifiers
author: Josh Bycer
published: '2015-11-19'
source_blog: Game Wisdom
source_site: https://game-wisdom.com
category: game programming
fetched: '2026-04-13'
---

A popular topic that I like to talk about is the standardization of game design; where developers standardized control methods and mechanics to make it easier to learn games. Instead of having control actions in the double digits, you could do the same with a condensed set of buttons; this also led to PC games being easier to port and play on the consoles.

For today’s post, I want to focus on a shortcut game designers use to get a lot of actions into a game without having to extend the control scheme out, and that is by using modifier actions.


## Action Mods:

Video game gamepads and keyboards are standardize pieces of equipment, meaning that everyone has to work with the same setup and limits of buttons. As a developer, that means you can’t program an action for a third analog stick or a ZLRP button. So, what happens if you want to have more actions than you have buttons for?

This is where the use of a modifier command comes into play, and will be defined as such:

**Modifier Command:**A command that alters the functionality of the other actions that the player has available.

This is an evolution of context-sensitive control schemes: Where certain actions would only take place under specific circumstances. Modifiers are very basic in their concept: The player holds down a button and their moveset will change. In some cases, only the functionality of the abilities will be altered, while in others, they player may access completely different abilities.

There are a few examples that come to mind. The main one is from DMC Devil May Cry. In the game, the player has three different types of weapons: Normal, Angel and Devil based attacks. Instead of assigning different types to different button commands, the developers implemented a modifier based system. Pressing one trigger button will transform all of Dante’s attacks into Angel mode, another for Devil, and not holding a trigger will do normal attacks. The beauty of this system was that it made combat very elegant, as the player could effortlessly switch between all three weapon types without requiring memorizing additional buttons.

![DMC Devil May Cry game design](../../assets/92abebb6aaacb074.jpg)


![DMC Devil May Cry game design](../../assets/92abebb6aaacb074.jpg)

Modifiers work best in real-time or action-based titles, where the player needs to perform a lot of actions really quickly

Another option is for fighting games or titles with fighting game mechanics like third person action games; where one action may become a modifier for others. In Mad Max, one of the enhanced moves you can learn is the ability to ram into enemies while running, which requires you to be running in order to activate.

Here, the designer gives the player a new action by using an already understood command and mechanic as a modifier. This extends the systems of the game, but not having to add a brand new button or element for the player to understand.

From the examples and what we’ve talked about, modifiers can be useful, but they have a very specific purpose and utility which limits their usefulness.

## When to Modify:

Modifiers are great as a way to add more mechanics to a game without adding more controls for the player to learn, but there are limitations to this system. Modifiers are typically used in action games; as turn-based or strategy games don’t have the immediacy that would be required of modifiers.

Button placement is a big deal for modifiers, because the player will have to hold down the button in order for the modifier to trigger. This is where the gamepad is superior to the keyboard and mouse thanks to easier hand placement. It’s awkward to have to hold down a key on a keyboard than it is to hold down a button on a gamepad, as your hands naturally rest near or on all the buttons that you need when using a gamepad. You do have the option of making the modifier a toggle, but that doesn’t flow as well compared to making it always off/on while holding.

Keep in mind that the modifier itself is not an action; holding down the button will not trigger anything on screen. For each modifier button you use for your game, that is one less button that you can make use of when defining your control scheme. Typically, designers will make shoulder or trigger buttons the modifier action, this is because your hands naturally rests on the buttons and the player can comfortably hold one of them down and press the face buttons easily.

![Mad Max game design](../../assets/68252169b842c978.jpg)


![Mad Max game design](../../assets/68252169b842c978.jpg)

In games that make use of commands built around different systems, you can get a bit more functionality by using modifiers related to specific actions.

This should be obvious, but a modifier should not be a context-sensitive command as well, because at that point you are just layering on complexity that’s going to make your game harder to learn. Another point is that one action is typically not enough to justify assigning a button command to be a modifier.

In the example from Mad Max, the run command was given the added functionality to trigger the ram attack, because it was just a natural extension of its use. With DMC Devil May Cry, each modifier affected all of Dante’s combat abilities and was a good use of modifying the action.

One final thing, keep in mind that there can be such a thing as too many modifiers. Each modifier can alter the functionality of the other button commands; effectively multiplying the number of actions in game.

So, if you have both the shoulder and trigger buttons as modifiers for the face buttons, that means you have 20 actions for the player to understand. And for the love of all that’s good in the world, do not have modifiers that modify other modifiers that modify other commands; at that point, you’re just making life difficult for people.

## Streamlining:

Modifiers are just another example of how the game industry standardized and streamlined the complex control schemes of yesteryear. None of you will ever have to face the horrors of trying to play Rainbow Six on a Dreamcast-styled controller. This is just one of many tricks that you can use to give your game added functionality without needing a unique controller or humanity to evolve extra fingers and hands.