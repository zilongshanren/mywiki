---
title: Accessibility in Videogames - Alan Zucconi
url: https://www.alanzucconi.com/2021/05/24/accessibility-in-videogames/
author: Alan Zucconi
published: '2021-05-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This article will focus on how to design accessible videogames for players living with a disability. The idea came after writing a long thread on Twitter which focused on **accessibility design**.

If this is a topic that interests you, and you want to learn what you can do to make your videogames more accessible, keep reading!

## Introduction

*Videogames are hard*. Not long ago, this would have been true for most games, which are often purposefully designed to include some kind of challenge. Overcoming these challenges is what many would say keeps players “in the flow”. But at which point games becomes so hard that it is impossible to play them? For many, selecting the “Easy” difficulty is enough to provide a challenging—yet entertaining—experience. But not for all. Many players, in fact, are living a disability which adds an extra layer of unwanted challenge to many games.

Sadly, the vast majority of games are not designed to be accessible. It is important to point out that making a game *truly* accessible to all people might often be impossible. But there are many small changes that can be done to a game to massively expand its potential audience.

With over 2 billion people in the world living with a disability, accessibility in videogame is something that can no longer be ignored.


The rest of this post will discuss some of the most common form of disability or impairment, and you can do as a game developer to ensure your game is accessible. You should also remember that disabilities are often very personal and that even different people with the same disability might requires different adjustments.

If you are unsure, the best thing to do is to make sure your games are tested by people who are living with disabilities, or to hire a consultant who specialises on this subject.

## Colour Blindness

Colour blindness is a form of visual impairment which affects the perception of certain colour tones. It is fairly common, with approximately 300 million people in the word living with it. There are also several different types of colour blindness, which can have different degrees of severity.

**Deuteranopia** is the most common, and it affects the perception of red tones. You can see below a simulation which roughly shows how colours are perceived by someone living with deuteranopia.

Games that are heavily relying on colour-coding to convey information (such as health bars and warnings) are particularly affected. Deuteranopia can also make harder to perceive the contrast between certain colours.

As a developer, you should:

- ✔️ Ensure not essential information is conveyed by a colour alone
- ✔️ Provide high contrast between text/UI and background
- ✔️ Allow a way to replace colour-coded information

Good compromises between aesthetics and accessibility can be seen in games such as “FTL” & “Hue”. Both games have the option to add patterns to shaded areas that could otherwise be missed by colour-blinded players.

![](../../assets/d2d2546af43d8e55.jpg)


![](../../assets/d2d2546af43d8e55.jpg)

“Hue”, in particular, has been praised for his attention to details and for how accessible his design was.

![](../../assets/260517d7529457bd.jpg)


![](../../assets/260517d7529457bd.jpg)

### Simulating Colour Blindness

