---
title: 'Audio is Math, Code is Art: Understanding Dynamic Audio Systems'
url: https://www.gamedeveloper.com/audio/audio-is-math-code-is-art-understanding-dynamic-audio-systems
author: Jacob Vorstenbosch
published: '2017-04-07'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Audio is Math, Code is Art: Understanding Dynamic Audio Systems

A summary of dynamic audio and how a change in perspective to programming and audio design can rapidly help implement a successful audio system.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

When it comes to video games, sound design has always been in a very bizarre position. Unlike graphics or gameplay, audio rarely stands out as the prominent feature in a game; yet as soon as the quality drops or it disappears completely, people can immediately notice that something feels wrong. With the rapid growth in quality and the surge of momentum that the industry has gotten, standards have been rapidly increasing for nearly all aspects of video games, including the sound design. Dynamic audio was, since its inception, a way of adding even more life to a game in ways that graphics could not compete through its ability to manipulate different audio pieces throughout the game in correspondence to the player’s actions. However, creating the proper system to facilitate dynamic audio is a challenge on its own, trying to keep the sound designer’s vision while also keeping everything optimized with the engine itself. To this regard, I have found that understanding where dynamic audio came from, and how designers and programmers can shift their thought process to work together on creating a system that works for your game to be the most effective way of creating a dynamic system.

The Background

