---
title: Arrangement for Vertical Layers Pt. 1
url: https://www.gamedeveloper.com/audio/arrangement-for-vertical-layers-pt-1
author: Winifred Phillips
published: '2015-09-29'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Arrangement for Vertical Layers Pt. 1

The first installment of a three-part series on arrangement for dynamic music systems, with examples from the LittleBigPlanet franchise. Part 1 focuses on techniques that help the main melody leap to the foreground in a complex vertical arrangement.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/a0a6eb17437cf50e.jpg)


Arrangement for interactivity is a complex subject, so I thought we should begin by developing a basic understanding of what arrangement is, and then move on to the reasons why it's especially important in interactive music.

When we talk about music, we often discuss the "melody" and the "accompaniment." The melody typically occupies the forefront of our attention, while the accompaniment supplies a chord structure and a series of musical events that embellish and support the foreground content. Both melody and accompaniment are expressed by musical instruments chosen to compliment each other when combined, or contrast with each other in the most desirable way. While the underlying melody and chord structure of a piece of music can be considered the essential skeleton of the piece, the creativity with which these structural elements are expressed by musical instruments is the true flesh-and-blood of the composition. This creative expression of music through musical instrumentation is known as the arrangement.

![Melody and chord structure: the skeletons of music, waiting to be fleshed out by the arrangement. Melody and chord structure: the skeletons of music, waiting to be fleshed out by the arrangement.](../../assets/69b920f08b05cd9c.jpg)


Melody and chord structure: the skeletons of music, waiting to be fleshed out by the arrangement.

Sound on Sound magazine has a great article written by George Webley about the art of traditional song arrangement. "Big George" was a well known writer, radio personality, and composer best known for the television theme music for Ricky Gervais's The Office. His article for Sound on Sound is a great educational resource for traditional linear arrangement.

![Big George Webley Big George Webley](../../assets/d5705c3a36d02164.jpg)


Big George Webley

According to Big George, "The line between composing or producing a tune and arranging it is a very thin one. If you're either the producer or the composer, arrangement goes with the territory."

# Interactive music: the LittleBigPlanet model

Traditional arrangement is a perfect expression of artistic control. As the composer/arranger, we decide on the instruments that will perform the composition and then write the notes that will be played by those instruments. When the arrangement is complete, the piece of music reaches a fixed state in which the only alterations take the form of subtle performance nuances by the musicians.

For interactive game music, we have to accept that the music will never reach a perfectly fixed state, but will instead exist in constant flux. By creating the music in component parts rather than as a contiguous whole, we enable the game's programming to manipulate the arrangement, activating and deactivating instruments, thinning and thickening the mix, adding and removing structural elements such as melody and harmony... the possibilities for variation are enormous.

![Photo of composer Winifred Phillips taken in the LittleBigPlanet 3 booth at the Electronic Entertainment Expo 2014. Photo of composer Winifred Phillips taken in the LittleBigPlanet 3 booth at the Electronic Entertainment Expo 2014.](../../assets/278cf6d12581a347.jpg)


Photo of composer Winifred Phillips taken in the LittleBigPlanet 3 booth at the Electronic Entertainment Expo 2014.

![Six simultaneous recordings Six simultaneous recordings](../../assets/b7d2aac76f7fa9d6.jpg)