Colour blindness is one of those disabilities which can be easily simulated on a screen. There are many different piece of software which can do that. For instance, [Color Oracle](https://colororacle.org/) can help changing how colours are rendered on your screen.

![](../../assets/a3bfb786b51a1679.gif)


![](../../assets/a3bfb786b51a1679.gif)

If you are a Unity developer, I also developed a simple Unity package which can be used to turn this feature on and off in the inspector. You can find it in an article which is entirely dedicated to the topic: [Accessibility Design: Colour Blindness](https://www.alanzucconi.com/2015/12/16/color-blindness/). While most of my assets are available on Patreon for a small price, this was intentionally made available for free.

## Earing Impairment

Audio can play a huge role in a game. Not just to set its tone and atmosphere, but also to convey information. As a bare minimum, all games which feature dialogues should include subtitles. This has the extra benefit of helping non-native speakers.

Many games, especially FPS, are heavily relying on audio clues as part of their gameplay. For instance, to indicate where enemies and threats are coming from. Games like “Minecraft” allows to show the direction sounds are coming from.

![](../../assets/0b05019a11a8ad26.png)


![](../../assets/0b05019a11a8ad26.png)

Other games, such as “Fortnite” are going as far as showing directional waveforms on the UI, helping players knowing where and what type of sound is being played around them.

![](../../assets/4632783e8a171272.jpg)


![](../../assets/4632783e8a171272.jpg)

As a developer, you should:

- ✔️ Provide subtitles for all important speech and important events
- ✔️ Provide separate volume controls for speech, sound effects and music
- ✔️ Provide indication of the sound direction, where this is necessary

### Subtitles

Reading subtitles adds an extra challenge to the medium. If you are watching a dubbed movie, you might have noticed how much tiring it can get to follow both the images and the text at the same time. For this reason, simply adding subtitles might not be enough: you should ensure the way in which they are incorporated in the game makes them easy to read.

These guides, originally designed for movies and TV, might help to get this right:

There are a few specific take-away messages:

- ✔️ Two lines maximum
- ✔️ The recommended subtitle speed is 160-180 words-per-minute (WPM) or 0.33 to 0.375 second per word
- ✔️ Enforce a blank between titles to help viewers notice the text change
- ✔️ Use colours to distinguish speakers from each other

## Cognitive Impairment

This category includes a vast range of disabilities, which can affect thoughts, memory or even how information is processed. Games that require to solve puzzles, complete long tasks or do a lot of backtracking are at risk of being inaccessible.

Some tips to improve the accessibility for cognitive impaired players are:

- ✔️ Remind about current objectives & inputs
- ✔️ Separate volume controls for effects, speech & music
- ✔️ Highlight important words and objects
- ✔️ Provide the option to remove combat, puzzles & enemies

“Shadow of the Tomb Raider” has a very comprehensive set of accessibility options. They not only make the game easier for players who prefer a more casual experience: they also make the experience much more accessible. Square Enix also provided a very detailed breakdown of their decisions in this article: [Shadow of the Tomb Raider – Difficulty and Accessibility](https://tombraider.square-enix-games.com/en-us/news/shadow-of-the-tomb-raider-difficulty-and-accessibility).

![](../../assets/5fcc870c30b96d2d.png)


![](../../assets/5fcc870c30b96d2d.png)

Many players with cognitive impairment might also struggle to distinguish background elements (which only serve as a decoration) to foreground elements (which may have an important gameplay role). Games such as “The Last Of Us Part II” go to an extreme length to ensure the game be accessible. You can read more in this article: [Accessibility options for The Last of Us Part II](https://www.playstation.com/en-us/games/the-last-of-us-part-ii/accessibility/)

![](../../assets/f29330af56cc2fcc.jpg)


![](../../assets/f29330af56cc2fcc.jpg)

In the image above, you can see how strong colours are used to indicate different gameplay elements. Blue for players, red for enemies and yellow for interactable objects. Reducing the visual clatter can also help players with attention disorders such as ADHD.

If you are a developer, creating such an effect is actually easier than you imagine. Unity, for instance, has a feature called [Replacement Shaders](https://docs.unity3d.com/Manual/SL-ShaderReplacement.html) which allow to easily change which shader is being used to render a material at runtime. This is often used to create minimaps, or to simulate X-ray vision. It can, however, be used to change how certain objects are coloured. Similarly, global shader properties can be used to achieve a similar effect in Unity.

“The Last Of Us Part II” is also using some simple edge detection shader to highlight the contrast between different objects. This is a topic that will be discussed in a future post.

### Dyslexia

Menus and subtitles are not exempt from accessibility requirements. There is preliminary research to suggest that the use of certain fonts might help players with dyslexia. [OpenDyslexic](https://opendyslexic.org/) is a typeface specifically designed to help people with dyslexia reading more easily.

![](../../assets/07c5ba4374d86baa.png)


![](../../assets/07c5ba4374d86baa.png)

Some letters, like *p*, *q*, *b* and *d* are based on the *exact* same symbol, flipped and rotated. This can create a lot of confusion for many people with dyslexia. OpenDyslexic—and other fonts designed with similar accessibility requirements—use symbols that are actually different. This helped distinguishing them much better.

### Motion Sickness

Motion sickness is not regarded as a cognitive impairment, although it is something that affects a significant portion of players and it does require several adjustments.

The main cause for motion sickness is when the game introduced a movement which does not match what the player is actually doing. This creates a dissonance between the eyes and the inner ear, which leads the brain to believe something is wrong such as being poisoned or seriously intoxicated. Ultimately, this is why motion sickness often causes being to feel sick.

As a developer, you should:

- ✔️ Allow to change the Field of View (FOV)
- ✔️ Allow the option to play in third person, instead of first person
- ✔️ Remove head bobbing when moving
- ✔️ Remove motion blur
- ✔️ Avoiding accelerating/decelerating
- ✔️ Maintain high framerate

As a player, there are a few things you can do to alleviate the effects of motion sickness as well:

- ✔️ Play in a well-lit room
- ✔️ Avoid playing the game in full-screen mode
- ✔️ Look away from the screen from time to time
- ✔️ Look at the border of the screen, not the center
- ✔️ Try moving your body with the game: for instance if the car is steering the the left, gently steer your body in the same direction

Motion sickness is also a very important topic in VR, where is affects a significantly higher percentage of players. You can read more it in [VR & Accessibility](https://www.gamasutra.com/blogs/IanHamilton/20161031/284491/VR__accessibility.php).

## Motor Impairment

A significant percentage of players are suffering with some kind of motor impairment. It is also common for otherwise non-disabled people to experience periods in which they required assistance due to injuries.

Some people who fall into this category are suffering from **dyspraxia** (sometimes also known as **developmental motor coordination disorder**): a disorder which affects their motor planning and motor coordination. Other conditions might result in a motor impairment, including **cerebral palsy**, **multiple sclerosis** or **Parkinson’s disease**.

One of the simples change you can make to improve the accessibility of your game is to make the controls fully remappable. This is specifically important because motor impairment can be very subjective, with different people requiring very different adjustments.

![](../../assets/e9a877d3ce1efb78.jpg)


![](../../assets/e9a877d3ce1efb78.jpg)

As a developer, you should:

- ✔️ Allow controls to be remapped
- ✔️ Include an option to adjust the sensitivity of the controls
- ✔️ Support more than one input device

One of the best examples of accessibility for motor impairment is “Celeste” Assist Mode. It allows to change several gameplay parameters such as how many times you can jump in mid-air, and even to turn invincibility and endless stamina on/off.

![](../../assets/167b0c555e2ed833.jpg)


![](../../assets/167b0c555e2ed833.jpg)

The choice of grouping these options under “Assist Mode” rather than “Accessibility Settings” has been received very positively, with many non-disabled players using it to customise the game to a level of difficulty they were comfortable with.

### Custom Game Controllers

Accessibility often means creating custom game controllers. This is true for many people who are living with severe motor impairment. Generally speaking, the creation of custom controllers is very expensive, and is something that at this stage is not commercially viable for the majority of developers. This is also because of the fact that those controllers might need to be tailored to each player’s specific needs.

![](../../assets/99772da142590c1c.jpg)


![](../../assets/99772da142590c1c.jpg)

[Assistive technology](https://en.wikipedia.org/wiki/Assistive_technology) is, after all, a relatively recent field. The game-related charity who is currently leading in this sector is [SpecialEffect](https://www.specialeffect.org.uk/). Over the years they have helped severely physically disabled and vulnerable people with their gaming and technology access needs. They work and mission are really outstanding, so is a charity worth supporting, if you can.

That being said, creating custom game controllers has never been easier. And while it remains a challenging task, it is something that you can do at home and within a very reasonable cost. Just to give you an idea, [Shake That Button](http://shakethatbutton.com) is a website which showcases hundreds of custom-made controllers. Most of them rely on technologies such as **Arduino**, **Raspberry Pi** and **Makey Makey**. The last one being the easiest if you want to create something that emulates a game controller or a reduced keyboard.

If you want to create your own alternative controller (but have not idea where to start!), I would suggest having a look at [A Bestiary of Alternative Game Controllers](https://www.alanzucconi.com/2015/10/28/from-hardware-to-software-a-bestiary-of-alternative-controllers/), which shows progressively more complex ways in which you can get started.

### Adaptive Difficulty

One very interesting idea which feeds into the wider discussion of accessibility, is **adaptive difficulty** (sometimes also known as [dynamic game balancing](https://en.wikipedia.org/wiki/Dynamic_game_difficulty_balancing)). The concept is technically simple: changing how difficult a game is, based on how the player is playing. This creates a closed-loop which, if done correctly, can dramatically enhance the gameplay experience.

One such example was a game called ACCELERUNNER, which I had the pleasure to work with with game developer and bear enthusiast Nicoll Hunt. In the game, “*when you run you run, when you jump you jump*“. However, how fast you run and how high you jump depends on how much you deviate from your average speed. This means that the game can be player *fairly* even by players with motor impairment. When showcased at EGX 2014, many wheelchair users where able to play a game that would have otherwise be targeted only to non-disabled players.

Balancing a game difficulty is, unsurprisingly, a difficult game design task. Which becomes even more difficult when dynamic balancing is added into the equation, making very difficult to test every possible combination. Mark Brown talked extensively about closed-loops in [How Games Use Feedback Loops](https://www.youtube.com/watch?v=H4kbJObhcHw&ab_channel=GameMaker%27sToolkit), including how certain design tweaks can avoid a “richer gets richer” cascade which would only further disadvantage players with a disability. One such example is Mario Kart, in which players who are behind are more likely to receive better bonuses.

![](../../assets/d638b47f0a090230.jpg)


![](../../assets/d638b47f0a090230.jpg)

Karma-based strategies which aim to “bring back balance” can really help, especially when it comes to multiplayer sessions with disable and non-disable players.

## Additional resources

One of the best resources you can find on accessibility is [Game Accessibility Guidelines](http://gameaccessibilityguidelines.com). It includes tips and examples for motor, cognitive, visual, hearing and speech impairments. Many of the suggestions you have seen in this article come directly from their website.

The [Xbox Accessibility Guidelines](https://docs.microsoft.com/en-us/gaming/accessibility/guidelines) (XAGs) are a set of best practices that have been developed in partnership with industry experts and members of the Gaming & Disability Community. The website provides a detailed set of guidelines which aim to make games more accessible and to create a coherent experience for Xbox players across different titles.

Mark Brown, creator of the successful [Game Maker’s Toolkit](https://www.youtube.com/channel/UCqJ-Xo29CKyLTjn6z2XwYAw) YouTube channel, made an entire playlist dedicated to designing games for disabled players.

[Laura Kate Dale](https://twitter.com/LaurakBuzz) published a series of videos about accessibility. She covers a variety of topics that usually receive less coverage, such as specific phobias, content-warnings, and even the complex subject of truthful trans representation.

Lastly, accessibility requirements are needed not just in computer games, but on tabletop games too. [Accessibility in Gaming Resources](https://docs.google.com/document/d/1ZFSXz-Yva1KZAsP7NblCdkoiQ6RcjxSV2gj98eXusJs/edit) is a comprehensive collection of resources for tabletop games, currently maintained by [Jennifer Kretchmer](https://twitter.com/dreamwisp).

### Writing About People with Disabilities

Talking about people with disability can sometimes be complex, especially since the words “disability” and “disable” are umbrella terms which refer to a vast group of very different people. There are many guidelines which help navigate this topic, such as:

[Inclusive language: words to use and avoid when writing about disability](https://www.gov.uk/government/publications/inclusive-communication/inclusive-language-words-to-use-and-avoid-when-writing-about-disability)by Office for Disability Issues, a UK government body;[Guidelines for Writing About People With Disabilities](https://adata.org/factsheet/ADANN-writing)by the Americans with Disabilities Act (ADA) National Network, founded by the National Institute on Disability, Independent Living, and Rehabilitation Research (NIDILRR);[Appropriate Terms to Use](http://nda.ie/Publications/Attitudes/Appropriate-Terms-to-Use-about-Disability/)by the National Disability Authority, an independent Irish body that provides information and advice to the Government.

The terminology used is constantly evolving, so it is unsurprising that many terms that were once popular (including old-fashioned medical terms such as “handicapped” or “spastic”) might now be considered offensive by some.

Please note that these guidelines are subjected to changes, and can different significantly based on your language, region or context.

## Conclusion

This article provided a brief introduction to the complex topic of accessibility in videogames.

Disability is allowed to exist only when there are no mitigating solutions.


Being short-sightedness, for instance, has stopped being a disability when eye glasses became an affordable solution. Likewise, we should strive as a community to make games more accessible Accessibility is not just for disabled players! After all, we are all fated to eventually become disabled, or to die before that happens.

## Leave a Reply Cancel reply