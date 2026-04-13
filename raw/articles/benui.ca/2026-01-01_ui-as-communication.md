---
title: UI as Communication
url: https://benui.ca/blog/ui-as-communication/
published: '2026-01-01'
source_blog: ben🌱ui
source_site: https://benui.ca/
category: unreal engine
fetched: '2026-04-13'
---

There are many approaches to user interface (UI) and user experience (UX) design. No single one of them is correct, but some of them can be useful tools to help us make better UI/UX for our games.

In this article let's think about **UI as a method for getting ideas from the game into the player's head**.

Ideas being moved from the game to the player's head.

![Ideas being moved from the game to the player's head.](/assets/ux/ideas-head-diagram.webp)

This might sound really obvious but it's another lens through which we can view UI design, and one that I believe is useful.

Before we think about **what** we might want to tell players, we're first going to talk about **how** we can communicate ideas to the player. We can then keep these methods in mind when we think about what we want to communicate.

## Methods of Communication

Humans are a predomenantly visual species, so the majority of methods listed below are visual. Each of these methods or attributes have varying amounts of

- Speed and ease for users to understand
- Amount of information each method can communicate

We will start with the simplest and least

### Size

![](../../assets/e672262d91ce4780.webp)

Varying size of elements is one of the most fundamental ways of communicating something about that element.

Size is not the only way of attracting the eye, but players will naturally look at larger elements first, followed by smaller elements. They will assume that the larger the element, the more important it is.

May seem obvious but it's worth stating: **relative size is a fundamental way of communicating relative importance of elements**.

Zach Gage explained this far better than I ever could in his GDC talk [Building games that can be understood at a glance](http://stfj.net/DesigningForSubwayLegibility/)

This example is patently absurd but you would be surprised how often unimportant elements are made the same size as extremely important ones.

![This example is patently absurd but you would be surprised how often unimportant elements are made the same size as extremely important ones.](/assets/ux/Size-Menu-Terrible.webp)

### Position

If you are primarily a reader of left-to-right languages, you probably assumed the top-left option in this menu was the most important, and assigned the bottom-right one least importance.

![If you are primarily a reader of left-to-right languages, you probably assumed the top-left option in this menu was the most important, and assigned the bottom-right one least importance.](/assets/ux/Order.webp)

Players typically assume that elements are ordered in the same way as their preferred language's writing system. In English that means we assume the top-left element is first and bottom-right is last. Similarly we assume the first element is the most important and the last, least important.

Position can therefore be used to communicate the **order** and implicit **importance** of elements.

### Shape

![](../../assets/1bb1214761cc514d.webp)

Along with colour, shape is an extremely basic way of communicating something about a visual element. Differentiating shapes is something humans learn as very young babies, and is something we immediately notice at a glance.

Related to

Shapes alone can convey feeling

Steph Chow illustrates [how shapes can convey the feel of Pacific Islands](https://www.gdcvault.com/play/1025340/Immersing-a-Creative-World-into).

![Steph Chow illustrates [how shapes can convey the feel of Pacific Islands](../../assets/db190110d07110d9.img).](/assets/ux/immersive-world-shapes.webp)

Colours, fonts and textures get a lot more coverage as ways of communicating the feel of a world, but simple [button shape can also go pretty far](https://www.gdcvault.com/play/1025340/Immersing-a-Creative-World-into).

Splatoon

Splatoon communicates its world's drippy feel through UI shapes. Compare them with Mario's shapes on the left. Image from [Splatoon UI talk](http://careerhack.en-japan.com/report/detail/965).

![Splatoon communicates its world's drippy feel through UI shapes. Compare them with Mario's shapes on the left. Image from [Splatoon UI talk](../../assets/20d94eaf1b97a33b.img).](/assets/ux/splatoon-shapes.webp)

### Icons

Icons can be thought of as complex shapes with some possible attached meaning.

### Brightness, Colour, Hue

These could be split into three parts, and I think visual artists will be disappointed that

It's important to be aware that colour is not equally visible to all players. Colour-blindness affects about 8% of men and 0.5% of women. Relying on it as a sole method of communication could mean that the information is lost to these players.

### Texture

![](../../assets/1082cfc7fccbfc24.webp)

A variation on brightness/colour/hue, texture can be

### Sound

![](/assets/ux/Sound.webp)

As with colour, not all players perceive sound in the same way. Hard-of-hearing players, deaf players, as well as anyone playing with the volume turned down will not pick up on things communicated through sound alone.

### Motion

![](/assets/ux/Motion.webp)

Any visual that changes over time can communicate

### Vibration

![](/assets/ux/Vibration.webp)

Most games console controllers and mobile phones have haptic rumble support. This can be used as a method of communication just as with sound or

It's not possible to rely on this though, some players may be playing on a device that does not support vibration, or they may have disabled vibration altogether.

### Text Meaning, Semantics

You may not be surprised to learn that text can be used to communicate with players. It takes the longest amount of time for players to get meaning from text in comparison to more fundamental things like colour and shape, but text can communicate the most amount of information.

It does come with some caveats though:

- Language ability is a factor in how much players can understand from the text. If the game is not available in their native language, or they are a very young player, or someone with a learning disability it is harder for them to
Text can be very tiring in comparison to other methods of communication.

- Text meaning
- Motion
- Something that plays over time
- Interaction, state that changes when player does something

- Rumble

## What can we communicate?

We've seen that there are a huge number of ways we can communicate with the player. But what do we want to communicate?

Obviously this depends on the game, the situation within the game,

### Importance

### Interactivity

### Order

Guide the eye through shapes Hierarchy of

### Setting and Theme

### Values of the World

Aesthetics Writing - Meat Units vs people's names

- Obviously information
- But also things like "hey I'm clickable"
- Hey this is important, this isn't
- Changing order of importance
- (three reads)

- Order, go here then here
- Communicate the setting and theme
- Also communicating the values of the world