[Interactive Game Music of LittleBigPlanet 3 (Concepts from my GDC Talk).](https://winifredphillips.wordpress.com/2015/03/16/interactive-game-music-of-littlebigplanet-3-concepts-from-my-gdc-talk/)" Here's a quote from that blog:

In a vertical layering music system, the music is not captured in a single audio recording. Instead, several audio recordings play in sync with one other. Each layer of musical sound features unique content. Each of the layers represents a certain percentage of the entire musical composition. Played all together, we hear the full mix embodying the entire musical composition. Played separately, we hear submixes that are still satisfying and entertaining for their own sake. The music system can play all the layers either together or separately, or can combine the layers into different sets that represent a portion of the whole mix.

When implemented into gameplay, layers are often activated when the player moves into a new area. This helps the music to feel responsive to the player’s actions. The music seems to acknowledge the player’s progress throughout the game. It’s important to think about the way in which individual layers may be activated, and the functions that the layers may be called upon to serve during the course of the game.


To make this abstract concept a bit more concrete, let's watch a video from the LittleBigPlanet franchise that breaks down the six layer music system and shows how it works. Here's the "Escape from San Crispin" level of the LittleBigPlanet Cross Controller game. Notice how the music layers are played separately in the beginning of the video, and then their activations and deactivations are indicated at the bottom of the screen throughout gameplay.

For a more elaborate discussion of the six layer system, we can watch this video I produced to explore the music system of the LittleBigPlanet Toy Story video game:

With this interactive music system in mind, let's now turn to a discussion of the relationship between the fundamentals of arrangement and the Vertical Layering system. We'll begin with one of the most important elements of any piece of music:

# The melody

Those of us who write music will instinctively understand the construction of a satisfying melody, but the strength of the melody can waver in the context of an interactive arrangement. Let's first go over a few arrangement concepts that are effective when developing a melody for arranging within an interactive framework. Then we'll address a few common arrangement techniques that can be questionable within this interactive music system.

## Effective technique: voice leading / step-wise movement

In arranging the instruments of an interactive composition based in Vertical Layers, we have to make basic decisions about which musical elements will reside in which layers. When we assign the main melody to a layer, we'll need to make sure that it feels satisfying when heard in isolation. The music system can (and probably will) play the melody layer by itself. In the case of the LittleBigPlanet music system, this means that only one-sixth of the piece will be playing.

![The conductor of an orchestra The conductor of an orchestra](../../assets/fada0c990c949e52.jpg)


For a melody layer, the graceful and aesthetically-pleasing shape of the musical movement becomes paramount. A composer might feel comfortable creating a melody with surprising leaps and unorthodox movement, confident that the rest of the arrangement will support these jumps... but remove the rest of the arrangement, and the melody becomes awkward and strange. Step-wise movement, otherwise known as voice leading, is the art of structuring a succession of notes so that they flow from one to another with an impression of natural progression. This sensation of "logical movement" stems from our human experience with melody, which includes the note sequences we're accustomed to hearing, and the scales that reside at the heart of popular music today.

One of the best explanations of this concept can be found in Bobby McFerrin's tremendously entertaining presentation at the event "Notes & Neurons: In Search of the Common Chorus" at the World Science Festival in 2009. [Bobby McFerrin](https://en.wikipedia.org/wiki/Bobby_McFerrin) is a pop vocalist famous for his popular 1988 hit song, "Don't Worry, Be Happy." In this awesome video, McFerrin demonstrates how the pentatonic scale has become so ingrained in our collective psyche that when given the beginning of a note sequence, we need little prompting to know how to complete it. The notes just feel natural, so we know what should come next.

When considering a melody for use in Vertical Layers, we should always try to incorporate logical step-wise movement. This will help to ensure that the melody still works, even when the arrangement drastically changes due to the interactive nature of the music system.

## Effective technique: instrumental motion

In Vertical Layering for a music system such as the one employed by the LittleBigPlanet franchise, the musical content has to be fairly busy in order to be flexible as an interactive construct. For LittleBigPlanet games, each individual layer needs to have enough content to stand on its own, and yet still work when all the layers are played simultaneously. This allows the music to be very interactive during gameplay: the layers can all be played separately, or they can be played in lots of different combinations. In fact, if the game fully utilized every available combination, then gamers would hear the music layers combined in 42 completely different ways, from singular layers, to combinations of 2, 3, 4, 5 and 6. With all these layers designed to have enough foreground content to stand alone, the result of this design can be a music mix that hovers on the edge of sounding excessively busy. How can the all-important foreground melody leap to the top of the mix if the arrangement tends to be quite active?

This can be addressed by a technique I described in my book ([A Composer's Guide to Game Music](http://amzn.com/0262026643)) as "compositional dynamics." Techniques such as arpeggios, glissandi, runs, trills and other types of ornamentation serve to enliven a melody. The resulting energy creates a sense of movement that helps the melodic theme to leap out of the mix. According to [Vince Corozine](https://www.linkedin.com/pub/vince-corozine/a4/645/78a), the author of [Arranging Music for the Real World](http://amzn.com/0786649615) (Mel Bay Publications), "instrumental motion, with its active design, captures more of the listener's attention." (p. 30)

![Author Vince Corozine Author Vince Corozine](../../assets/10e22e9e2a436840.jpg)


Author Vince Corozine

A good example of this can be found in the LittleBigPlanet 3 Ziggurat Theme, which I composed and arranged for the LittleBigPlanet 3 video game. In this piece of music, the melody is arranged as a polyphonic construct according to the tenets of the classical fugue. Because of this, the melody exhibits constant motion and activity, which helps it to leap out of the mix. Here's a short excerpt of the layer containing the melody:

And here's the full mix at that specific point in the composition, showing how energetic activity can help a melody leap out of a busy arrangement:

## Effective technique: frequency range isolation

As we know, Equalization (EQ) is the process whereby a mixing engineer adjusts the perceived volume level of audio frequencies in sonic sources in order to produce a result that is ideal for the recording in which the sound resides. These adjustments take place on frequency ranges - some high, some middle, and some low. To create a good mix, all the musical elements should occupy a portion of the frequency spread that isn't already cluttered with content. There should be a balanced and satisfying combination of high, middle and low sounds that are clearly perceived within their respective frequency ranges.

![An graphical equalizer can adjust frequencies, from low to high. An graphical equalizer can adjust frequencies, from low to high.](../../assets/799b2a49bc64f408.jpg)


## Questionable technique: doubling

In traditional arrangement, doubling is the reinforcement of a particular instrument part by virtue of its exact replication in another section of the ensemble. For instance, the flute section may double the violins when they are carrying a melody line, and this doubling may serve to brighten the sound, give clarity to the articulations and help the melody to soar brightly over the rest of the arrangement.

![Identical doubling can be problematic. Identical doubling can be problematic.](../../assets/48fcedc5d4ec64f8.jpg)


In this case, if we intend to have certain instruments doubling each other within the arrangement, it makes sense for us to combine those instruments in the same interactive layer.

## Questionable technique: harmonized melody

A useful way for us to add interest and color to a melody is the arrangement technique of adding a harmony line. The harmony supports and embellishes the melody. It's typically constructed in three possible ways:

A line moving in a constant parallel interval such as a diatonic third,

A line with parallel motion but a variable interval that uses the available notes of the underlying chord structure,

A parallel harmony line that uses the tones of the pentatonic scale in the current key signature of the piece.


This approach can work within Vertical Layers if the melody and its accompanying harmony line are grouped in the same layer. However, separating the melody and harmony lines into different layers is problematic for this interactive system. Because the pitches of the harmony line will necessarily move up and down in very similar ways with an identical rhythmic structure, it will bear a strong resemblance to the original melody. This can result in two layers that have strikingly similar content. It's much better to create a full-blown counter-melody (which is a topic we'll be discussing in part two of this blog series).

## Questionable technique: the full homophonic tutti

![All together now... All together now...](../../assets/aabaa575676badab.jpg)


Having the whole ensemble come together to state a theme can be a powerful technique within a traditionally arranged piece of music. However, as we've learned from the sections about harmonized melody and doubling, whenever we use an arrangement technique that creates similar or identical content between layers, we deteriorate the interactive utility of the piece of music we're arranging. If the layers sound similar (or the same), they'll make no impact when they're activated or deactivated in the game.

# Conclusion

So, now we've completed this discussion of some arrangement techniques for melodies that work well within the structure of a Vertical Layering composition. In the next installment of this series, I'll be talking about techniques for effective countermelodies in Vertical Layers, and then later we'll explore voicing techniques for effective harmonic support.


![Composer Winifred Phillips Composer Winifred Phillips](../../assets/00c2c1b9bace2643.png)

[A COMPOSER'S GUIDE TO GAME MUSIC](http://amzn.com/0262026643), published by the Massachusetts Institute of Technology Press. As a VR game music expert, she writes frequently on the future of music in virtual reality video games.

Follow her on Twitter [@winphillips](http://www.twitter.com/winphillips).