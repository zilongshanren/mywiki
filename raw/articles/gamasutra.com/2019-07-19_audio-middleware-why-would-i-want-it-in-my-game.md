---
title: 'Audio Middleware: Why would I want it in my game?'
url: https://www.gamedeveloper.com/audio/audio-middleware-why-would-i-want-it-in-my-game-
author: Theo Nogueira
published: '2019-07-19'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Audio Middleware: Why would I want it in my game?

On our current day and age of game development, almost all AAA game studios use audio middleware and so does a good amount of indie game developers. However, a lot of indie developers wonder what is it, where does it come from and why do they need it.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

# Audio Middleware: Why would I want it in my game?

On our current day and age of game development, almost all AAA game studios use audio middleware and so does a good amount of indie game developers. However, a lot of indie developers wonder what is it, where does it come from and why do they need it as a part of their game?

## What will you find in this blog:

[-> ](https://www.gamedeveloper.com/audio/audio-middleware-why-would-i-want-it-in-my-game-#FMOD%20Space%20Racer)[FMOD Space Racer - Demo Video](https://youtu.be/R0ydql8b7eA)

[-> ](https://www.gamedeveloper.com/audio/audio-middleware-why-would-i-want-it-in-my-game-#Wwise%20Space%20Racer)[Wwise Space Racer - Demo Video](https://youtu.be/4Q7lQfI7KGA)

[-> ](https://www.gamedeveloper.com/audio/audio-middleware-why-would-i-want-it-in-my-game-#Wwise%20Footsteps)[Wwise Footsteps - Demo Video](https://youtu.be/UnodOW0wqWo)

[- > ](https://www.gamedeveloper.com/audio/audio-middleware-why-would-i-want-it-in-my-game-#FMOD%20Adaptive%20Music)[FMOD Adaptive Music - Demo Video](https://youtu.be/yCfsUjGZeTM)

## What & Why?

Some will say:

1."Unity has a really good audio tool and I don't need more than that," or

2."I can make all that by scripting it for you," or

3."It's too expensive and I don't exactly know how much I'll pay to have it in my game," or

4."It's very complicated and my programmers and designers will not want to learn it!"

Well, first, lets demystify some of that:

1. Game Engines have good and simple audio tools that are alright for certain games, but they are not enough anymore for the level of audio quality and implementation that most games require, whether they are Indie or [#AAA](https://www.theonogueira.com/blog/search/.hash.aaa).

2. Yes, programmers can definitely create a whole new middleware application specific for your game. However, your sound designer will have to learn how to use it, deal with bugs and it will be a back and forth between them and the programmers, which takes time, something most of us cannot afford. The amount of time spent is not worth it, when your sound designer/composer can use a tool they are already comfortable with and that will get the job done giving the programmers only simple parameters and a few scripts that will make the audio run exactly as planned.

3. Yes, you do pay for the usage of middleware if your game is very successful, but only after profit (I'll be breaking down the prices below). In short, if your game needs to pay for Middleware, it is because you made enough money to pay for it without making a big hole in your budget.

4. As for being complicated, your programmers will not have to learn how to use it. The [#SoundDesigner](https://www.theonogueira.com/blog/search/.hash.sounddesigner) / [#Composer](https://www.theonogueira.com/blog/search/.hash.composer) job is to make the implementation process through [#Middleware](https://www.theonogueira.com/blog/search/.hash.middleware) easier for the programmer, who in some cases will only have to write a few audio scripts to get the middleware connected to the game engine and the rest was already done inside the middleware.

So, through this article, I want to show you why should you consider Audio Middleware for your game and how it can improve the usability of audio and make transitions very smooth.

To start, I'd like to point out the most used Audio Middleware on the Market:

And below you can see a simple comparison between them:

![Middleware Comparison Chart Middleware Comparison Chart](../../assets/176bb4d842a7667e.png)


All [#Middleware](https://www.theonogueira.com/blog/search/.hash.middleware) have their pros and cons, however, for the purpose of this article, I am going to talk more specifically about [#FMOD](https://www.theonogueira.com/blog/search/.hash.fmod) and [#Wwise](https://www.theonogueira.com/blog/search/.hash.wwise). [#Fabric](https://www.theonogueira.com/blog/search/.hash.fabric) is not as used nowadays and I personally have no experience with [#Criware](https://www.theonogueira.com/blog/search/.hash.criware), which is mostly used by big studios Game companies in Asia, such as [#Capcom](https://www.theonogueira.com/blog/search/.hash.capcom). And as for [#Elias](https://www.theonogueira.com/blog/search/.hash.elias), I wrote two blogs about the software, which I really enjoy, however, as I want to focus on both sound design and adaptive music on this blog, [#Elias](https://www.theonogueira.com/blog/search/.hash.elias) would only fit one side and you can check my other blogs "[From Linear to Adaptive - How a Film Composer Fell in Love with Adaptive Music](https://www.theonogueira.com/blog/from-linear-to-adaptive1)" and "[From Linear to Adaptive - A Deeper look into Elias Studio 3 MIDI Capabilities](https://www.theonogueira.com/blog/from-linear-to-adaptive-a-deeper-look-into-elias-studio-3-midi-capabilities)" to find more about this amazing tool.

## How can [#middleware](https://www.theonogueira.com/blog/search/.hash.middleware) improve my game?

There are many ways that middleware can improve your game. The first one is when it comes to creating organic sounds, for example a vehicle engine. On the example below, I created a space racer engine using FMOD and Wwise. In FMOD, you can see I used 2 different parameters, RPM and Load. RPM will show the speed of the racer as it changes gears (I know, why would a space vehicle change gears? Because it sounds cool!), and Load tells if the vehicle is accelerating or decelerating.

Disclaimer Note: On the videos below, you will not hear me talking. These are just simple sessions to demonstrate what you can accomplish so easily and accurately on middleware. The sessions were created specifically for this blog, so there's not many complicated features being used as they would make it harder to understand the point. However, Middleware sessions tend to contain all of their audio elements together and use a lot of events, tracks and plugins to achieve their goal.

While in FMOD you create the audio tracks still on a linear-format thought-process (although it is still non-linear), in Wwise, there is a lot more freedom when choosing how an audio file will react to different switches and states.

## Multiplying & Diversifying - Footsteps

Another way that audio middleware can improve your game is to improve loops and sounds that need to be repeated, so they never sound exactly the same and your player never gets tired of them. Some examples relate to footsteps, ambiences, and a way to randomize vocal sounds and dialog. Below you can see an example from a Wwise session where I created footsteps sounds on three different materials. There are only four footsteps sounds for material, but because of randomization of pitch, order and effects, they sound like there are thirty footsteps recorded, while you save space on your data budget and store only four sounds of each. This can also be accomplished with only two or even one sound of each.

## Making the Ambience More Realistic

Ambiences can be tricky, mostly because players tend to spend a good amount of time in a single location. So, to avoid a simple loop of a one-minute countryside morning and hearing the same birds over and over, we turn to middleware. By using them, you can have multiple base ambiences of a couple minutes and add multiple insects, birds and other nature sounds in a random order. Doing that, you are able to create a much more realistic-sounding location. And moreover, you can use middleware to smoothly change the time of day and transition between locations with a correct fade curve.

Below you can hear an example of how I created a countryside ambience and make it go from day to night and from no-rain to heavy rain with thunders. Notice that the birds in the morning do not repeat often and their tracks play randomly, making it harder for the player to identify a looping-point. The thunders follow the same suit, never playing the same track the same way and always playing on random moments.

## Complex and Long Dialog Script

All middleware are better implementers than the game engines when it comes to dialog. If you think about the fact that you might have twenty to fifty characters, each with over ten lines in twenty different languages and you still need all of the audio to play the correct way and perfect timing, with the same effects. With middleware you can organize them all correctly and make sure they have the same effects. Another important use of middleware is if you utilize multiple takes, or lines that can be used for the same goal, you can group them and either call them randomly, or choose an order. Check the very simple dialog demo on FMOD below.

## Other Important Factors

Lets say you have a character that goes inside a cave. The reverberation within that cave should completely change the character's dialog, the sound effects and the ambience. However, unless you want to, usually the music should stay the same. In a game engine, you would probably need to program the reverb and delay to react on every single one of those tracks. However, in Middleware, you only have to create a state in which all of the sounds you choose will change unnoticed. With Middleware, you can change the sounds on the go and they will automatically change within the game, without any issues in a matter of minutes.

FMOD and Wwise have capabilities of connection with other software and external plugins that allow audio artists to create exactly the sound they, together with the game developers envision.

## And what about Adaptive Music?

I talked extensively about Adaptive music on my blogs about Elias, which can check out through these links, if you have not yet read them:

Music in Films and TV Series are cut to fit the scenes and to hit certain points organically. However, in a game, it is very hard to transition a track into the perfect hit point without making it fully adaptive. And to do that, you MUST use audio middleware. In the demo below I created two moments: Scene 1 and Battle. Scene one has no extra layers, but one of its tracks randomly chooses synths that complements its top line. It also has an intro that will only play once and go into the Scene cue, which will loop until a call for a change. As for the Battle cue, it has both an intro and an outro. It also has four layers. To control those layers, I created a parameter called Battle Level from 1 to 4. Lastly, the MusicState parameter controls the moment where the player is located. If the player is on Scene 1, the Music State is at 1, however, if the player is in combat, the Music State is at 2, triggering the Battle Sequence. The battle levels can be used in multiple ways, such as the danger the player is in, or how close to the end of the battle the player is in.

## Quick note on VR/AR/MR and 360 audio

When it comes to VR/AR/MR, middleware is also on it. There are plugins constantly being developed that can fulfill the spatial audio needs within games through middleware. The most commonly used at the time of this blog writing is the Google VR plugin, which allows you to correctly place sounds within the field for VR.

## Conclusion

Audio Middleware is a tool that can improve your game immensely, whether it is for a AAA game or a simple Tetris indie remake. And besides all the points I made above, Middleware can push audio data budget down by a lot. Both FMOD and Wwise have the capability of compress-exporting it accordingly to fit that budget, by choosing the sound format, its bit rate and sample rate. Moreover, through middleware you can add effects and randomization to all kinds of sounds, without the need of various recordings of the same sound, which in return also brings down the audio data budget.

Thus, dear game designer and developer friend, I hope this can shine some light on your understanding why your sound designer or composer is asking you to use one of these in your game. They see the value of it and understand the importance of a great soundtrack to make your game sound perfect.

If you have any questions, I would be more than glad to answer them. I am very well versed in both sound design and music and I have full knowledge of FMOD and Wwise. You can contact me via email to [[email protected]](https://www.gamedeveloper.com/cdn-cgi/l/email-protection#2f4c40415b4e4c5b6f5b474a404140485a4a465d4e014c4042)