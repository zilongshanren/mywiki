---
title: A Bestiary of Alternative Game Controllers - Alan Zucconi
url: https://www.alanzucconi.com/2015/10/28/from-hardware-to-software-a-bestiary-of-alternative-controllers/
author: Alan Zucconi
published: '2015-10-28'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Many game developers are suspicious about alternative controllers, believing that since they can’t be easily mass produced, they are useless. Well, this is the story of how an Arduino got me to San Francisco for free. Twice.

- Part 1.
~~Rise~~Fall of the indies - Part 2.
[Rise of the](https://www.alanzucconi.com#part2)~~indies~~controllers - Part 3.
[Build your own controller](https://www.alanzucconi.com#part3) - Part 3.5.
[The curious case of Virtual Reality](https://www.alanzucconi.com#part4) [Conclusion](https://www.alanzucconi.com#conclusion)

![alt1](../../assets/d068fd71b46e8c58.png)

It’s undeniable that the innovation and creativity brought by the first indie titles kickstarted a revolution within the entertainment industry. Now that making games has never been easier, discoverability has became one of the biggest issues for developers. In just about three years we have moved from the **Golden Age of Indies** to their supposed **Indiepocalypse**. We can safely say that “*Hey, I’m an indie developer!*” is not a pick up line any more. If you want to keep being a hipster, making games is simply not enough in such an overcrowded industry.

We can safely say that «Hey, I’m an indie developer!» is not a pick up line any more.


There are indeed games that succeed in pushing the boundaries of innovation, such as [Mushroom 11](http://store.steampowered.com/app/243160/) or [Monument Valley](http://www.monumentvalleygame.com/)), but the more games are being released, the harder it is to create something that is *truly* new. Whether indie games are actually doomed or not, there is something else which is growing bigger and bigger: **alternative controllers**. If there is something that we should have learned from history, is that it repeats itself. Alternative controllers are replicating, on a smaller scale, what have happened already to indie games. They are filling a gap in the industry, providing novel and unprecedented experiences. And, exactly like indie games few years ago, the alternative controllers of today are rough, yet full of potential. The first Tomb Raider looks photorealistic when compared to PacMan; yet, it is almost embarrassing to play now that we have Physically Based Rendering. When players don’t have anything else they can use for a comparison, you can afford to leave some rough edges. And **now** there’s nothing as fresh as alternative controllers.

![alt2](../../assets/26bd8a594a682b06.png)

If you’re wondering how this can be related to your game… well, we’re getting there. More and more developers every year are submitting their games to competitions such as [IndieCade](http://indiecade.com/), the [Experimental Gameplay Workshop](http://www.experimental-gameplay.org/) and [Fantastic Arcade](http://fantasticfest.com/arcade). And each year, the quality of the games that are selected increases, making the competition even harder. IGF alone counted over 1000 submissions (main and student entries), and IndieCade reached over 1300. And is worth noticing is that the number of alternative controllers featured in game competitions is increasing. From 2012 to 2015, the numbers of alternative controllers showcased at IndieCade almost doubled. And given the fact that the majority of games are, indeed, *just* games, alternative controllers have a much higher chance of being selected. Just to name a few, these are some of the most **controller friendly** events:

Let’s say this in another way: if you want to maximise the chance of having your game selected at an event, you better start working on an alternative controller. Yes, custom peripherals are very hard to mass produce, but this is not the point. I am not trying to sell them, and unless this is your main product, you shouldn’t either. Compared to most of indie games, the majority of alternative controllers are not for sale. They recoup their investment in a different way: media attention and access to game events.

If you want to maximise the chance of having your game selected at an event, you better start working on an alternative controller.


![alt3](../../assets/53ca9ed7a233cf6e.png)

Ok: now that we know that alternative controllers are great, the next natural step is building your first one. If you’re already working on a game and want to increase its visibility, adding some custom tech can definitely help to get into events and showcases. The challenge is to find something that *fits* your game.

#### Hacked controllers

The easiest thing you can do is to hack an existing controller, whether it’s a keyboard, a mouse or a gamepad. Droqen’s [Bonus Look](http://www.droqen.com/bonuslook/), for instance, is a two player games which uses two keyboards: one has only letter keys, the other one only arrow keys. Similarly, a game called [Panoramical](http://xiwielectronics.com/products/panoramical-interface) has refitted a MIDI controller into a custom controller.

#### Emulated keyboards and mouses

Hacked controllers can get only get you so far. You are in fact constrained by the devices you can hack. The next step is to create your own controller, and connect it so that your computer will detect it as a keyboard or a mouse. The big advantage of this technique is that your game doesn’t know that you are using an alternative controller. This is great if you want to spice up an existing game, providing a completely new type of interaction. It’s the case of [Space Beagles](https://twitter.com/spacebeagles)‘s [Butt Sniffin Pugs](http://www.buttsniffinpugs.com/); while the ball controller is made out of a hacked mouse, the remaining controllers emulate a mouse.

Emulating a keyboard or a mouse sounds hard, but is actually easier than you think: there are many micro-controllers that can do that, such as [Teensy 4.1](https://www.amazon.co.uk/Teensy-4-1-Without-Pins/dp/B088D3FWR7?dib=eyJ2IjoiMSJ9.DMFXLg9QmiK6qgnBtWCOZvc--EDBSDRQrWu4Y7mC8WqeYoL4IuYf4msbp3kvDUTByMVgrSvbl7PehHnshABIUda1dnf5e_-GnmUnQFqOh5uAPF2Zlmnsv2AuSDyDPGPE1CmZ2g81J5ye_o5hb-AbnP1PedrQjo5yDDXfUyTcICdnQYOpjimY3sajWMyrKf3HQibvXrsCV8-aqWuWHl-ATbAyj9YtJV-TLnfOXJfMrSsjqKNZkG1PnXVk0wZuReWXundsgarqxHOYFMexexrAPdsQYu__kgdgmDEXli6mCpE.xZeMGb3RkzZ9MEuJJiAgNBYn8oLkYxvQo6EKc8kW4HQ&dib_tag=se&keywords=Teensy&qid=1724317154&s=computers&search-type=ss&sr=1-1&linkCode=ll1&tag=alanzucc-21&linkId=66e835b206178e8b13fd4a1a77f02187&language=en_GB&ref_=as_li_ss_tl). Unfortunately not all Arduinos can be natively configured to emulate keyboards and mouses. The ones based with a ATmega 32U4 microcontroller can, which includes [Arduino Due](https://www.amazon.co.uk/Arduino-A000062-Due-Microcontroller/dp/B00A6C3JN2?crid=OLA0XCXE4PDV&dib=eyJ2IjoiMSJ9.G0SVvgAfgkYdxt9jxXksrd08JSMawpGWwoGzs8wsB3choQK6G45ojckcoyMvgIfkqquVaeLkschF__uoyypuuUEit8p6QIemuOkTwIK3K_GyTT8BkkzNohgXvzKdQfLYwDFDxDIlGTQeqKVdyTpSZmVa20I23C03yWA7cchs5_3hUKlc9mmdwPcYCSFO_K0aTTvRVP8-SNV6wMeQWfdzdx03-sV2x_JdYsCHcKpX4vc.7bvpfDxL_0iX03Ogn_YzcOsVeifVrLT3cIoY-cYppdE&dib_tag=se&keywords=arduino+due&qid=1724330440&sprefix=arduino+due%2Caps%2C74&sr=8-3&linkCode=ll1&tag=alanzucc-21&linkId=048a73634a53da58ea93cfb93f8f9bd5&language=en_GB&ref_=as_li_ss_tl), [Arduino Leonardo](https://www.amazon.co.uk/Arduino-Leonardo-Microcontroller-Board-Headers/dp/B008A36R2Y?dib=eyJ2IjoiMSJ9.vR1UPuzBZ3OQRQQsIjTVPWPnvDCu6Hvy60v6OWdCKCh1sZS9UB_aj-2hdug5UWNUvy_ufLx0PPQ4W1MftByV1x-rn4zY9uQcZdXb699acTtbXhdw0Lo5jp6WnlsOeiDODM0V9iVjRh_1UhJUQDOkHnNEdKUcU2GkjbGDKCkYQKIT-paHodKPpTxdwKft4PJhIiku51b9QEWknY0EBq4Dfvf79bYguc3BM79o3aum5kk.v6v6khY7fFOiyN75r_WTTZ6zzvo9cgMe25RF8X2wR7Q&dib_tag=se&keywords=arduino+leonardo&qid=1724330382&sr=8-2&linkCode=ll1&tag=alanzucc-21&linkId=f093bc8a95099d53da003439b4c1ebe4&language=en_GB&ref_=as_li_ss_tl), and [Arduino Yun](https://www.amazon.co.uk/Arduino-ABX00087-Uno-R4-WiFi/dp/B0C8V88Z9D?crid=3S2F7C8DUH7HQ&dib=eyJ2IjoiMSJ9.YGFCFx28glIHKEmwCj4v4X7a_6Jb5KCCg2xjs0iWSE5-4xbQON_MLDV3EPlzX0IWiiOzzUT8DwynNW04mTWhUSLpC0PqzEciIXuDLecK-BVfaO_TqBsqUKKZkk22cUfVrO9xYgA3Yt4-vtBEVtcdhOg4kM6fhZeyuQHtXu58yTGxpr6lqaAFI_3hEBegqgiFeLB12oHIOXp31H16f1P0HDFbCvN8gFtio1ey-RROy7U.hbeheHoiSySc5gLa6PA_gJ9Dw0NlWBqBCX3oLM0rgPg&dib_tag=se&keywords=arduino+yun&qid=1724330490&sprefix=arduino+yun%2Caps%2C81&sr=8-3&linkCode=ll1&tag=alanzucc-21&linkId=b6de63821864a2500b7b49de58525c38&language=en_GB&ref_=as_li_ss_tl).

### 🪛 Recommended Components

There are several micro controllers available at a much lower price (usually referred as “Arduino compatible” or “Arduino clones”), but is hard to guarantee for their quality and durability.

#### Alternative controllers

If you want to push you game further, you might have to provide data to your game in a format which cannot be easily converted in keyboard strokes or mouse movements. When this is the case, the only alternative is to create a controller which has its own communication protocol. This allows you to send all the data you want, and you can also receive data back from it. A game that does this very well is [Fabulous Beasts](http://playfabulousbeasts.com/). By balancing bizarrely shaped blocks onto a tower, you can affect the world on your laptop. Another interesting example is [Spacebro Justice Rocket](http://www.radsandwich.com/spacebro-justice-rocket) which uses custom made gloves called High-5000.

Basically any microcontroller can be used for this. One of the most commonly used for beginners is [Arduino Uno](https://www.amazon.co.uk/Arduino-ABX00087-Uno-R4-WiFi/dp/B0C8V88Z9D?crid=3S2F7C8DUH7HQ&dib=eyJ2IjoiMSJ9.YGFCFx28glIHKEmwCj4v4X7a_6Jb5KCCg2xjs0iWSE5-4xbQON_MLDV3EPlzX0IWiiOzzUT8DwynNW04mTWhUSLpC0PqzEciIXuDLecK-BVfaO_TqBsqUKKZkk22cUfVrO9xYgA3Yt4-vtBEVtcdhOg4kM6fhZeyuQHtXu58yTGxpr6lqaAFI_3hEBegqgiFeLB12oHIOXp31H16f1P0HDFbCvN8gFtio1ey-RROy7U.hbeheHoiSySc5gLa6PA_gJ9Dw0NlWBqBCX3oLM0rgPg&dib_tag=se&keywords=arduino+yun&qid=1724330490&sprefix=arduino+yun%2Caps%2C81&sr=8-3&linkCode=ll1&tag=alanzucc-21&linkId=2f08a895934ac059bea174ef0a1196e9&language=en_GB&ref_=as_li_ss_tl), which is powerful and easy to use. There is no standard way to connect Arduino and Unity, although I have been writing [a tutorial](https://www.alanzucconi.com/2015/10/07/how-to-integrate-arduino-with-unity/) that explains how to do it in great detail. Alternatively, you can also use Arduino to provide an additional feedback to your players, whether it’s a chair vibration or a change in the lighting.

#### Alternative games

The ultimate step of alternative controller is creating an entirely novel, self-contained experience. Alternative games can grab much more attention, since everything about them is new. The beautiful [Robin Baumgarten](https://twitter.com/Robin_B)‘s [Line Wobbler](http://aipanic.com/projects/wobbler), for example, has been exhibited all over the world in over 30 game events and exhibitions. [Jerry Belich](https://twitter.com/j3rrytron) successfully raised over $75.000 on Kickstarter for his [The Choosatron](http://choosatron.com/).

Creating an alternative game is obviously challenging and time consuming, but it has its own advantage. When you create a video game, players have a lot of expectations and can compare it to other thousands of similar products. But when you create something new, expectation is sublimated by surprise.

When you create something new, expectation is sublimated by surprise.


I have recently written a [tutorial](https://www.alanzucconi.com/2015/10/21/everything-you-need-to-know-about-leds/) on how to use LEDs and NeoPixels strips. They are at the heart of many existing alternative games, and are still massively unexplored.

### 🪛 Recommended LEDs

#### Alternative experiences

Even the most immersive game still relies on a monitor and a headset. Players are not used to other types of feedback, and this is why is possible to surprise them with very little. Oliver Kreylos’s [AR Sandbox](http://idav.ucdavis.edu/~okreylos/ResDev/SARndbox/), for instance, is an interactive experience which literally an *augmented reality sandbox.*

Sometimes is even possible to provide an enhanced feedback just by taking the player out of its comfort zone. [Taphobos](http://taphobos.com/), for instance, provides the truly unique experience of being buried alive. Is a two player game, in which one is locked inside a coffin. The games does its best at recreating that very feeling, and it uses nothing more than a coffin and a headset.

If I have to be completely honest, is very unlikely that any alternative controller you’ll make will become a successful hit. Manufacturing hardware is hard, very hard. Most likely, you game will be a nice addition to a game event or a party. There’s an notorious exception to this: **virtual reality**. Oculus Rift, Morpheus and Hololens sit in a grey area, in between traditional and alternative controllers. They are indeed alternative, if compared to mice and keyboards, but they’ll be also mass produced. If you have ever attended a game event, you’ll know that nothing creates a queue like a VR headset. VR made very clear that players are eager to test new gaming experiences, even if they are likely to make them sick. What makes VR so appealing is not the quality of the experience, but its novelty. When you have a new controller, even an old experience can suddenly become interesting again.

When you have a new controller, even an old experience can suddenly become interesting again.


There are very few examples in which VR has been successfully integrated into the gameplay, such as [Henry Hoffman](https://twitter.com/HenryHoffman)‘s [Aboard the Lookinglass](http://thehen.itch.io/lookinglass), which uses a **Leap Motion sensor** to detect the player’s hands.

I’m personally very reluctant to classify VR as an alternative controller. For the majority of games, VR is nothing more than an immersive monitor.

Alternative controllers are not only awesome; they are the perfect way to focus the media attention towards your game. In an industry that is so overcrowded, it won’t hurt having something a little bit extra-ordinary. There are several events that focuses on alternative controllers only, such as:

The most important, [ALT.CTRL.GDC](http://www.gdconf.com/news/submit_your_unique_alternative.html) is now accepting submissions; it’s one of the most innovative and experimental exhibitions at GDC San Francisco, and you should totally get involved. I had the amazing chance of presenting my work there for two years in a row, and I’ll definitely submit a controller again. Compared to other events which have 1000+ entries, ALT.CTRL.GDC counts “only” 100+ submissions. Don’t miss this chance.

#### Other resources

[What is really killing indie games](https://medium.com/steam-spy/on-indiepocalypse-what-is-really-killing-indie-games-3da3c3a1ea76): an insightful post by SteamSpy;[VUSB Keyboard tutorial](http://www.practicalarduino.com/projects/virtual-usb-keyboard): the circuit necessary to emulate a keyboard with an Arduino Uno;[Alternative game controllers](http://www.gamasutra.com/view/feature/130527/alternative_game_controllers.php?print=1): an article on more commercial approaches to alternative controller.

## Leave a Reply Cancel reply