Dynamic audio has been in the industry for quite some time now, with the first recorded case being the arcade game ‘Frogger’ back in 1981. Back then, dynamic audio simply meant that when the state of the game changed, so did the audio; when you made it to safety, the music in the game changed. Nothing about the change was smooth, but it was a step in the right direction to add more life to the video game’s audio. The next big step was the creation of the first dynamic audio engine, iMuse. Implemented by LucasArts, the engine created nearly seamless segues between tracks, and was a staple for the studio’s development in all of their games after Monkey Island 2. However, this was still extremely programmer heavy – audio designers really didn’t have way of understanding what was actually going on with their music behind the scenes until the introduction of MaxMSP and Pure Data. The introduction of visual programming tools was the first step of having designers completely integrated with the code so that they could work alongside the programmers to understand the implementation of their vision. For the vast customization options of Spore, EA and Maxis wanted procedurally generated audio to which they implemented a custom version of Pure Data, and went on to be one of the first companies to do so proving the computational prowess of visual programming tools. (More on Spore here: [LINK](https://archive.org/details/GDC2008Jolly))

![](../../assets/e87b5d1e20c256a0.png)

![](../../assets/30d539a5eec3140e.jpg)

![](../../assets/aaba9c3e6cfeed73.jpg)


Only in audio development history do these three titles make sense together.

Sources(left to right): Frogger © Konami, Monkey Island 2 © LucasArts, Spore © EA, Maxis

The Problems Arise

All of these audio innovations helped fight against stagnation, yet it also came at a great cost: the increase in demanded complexity. Games were getting more complex with their graphics, their engines and their mechanics; adding more complexity required the audio designers to step up and add more effects to compliment the visuals. The previous solution was to have somebody called the ‘audio guy’. The entire audio department would ride on this person’s shoulders, with the expectation that they would design, create and implement all of the audio needed for the game to work properly. Hirokazu Tanaka is a prime example of this, as he was not only the man who composed the entire Metroid soundtrack, but also created the sound cards for the Nintendo consoles as well to properly optimize the audio he created. Rob Hubbard, the man who spearheaded much of the audio for the Commodore 64, had to code all of his music in assembly for the SID cards because nobody else could do it.

The issue with this method is that with only one person controlling the audio, what happens when they are not available? The lovingly named Bus Theory states: ‘when looking around the office, could you point to somebody that, if they were to be hit by a bus tomorrow, would cripple the entire workflow of the rest of the office?’ For ‘audio guys’, this was a serious threat to any possible work, as most other programmers would not even bother to look at the sound code since they did not have to. However, the idea of an ‘audio guy’ is still around in many studios, as I was able to experience firsthand with my own team projects. Indie studios rarely can afford to have more than one person working on audio, so they require the audio developer to do everything. While this works in short term solutions, it can have long-term repercussions if the audio designer/programmer ever leaves or becomes ill.

![](https://www.c64-wiki.com/images/b/b4/Rob_Hubbard-1983.jpg?width=164&auto=webp&quality=80&disable=upscale)

![](http://www.vgmonline.net/wp-content/uploads/hirokazutanakaprofile.jpg?width=187&auto=webp&quality=80&disable=upscale)


Rob Hubbard (left) and Hirokazu Tanaka (right) - argueably the forefathers of videogame audio, not argueably great examples of the 'bus theory'

On the other side of the spectrum, however, is what I like to call the ‘Great Divide’ – when a professional composer is hired to handle the audio, and the programmer simply implement the work done, and have no input on what the other is doing, which causes a loss in vision and communication. It also slows down the process exponentially, as every iteration of audio has to be tested, given back to the composer for feedback, and then iterated upon, and so on and so forth. Professional composers are also much more expensive, and must have an orchestra/band for the actual pieces themselves, which increase costs. There is also the issue of interesting bugs occurring due to the lack of communication between the two. Marty O’Donnel ran into a bizarre issue with the 3D sound in Halo, where the mix would jump around the stereo speakers when the camera swapped out of a dialogue because nobody bothered to check if that would ever be an issue.

One Solution

So how can we create a dynamic audio system that avoids the pitfalls of the previous solutions? Many have found that middleware to be the optimal solution to this issue, as Audiokinetic’s Wwise and Firelight’s FMOD have done an absolutly fantastic job of creating software that gives the sound designer a visually understanding interface, as well as a robust engine built on years of research and algorithms to help create fantastic dynamic audio. Overwatch and The Witcher 3 being two fantastic examples of the depth that middleware can allow sound designers to achieve. However, not all developers can afford this software or simply want to have their own in house audio engine instead of relying on outside affordances. After programming the sounds for a few project games and stumbling upon Leonard J Paul’s paper “Game Audio: Coding Vs Aesthetics”, I have come to the realization that it really takes a shift in perception and a massive amount of proper communication. The shift towards realizing how sound design and programming can interact with each other and understand how the other sees the engine are the fundamentals to creating a solid audio system from scratch.

Bringing the Two Ideas Together

![](https://code.visualstudio.com/images/whyvscode_macwinlinux2.png?width=550&auto=webp&quality=80&disable=upscale)


Source: Visual Studio © Microsoft [[Image](https://code.visualstudio.com/docs/editor/whyvscode)]

The importance is that the audio designer and the programmers switch over to the opposite style of thinking. For sound designers, they need to think about the mathematics that goes into the sound design. In an audio system, the sound designer needs to be able to understand where all the calculations for the DSP effects, volume shifts and triggers would occur so that they are aware of what they need to apply to their own mix. If the reverb calculations do not seem optimal to what the sound designer believes, they can tweak the numbers themselves in the mix before submitting it to the system engine for testing. They also need to be aware of their own overhead, as audio is arguably the most susceptible to acquiring a massive memory overhead if the designer does not take any of this into consideration. Being able to also understand where in the system and engine the audio code is situated also allows for faster iterative process, as the designer themselves can go in and test out how their mix sounds at different locations in the game and make any tweaks to variables that they can identify quickly.

![](https://www.image-line.com/flstudio/fl12full_1.jpg?width=550&auto=webp&quality=80&disable=upscale)


Source: FL Studio 12 © Image Line [[Image](https://www.image-line.com/flstudio/)]

On the opposite side, the programmer needs to understand the vision and creativity that the sound designer is trying to optimize with this dynamic audio system. Understanding where the triggers are, how the mix emphasizes specific parts of the track and how different sound effects can emphasize different aspects is integral for the programmer to understand what the sound designer is trying to convey, and create the system accordingly. Programming is also creative in its own way, that the differing ways that each programmer solves problems is staggering. This allows the programmer to create the audio system in a way that both they and the sound designers can understand best, allowing for a more fluid system overall between the two.

Final Words

The goal of this method is that, with indie studios constantly desiring growth, those wishing the same would be able to switch out of the ‘audio guy’ mentality quicker and adopt a more stable audio development team. Games such as Bastion have helped prove that one audio developer can be at the conception of a game and help mold it into its final product, so there is no reason for audio designers to go unheard in the development of the system that the audio so necessarily needs. Even if there is only one sound designer, the ability to support them with a programmer that understands what the audio needs is the foundation of creating a solid dynamic audio system. Creating an environment where both the engine team and the sound design team can share in the same vision is what we all strive for in audio development, and it can be a beautiful thing to see a game’s sound design flower into something more than just support for the visuals.


Link to Leonard J Paul's article below:

More on Rob Hubbard's crazy techniques with assembly for those interested: